/**
 * Tests for MessageList component
 */

import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import MessageList from '@/components/ChatInterface/MessageList'
import { render as customRender } from '../../utils/test-utils'
import { useChatContext } from '@/context/ChatContext'

// Clear localStorage before each test to avoid interference
beforeEach(() => {
  localStorage.clear()
})

// Mock useChatContext
const MockMessageList = () => {
  const { messages, addMessage } = useChatContext()
  
  React.useEffect(() => {
    // Add test messages
    addMessage({ content: 'Hello', role: 'user' })
    addMessage({ content: 'Hi there!', role: 'assistant', agent: 'supervisor' })
  }, [addMessage])
  
  return <MessageList />
}

describe('MessageList component', () => {
  it('should render empty state when no messages', async () => {
    customRender(<MessageList />)

    await waitFor(() => {
      expect(screen.getByText(/Welcome to the Aerospace Company Customer Service Agent/i)).toBeInTheDocument()
    })
  })

  it('should render messages correctly', async () => {
    customRender(<MockMessageList />)

    await waitFor(() => {
      expect(screen.getByText('Hello')).toBeInTheDocument()
      expect(screen.getByText('Hi there!')).toBeInTheDocument()
    })
  })

  it('should display agent name for assistant messages', async () => {
    customRender(<MockMessageList />)

    await waitFor(() => {
      expect(screen.getByText('Hi there!')).toBeInTheDocument()
    }, { timeout: 5000 })
    
    // Agent name is displayed as "AI-Customer-Agent:" in the header
    expect(screen.getByText(/AI-Customer-Agent:/i)).toBeInTheDocument()
  })

  it('should display contributing agents when present', async () => {
    const MessageListWithContributingAgents = () => {
      const { messages, addMessage } = useChatContext()
      
      React.useEffect(() => {
        // Add user message first, then assistant with contributing agents
        addMessage({ 
          content: 'Question', 
          role: 'user'
        })
        addMessage({ 
          content: 'Response', 
          role: 'assistant', 
          agent: 'supervisor',
          contributingAgents: ['Technical Tool Agent', 'Policy Tool Agent']
        })
      }, [addMessage])
      
      return <MessageList />
    }

    customRender(<MessageListWithContributingAgents />)

    await waitFor(() => {
      expect(screen.getByText('Response')).toBeInTheDocument()
    }, { timeout: 3000 })

    await waitFor(() => {
      expect(screen.getByText(/Contributing Agent Calls:/i)).toBeInTheDocument()
    }, { timeout: 3000 })

    expect(screen.getByText(/Technical Tool Agent/i)).toBeInTheDocument()
    expect(screen.getByText(/Policy Tool Agent/i)).toBeInTheDocument()
  })

  it('should display contributing models when present', async () => {
    const MessageListWithContributingModels = () => {
      const { messages, addMessage } = useChatContext()
      const messagesAdded = React.useRef(false)
      
      React.useEffect(() => {
        const timer = setTimeout(() => {
          if (!messagesAdded.current && messages.length === 0) {
            messagesAdded.current = true
            addMessage({ 
              content: 'Question', 
              role: 'user'
            })
            addMessage({ 
              content: 'Response', 
              role: 'assistant', 
              agent: 'supervisor',
              contributingModels: ['AWS Bedrock Claude 3 Haiku', 'OpenAI gpt-4o-mini']
            })
          }
        }, 100)
        
        return () => clearTimeout(timer)
      }, [addMessage, messages.length])
      
      return <MessageList />
    }

    customRender(<MessageListWithContributingModels />)

    await waitFor(() => {
      expect(screen.getByText('Response')).toBeInTheDocument()
    }, { timeout: 5000 })

    await waitFor(() => {
      expect(screen.getByText(/Contributing Model Calls:/i)).toBeInTheDocument()
    }, { timeout: 5000 })

    expect(screen.getByText(/AWS Bedrock Claude 3 Haiku/i)).toBeInTheDocument()
    expect(screen.getByText(/OpenAI gpt-4o-mini/i)).toBeInTheDocument()
  })

  it('should display both contributing agents and models when both are present', async () => {
    const MessageListWithBoth = () => {
      const { messages, addMessage } = useChatContext()
      const messagesAdded = React.useRef(false)
      
      React.useEffect(() => {
        const timer = setTimeout(() => {
          if (!messagesAdded.current && messages.length === 0) {
            messagesAdded.current = true
            addMessage({ 
              content: 'Question', 
              role: 'user'
            })
            addMessage({ 
              content: 'Response', 
              role: 'assistant', 
              agent: 'supervisor',
              contributingAgents: ['Technical Tool Agent'],
              contributingModels: ['AWS Bedrock Claude 3 Haiku', 'OpenAI gpt-4o-mini']
            })
          }
        }, 100)
        
        return () => clearTimeout(timer)
      }, [addMessage, messages.length])
      
      return <MessageList />
    }

    customRender(<MessageListWithBoth />)

    await waitFor(() => {
      expect(screen.getByText('Response')).toBeInTheDocument()
    }, { timeout: 5000 })

    await waitFor(() => {
      expect(screen.getByText(/Contributing Agent Calls:/i)).toBeInTheDocument()
    }, { timeout: 5000 })

    expect(screen.getByText(/Contributing Model Calls:/i)).toBeInTheDocument()
    expect(screen.getByText(/Technical Tool Agent/i)).toBeInTheDocument()
    expect(screen.getByText(/AWS Bedrock Claude 3 Haiku/i)).toBeInTheDocument()
  })

  it('should not display contributing info section when neither agents nor models are present', async () => {
    customRender(<MockMessageList />)

    await waitFor(() => {
      expect(screen.getByText('Hi there!')).toBeInTheDocument()
    })

    // Should not show contributing agents or models section
    expect(screen.queryByText(/Contributing Agent Calls:/i)).not.toBeInTheDocument()
    expect(screen.queryByText(/Contributing Model Calls:/i)).not.toBeInTheDocument()
  })
})

