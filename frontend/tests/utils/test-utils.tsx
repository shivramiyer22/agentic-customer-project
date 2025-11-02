/**
 * Test utilities for React Testing Library
 */

import React, { ReactElement } from 'react'
import { render, RenderOptions } from '@testing-library/react'
import { ChatProvider } from '@/context/ChatContext'
import { SessionProvider } from '@/context/SessionContext'
import { UploadProvider } from '@/context/UploadContext'

// Custom render function that includes providers
const AllTheProviders = ({ children }: { children: React.ReactNode }) => {
  return (
    <SessionProvider>
      <UploadProvider>
        <ChatProvider>{children}</ChatProvider>
      </UploadProvider>
    </SessionProvider>
  )
}

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: AllTheProviders, ...options })

// Re-export everything
export * from '@testing-library/react'

// Override render method
export { customRender as render }

