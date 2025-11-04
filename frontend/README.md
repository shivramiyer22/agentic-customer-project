# Frontend Application - The Aerospace Company Customer Service Agent

Next.js frontend application for the multi-agent AI customer service system.

**Version:** 1.0.0  
**Framework:** Next.js 16.0.1  
**React Version:** 19.2.0

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## Overview

This frontend application provides a React-based user interface for:

- **Chat Interface:** Real-time chat with the multi-agent AI system using Server-Sent Events (SSE) streaming
- **Document Upload:** Drag-and-drop file upload interface for knowledge base documents
- **Knowledge Base Management:** Select target collection (billing, technical, policy) for document uploads
- **Session Management:** Persistent chat sessions with conversation history
- **Contributing Agents/Models Display:** Shows which AI agents and models contributed to responses
- **Satisfaction Feedback:** User feedback collection for responses

The application uses:
- **Next.js 16.0.1** with App Router for server-side rendering
- **React 19.2.0** for component-based UI
- **TypeScript** for type safety
- **Tailwind CSS 4** for styling
- **Server-Sent Events (SSE)** for real-time streaming
- **React Context API** for state management
- **localStorage** for client-side persistence

---

## Features

### ✅ Implemented

- ✅ Chat interface with real-time SSE streaming
- ✅ Message history with contributing agents/models display
- ✅ Document upload with drag-and-drop support
- ✅ Knowledge base selector (billing, technical, policy)
- ✅ Upload progress tracking
- ✅ File preview and validation
- ✅ Session management with persistent chat history
- ✅ Satisfaction feedback collection
- ✅ Responsive design with Tailwind CSS
- ✅ TypeScript for type safety
- ✅ Client-side chat history persistence with localStorage
- ✅ Hydration mismatch prevention for SSR
- ✅ Contributing agents and models tracking
- ✅ Token usage tracking and cost calculation
- ✅ Tooltip information for token count and total cost breakdown
- ✅ Restart script (`restart_frontend.sh`) for easy application restart
- ✅ Comprehensive test suite (81 tests with 100% pass rate)

### 🚧 Future Enhancements

- 🚧 Real-time notification system
- 🚧 Advanced file preview (PDF viewer, image gallery)
- 🚧 Chat export functionality
- 🚧 Dark mode support
- 🚧 Accessibility improvements (WCAG compliance)

---

## Requirements

### System Requirements

- **Node.js:** 18.0 or higher
- **npm:** 9.0 or higher (or yarn/pnpm/bun)
- **Operating System:** macOS, Linux, or Windows
- **Memory:** Minimum 4GB RAM (8GB+ recommended)
- **Disk Space:** ~500MB for dependencies and build files

### Node.js Packages

All dependencies are listed in `package.json`. Key packages include:

- `next@16.0.1` - React framework with App Router
- `react@19.2.0` - UI library
- `typescript@5` - Type safety
- `tailwindcss@4` - CSS framework
- `@testing-library/react@16.3.0` - Testing utilities
- `jest@30.2.0` - Testing framework

---

## Installation

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
# or
yarn install
# or
pnpm install
```

### 3. Verify Installation

```bash
# Check Node.js version
node --version  # Should be 18.0 or higher

# Check npm version
npm --version  # Should be 9.0 or higher

# Verify dependencies installed
npm list --depth=0
```

---

## Environment Variables

Create a `.env` file in the `frontend/` directory with the following variables:

### Required

```env
# Backend API URL (Required)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Optional (with defaults)

```env
# If not set, defaults to http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Environment Variable Descriptions

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | ✅ Yes | `http://localhost:8000` | Backend API base URL |

**Note:** All environment variables prefixed with `NEXT_PUBLIC_` are exposed to the browser. Do not include sensitive information (API keys, secrets) in these variables.

---

## Running the Application

### Development Mode

```bash
# Start the development server
npm run dev
# or
yarn dev
# or
pnpm dev
```

The application will be available at:
- **Local:** http://localhost:3000
- **Network:** http://[your-ip]:3000

### Production Mode

```bash
# Build the application
npm run build

# Start the production server
npm start
# or
yarn start
# or
pnpm start
```

### Using Restart Script

A convenient restart script is available:

```bash
# Make script executable (first time only)
chmod +x restart_frontend.sh

# Restart the frontend application
./restart_frontend.sh
```

This script will:
- Kill any existing processes on port 3000
- Start the Next.js development server
- Run the server in the background

**Note:** The script runs the server in the background. Check the output for the process ID if you need to stop it manually.

### Application URLs

Once running, the application provides:

- **Chat Page:** http://localhost:3000/
- **Upload Page:** http://localhost:3000/upload
- **API Docs (Backend):** http://localhost:8000/docs (if backend is running)

### Hot Module Replacement (HMR)

The development server supports hot module replacement. Changes to components will automatically refresh in the browser without a full page reload.

---

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Chat page (/)
│   │   └── upload/
│   │       └── page.tsx       # Upload page (/upload)
│   │
│   ├── components/            # React components
│   │   ├── ChatInterface/    # Chat-related components
│   │   │   ├── InputBox.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── SatisfactionFeedback.tsx
│   │   │   └── StreamingResponse.tsx
│   │   └── DocumentUpload/   # Upload-related components
│   │       ├── FilePreview.tsx
│   │       ├── FileUploader.tsx
│   │       ├── KnowledgeBaseSelector.tsx
│   │       └── UploadProgress.tsx
│   │
│   ├── context/               # React Context providers
│   │   ├── ChatContext.tsx   # Chat state management
│   │   ├── SessionContext.tsx  # Session state management
│   │   └── UploadContext.tsx   # Upload state management
│   │
│   ├── hooks/                 # Custom React hooks
│   │   ├── useChat.ts        # Chat functionality with SSE
│   │   ├── useSession.ts     # Session management
│   │   └── useUpload.ts      # File upload functionality
│   │
│   ├── services/             # API client services
│   │   └── api-client.ts     # HTTP client and SSE streaming
│   │
│   ├── constants/            # Application constants
│   │   ├── api-endpoints.ts  # API endpoint definitions
│   │   └── pricing.ts        # Token pricing constants (Claude 3 Haiku)
│   │
│   ├── utils/                # Utility functions
│   │   ├── cn.ts             # className utility (Tailwind)
│   │   ├── file-handlers.ts  # File validation and processing
│   │   └── stream-parser.ts  # SSE message parsing
│   │
│   ├── styles/               # Global styles
│   │   └── globals.css      # Tailwind CSS imports
│   │
│   └── layouts/              # Layout components
│       └── Header.tsx        # Application header
│
├── public/                   # Static assets
│   ├── airplane.svg          # Logo/icon
│   └── [other assets]
│
├── tests/                    # Test files
│   ├── components/          # Component tests
│   ├── context/             # Context tests
│   ├── hooks/                # Hook tests
│   ├── services/            # Service tests
│   ├── utils/                # Utility tests
│   └── utils/
│       └── test-utils.tsx   # Test utilities and providers
│
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
├── jest.config.js           # Jest configuration
├── jest.setup.js            # Jest setup file
├── next.config.js           # Next.js configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── postcss.config.mjs       # PostCSS configuration
├── eslint.config.mjs        # ESLint configuration
├── .env                     # Environment variables (git-ignored)
├── .env.example             # Environment variables template
├── README_TESTING.md        # Testing documentation
├── TEST_RESULTS.md          # Test results
├── TROUBLESHOOTING.md       # Troubleshooting guide
└── restart_frontend.sh      # Restart script
```

---

## Testing

### Running Tests

```bash
# Run all tests
npm test
# or
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### Test Coverage

The test suite includes **81 tests** with **100% pass rate**:

- ✅ **Utility Functions** (8 tests) - `utils/__tests__/`
  - `cn.test.ts` - className utility
  - `file-handlers.test.ts` - File validation
  - `stream-parser.test.ts` - SSE parsing

- ✅ **Services** (9 tests) - `services/__tests__/`
  - `api-client.test.ts` - API client and SSE streaming

- ✅ **Context Providers** (8 tests) - `context/__tests__/`
  - `ChatContext.test.tsx` - Chat state management
  - `SessionContext.test.tsx` - Session state management

- ✅ **Custom Hooks** (12 tests) - `hooks/__tests__/`
  - `useChat.test.tsx` - Chat hook (includes 3 Contributing Models tests)
  - `useUpload.test.tsx` - Upload hook
  - `useSession.test.tsx` - Session hook

- ✅ **Components** (40 tests) - `components/__tests__/`
  - `MessageList.test.tsx` - Message display (includes 4 Contributing Models tests)
  - `InputBox.test.tsx` - Input component
  - `Header.test.tsx` - Header component
  - `FileUploader.test.tsx` - File upload component
  - `UploadProgress.test.tsx` - Upload progress component
  - `KnowledgeBaseSelector.test.tsx` - Collection selector
  - `FilePreview.test.tsx` - File preview component
  - `StreamingResponse.test.tsx` - Streaming response component
  - `SatisfactionFeedback.test.tsx` - Feedback component

- ✅ **Layout** (1 test) - `app/__tests__/`
  - Layout component tests

For detailed test documentation, see `README_TESTING.md` and `TEST_RESULTS.md`.

### Test Requirements

Tests require:
- All dependencies from `package.json`
- Backend API running at `NEXT_PUBLIC_API_URL` (for integration tests)
- Jest and React Testing Library configured

### Writing Tests

Follow the existing test patterns:

```typescript
import { render, screen, waitFor } from '@testing-library/react'
import { render as customRender } from '../../utils/test-utils'
import MyComponent from '@/components/MyComponent'

describe('MyComponent', () => {
  it('should render correctly', () => {
    customRender(<MyComponent />)
    expect(screen.getByText('Expected Text')).toBeInTheDocument()
  })
})
```

---

## Development

### Code Style

- Follow TypeScript best practices
- Use functional components with hooks
- Use Tailwind CSS for styling (avoid inline styles)
- Use React Context for global state
- Use custom hooks for reusable logic
- Document components and functions with JSDoc comments

### Adding New Components

1. Create component in `src/components/`
2. Add TypeScript interfaces for props
3. Use Tailwind CSS for styling
4. Add tests in `tests/components/__tests__/`
5. Export from `components/index.ts` (if creating an index file)

### Adding New Pages

1. Create page in `src/app/`
2. Follow Next.js App Router conventions
3. Use layout components for shared UI
4. Add navigation in `Header.tsx` if needed

### Adding New API Endpoints

1. Add endpoint to `src/constants/api-endpoints.ts`
2. Implement client function in `src/services/api-client.ts`
3. Add tests in `tests/services/__tests__/`
4. Use the client function in components/hooks

### State Management

The application uses React Context API for state management:

- **ChatContext:** Chat messages, conversation history, contributing agents/models
- **SessionContext:** Session management and persistence
- **UploadContext:** File upload state and progress

For local component state, use `useState` and `useReducer` hooks.

### Styling

Use Tailwind CSS utility classes:

```tsx
<div className="flex items-center justify-between p-4 bg-white rounded-lg shadow">
  <h1 className="text-2xl font-bold text-gray-900">Title</h1>
</div>
```

Use the `cn` utility for conditional classes:

```tsx
import { cn } from '@/utils/cn'

<div className={cn(
  "base-class",
  condition && "conditional-class",
  anotherCondition && "another-class"
)}>
```

---

## Troubleshooting

### Common Issues

#### 1. Port 3000 Already in Use

**Error:** `Port 3000 is already in use`

**Solutions:**
- Kill existing process:
  ```bash
  lsof -ti:3000 | xargs kill -9
  ```
- Or change port:
  ```bash
  npm run dev -- -p 3001
  ```

#### 2. Module Not Found Errors

**Error:** `Module not found: Can't resolve '@/components/...'`

**Solutions:**
- Verify TypeScript path aliases in `tsconfig.json`:
  ```json
  {
    "compilerOptions": {
      "paths": {
        "@/*": ["./src/*"]
      }
    }
  }
  ```
- Restart the development server
- Clear `.next` cache:
  ```bash
  rm -rf .next
  npm run dev
  ```

#### 3. API Connection Errors

**Error:** `Failed to fetch` or `Network request failed`

**Solutions:**
- Verify backend is running at `http://localhost:8000`
- Check `NEXT_PUBLIC_API_URL` in `.env` file
- Verify backend health:
  ```bash
  curl http://localhost:8000/health
  ```
- Check browser console for CORS errors (should be handled by backend)

#### 4. SSE Streaming Not Working

**Error:** Messages not streaming or stuck at "Generating response..."

**Solutions:**
- Verify backend SSE endpoint is working
- Check browser console for SSE errors
- Verify `streamSSE` function in `api-client.ts`
- Check network tab in browser DevTools for SSE events
- Ensure backend is sending proper SSE format

#### 5. Chat History Not Persisting

**Error:** Chat history lost on page refresh or navigation

**Solutions:**
- Verify `localStorage` is available (not in private/incognito mode)
- Check browser console for `localStorage` errors
- Verify `ChatContext` is loading from `localStorage` on mount
- Check `isHydrated` state in `ChatContext.tsx`

#### 6. Hydration Mismatch Error

**Error:** `Hydration failed because the server rendered HTML didn't match the client`

**Solutions:**
- Verify `ChatContext` initializes with empty state on server
- Check `localStorage` loading happens only in `useEffect` (client-side)
- Ensure no client-only APIs are called during SSR
- Check for date/time formatting that differs between server and client

#### 7. Token Count or Cost Not Displaying

**Error:** Token count or cost not showing or showing as 0

**Solutions:**
- Verify backend is sending `token_usage` in chat response metadata
- Check `ChatContext` is properly updating `tokenUsage` state
- Verify `useChat` hook is extracting `token_usage` from SSE metadata
- Check browser console for errors in token usage calculation
- Ensure pricing constants are correctly imported from `constants/pricing.ts`

#### 8. File Upload Not Working

**Error:** Files not uploading or validation errors

**Solutions:**
- Check file size (max 20 MB per file)
- Verify file format is supported (PDF, TXT, Markdown, JSON)
- Check backend upload endpoint is accessible
- Verify `UploadContext` is properly initialized
- Check browser console for upload errors

#### 9. Contributing Agents/Models Not Displaying

**Error:** Contributing agents/models section not shown

**Solutions:**
- Verify backend is sending metadata in SSE chunks
- Check `MessageList` component is extracting metadata correctly
- Verify `contributingAgents` and `contributingModels` are in message object
- Check browser console for metadata structure
- Review `useChat` hook metadata extraction logic

### Debug Mode

Enable verbose logging in development:

```typescript
// In api-client.ts or useChat.ts
console.log('Debug info:', data)
```

Use React DevTools to inspect component state and props.

### Checking Application Status

#### Verify Frontend is Running

```bash
# Check if Next.js is running
curl http://localhost:3000

# Check process status
lsof -ti:3000

# View process details
ps aux | grep "next dev"
```

#### Check Build Errors

```bash
# Check for TypeScript errors
npm run build

# Check for linting errors
npm run lint
```

---

## API Integration

The frontend communicates with the backend API at `NEXT_PUBLIC_API_URL` (default: `http://localhost:8000`).

### Available Endpoints

- **Health:** `GET /health`
- **Collections:** `GET /collections`
- **Upload:** `POST /upload` (multipart/form-data)
- **Upload Status:** `GET /upload/status/{upload_id}`
- **Sessions:** `GET|POST|DELETE /sessions/{session_id}`
- **Chat:** `POST /chat` (with SSE streaming support)

See `src/constants/api-endpoints.ts` for complete endpoint definitions.

### Token Usage and Cost Calculation

The application tracks token usage and calculates costs in real-time:

- **Token Count Tracking:** Input and output tokens are tracked per chat session
- **Cost Calculation:** Costs are calculated based on Claude 3 Haiku pricing:
  - Input: $0.00025 per 1,000 tokens
  - Output: $0.00125 per 1,000 tokens
- **Interactive Tooltips:** 
  - Token count tooltip shows breakdown of what's included in input/output tokens
  - Cost tooltip shows pricing model and unit prices
- **Pricing Constants:** Defined in `src/constants/pricing.ts`

Token usage is extracted from chat response metadata and displayed in the satisfaction feedback section.

### Server-Sent Events (SSE)

The chat interface uses SSE for real-time streaming:

```typescript
streamSSE(url, {
  onMessage: (message) => {
    // Handle streaming message chunks
  },
  onDone: () => {
    // Handle stream completion
  },
  onError: (error) => {
    // Handle errors
  }
})
```

---

## Performance Considerations

### Optimizations

- **Code Splitting:** Next.js automatically splits code by route
- **Image Optimization:** Use Next.js `Image` component for images
- **Lazy Loading:** Components are lazy-loaded where appropriate
- **Memoization:** Use `React.memo` and `useMemo` for expensive computations
- **SSE Streaming:** Reduces initial response time by streaming content

### Bundle Size

Monitor bundle size:

```bash
npm run build
# Check .next/analyze for bundle analysis
```

---

## Deployment

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

### Environment Variables

Ensure production environment variables are set:

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Docker (Future)

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

CMD ["npm", "start"]
```

---

## Support

For issues or questions:

1. Check this README and troubleshooting section
2. Review `TROUBLESHOOTING.md` for common issues
3. Check browser console for errors
4. Review test files for usage examples
5. Check backend API logs for server-side errors

---

## License

Proprietary - The Aerospace Company

---

**Last Updated:** November 2025  
**Version:** 1.0.0
