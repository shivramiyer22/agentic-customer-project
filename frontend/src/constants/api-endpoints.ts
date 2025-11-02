/**
 * API Endpoint URLs for backend communication
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  // Chat endpoints
  CHAT: `${API_BASE_URL}/chat`,
  
  // Session management endpoints
  SESSIONS: `${API_BASE_URL}/sessions`,
  SESSION_BY_ID: (sessionId: string) => `${API_BASE_URL}/sessions/${sessionId}`,
  
  // Document upload endpoints
  UPLOAD: `${API_BASE_URL}/upload`,
  COLLECTIONS: `${API_BASE_URL}/collections`,
  
  // Feedback endpoint
  FEEDBACK: `${API_BASE_URL}/feedback`,
  
  // Health endpoint
  HEALTH: `${API_BASE_URL}/health`,
} as const;

export type ApiEndpoints = typeof API_ENDPOINTS;

