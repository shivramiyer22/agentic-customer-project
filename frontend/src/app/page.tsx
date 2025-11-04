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
        <div className="flex flex-col h-screen">
          {/* Fixed Header */}
          <div className="flex-shrink-0">
            <Header />
          </div>
          
          {/* Scrollable Center Pane - Messages */}
          <div className="flex-1 flex flex-col items-center overflow-y-auto">
            <div className="w-full flex-1 flex flex-col max-w-[86.4rem]">
              <MessageList />
              <StreamingResponse />
            </div>
          </div>
          
          {/* Fixed Bottom Pane - Input Box and Feedback */}
          <div className="flex-shrink-0 w-full flex flex-col">
            <InputBox />
            <SatisfactionFeedback />
          </div>
        </div>
      </ChatProvider>
    </SessionProvider>
  );
}
