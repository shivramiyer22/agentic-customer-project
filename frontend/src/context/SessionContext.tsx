'use client';

/**
 * Session context provider for session management
 */

import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { sessionApi } from '@/services/api-client';

export interface Session {
  session_id: string;
  created_at: string;
  updated_at: string;
  message_count?: number;
  agent?: string;
}

export interface SessionContextType {
  sessions: Session[];
  activeSession: Session | null;
  loading: boolean;
  setActiveSession: (session: Session | null) => void;
  createSession: () => Promise<string>;
  loadSessions: () => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

export function SessionProvider({ children }: { children: React.ReactNode }) {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeSession, setActiveSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(false);

  const createSession = useCallback(async (): Promise<string> => {
    const sessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    const newSession: Session = {
      session_id: sessionId,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      message_count: 0,
    };
    
    setSessions((prev) => [newSession, ...prev.slice(0, 2)]); // Keep last 3 (FIFO)
    setActiveSession(newSession);
    
    return sessionId;
  }, []);

  const loadSessions = useCallback(async () => {
    setLoading(true);
    try {
      const response = await sessionApi.getSessions() as { sessions?: Session[] };
      if (response.sessions) {
        setSessions(response.sessions);
      }
    } catch (error) {
      console.error('Failed to load sessions:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteSession = useCallback(async (sessionId: string) => {
    try {
      await sessionApi.deleteSession(sessionId);
      setSessions((prev) => prev.filter((s) => s.session_id !== sessionId));
      if (activeSession?.session_id === sessionId) {
        setActiveSession(null);
      }
    } catch (error) {
      console.error('Failed to delete session:', error);
      throw error;
    }
  }, [activeSession]);

  // Load sessions on mount
  useEffect(() => {
    loadSessions();
  }, [loadSessions]);

  return (
    <SessionContext.Provider
      value={{
        sessions,
        activeSession,
        loading,
        setActiveSession,
        createSession,
        loadSessions,
        deleteSession,
      }}
    >
      {children}
    </SessionContext.Provider>
  );
}

export function useSessionContext() {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error('useSessionContext must be used within a SessionProvider');
  }
  return context;
}

