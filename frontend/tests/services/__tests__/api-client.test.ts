/**
 * Tests for API client services
 */

import { API_ENDPOINTS } from '@/constants/api-endpoints'
import * as apiClient from '@/services/api-client'

// Mock fetch globally
global.fetch = jest.fn()

describe('API Client', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('chatApi', () => {
    it('should send message correctly', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({ message: 'Test response' }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      const response = await apiClient.chatApi.sendMessage('session-1', 'Hello', false)
      expect(response).toBeDefined()
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining(API_ENDPOINTS.CHAT),
        expect.objectContaining({
          method: 'POST',
        })
      )
    })
  })

  describe('uploadApi', () => {
    it('should upload files correctly', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({ upload_id: 'upload-123', status: 'queued' }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      const files = [new File(['content'], 'test.pdf', { type: 'application/pdf' })]
      const response = await apiClient.uploadApi.uploadFiles(files, 'billing_knowledge_base')

      expect(response).toBeDefined()
      expect(global.fetch).toHaveBeenCalled()
    })

    it('should get collections correctly', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({
          collections: ['billing_knowledge_base', 'technical_knowledge_base'],
        }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      const response = await apiClient.uploadApi.getCollections()
      expect(response.collections).toBeDefined()
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining(API_ENDPOINTS.COLLECTIONS),
        expect.objectContaining({
          method: 'GET',
        })
      )
    })

    it('should get upload status correctly', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({
          upload_id: 'upload-123',
          status: 'processing',
          overall_progress: 50,
        }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      const response = await apiClient.uploadApi.getUploadStatus('upload-123')
      expect(response.upload_id).toBe('upload-123')
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining(`${API_ENDPOINTS.UPLOAD}/status/upload-123`),
        expect.objectContaining({
          method: 'GET',
        })
      )
    })
  })

  describe('sessionApi', () => {
    it('should get sessions correctly', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({ sessions: [] }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      await apiClient.sessionApi.getSessions()
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining(API_ENDPOINTS.SESSIONS),
        expect.objectContaining({
          method: 'GET',
        })
      )
    })

    it('should get session by id correctly', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({ session_id: 'session-123' }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      const response = await apiClient.sessionApi.getSession('session-123')
      expect(response.session_id).toBe('session-123')
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining(`${API_ENDPOINTS.SESSIONS}/session-123`),
        expect.objectContaining({
          method: 'GET',
        })
      )
    })

    it('should delete session correctly', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({ success: true }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      await apiClient.sessionApi.deleteSession('session-123')
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining(`${API_ENDPOINTS.SESSIONS}/session-123`),
        expect.objectContaining({
          method: 'DELETE',
        })
      )
    })
  })

  describe('feedbackApi', () => {
    it('should submit feedback correctly', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({ success: true }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      await apiClient.feedbackApi.submitFeedback('session-123', 'thumbs_up', 'Great!')
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining(API_ENDPOINTS.FEEDBACK),
        expect.objectContaining({
          method: 'POST',
        })
      )
    })
  })
})

