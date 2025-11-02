/**
 * Tests for useSession hook
 */

import React from 'react'
import { render, screen, act, waitFor } from '@testing-library/react'
import { useSession } from '@/hooks/useSession'
import * as apiClient from '@/services/api-client'
import { render as customRender } from '../../utils/test-utils'

// Mock API client
jest.mock('@/services/api-client')

const TestComponent = () => {
  const { sessions, activeSession, switchSession, createNewSession, removeSession } = useSession()

  return (
    <div>
      <div data-testid="sessions-count">{sessions.length}</div>
      <div data-testid="active-session">{activeSession?.session_id || 'none'}</div>
      <button onClick={createNewSession} data-testid="create-session">
        Create Session
      </button>
    </div>
  )
}

describe('useSession hook', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    ;(apiClient.sessionApi.getSessions as jest.Mock) = jest.fn().mockResolvedValue({ sessions: [] })
  })

  it('should initialize with empty sessions', async () => {
    customRender(<TestComponent />)

    await waitFor(() => {
      expect(screen.getByTestId('sessions-count')).toBeInTheDocument()
      expect(screen.getByTestId('active-session')).toHaveTextContent('none')
    })
  })

  it('should create new session correctly', async () => {
    customRender(<TestComponent />)

    await waitFor(async () => {
      const createButton = screen.getByTestId('create-session')
      await act(async () => {
        createButton.click()
      })
    })

    // Session creation is handled by SessionContext.createSession (local, not API call)
    await waitFor(() => {
      expect(screen.getByTestId('active-session')).not.toHaveTextContent('none')
    })
  })
})

