/**
 * Tests for useUpload hook
 */

import React from 'react'
import { render, screen, act, waitFor } from '@testing-library/react'
import { useUpload } from '@/hooks/useUpload'
import * as apiClient from '@/services/api-client'

// Mock API client
jest.mock('@/services/api-client')

const TestComponent = () => {
  const { uploadState, addFiles, removeFile, setTargetCollection, uploadFiles } = useUpload()

  return (
    <div>
      <div data-testid="files-count">{uploadState.files.length}</div>
      <div data-testid="target-collection">{uploadState.targetCollection || 'none'}</div>
      <div data-testid="uploading">{uploadState.isUploading ? 'true' : 'false'}</div>
      <button
        onClick={() => {
          const file = new File(['content'], 'test.pdf', { type: 'application/pdf' })
          addFiles([file])
        }}
        data-testid="add-files"
      >
        Add Files
      </button>
      <button onClick={() => uploadFiles()} data-testid="upload-files">
        Upload
      </button>
    </div>
  )
}

describe('useUpload hook', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    ;(apiClient.uploadApi.uploadFiles as jest.Mock) = jest.fn().mockResolvedValue({
      upload_id: 'upload-123',
      status: 'queued',
      files: [],
    })
    ;(apiClient.uploadApi.getUploadStatus as jest.Mock) = jest.fn().mockResolvedValue({
      upload_id: 'upload-123',
      status: 'completed',
      files: [],
      overall_progress: 100,
    })
  })

  it('should initialize with empty state', () => {
    render(<TestComponent />)

    expect(screen.getByTestId('files-count')).toHaveTextContent('0')
    expect(screen.getByTestId('target-collection')).toHaveTextContent('none')
    expect(screen.getByTestId('uploading')).toHaveTextContent('false')
  })

  it('should add files correctly', () => {
    render(<TestComponent />)

    const addButton = screen.getByTestId('add-files')
    act(() => {
      addButton.click()
    })

    expect(screen.getByTestId('files-count')).toHaveTextContent('1')
  })

  it('should upload files correctly', async () => {
    render(<TestComponent />)

    // Add file first
    act(() => {
      screen.getByTestId('add-files').click()
    })

    expect(screen.getByTestId('files-count')).toHaveTextContent('1')

    // Upload - wait for files to be added first
    await waitFor(() => {
      expect(screen.getByTestId('files-count')).toHaveTextContent('1')
    })

    // Note: uploadFiles requires files with status 'pending' or 'error'
    // Newly added files have status 'pending', so upload should work
    const uploadButton = screen.getByTestId('upload-files')
    
    await waitFor(async () => {
      await act(async () => {
        uploadButton.click()
      })
    })

    // Check that upload was attempted
    await waitFor(() => {
      // The upload function should be called if files are pending
      expect(apiClient.uploadApi.uploadFiles).toHaveBeenCalled()
    }, { timeout: 3000 })
  })
})

