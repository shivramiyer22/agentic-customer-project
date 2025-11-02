/**
 * Tests for UploadProgress component
 */

import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import UploadProgress from '@/components/DocumentUpload/UploadProgress'
import { render as customRender } from '../../utils/test-utils'

// Mock useUploadContext hook but preserve UploadProvider
const mockUploadContext = {
  uploadState: {
    files: [
      {
        id: '1',
        file: new File(['content'], 'test.pdf', { type: 'application/pdf' }),
        status: 'uploading',
        progress: 50,
      },
      {
        id: '2',
        file: new File(['content'], 'test2.txt', { type: 'text/plain' }),
        status: 'success',
        progress: 100,
        chunksCount: 5,
      },
    ],
    targetCollection: 'billing_knowledge_base',
    isUploading: true,
    overallProgress: 75,
  },
  uploadFiles: jest.fn(),
  clearCompletedFiles: jest.fn(),
}

jest.mock('@/context/UploadContext', () => {
  const actual = jest.requireActual('@/context/UploadContext')
  return {
    ...actual,
    useUploadContext: () => mockUploadContext,
  }
})

describe('UploadProgress component', () => {
  it('should render progress correctly', async () => {
    customRender(<UploadProgress />)

    await waitFor(() => {
      expect(screen.getByText(/75/)).toBeInTheDocument()
      expect(screen.getByText('test.pdf')).toBeInTheDocument()
      expect(screen.getByText('test2.txt')).toBeInTheDocument()
    })
  })

  it('should display file status correctly', async () => {
    customRender(<UploadProgress />)

    await waitFor(() => {
      expect(screen.getByText(/uploading/i)).toBeInTheDocument()
      expect(screen.getByText(/success/i)).toBeInTheDocument()
    })
  })

  it('should display chunks count for completed files', async () => {
    customRender(<UploadProgress />)

    await waitFor(() => {
      expect(screen.getByText(/5 chunks/i)).toBeInTheDocument()
    })
  })
})

