/**
 * Tests for Header component
 */

import React from 'react'
import { render, screen } from '@testing-library/react'
import Header from '@/layouts/Header'

describe('Header component', () => {
  it('should render header with title', () => {
    render(<Header />)

    expect(screen.getByText('The Aerospace Company Customer Service Agent')).toBeInTheDocument()
  })

  it('should render airplane icon', () => {
    render(<Header />)

    // Icon is an Image component with alt text
    const icon = screen.getByAltText(/airplane|logo/i)
    expect(icon).toBeInTheDocument()
  })

  it('should have proper structure', () => {
    render(<Header />)

    const header = screen.getByRole('banner')
    expect(header).toBeInTheDocument()
  })
})

