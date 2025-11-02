/**
 * Main chat interface page integrating MessageList, InputBox,
 * StreamingResponse, and SatisfactionFeedback components
 */

'use client';

import { ChatProvider } from '@/context/ChatContext';
import { SessionProvider } from '@/context/SessionContext';
import MessageList from '@/components/ChatInterface/MessageList';
import InputBox from '@/components/ChatInterface/InputBox';
import StreamingResponse from '@/components/ChatInterface/StreamingResponse';
import SatisfactionFeedback from '@/components/ChatInterface/SatisfactionFeedback';
import Header from '@/layouts/Header';

export default function ChatPage() {
  return (
    <SessionProvider>
      <ChatProvider>
        <div className="flex flex-col min-h-screen">
          <Header />
          <div className="flex-1 flex flex-col items-center overflow-hidden">
            <div className="w-full flex-1 flex flex-col max-w-6xl px-4">
              <MessageList />
              <StreamingResponse />
            </div>
            <div className="w-full flex flex-col">
              <InputBox />
              <SatisfactionFeedback />
            </div>
          </div>
        </div>
      </ChatProvider>
    </SessionProvider>
  );
}
