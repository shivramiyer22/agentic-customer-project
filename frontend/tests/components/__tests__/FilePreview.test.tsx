/**
 * Tests for FilePreview component
 */

import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import FilePreview from '@/components/DocumentUpload/FilePreview'
import { render as customRender } from '../../utils/test-utils'

describe('FilePreview component', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('should render empty state when no files', async () => {
    const { container } = customRender(<FilePreview />)

    // FilePreview returns null when no files, so container should be empty
    await waitFor(() => {
      expect(container.firstChild).toBeNull()
    })
  })
})

