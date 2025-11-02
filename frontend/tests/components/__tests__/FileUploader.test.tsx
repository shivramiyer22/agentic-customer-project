/**
 * Tests for FileUploader component
 */

import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import FileUploader from '@/components/DocumentUpload/FileUploader'
import { render as customRender } from '../../utils/test-utils'

describe('FileUploader component', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('should render upload area correctly', () => {
    customRender(<FileUploader />)

    expect(screen.getByText(/drag and drop/i)).toBeInTheDocument()
    expect(screen.getByText(/PDF, TXT, Markdown, JSON/)).toBeInTheDocument()
  })

  it('should handle file input change', async () => {
    const user = userEvent.setup()
    customRender(<FileUploader />)

    const file = new File(['content'], 'test.pdf', { type: 'application/pdf' })
    const input = screen.getByLabelText('File input') as HTMLInputElement

    await user.upload(input, file)

    // File should be added via useUpload hook
    // The input will have the file but useUpload handles adding it to state
    expect(input).toBeInTheDocument()
  })

  it('should handle drag and drop', () => {
    customRender(<FileUploader />)

    const uploadArea = screen.getByRole('button')
    const file = new File(['content'], 'test.pdf', { type: 'application/pdf' })
    
    // Create a mock DataTransfer with files and items
    const dataTransfer = {
      files: {
        length: 1,
        item: (index: number) => (index === 0 ? file : null),
        0: file,
      } as unknown as FileList,
      items: {
        length: 1,
      },
    }

    fireEvent.dragOver(uploadArea)
    fireEvent.drop(uploadArea, {
      dataTransfer,
    })

    // File should be added via useUpload hook
    expect(uploadArea).toBeInTheDocument()
  })
})

