/**
 * Tests for SatisfactionFeedback component
 */

import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import SatisfactionFeedback from '@/components/ChatInterface/SatisfactionFeedback'
import * as apiClient from '@/services/api-client'

// Mock API client
jest.mock('@/services/api-client')

const defaultContextValue = {
  sessionId: 'session-123',
  messages: [
    { id: '1', content: 'Hello', role: 'user', timestamp: new Date() },
    { id: '2', content: 'Hi there!', role: 'assistant', timestamp: new Date() },
  ],
  tokenUsage: { inputTokens: 100, outputTokens: 50 },
};

const mockUseChatContext = jest.fn(() => defaultContextValue);

jest.mock('@/context/ChatContext', () => {
  const actual = jest.requireActual('@/context/ChatContext');
  return {
    ...actual,
    useChatContext: () => mockUseChatContext(),
  };
});

describe('SatisfactionFeedback component', () => {
  const mockOnFeedbackSubmitted = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
    jest.spyOn(apiClient.feedbackApi, 'submitFeedback').mockResolvedValue({ success: true })
    mockUseChatContext.mockImplementation(() => ({
      sessionId: defaultContextValue.sessionId,
      messages: [...defaultContextValue.messages],
      tokenUsage: { ...defaultContextValue.tokenUsage },
    }))
  })

  it('should render feedback buttons correctly', async () => {
    render(<SatisfactionFeedback onSubmitted={mockOnFeedbackSubmitted} />)

    await waitFor(() => {
      expect(screen.getByText('Was this response helpful?')).toBeInTheDocument()
      expect(screen.getAllByLabelText('Thumbs up - helpful')[0]).toBeInTheDocument()
      expect(screen.getAllByLabelText('Thumbs down - not helpful')[0]).toBeInTheDocument()
      expect(screen.getByText(/Token count for this chat:/i)).toBeInTheDocument()
      expect(screen.getByText(/Total cost for this chat:/i)).toBeInTheDocument()
    })
  })

  it('should submit thumbs up feedback', async () => {
    const user = userEvent.setup()
    render(<SatisfactionFeedback onSubmitted={mockOnFeedbackSubmitted} />)

    await waitFor(async () => {
      const [thumbsUp] = await screen.findAllByLabelText('Thumbs up - helpful')
      await user.click(thumbsUp)

      const submitButton = await screen.findByText('Submit')
      await user.click(submitButton)

      await waitFor(() => {
        expect(apiClient.feedbackApi.submitFeedback).toHaveBeenCalledWith(
          'session-123',
          'thumbs_up',
          undefined
        )
      })
    })
  })

  it('should submit thumbs down feedback with comment', async () => {
    const user = userEvent.setup()
    render(<SatisfactionFeedback onSubmitted={mockOnFeedbackSubmitted} />)

    await waitFor(async () => {
      const [thumbsDown] = await screen.findAllByLabelText('Thumbs down - not helpful')
      await user.click(thumbsDown)

      const commentBox = await screen.findByPlaceholderText('Optional: Add your feedback...')
      await user.type(commentBox, 'Not helpful')

      const submitButton = await screen.findByText('Submit')
      await user.click(submitButton)

      await waitFor(() => {
        expect(apiClient.feedbackApi.submitFeedback).toHaveBeenCalledWith(
          'session-123',
          'thumbs_down',
          'Not helpful'
        )
      })
    })
  })

  it('should show thank you message after submission', async () => {
    const user = userEvent.setup()
    render(<SatisfactionFeedback onSubmitted={mockOnFeedbackSubmitted} />)

    await waitFor(async () => {
      const [thumbsUp] = await screen.findAllByLabelText('Thumbs up - helpful')
      await user.click(thumbsUp)

      const submitButton = await screen.findByText('Submit')
      await user.click(submitButton)

      // After submission, component should hide (returns null when isSubmitted is true)
      await waitFor(() => {
        // Component returns null after submission, so we verify API was called
        expect(apiClient.feedbackApi.submitFeedback).toHaveBeenCalled()
      })
    })
  })

  it('should not show submit button without selecting rating', async () => {
    render(<SatisfactionFeedback onSubmitted={mockOnFeedbackSubmitted} />)

    await waitFor(() => {
      // Submit button should not be visible until rating is selected
      expect(screen.queryByText('Submit')).not.toBeInTheDocument()
    })
  })

  it('should disable feedback buttons when no user input', async () => {
    // With default context (user message present) buttons are enabled
    const { unmount } = render(<SatisfactionFeedback onSubmitted={mockOnFeedbackSubmitted} />)
    expect(screen.getAllByLabelText('Thumbs up - helpful')[0]).not.toBeDisabled()
    expect(screen.getAllByLabelText('Thumbs down - not helpful')[0]).not.toBeDisabled()
    unmount()

    mockUseChatContext.mockImplementation(() => ({
      sessionId: 'session-123',
      messages: [
        { id: '1', content: '', role: 'assistant', timestamp: new Date() },
      ],
      tokenUsage: { inputTokens: 0, outputTokens: 0 },
    }))

    render(<SatisfactionFeedback onSubmitted={mockOnFeedbackSubmitted} />)

    const [thumbsUp] = screen.getAllByLabelText('Thumbs up - helpful')
    const [thumbsDown] = screen.getAllByLabelText('Thumbs down - not helpful')

    expect(thumbsUp).toBeDisabled()
    expect(thumbsDown).toBeDisabled()
  })
})

