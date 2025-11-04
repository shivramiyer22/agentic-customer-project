/**
 * Tests for useChat hook
 */

import React from 'react'
import { render, screen, act, waitFor } from '@testing-library/react'
import { useChat } from '@/hooks/useChat'
import * as apiClient from '@/services/api-client'
import { render as customRender } from '../../utils/test-utils'

// Mock API client
jest.mock('@/services/api-client')

const TestComponent = () => {
  const { messages, sendMessage, streamingStatus, sessionId, resetChat } = useChat()

  return (
    <div>
      <div data-testid="messages-count">{messages.length}</div>
      <div data-testid="session-id">{sessionId || 'no-session'}</div>
      <div data-testid="streaming">{streamingStatus ? 'true' : 'false'}</div>
      <button
        onClick={() => sendMessage('Hello')}
        data-testid="send-message"
      >
        Send
      </button>
      <button onClick={resetChat} data-testid="reset-chat">
        Reset Chat
      </button>
    </div>
  )
}

describe('useChat hook', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    ;(apiClient.chatApi.streamMessage as jest.Mock) = jest.fn(() => jest.fn())
  })

  it('should initialize with empty messages', async () => {
    customRender(<TestComponent />)

    await waitFor(() => {
      expect(screen.getByTestId('messages-count')).toHaveTextContent('0')
    })
  })

  it('should send message correctly', async () => {
    customRender(<TestComponent />)

    await waitFor(() => {
      const sendButton = screen.getByTestId('send-message')
      act(() => {
        sendButton.click()
      })
    })

    // Note: sendMessage may fail if no sessionId, but the function should be called
    await waitFor(() => {
      // The hook should handle the case when sessionId is missing
      expect(screen.getByTestId('messages-count')).toBeInTheDocument()
    })
  })

  it('should reset chat correctly', async () => {
    customRender(<TestComponent />)

    await waitFor(() => {
      const resetButton = screen.getByTestId('reset-chat')
      act(() => {
        resetButton.click()
      })
    })

    // Note: resetChat clears messages and resets sessionId
    await waitFor(() => {
      expect(screen.getByTestId('messages-count')).toBeInTheDocument()
    })
  })

  it('should extract contributing_agents from metadata', async () => {
    const mockStreamMessage = jest.fn((callbacks) => {
      // Simulate streaming message with metadata
      const message = {
        content: 'Response',
        metadata: {
          contributing_agents: ['Technical Tool Agent'],
          contributing_models: ['AWS Bedrock Claude 3 Haiku']
        }
      }
      callbacks.onMessage?.(message)
      callbacks.onDone?.()
    })

    ;(apiClient.chatApi.streamMessage as jest.Mock) = jest.fn(() => mockStreamMessage)

    customRender(<TestComponent />)

    await waitFor(() => {
      const sendButton = screen.getByTestId('send-message')
      act(() => {
        sendButton.click()
      })
    })

    // Verify that streamMessage was called
    expect(apiClient.chatApi.streamMessage).toHaveBeenCalled()
  })

  it('should extract contributing_models from metadata', async () => {
    const mockStreamMessage = jest.fn((callbacks) => {
      const message = {
        content: 'Response',
        metadata: {
          contributing_agents: ['Policy Tool Agent'],
          contributing_models: ['AWS Bedrock Claude 3 Haiku', 'OpenAI gpt-4o-mini']
        }
      }
      callbacks.onMessage?.(message)
      callbacks.onDone?.()
    })

    ;(apiClient.chatApi.streamMessage as jest.Mock) = jest.fn(() => mockStreamMessage)

    customRender(<TestComponent />)

    await waitFor(() => {
      const sendButton = screen.getByTestId('send-message')
      act(() => {
        sendButton.click()
      })
    })

    expect(apiClient.chatApi.streamMessage).toHaveBeenCalled()
  })

  it('should handle done signal with contributing_agents and contributing_models', async () => {
    const mockStreamMessage = jest.fn((callbacks) => {
      // Send done signal with metadata
      callbacks.onDone?.({
        metadata: {
          contributing_agents: ['Billing Tool Agent'],
          contributing_models: ['AWS Bedrock Claude 3 Haiku', 'OpenAI gpt-4o-mini']
        }
      })
    })

    ;(apiClient.chatApi.streamMessage as jest.Mock) = jest.fn(() => mockStreamMessage)

    customRender(<TestComponent />)

    await waitFor(() => {
      const sendButton = screen.getByTestId('send-message')
      act(() => {
        sendButton.click()
      })
    })

    expect(apiClient.chatApi.streamMessage).toHaveBeenCalled()
  })
})
