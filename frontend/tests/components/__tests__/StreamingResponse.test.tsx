/**
 * Tests for StreamingResponse component
 */

import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import StreamingResponse from '@/components/ChatInterface/StreamingResponse'
import { render as customRender } from '../../utils/test-utils'

// Mock useChatContext
jest.mock('@/context/ChatContext', () => ({
  ...jest.requireActual('@/context/ChatContext'),
  useChatContext: () => ({
    streamingStatus: false,
  }),
}))

describe('StreamingResponse component', () => {
  it('should not render when not streaming', async () => {
    const { container } = customRender(<StreamingResponse />)
    
    await waitFor(() => {
      expect(container.firstChild).toBeNull()
    })
  })
})

