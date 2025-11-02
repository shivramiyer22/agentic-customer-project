/**
 * Tests for ChatContext
 */

import React from 'react'
import { render, screen, act } from '@testing-library/react'
import { ChatProvider, useChatContext } from '@/context/ChatContext'

// Test component that uses ChatContext
const TestComponent = () => {
  const { messages, addMessage, clearMessages, streamingStatus, setStreamingStatus, sessionId, setSessionId } = useChatContext()

  return (
    <div>
      <div data-testid="messages-count">{messages.length}</div>
      <div data-testid="session-id">{sessionId || 'no-session'}</div>
      <div data-testid="streaming">{streamingStatus ? 'true' : 'false'}</div>
      <button
        onClick={() => addMessage({ content: 'Test', role: 'user' })}
        data-testid="add-message"
      >
        Add Message
      </button>
      <button onClick={clearMessages} data-testid="clear-messages">
        Clear
      </button>
      <button onClick={() => setStreamingStatus(true)} data-testid="set-streaming">
        Set Streaming
      </button>
      <button onClick={() => setSessionId('test-session')} data-testid="set-session">
        Set Session
      </button>
    </div>
  )
}

describe('ChatContext', () => {
  it('should provide default values', () => {
    render(
      <ChatProvider>
        <TestComponent />
      </ChatProvider>
    )

    expect(screen.getByTestId('messages-count')).toHaveTextContent('0')
    expect(screen.getByTestId('session-id')).toHaveTextContent('no-session')
    expect(screen.getByTestId('streaming')).toHaveTextContent('false')
  })

  it('should add messages correctly', () => {
    render(
      <ChatProvider>
        <TestComponent />
      </ChatProvider>
    )

    const addButton = screen.getByTestId('add-message')
    act(() => {
      addButton.click()
    })

    expect(screen.getByTestId('messages-count')).toHaveTextContent('1')
  })

  it('should clear messages correctly', () => {
    render(
      <ChatProvider>
        <TestComponent />
      </ChatProvider>
    )

    // Add a message first
    act(() => {
      screen.getByTestId('add-message').click()
    })

    // Clear messages
    act(() => {
      screen.getByTestId('clear-messages').click()
    })

    expect(screen.getByTestId('messages-count')).toHaveTextContent('0')
  })

  it('should update streaming status', () => {
    render(
      <ChatProvider>
        <TestComponent />
      </ChatProvider>
    )

    act(() => {
      screen.getByTestId('set-streaming').click()
    })

    expect(screen.getByTestId('streaming')).toHaveTextContent('true')
  })

  it('should update session ID', () => {
    render(
      <ChatProvider>
        <TestComponent />
      </ChatProvider>
    )

    act(() => {
      screen.getByTestId('set-session').click()
    })

    expect(screen.getByTestId('session-id')).toHaveTextContent('test-session')
  })

  it('should throw error when used outside provider', () => {
    // Suppress console.error for this test
    const originalError = console.error
    console.error = jest.fn()

    expect(() => {
      render(<TestComponent />)
    }).toThrow('useChatContext must be used within a ChatProvider')

    console.error = originalError
  })
})

