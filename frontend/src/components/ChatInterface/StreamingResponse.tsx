/**
 * StreamingResponse component to handle and display SSE streaming tokens in real-time
 */

'use client';

import { useEffect, useRef } from 'react';
import { useChatContext } from '@/context/ChatContext';

export default function StreamingResponse() {
  const { streamingStatus, messages } = useChatContext();
  const lastMessageRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (lastMessageRef.current) {
      lastMessageRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  if (!streamingStatus) {
    return null;
  }

  return (
    <div className="flex items-center gap-2 px-4 py-2 text-sm text-gray-600">
      <div className="flex gap-1">
        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
      </div>
      <span>AI is typing...</span>
      <div ref={lastMessageRef} />
    </div>
  );
}

