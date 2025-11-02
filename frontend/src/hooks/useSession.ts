/**
 * Custom hook for session management (create, list, switch, delete)
 */

import { useCallback } from 'react';
import { useSessionContext, type Session } from '@/context/SessionContext';
import { useChatContext } from '@/context/ChatContext';

export function useSession() {
  const {
    sessions,
    activeSession,
    loading,
    setActiveSession,
    createSession,
    loadSessions,
    deleteSession,
  } = useSessionContext();
  
  const { clearMessages, setSessionId } = useChatContext();

  const switchSession = useCallback(
    async (session: Session | null) => {
      setActiveSession(session);
      setSessionId(session?.session_id || null);
      clearMessages();
      
      // Load session history if available
      if (session) {
        // This would load the conversation history
        // For now, we just clear messages and set the session
      }
    },
    [setActiveSession, setSessionId, clearMessages]
  );

  const createNewSession = useCallback(async () => {
    const sessionId = await createSession();
    setSessionId(sessionId);
    clearMessages();
    return sessionId;
  }, [createSession, setSessionId, clearMessages]);

  const removeSession = useCallback(
    async (sessionId: string) => {
      await deleteSession(sessionId);
      
      // If deleted session was active, clear active session
      if (activeSession?.session_id === sessionId) {
        setActiveSession(null);
        setSessionId(null);
        clearMessages();
      }
    },
    [deleteSession, activeSession, setActiveSession, setSessionId, clearMessages]
  );

  return {
    sessions,
    activeSession,
    loading,
    switchSession,
    createNewSession,
    removeSession,
    loadSessions,
  };
}

