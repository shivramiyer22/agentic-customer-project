/**
 * Tests for KnowledgeBaseSelector component
 */

import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import KnowledgeBaseSelector from '@/components/DocumentUpload/KnowledgeBaseSelector'
import * as apiClient from '@/services/api-client'
import { render as customRender } from '../../utils/test-utils'

// Mock API client
jest.mock('@/services/api-client')

describe('KnowledgeBaseSelector component', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    ;(apiClient.uploadApi.getCollections as jest.Mock) = jest.fn().mockResolvedValue({
      collections: ['billing_knowledge_base', 'technical_knowledge_base', 'policy_knowledge_base'],
    })
  })

  it('should render selector correctly', async () => {
    customRender(<KnowledgeBaseSelector />)

    await waitFor(() => {
      expect(screen.getByLabelText(/Select knowledge base collection/i)).toBeInTheDocument()
    })
  })

  it('should load and display collections', async () => {
    customRender(<KnowledgeBaseSelector />)

    await waitFor(() => {
      expect(screen.getByText(/Auto-Map/i)).toBeInTheDocument()
    })
  })
})

