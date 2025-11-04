/**
 * MessageList component to display conversation history
 * with clear visual distinction between user and AI messages
 */

'use client';

import React, { useEffect } from 'react';
import Image from 'next/image';
import { useChatContext } from '@/context/ChatContext';
import { cn } from '@/utils/cn';

export default function MessageList() {
  const { messages, streamingStatus } = useChatContext();
  
  // Debug logging
  useEffect(() => {
    console.log('[MessageList] Messages updated:', {
      count: messages.length,
      streamingStatus,
      messages: messages.map(m => ({
        id: m.id,
        role: m.role,
        contentLength: m.content?.length || 0,
        hasContent: !!m.content?.trim(),
        contentIsEmpty: !m.content || !m.content.trim(),
        preview: m.content?.substring(0, 50) || 'empty',
        fullContent: m.content
      }))
    });
    
    // Check specifically for assistant messages
    const assistantMessages = messages.filter(m => m.role === 'assistant');
    console.log('[MessageList] Assistant messages:', assistantMessages.map(m => ({
      id: m.id,
      contentLength: m.content?.length || 0,
      content: m.content || 'EMPTY',
      preview: m.content?.substring(0, 100) || 'NO CONTENT'
    })));
  }, [messages, streamingStatus]);

  if (messages.length === 0) {
     return (
      <div className="flex-1 flex items-center justify-center py-6 max-h-[33vh]">
        <div className="w-full max-w-full mx-auto px-4" style={{ paddingLeft: '144px', paddingRight: '16px' }}>
          <div className="w-full flex justify-center">
            <div className="text-center bg-primary text-white rounded-3xl shadow-2xl px-10 py-12 space-y-4 border border-white/40 max-w-3xl">
              <p className="text-4xl font-extrabold tracking-wide drop-shadow">
                Welcome to the Aerospace Company Customer Service Agent
              </p>
              <p className="text-xl font-semibold opacity-90">
                Ask a question about billing, technical support, or policy compliance
              </p>
              <p className="text-xs font-normal italic opacity-70 mt-6 pt-4 border-t border-white/30">
                AI generated output may not be accurate or complete. Always verify output before using.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto py-6">
      <div className="w-full max-w-full mx-auto px-4" style={{ paddingLeft: '144px', paddingRight: '16px' }}>
        <div className="max-w-[93%] ml-auto mr-auto space-y-6">
        {messages.map((message) => {
          const isUser = message.role === 'user';
          // Ensure content is a string, not an object or other type
          let formattedContent: string = '';
          if (message.content) {
            if (typeof message.content === 'string') {
              formattedContent = message.content;
            } else if (typeof message.content === 'object' && message.content !== null) {
              // If content is an object, try to extract string value
              if ('content' in message.content && typeof (message.content as any).content === 'string') {
                formattedContent = (message.content as any).content;
              } else {
                // Otherwise, log warning and use empty string
                console.warn('[MessageList] Content is an object without string value:', message.content);
                formattedContent = '';
              }
            } else {
              // Convert other types to string
              formattedContent = String(message.content);
            }
          }
          formattedContent = formattedContent.trim();
          const timestamp = message.timestamp.toLocaleTimeString();
          
          // Debug logging for assistant messages
          if (!isUser && formattedContent) {
            console.log('[MessageList] Rendering assistant message:', {
              id: message.id,
              contentLength: formattedContent.length,
              preview: formattedContent.substring(0, 100)
            });
          }

          return (
            <div key={message.id} className="w-full">
              <div
                className={cn(
                  'w-full rounded-2xl shadow-lg border px-6 py-5 space-y-3 transition-all',
                  isUser
                    ? 'bg-sky-100 border-sky-200 text-sky-900'
                    : 'bg-white border-gray-200 text-gray-900'
                )}
              >
                <div className="flex items-center gap-3">
                  {!isUser && (
                    <Image
                      src="/airplane.svg"
                      alt="AI Agent"
                      width={28}
                      height={28}
                      className="w-7 h-7"
                    />
                  )}
                  <span
                    className={cn(
                      'text-sm font-semibold uppercase tracking-wide',
                      isUser ? 'text-sky-700' : 'text-primary'
                    )}
                  >
                    {isUser ? 'User:' : 'AI-Customer-Agent:'}
                  </span>
                  <span className="text-xs text-gray-500 ml-auto">{timestamp}</span>
                </div>

                <p className="text-base leading-relaxed whitespace-pre-wrap break-words">
                  {formattedContent || (isUser ? '—' : (streamingStatus ? 'Generating response...' : 'No response received'))}
                </p>
                {/* Contributing Agents and Models display - on same line with || separator */}
                {!isUser && (message.contributingAgents && message.contributingAgents.length > 0 || message.contributingModels && message.contributingModels.length > 0) && (
                  <div className="text-xs text-gray-500 mt-2 pt-2 border-t border-gray-200">
                    <div className="flex flex-wrap items-center gap-2">
                      {message.contributingAgents && message.contributingAgents.length > 0 && (
                        <span>
                          <span className="font-bold">Contributing Agent Calls:</span>{' '}
                          <span className="text-gray-600 font-normal">
                            {message.contributingAgents.join(', ')}
                          </span>
                        </span>
                      )}
                      {message.contributingAgents && message.contributingAgents.length > 0 && message.contributingModels && message.contributingModels.length > 0 && (
                        <span className="text-gray-400 font-bold">||</span>
                      )}
                      {message.contributingModels && message.contributingModels.length > 0 && (
                        <span>
                          <span className="font-bold">Contributing Model Calls:</span>{' '}
                          <span className="text-gray-600 font-normal">
                            {message.contributingModels.join(', ')}
                          </span>
                        </span>
                      )}
                    </div>
                  </div>
                )}

                {message.sources && message.sources.length > 0 && (
                  <div className="pt-3 border-t border-gray-200">
                    <details className="text-xs text-gray-600">
                      <summary className="cursor-pointer font-semibold">Sources ({message.sources.length})</summary>
                      <div className="mt-2 space-y-1">
                        {message.sources.map((source, index) => (
                          <div key={index} className="text-gray-600">
                            <span className="font-semibold">{source.name}</span>
                            <p className="text-xs mt-1 italic">{source.excerpt}</p>
                          </div>
                        ))}
                      </div>
                    </details>
                  </div>
                )}
              </div>
            </div>
          );
        })}
        </div>
      </div>
    </div>
  );
}

