"""
Chat endpoint router for handling chat messages and streaming responses

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/agents
Last Verified: November 2025
"""

from collections import defaultdict
from typing import Dict, Any, Set, Tuple

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import asyncio
import uuid
from app.schemas.chat import ChatMessage, ChatResponse, ChatStreamChunk
from app.agents.orchestrator import get_supervisor_agent_singleton
from app.utils.logger import app_logger

router = APIRouter(prefix="/chat", tags=["chat"])


# Token usage tracking per session (in-memory)
SESSION_TOKEN_STATS: Dict[str, Dict[str, int]] = defaultdict(
    lambda: {"input_tokens": 0, "output_tokens": 0}
)


def _parse_token_usage(raw_usage: Any) -> Tuple[int, int]:
    """Normalize raw usage payloads into input/output token counts."""
    input_tokens = None
    output_tokens = None

    if isinstance(raw_usage, dict):
        # Nested structures {"input": {"tokens": int}, "output": {...}}
        if isinstance(raw_usage.get("input"), dict):
            input_tokens = raw_usage["input"].get("tokens") or raw_usage["input"].get("token_count")
        if isinstance(raw_usage.get("output"), dict):
            output_tokens = raw_usage["output"].get("tokens") or raw_usage["output"].get("token_count")

        # Common flat keys across providers
        for key in ("input_tokens", "prompt_tokens", "promptTokens", "inputTokens", "inputTokenCount"):
            if raw_usage.get(key) is not None and input_tokens is None:
                input_tokens = raw_usage[key]
        for key in ("output_tokens", "completion_tokens", "completionTokens", "outputTokens", "outputTokenCount"):
            if raw_usage.get(key) is not None and output_tokens is None:
                output_tokens = raw_usage[key]

        # Some providers expose total tokens only; treat as output if nothing else present
        if raw_usage.get("total_tokens") is not None:
            total = raw_usage.get("total_tokens")
            if output_tokens is None:
                output_tokens = total
            if input_tokens is None:
                input_tokens = 0

    elif isinstance(raw_usage, (int, float)):
        # Fallback if a single numeric value is provided
        output_tokens = raw_usage

    def _safe_int(value: Any) -> int:
        try:
            if value is None:
                return 0
            return int(value)
        except (TypeError, ValueError):
            return 0

    return _safe_int(input_tokens), _safe_int(output_tokens)


def _update_session_token_usage(session_id: str, message: Any, processed_ids: Set[str]) -> None:
    """Update session token counters from message response metadata."""

    metadata = getattr(message, "response_metadata", None)
    if not metadata or not isinstance(metadata, dict):
        return

    msg_identifier = getattr(message, "id", None) or getattr(message, "uuid", None)
    if msg_identifier is None:
        msg_identifier = f"{type(message).__name__}_{id(message)}"

    if msg_identifier in processed_ids:
        return

    raw_usage = (
        metadata.get("usage")
        or metadata.get("token_usage")
        or metadata.get("tokenUsage")
        or metadata.get("metrics", {}).get("usage")
        or metadata.get("result_metadata", {}).get("usage")
    )

    if not raw_usage:
        return

    input_tokens, output_tokens = _parse_token_usage(raw_usage)
    if input_tokens == 0 and output_tokens == 0:
        return

    session_stats = SESSION_TOKEN_STATS[session_id]
    session_stats["input_tokens"] += input_tokens
    session_stats["output_tokens"] += output_tokens
    processed_ids.add(msg_identifier)


async def generate_agent_stream(supervisor_agent, message: str, session_id: str):
    """
    Generate streaming response from supervisor agent
    
    Args:
        supervisor_agent: Supervisor agent instance
        message: User message
        session_id: Session identifier (used as thread_id)
        
    Yields:
        SSE-formatted chunks from agent stream
    """
    try:
        app_logger.info(f"Starting agent stream for session {session_id} with message: {message[:100]}")
        
        # Configuration for conversation persistence using thread_id
        agent_config = {"configurable": {"thread_id": session_id}}
        
        # Create input messages
        input_messages = [{"role": "user", "content": message}]
        
        # Stream response from supervisor agent
        # Agent astream yields chunks with state updates
        # In LangChain v1.0, astream yields dicts with node names as keys and state as values
        previous_content = ""
        chunk_count = 0
        accumulated_content = ""
        contributing_agents = []  # Track which worker agents contributed (preserve order)
        contributing_models = []  # Track which LLM models were used (preserve order)
        processed_tool_call_ids = set()  # Track which tool_calls we've already processed
        processed_token_message_ids: Set[str] = set()  # Track token usage updates
        session_token_stats = SESSION_TOKEN_STATS[session_id]
        tool_name_to_agent = {
            "billing_tool": "Billing Tool Agent",
            "technical_tool": "Technical Tool Agent",
            "policy_tool": "Policy Tool Agent",
        }
        tool_name_to_model = {
            "billing_tool": "OpenAI gpt-4o-mini",
            "technical_tool": "OpenAI gpt-4o-mini",
            "policy_tool": "OpenAI gpt-4o-mini",
        }
        # Supervisor model (AWS Bedrock Claude 3 Haiku) - add first as it's always invoked first
        from app.utils.config import config
        supervisor_model = config.AWS_BEDROCK_MODEL.replace("bedrock:", "AWS Bedrock ").replace("-", " ").title()
        contributing_models.append(supervisor_model)
        
        async for chunk in supervisor_agent.astream(
            {"messages": input_messages},
            config=agent_config,
            stream_mode="values"  # Stream the state values
        ):
            chunk_count += 1
            app_logger.debug(f"Received chunk {chunk_count} for session {session_id}: {type(chunk)}")
            app_logger.debug(f"Chunk keys: {chunk.keys() if isinstance(chunk, dict) else 'not a dict'}")
            
            # Extract content from agent stream
            # Chunks contain full state with messages
            if isinstance(chunk, dict):
                # Check if chunk has messages in the state
                messages = chunk.get("messages", [])
                if not messages and "messages" not in chunk:
                    # Try accessing messages directly from state
                    if hasattr(chunk, "get"):
                        messages = chunk.get("messages", [])
                    elif hasattr(chunk, "messages"):
                        messages = chunk.messages
                
                if messages:
                    # Update session token usage from message metadata
                    for msg in messages:
                        _update_session_token_usage(session_id, msg, processed_token_message_ids)

                    if session_token_stats["input_tokens"] or session_token_stats["output_tokens"]:
                        app_logger.debug(
                            "Session %s token usage updated: input=%s, output=%s",
                            session_id,
                            session_token_stats["input_tokens"],
                            session_token_stats["output_tokens"],
                        )

                    # Track tool calls to identify which agents contributed
                    # Process only NEW tool_calls we haven't seen before to preserve order
                    for msg in messages:
                        msg_type = type(msg).__name__
                        
                        # Track AIMessage with tool_calls to identify which tools were called
                        if msg_type == "AIMessage":
                            # Check if this AIMessage contains tool_calls
                            if hasattr(msg, "tool_calls") and msg.tool_calls:
                                for tool_call in msg.tool_calls:
                                    # Extract tool_call_id for deduplication
                                    tool_call_id = None
                                    tool_name = None
                                    
                                    if isinstance(tool_call, dict):
                                        tool_call_id = tool_call.get("id")
                                        tool_name = tool_call.get("name")
                                    elif hasattr(tool_call, "id") and hasattr(tool_call, "name"):
                                        tool_call_id = tool_call.id
                                        tool_name = tool_call.name
                                    
                                    # Skip if we've already processed this tool_call
                                    if tool_call_id and tool_call_id in processed_tool_call_ids:
                                        continue
                                    
                                    if tool_call_id:
                                        processed_tool_call_ids.add(tool_call_id)
                                    
                                    if tool_name:
                                        agent_name = tool_name_to_agent.get(tool_name)
                                        # Append in order - deduplication handled by tool_call_id tracking
                                        if agent_name:
                                            contributing_agents.append(agent_name)
                                            app_logger.info(f"Detected contributing agent: {agent_name} (from tool: {tool_name}, id: {tool_call_id})")
                                        
                                        # Track model used by this tool's agent (preserve order)
                                        model_name = tool_name_to_model.get(tool_name)
                                        if model_name:
                                            contributing_models.append(model_name)
                                            app_logger.info(f"Detected contributing model: {model_name} (from tool: {tool_name})")
                                        
                        # Note: ToolMessages appear after tools execute, but we track based on AIMessage tool_calls
                        # which appear in the order tools are invoked, and use tool_call_id for deduplication
                    
                    # Get last message (most recent assistant message) for streaming
                    last_message = messages[-1]
                    message_type = type(last_message).__name__
                    
                    app_logger.debug(f"Last message type: {message_type}, has content: {hasattr(last_message, 'content')}")
                    
                    # Check if it's a text message with content (AIMessage or ToolMessage)
                    if hasattr(last_message, "content"):
                        content = last_message.content
                        
                        # Handle string content
                        if isinstance(content, str) and content:
                            # Only stream AIMessage content (final responses), skip ToolMessage for cleaner streaming
                            # ToolMessage content is passed to the agent and will appear in final AIMessage
                            if message_type == "AIMessage":
                                # If content has changed, send the delta
                                if content != accumulated_content:
                                    # Calculate new content (delta from previous)
                                    new_content = content[len(accumulated_content):] if accumulated_content else content
                                    
                                    if new_content:
                                        accumulated_content = content
                                        
                                        app_logger.info(f"Sending content chunk: {len(new_content)} chars (total: {len(content)}), contributing agents: {list(contributing_agents)}")
                                        
                                        # Send content delta as SSE chunk with contributing agents and models in metadata
                                        # Lists preserve order, so agents/models are in invocation sequence
                                        chunk_data = ChatStreamChunk(
                                            content=new_content,
                                            agent="supervisor_agent",
                                            metadata={
                                                "contributing_agents": contributing_agents,
                                                "contributing_models": contributing_models,
                                                "token_usage": {
                                                    "input_tokens_total": session_token_stats["input_tokens"],
                                                    "output_tokens_total": session_token_stats["output_tokens"],
                                                    "total_tokens": session_token_stats["input_tokens"] + session_token_stats["output_tokens"],
                                                },
                                            },
                                        )
                                        yield f"data: {chunk_data.model_dump_json(exclude_none=True)}\n\n"
                                        previous_content = content  # Keep track for comparison
            
            # Small delay to prevent overwhelming the stream
            await asyncio.sleep(0.01)
        
        app_logger.info(f"Agent stream completed for session {session_id} after {chunk_count} chunks")
        
        # If no content was streamed, check if we need to get the final response
        if not previous_content:
            app_logger.warning(f"No content streamed for session {session_id}, attempting to get final response")
            try:
                # Get final response non-streaming as fallback
                result = supervisor_agent.invoke(
                    {"messages": input_messages},
                    config=agent_config
                )
                
                if "messages" in result and result["messages"]:
                    for msg in result["messages"]:
                        _update_session_token_usage(session_id, msg, processed_token_message_ids)

                    final_message = result["messages"][-1]
                    if hasattr(final_message, "content") and final_message.content:
                        content = str(final_message.content)
                        app_logger.info(f"Retrieved final response: {len(content)} chars")
                        
                        chunk_data = ChatStreamChunk(
                            content=content,
                            agent="supervisor_agent",
                            metadata={
                                "contributing_agents": contributing_agents,
                                "contributing_models": contributing_models,
                                "token_usage": {
                                    "input_tokens_total": session_token_stats["input_tokens"],
                                    "output_tokens_total": session_token_stats["output_tokens"],
                                    "total_tokens": session_token_stats["input_tokens"] + session_token_stats["output_tokens"],
                                },
                            },
                        )
                        yield f"data: {chunk_data.model_dump_json(exclude_none=True)}\n\n"
            except Exception as fallback_error:
                app_logger.error(f"Error getting fallback response: {fallback_error}")
        
        # Send done signal with final contributing agents and models list (preserve order)
        done_chunk = ChatStreamChunk(
            content="",
            agent="supervisor_agent",
            done=True,
            metadata={
                "contributing_agents": contributing_agents,
                "contributing_models": contributing_models,
                "token_usage": {
                    "input_tokens_total": session_token_stats["input_tokens"],
                    "output_tokens_total": session_token_stats["output_tokens"],
                    "total_tokens": session_token_stats["input_tokens"] + session_token_stats["output_tokens"],
                },
            },
        )
        yield f"data: {done_chunk.model_dump_json(exclude_none=True)}\n\n"
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        app_logger.error(f"Error streaming agent response: {e}", exc_info=True)
        import traceback
        app_logger.error(f"Traceback: {traceback.format_exc()}")
        error_chunk = ChatStreamChunk(
            content=f"Error processing your request: {str(e)}",
            agent="supervisor_agent"
        )
        yield f"data: {error_chunk.model_dump_json(exclude_none=True)}\n\n"
        yield "data: [DONE]\n\n"


def get_agent_response_non_streaming(supervisor_agent, message: str, session_id: str) -> ChatResponse:
    """
    Get non-streaming response from supervisor agent
    
    Args:
        supervisor_agent: Supervisor agent instance
        message: User message
        session_id: Session identifier (used as thread_id)
        
    Returns:
        ChatResponse with agent response
    """
    try:
        # Configuration for conversation persistence using thread_id
        agent_config = {"configurable": {"thread_id": session_id}}
        
        # Create input messages
        input_messages = [{"role": "user", "content": message}]
        
        # Invoke supervisor agent
        result = supervisor_agent.invoke(
            {"messages": input_messages},
            config=agent_config
        )
        
        # Extract final message content
        processed_token_message_ids: Set[str] = set()
        if isinstance(result, dict) and "messages" in result:
            for msg in result["messages"]:
                _update_session_token_usage(session_id, msg, processed_token_message_ids)

        session_token_stats = SESSION_TOKEN_STATS[session_id]

        if "messages" in result and result["messages"]:
            final_message = result["messages"][-1]
            response_content = final_message.content if hasattr(final_message, "content") else str(final_message)
        else:
            response_content = str(result)
        
        return ChatResponse(
            session_id=session_id,
            message=response_content,
            agent="supervisor_agent",
            sources=[],
            metadata={
                "token_usage": {
                    "input_tokens_total": session_token_stats["input_tokens"],
                    "output_tokens_total": session_token_stats["output_tokens"],
                    "total_tokens": session_token_stats["input_tokens"] + session_token_stats["output_tokens"],
                }
            }
        )
        
    except Exception as e:
        app_logger.error(f"Error getting agent response: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}"
        )


def generate_session_id() -> str:
    """
    Generate unique session ID (thread_id) for new conversations
    
    Returns:
        Unique session identifier
    """
    return str(uuid.uuid4())


@router.post("/")
async def chat(message: ChatMessage):
    """
    Handle chat messages and return streaming responses from supervisor agent
    
    Args:
        message: Chat message request with session_id, message, and stream flag
        
    Returns:
        Streaming SSE response or JSON response based on stream flag
    """
    try:
        # Generate session_id if not provided
        session_id = message.session_id or generate_session_id()
        
        app_logger.info(f"Received chat message for session {session_id}: {message.message[:50]}...")
        
        # Get supervisor agent instance
        supervisor_agent = get_supervisor_agent_singleton()
        
        if message.stream:
            # Return streaming SSE response
            return StreamingResponse(
                generate_agent_stream(supervisor_agent, message.message, session_id),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                },
            )
        else:
            # Return non-streaming JSON response
            response = get_agent_response_non_streaming(
                supervisor_agent,
                message.message,
                session_id
            )
            return response.model_dump()
            
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error processing chat message: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}"
        )


