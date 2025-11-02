/**
 * Tests for SessionContext
 */

import React from 'react'
import { render, screen, act, waitFor } from '@testing-library/react'
import { SessionProvider, useSessionContext } from '@/context/SessionContext'
import * as apiClient from '@/services/api-client'

// Mock API client
jest.mock('@/services/api-client')

const TestComponent = () => {
  const {
    sessions,
    activeSession,
    loading,
    createSession,
    deleteSession,
  } = useSessionContext()

  return (
    <div>
      <div data-testid="sessions-count">{sessions.length}</div>
      <div data-testid="active-session">{activeSession?.session_id || 'none'}</div>
      <div data-testid="loading">{loading ? 'true' : 'false'}</div>
      <button
        onClick={() => createSession()}
        data-testid="create-session"
      >
        Create Session
      </button>
      <button
        onClick={() => deleteSession('session-1')}
        data-testid="delete-session"
      >
        Delete Session
      </button>
    </div>
  )
}

describe('SessionContext', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    // Mock getSessions to return proper structure
    const mockGetSessions = jest.fn().mockResolvedValue({ sessions: [] })
    ;(apiClient.sessionApi.getSessions as jest.Mock) = mockGetSessions
    // Also ensure sessionApi is properly mocked
    if (!apiClient.sessionApi.getSessions) {
      (apiClient.sessionApi as any).getSessions = mockGetSessions
    }
  })

  it('should provide default values', async () => {
    render(
      <SessionProvider>
        <TestComponent />
      </SessionProvider>
    )

    await waitFor(() => {
      expect(screen.getByTestId('sessions-count')).toHaveTextContent('0')
      expect(screen.getByTestId('active-session')).toHaveTextContent('none')
      expect(screen.getByTestId('loading')).toHaveTextContent('false')
    })
  })

  it('should create session correctly', async () => {
    render(
      <SessionProvider>
        <TestComponent />
      </SessionProvider>
    )

    await waitFor(() => {
      const createButton = screen.getByTestId('create-session')
      act(() => {
        createButton.click()
      })
    })

    // Session creation is handled locally by SessionContext (not API call)
    await waitFor(() => {
      expect(screen.getByTestId('active-session')).not.toHaveTextContent('none')
    })
  })

  it('should delete session correctly', async () => {
    ;(apiClient.sessionApi.deleteSession as jest.Mock) = jest.fn().mockResolvedValue({})

    render(
      <SessionProvider>
        <TestComponent />
      </SessionProvider>
    )

    await waitFor(() => {
      const deleteButton = screen.getByTestId('delete-session')
      act(() => {
        deleteButton.click()
      })
    })

    await waitFor(() => {
      expect(apiClient.sessionApi.deleteSession).toHaveBeenCalledWith('session-1')
    })
  })

  it('should throw error when used outside provider', () => {
    // Suppress console.error for this test
    const originalError = console.error
    console.error = jest.fn()

    expect(() => {
      render(<TestComponent />)
    }).toThrow('useSessionContext must be used within a SessionProvider')

    console.error = originalError
  })
})
