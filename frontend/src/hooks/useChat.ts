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

      // Add placeholder assistant message for streaming
      addMessage({
        role: 'assistant',
        content: '',
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
          
          if (message.content && message.content.trim()) {
            console.log('[useChat] Updating streaming message with content:', message.content.substring(0, 100));
            // Extract contributing agents from metadata
            const contributingAgents = message.metadata?.contributing_agents || [];
            const contributingModels = message.metadata?.contributing_models || [];
            console.log('[useChat] Contributing agents:', contributingAgents);
            console.log('[useChat] Contributing models:', contributingModels);
            // The backend sends full accumulated content, so we replace it
            updateStreamingMessage(message.content, contributingAgents, contributingModels);
          } else if (message.done) {
            // Final update with contributing agents if provided
            if (message.metadata?.contributing_agents) {
              const contributingAgents = message.metadata.contributing_agents;
              console.log('[useChat] Final contributing agents from done signal:', contributingAgents);
              // Update the last message with contributing agents using context function
              updateContributingAgents(contributingAgents);
            }
            
            if (message.metadata?.contributing_models) {
              const contributingModels = message.metadata.contributing_models;
              console.log('[useChat] Final contributing models from done signal:', contributingModels);
              // Update the last message with contributing models using context function
              updateContributingModels(contributingModels);
            }
            console.log('[useChat] Stream done signal received');
            // Ensure streaming status is updated
            setStreamingStatus(false);
          } else {
            console.log('[useChat] Message received but no content:', message);
          }
          
          // Handle metadata (agent, sources)
          if (message.metadata) {
            // Update last message with metadata
            // This will be handled in the context update
            console.log('[useChat] Message metadata:', message.metadata);
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
  };
}

