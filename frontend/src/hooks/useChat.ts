/**
 * Custom hook for chat functionality with SSE streaming support
 */

import { useCallback, useRef } from 'react';
import { chatApi } from '@/services/api-client';
import { useChatContext } from '@/context/ChatContext';
import { useSessionContext } from '@/context/SessionContext';

export function useChat() {
  const {
    messages,
    streamingStatus,
    sessionId,
    setSessionId,
    addMessage,
    updateStreamingMessage,
    updateContributingAgents,
    updateContributingModels,
    setStreamingStatus,
    tokenUsage,
    updateTokenUsage,
    clearMessages,
  } = useChatContext();
  
  const { activeSession, createSession } = useSessionContext();
  const abortControllerRef = useRef<(() => void) | null>(null);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim()) return;

      // Ensure we have a session
      let currentSessionId = sessionId || activeSession?.session_id;
      if (!currentSessionId) {
        currentSessionId = await createSession();
        setSessionId(currentSessionId);
      }

      // Add user message
      addMessage({
        role: 'user',
        content: content.trim(),
      });

      // Add placeholder assistant message for streaming (clear contributing agents/models)
      addMessage({
        role: 'assistant',
        content: '',
        contributingAgents: [],
        contributingModels: [],
      });

      setStreamingStatus(true);

      // Abort any existing stream
      if (abortControllerRef.current) {
        abortControllerRef.current();
      }

      // Start streaming
      const abort = chatApi.streamMessage(
        currentSessionId,
        content.trim(),
        (message: any) => {
          // Handle streaming message
          console.log('[useChat] Received message:', message);
          
          // Ensure message is an object, not a string
          let parsedMessage = message;
          if (typeof message === 'string') {
            try {
              parsedMessage = JSON.parse(message);
            } catch (e) {
              console.error('[useChat] Failed to parse message string:', e);
              // If it's a plain string, treat it as content
              if (message && message.trim()) {
                updateStreamingMessage(message);
                return;
              }
              return;
            }
          }
          
          // Ensure we have a valid message object
          if (!parsedMessage || typeof parsedMessage !== 'object') {
            console.warn('[useChat] Invalid message format:', parsedMessage);
            return;
          }
          
          const tokenUsageMetadata = parsedMessage.metadata?.token_usage;
          if (tokenUsageMetadata) {
            const inputTokensTotal = Number(tokenUsageMetadata.input_tokens_total) || 0;
            const outputTokensTotal = Number(tokenUsageMetadata.output_tokens_total) || 0;
            updateTokenUsage({
              inputTokens: inputTokensTotal,
              outputTokens: outputTokensTotal,
            });
          }

          // Handle content chunks
          if (parsedMessage.content !== undefined && parsedMessage.content !== null) {
            const contentStr = String(parsedMessage.content);
            if (contentStr.trim()) {
              console.log('[useChat] Updating streaming message with content:', contentStr.substring(0, 100));
              // Extract contributing agents from metadata
              const contributingAgents = parsedMessage.metadata?.contributing_agents || [];
              const contributingModels = parsedMessage.metadata?.contributing_models || [];
              console.log('[useChat] Contributing agents:', contributingAgents);
              console.log('[useChat] Contributing models:', contributingModels);
              // The backend sends full accumulated content, so we replace it
              updateStreamingMessage(contentStr, contributingAgents, contributingModels);
            }
          }
          
          // Handle done signal (only metadata update, don't overwrite content)
          if (parsedMessage.done === true) {
            // Final update with contributing agents if provided (without changing content)
            if (parsedMessage.metadata?.contributing_agents) {
              const contributingAgents = parsedMessage.metadata.contributing_agents;
              console.log('[useChat] Final contributing agents from done signal:', contributingAgents);
              // Update the last message with contributing agents using context function
              updateContributingAgents(contributingAgents);
            }
            
            if (parsedMessage.metadata?.contributing_models) {
              const contributingModels = parsedMessage.metadata.contributing_models;
              console.log('[useChat] Final contributing models from done signal:', contributingModels);
              // Update the last message with contributing models using context function
              updateContributingModels(contributingModels);
            }
            console.log('[useChat] Stream done signal received');
            // Ensure streaming status is updated
            setStreamingStatus(false);
          }
        },
        (error: Error) => {
          console.error('[useChat] Stream error:', error);
          setStreamingStatus(false);
          
          // Update last message with error
          updateStreamingMessage(
            'Sorry, an error occurred while processing your request. Please try again.'
          );
        },
        () => {
          // Stream done
          console.log('[useChat] Stream completed');
          setStreamingStatus(false);
          abortControllerRef.current = null;
          // Note: Content is already updated via updateStreamingMessage
          // The ChatContext state update should trigger re-render automatically
        }
      );

      abortControllerRef.current = abort;
    },
    [
      sessionId,
      activeSession,
      createSession,
      setSessionId,
      addMessage,
      updateStreamingMessage,
      updateContributingAgents,
      updateContributingModels,
      setStreamingStatus,
      updateTokenUsage,
    ]
  );

  const stopStreaming = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current();
      abortControllerRef.current = null;
      setStreamingStatus(false);
    }
  }, [setStreamingStatus]);

  const resetChat = useCallback(() => {
    stopStreaming();
    clearMessages();
    setSessionId(null);
  }, [stopStreaming, clearMessages, setSessionId]);

  return {
    messages,
    streamingStatus,
    sessionId: sessionId || activeSession?.session_id,
    sendMessage,
    stopStreaming,
    resetChat,
    tokenUsage,
  };
}

