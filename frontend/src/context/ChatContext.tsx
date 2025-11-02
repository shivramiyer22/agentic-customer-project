'use client';

/**
 * Chat context provider for chat state management
 */

import React, { createContext, useContext, useState, useCallback } from 'react';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  agent?: string;
  contributingAgents?: string[];
  contributingModels?: string[];
  sources?: Array<{ name: string; excerpt: string }>;
}

export interface ChatContextType {
  messages: Message[];
  streamingStatus: boolean;
  sessionId: string | null;
  setSessionId: (sessionId: string | null) => void;
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void;
  updateStreamingMessage: (content: string, contributingAgents?: string[], contributingModels?: string[]) => void;
  updateContributingAgents: (contributingAgents: string[]) => void;
  updateContributingModels: (contributingModels: string[]) => void;
  setStreamingStatus: (status: boolean) => void;
  clearMessages: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

const STORAGE_KEY = 'aerospace_chat_history';
const SESSION_KEY = 'aerospace_session_id';

export function ChatProvider({ children }: { children: React.ReactNode }) {
  // Start with empty messages to avoid hydration mismatch
  // Load from localStorage after component mounts (client-side only)
  const [messages, setMessages] = useState<Message[]>([]);
  const [streamingStatus, setStreamingStatus] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isHydrated, setIsHydrated] = useState(false);
  
  // Load from localStorage after hydration (client-side only)
  React.useEffect(() => {
    if (typeof window === 'undefined') return;
    
    try {
      // Load messages
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        // Convert timestamp strings back to Date objects
        const loadedMessages = parsed.map((msg: any) => ({
          ...msg,
          timestamp: new Date(msg.timestamp)
        }));
        if (loadedMessages.length > 0) {
          setMessages(loadedMessages);
        }
      }
      
      // Load session ID
      const storedSessionId = localStorage.getItem(SESSION_KEY);
      if (storedSessionId) {
        setSessionId(storedSessionId);
      }
      
      setIsHydrated(true);
    } catch (e) {
      console.error('[ChatContext] Error loading from localStorage:', e);
      setIsHydrated(true);
    }
  }, []);
  
  // Persist messages to localStorage whenever they change (only after hydration)
  React.useEffect(() => {
    if (!isHydrated || typeof window === 'undefined') return;
    
    if (messages.length > 0) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
      } catch (e) {
        console.error('[ChatContext] Error saving to localStorage:', e);
      }
    } else {
      // Clear if messages are empty
      try {
        localStorage.removeItem(STORAGE_KEY);
      } catch (e) {
        console.error('[ChatContext] Error clearing localStorage:', e);
      }
    }
  }, [messages, isHydrated]);
  
  // Persist sessionId to localStorage (only after hydration)
  React.useEffect(() => {
    if (!isHydrated || typeof window === 'undefined') return;
    
    if (sessionId) {
      try {
        localStorage.setItem(SESSION_KEY, sessionId);
      } catch (e) {
        console.error('[ChatContext] Error saving sessionId to localStorage:', e);
      }
    } else {
      try {
        localStorage.removeItem(SESSION_KEY);
      } catch (e) {
        console.error('[ChatContext] Error removing sessionId from localStorage:', e);
      }
    }
  }, [sessionId, isHydrated]);

  const addMessage = useCallback((message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      ...message,
      id: `msg-${Date.now()}-${Math.random()}`,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, newMessage]);
  }, []);

  const updateStreamingMessage = useCallback((content: string, contributingAgents?: string[], contributingModels?: string[]) => {
    console.log('[ChatContext] updateStreamingMessage called with content length:', content.length);
    setMessages((prev) => {
      console.log('[ChatContext] Current messages count:', prev.length);
      const lastMessage = prev[prev.length - 1];
      console.log('[ChatContext] Last message:', lastMessage ? { role: lastMessage.role, hasContent: !!lastMessage.content, contentLength: lastMessage.content?.length || 0 } : 'null');
      
      if (lastMessage && lastMessage.role === 'assistant') {
        // For streaming, the backend sends the FULL accumulated content each time
        // So we should replace, not append, unless we're doing token-by-token streaming
        // Since backend sends full content deltas, we replace with the new content
        const updatedContent = content;
        console.log('[ChatContext] Updating message content:', {
          previousLength: lastMessage.content?.length || 0,
          newLength: content.length,
          preview: content.substring(0, 100),
          contributingAgents
        });
        
        const updatedMessage = { 
          ...lastMessage, 
          content: updatedContent,
          // Update contributing agents if provided
          ...(contributingAgents && contributingAgents.length > 0 ? { contributingAgents } : {}),
          ...(contributingModels && contributingModels.length > 0 ? { contributingModels } : {})
        };
        const newMessages = [...prev.slice(0, -1), updatedMessage];
        console.log('[ChatContext] Updated messages count:', newMessages.length);
        console.log('[ChatContext] Last message after update:', {
          role: newMessages[newMessages.length - 1].role,
          contentLength: newMessages[newMessages.length - 1].content.length,
          preview: newMessages[newMessages.length - 1].content.substring(0, 100),
          contributingAgents: newMessages[newMessages.length - 1].contributingAgents,
          contributingModels: newMessages[newMessages.length - 1].contributingModels
        });
        return newMessages;
      } else {
        console.warn('[ChatContext] No assistant message to update:', { 
          messagesCount: prev.length, 
          lastMessage: prev[prev.length - 1] ? { role: prev[prev.length - 1].role } : 'null',
          expectedRole: 'assistant'
        });
      }
      return prev;
    });
  }, []);

  const updateContributingAgents = useCallback((contributingAgents: string[]) => {
    setMessages((prev) => {
      const lastMessage = prev[prev.length - 1];
      if (lastMessage && lastMessage.role === 'assistant' && contributingAgents.length > 0) {
        return [...prev.slice(0, -1), { ...lastMessage, contributingAgents }];
      }
      return prev;
    });
  }, []);

  const updateContributingModels = useCallback((contributingModels: string[]) => {
    setMessages((prev) => {
      const lastMessage = prev[prev.length - 1];
      if (lastMessage && lastMessage.role === 'assistant' && contributingModels.length > 0) {
        return [...prev.slice(0, -1), { ...lastMessage, contributingModels }];
      }
      return prev;
    });
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setStreamingStatus(false);
    // Clear from localStorage too
    if (typeof window !== 'undefined') {
      try {
        localStorage.removeItem(STORAGE_KEY);
      } catch (e) {
        console.error('[ChatContext] Error clearing localStorage:', e);
      }
    }
  }, []);

  return (
    <ChatContext.Provider
      value={{
        messages,
        streamingStatus,
        sessionId,
        setSessionId,
        addMessage,
        updateStreamingMessage,
        updateContributingAgents,
        setStreamingStatus,
        clearMessages,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChatContext() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }
  return context;
}

