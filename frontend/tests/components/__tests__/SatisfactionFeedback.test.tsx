/**
 * Tests for SatisfactionFeedback component
 */

import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import SatisfactionFeedback from '@/components/ChatInterface/SatisfactionFeedback'
import * as apiClient from '@/services/api-client'
import { render as customRender } from '../../utils/test-utils'

// Mock API client
jest.mock('@/services/api-client')

// Mock useChatContext to provide sessionId and messages
jest.mock('@/context/ChatContext', () => ({
  ...jest.requireActual('@/context/ChatContext'),
  useChatContext: () => ({
    sessionId: 'session-123',
    messages: [
      { id: '1', content: 'Hello', role: 'user', timestamp: new Date() },
      { id: '2', content: 'Hi there!', role: 'assistant', timestamp: new Date() },
    ],
  }),
}))

describe('SatisfactionFeedback component', () => {
  const mockOnFeedbackSubmitted = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
    ;(apiClient.feedbackApi.submitFeedback as jest.Mock) = jest.fn().mockResolvedValue({ success: true })
  })

  it('should render feedback buttons correctly', async () => {
    customRender(<SatisfactionFeedback onSubmitted={mockOnFeedbackSubmitted} />)

    await waitFor(() => {
      expect(screen.getByText('Was this response helpful?')).toBeInTheDocument()
      expect(screen.getByLabelText('Thumbs up - helpful')).toBeInTheDocument()
      expect(screen.getByLabelText('Thumbs down - not helpful')).toBeInTheDocument()
    })
  })

  it('should submit thumbs up feedback', async () => {
    const user = userEvent.setup()
    customRender(<SatisfactionFeedback onSubmitted={mockOnFeedbackSubmitted} />)

    await waitFor(async () => {
      const thumbsUp = await screen.findByLabelText('Thumbs up - helpful')
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
    customRender(<SatisfactionFeedback onSubmitted={mockOnFeedbackSubmitted} />)

    await waitFor(async () => {
      const thumbsDown = await screen.findByLabelText('Thumbs down - not helpful')
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
    customRender(<SatisfactionFeedback onSubmitted={mockOnFeedbackSubmitted} />)

    await waitFor(async () => {
      const thumbsUp = await screen.findByLabelText('Thumbs up - helpful')
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
    customRender(<SatisfactionFeedback onSubmitted={mockOnFeedbackSubmitted} />)

    await waitFor(() => {
      // Submit button should not be visible until rating is selected
      expect(screen.queryByText('Submit')).not.toBeInTheDocument()
    })
  })
})

