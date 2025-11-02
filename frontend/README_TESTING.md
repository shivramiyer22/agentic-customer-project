# Frontend Testing Guide

## Overview

This frontend application uses **Jest** and **React Testing Library** for comprehensive testing.

## Test Infrastructure

### Setup Files

- **`jest.config.js`**: Jest configuration with Next.js integration
- **`jest.setup.js`**: Global test setup (mocks, matchers)
- **`tests/utils/test-utils.tsx`**: Custom render function with providers

### Test Organization

```
tests/
├── components/        # Component tests
├── context/          # Context provider tests
├── hooks/            # Custom hook tests
├── services/         # API client tests
└── utils/            # Utility function tests
```

## Running Tests

### Run All Tests
```bash
npm test
```

### Run Tests in Watch Mode
```bash
npm run test:watch
```

### Run Tests with Coverage
```bash
npm run test:coverage
```

### Run Specific Test File
```bash
npm test -- path/to/test/file.test.tsx
```

## Test Structure

### Example Test File
```typescript
import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import { render as customRender } from '../../utils/test-utils'
import MyComponent from '@/components/MyComponent'

describe('MyComponent', () => {
  it('should render correctly', async () => {
    customRender(<MyComponent />)
    
    await waitFor(() => {
      expect(screen.getByText('Hello')).toBeInTheDocument()
    })
  })
})
```

## Testing Best Practices

1. **Use Custom Render**: Always use `customRender` from `test-utils.tsx` for components that use context
2. **Wait for Async**: Use `waitFor` for async operations
3. **Mock External Dependencies**: Mock API calls and external services
4. **Test User Interactions**: Use `@testing-library/user-event` for user interactions
5. **Accessibility**: Use queries that encourage accessibility (getByLabelText, getByRole)

## Mocking

### API Client Mocking
```typescript
jest.mock('@/services/api-client')
;(apiClient.chatApi.sendMessage as jest.Mock) = jest.fn().mockResolvedValue({})
```

### Context Mocking
```typescript
jest.mock('@/context/ChatContext', () => ({
  useChatContext: () => ({
    messages: [],
    sessionId: 'test-session',
  }),
}))
```

## Current Test Coverage

- ✅ **Utility Functions**: 8/8 tests (100%)
- ✅ **Services**: 9/9 tests (100%)
- ✅ **Context Providers**: 8/8 tests (100%)
- ✅ **Custom Hooks**: 12/12 tests (100%) - Includes contributing models metadata extraction
- ✅ **Components**: 40/40 tests (100%) - Includes contributing agents and models display
- ✅ **Layout**: 1/1 tests (100%)

**Total: 78/78 tests passing (100%)**

### New Test Coverage (Contributing Models Feature)

- ✅ **MessageList Component**: Tests for displaying contributing agents and models
  - Display contributing agents when present
  - Display contributing models when present
  - Display both when both are present
  - Hide section when neither is present

- ✅ **useChat Hook**: Tests for metadata extraction
  - Extract contributing_agents from metadata
  - Extract contributing_models from metadata
  - Handle done signal with both agents and models

## Troubleshooting

### Tests Fail Due to Missing Context
- Ensure components are wrapped with `customRender` which includes providers

### Fetch Not Defined
- Global fetch is mocked in `jest.setup.js`
- If custom mocking needed, override in test file

### Async Operations Not Completing
- Use `waitFor` with proper timeout
- Check that async operations are properly awaited

