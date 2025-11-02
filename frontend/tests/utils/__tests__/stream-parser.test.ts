/**
 * Tests for stream-parser utility functions
 */

import { parseSSEMessage, readSSEStream } from '@/utils/stream-parser'

describe('stream-parser utilities', () => {
  describe('parseSSEMessage', () => {
    it('should parse SSE message correctly', () => {
      const message = parseSSEMessage('data: {"content": "Hello"}')
      expect(message).not.toBeNull()
      expect(message?.type).toBe('message')
      expect(message?.content).toBe('Hello')
    })

    it('should parse DONE message', () => {
      const message = parseSSEMessage('data: [DONE]')
      expect(message).not.toBeNull()
      expect(message?.type).toBe('done')
    })

    it('should handle invalid JSON gracefully', () => {
      const message = parseSSEMessage('data: invalid json')
      expect(message).not.toBeNull()
      expect(message?.type).toBe('message')
      expect(message?.content).toBe('invalid json')
    })

    it('should handle empty lines', () => {
      const message = parseSSEMessage('')
      expect(message).toBeNull()
    })

    it('should handle event lines', () => {
      const message = parseSSEMessage('event: error')
      expect(message).not.toBeNull()
      expect(message?.type).toBe('error')
    })
  })
})

