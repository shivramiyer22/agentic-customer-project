/**
 * InputBox component with multi-line text input field and "Send" button
 */

'use client';

import { useState, useRef, KeyboardEvent } from 'react';
import { useChat } from '@/hooks/useChat';
import { cn } from '@/utils/cn';

export default function InputBox() {
  const [input, setInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { sendMessage, streamingStatus, resetChat } = useChat();

  const handleSend = async () => {
    if (!input.trim() || isSending || streamingStatus) return;

    setIsSending(true);
    try {
      await sendMessage(input);
      setInput('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  };

  const isDisabled = !input.trim() || isSending || streamingStatus;

  return (
    <div className="border-t border-white/50 bg-white/80 backdrop-blur-lg shadow-[0_-10px_40px_rgba(15,23,42,0.08)]">
      {/* Input box container - offset from sidebar (128px + margin) */}
      <div className="w-full max-w-full mx-auto py-4" style={{ paddingLeft: '144px', paddingRight: '16px' }}>
        <div className="max-w-[93%] ml-auto mr-auto">
          <div className="flex flex-col md:flex-row md:items-end gap-3 w-full">
            <div className="flex-1">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={handleChange}
                onKeyDown={handleKeyDown}
                placeholder="Type your message... (Press Enter to send, Shift+Enter for new line)"
                className={cn(
                  'w-full resize-none rounded-2xl border-4 border-gray-800 bg-white/90 px-4 py-3 shadow-inner text-base',
                  'focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary',
                  'disabled:bg-gray-100 disabled:cursor-not-allowed disabled:border-gray-400',
                  'min-h-[80px] max-h-[240px] placeholder:text-gray-400'
                )}
                disabled={isSending || streamingStatus}
                rows={1}
                aria-label="Chat input"
              />
              <div className="text-xs text-gray-500 mt-1 text-right">
                {input.length} characters
              </div>
            </div>

            <div className="flex items-center gap-3 justify-center md:justify-end self-end">
              <button
                type="button"
                onClick={handleSend}
                disabled={isDisabled}
                className={cn(
                  'flex items-center justify-center w-14 h-14 rounded-full border-2 border-primary text-white shadow-md transition hover:bg-primary-dark hover:border-primary-dark focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2',
                  isDisabled ? 'bg-gray-300 border-gray-300 cursor-not-allowed' : 'bg-primary cursor-pointer'
                )}
                aria-label="Send message"
                title={isDisabled ? 'Enter a message to send' : 'Send message'}
              >
                {isSending || streamingStatus ? (
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    className="w-6 h-6 animate-spin"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                  >
                    <circle cx="12" cy="12" r="10" className="opacity-25" />
                    <path d="M12 2a10 10 0 0 1 10 10" className="opacity-75" />
                  </svg>
                ) : (
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    className="w-6 h-6"
                  >
                    <path d="M3 3l18 9-18 9 4-9-4-9z" />
                    <path d="M13 12L7 9l6 3-6 3 6-3z" />
                  </svg>
                )}
              </button>

              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={resetChat}
                  className={cn(
                    'flex items-center justify-center w-14 h-14 rounded-full border-2 border-primary bg-primary text-white shadow-md transition hover:bg-primary-dark hover:border-primary-dark focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2'
                  )}
                  title="Start a new chat"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    className="w-5 h-5"
                  >
                    <path d="M4 5h12" />
                    <path d="M4 10h8" />
                    <path d="M4 15h6" />
                    <path d="M14 19l4-4-4-4" />
                    <path d="M18 15h-7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

