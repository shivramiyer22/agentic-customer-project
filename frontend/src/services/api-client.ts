/**
 * API client utilities for backend communication
 */

import { API_ENDPOINTS } from '@/constants/api-endpoints';

export interface ApiError {
  message: string;
  status?: number;
  statusText?: string;
}

/**
 * Custom fetch wrapper with error handling
 */
async function fetchApi(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response;
}

/**
 * GET request
 */
export async function get<T>(url: string): Promise<T> {
  const response = await fetchApi(url, { method: 'GET' });
  return response.json();
}

/**
 * POST request
 */
export async function post<T>(url: string, data?: any): Promise<T> {
  const response = await fetchApi(url, {
    method: 'POST',
    body: data ? JSON.stringify(data) : undefined,
  });
  return response.json();
}

/**
 * DELETE request
 */
export async function del<T>(url: string): Promise<T> {
  const response = await fetchApi(url, { method: 'DELETE' });
  return response.json();
}

/**
 * POST request with multipart form data (for file uploads)
 */
export async function postFormData<T>(
  url: string,
  formData: FormData
): Promise<T> {
  const response = await fetch(url, {
    method: 'POST',
    body: formData,
    // Don't set Content-Type header - browser will set it with boundary
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

/**
 * SSE (Server-Sent Events) streaming request
 */
export function streamSSE(
  url: string,
  data: any,
  onMessage: (message: any) => void,
  onError?: (error: Error) => void,
  onDone?: () => void
): () => void {
  const abortController = new AbortController();

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
    signal: abortController.signal,
  })
    .then(async (response) => {
      console.log('[streamSSE] Response received:', response.status, response.statusText);
      
      if (!response.ok) {
        console.error('[streamSSE] Response not OK:', response.status, response.statusText);
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        console.error('[streamSSE] Response body is not readable');
        throw new Error('Response body is not readable');
      }

      console.log('[streamSSE] Starting to read stream');
      const decoder = new TextDecoder();
      let buffer = '';

      try {
        while (true) {
          const { done, value } = await reader.read();

          if (done) {
            // Process remaining buffer
            if (buffer.trim()) {
              console.log('[streamSSE] Processing final buffer:', buffer.substring(0, 200));
              const lines = buffer.split('\n');
              for (const line of lines) {
                if (line.startsWith('data:')) {
                  const content = line.slice(5).trim();
                  if (content === '[DONE]') {
                    console.log('[streamSSE] Received [DONE] signal');
                    onDone?.();
                    return;
                  }
                  try {
                    const parsed = JSON.parse(content);
                    console.log('[streamSSE] Parsed message:', parsed);
                    onMessage(parsed);
                  } catch (e) {
                    console.log('[streamSSE] Failed to parse, sending raw content:', content.substring(0, 100));
                    onMessage({ content });
                  }
                }
              }
            }
            console.log('[streamSSE] Stream done, calling onDone');
            onDone?.();
            break;
          }

          // Decode chunk and add to buffer
          const decoded = decoder.decode(value, { stream: true });
          buffer += decoded;

          // Process complete lines
          const lines = buffer.split('\n');
          buffer = lines.pop() || ''; // Keep incomplete line in buffer

          for (const line of lines) {
            if (line.startsWith('data:')) {
              const content = line.slice(5).trim();
              
              if (content === '[DONE]') {
                console.log('[streamSSE] Received [DONE] signal');
                onDone?.();
                return;
              }
              
              try {
                const parsed = JSON.parse(content);
                console.log('[streamSSE] Parsed message:', parsed);
                onMessage(parsed);
              } catch (e) {
                console.log('[streamSSE] Failed to parse JSON:', e, 'Content:', content.substring(0, 100));
                onMessage({ content });
              }
            }
          }
        }
      } catch (error) {
        console.error('[streamSSE] Error in stream processing:', error);
        if (error instanceof Error && error.name !== 'AbortError') {
          onError?.(error);
        }
      }
    })
    .catch((error) => {
      if (error.name !== 'AbortError') {
        onError?.(error instanceof Error ? error : new Error('Unknown error'));
      }
    });

  // Return abort function
  return () => {
    abortController.abort();
  };
}

/**
 * Chat API client functions
 */
export const chatApi = {
  sendMessage: async (sessionId: string, message: string) => {
    return post(API_ENDPOINTS.CHAT, { session_id: sessionId, message });
  },
  
  streamMessage: (
    sessionId: string,
    message: string,
    onMessage: (message: any) => void,
    onError?: (error: Error) => void,
    onDone?: () => void
  ) => {
    return streamSSE(
      API_ENDPOINTS.CHAT,
      { session_id: sessionId, message, stream: true },
      onMessage,
      onError,
      onDone
    );
  },
};

/**
 * Session API client functions
 */
export const sessionApi = {
  getSessions: async () => {
    return get(API_ENDPOINTS.SESSIONS);
  },
  
  getSession: async (sessionId: string) => {
    return get(API_ENDPOINTS.SESSION_BY_ID(sessionId));
  },
  
  deleteSession: async (sessionId: string) => {
    return del(API_ENDPOINTS.SESSION_BY_ID(sessionId));
  },
};

/**
 * Upload API client functions
 */
export const uploadApi = {
  uploadFiles: async (files: File[], targetCollection?: string) => {
    const formData = new FormData();
    
    files.forEach((file) => {
      formData.append('files', file);
    });
    
    if (targetCollection && targetCollection !== 'auto-map') {
      formData.append('target_collection', targetCollection);
    } else {
      formData.append('target_collection', 'auto-map');
    }
    
    return postFormData<{
      upload_id: string;
      status: string;
      files: Array<{
        file_name: string;
        file_size: number;
        status: string;
        progress: number;
        error?: string;
        target_collection?: string;
        chunks_count?: number;
      }>;
      overall_progress: number;
      created_at: string;
      message?: string;
    }>(API_ENDPOINTS.UPLOAD, formData);
  },
  
  getCollections: async () => {
    return get<{
      collections: string[];
      configured?: string[];
      count: number;
      error?: string;
    }>(API_ENDPOINTS.COLLECTIONS);
  },
  
  getUploadStatus: async (uploadId: string) => {
    return get<{
      upload_id: string;
      status: string;
      files: Array<{
        file_name: string;
        file_size: number;
        status: string;
        progress: number;
        error?: string;
        target_collection?: string;
        chunks_count?: number;
      }>;
      overall_progress: number;
      created_at: string;
      updated_at: string;
    }>(`${API_ENDPOINTS.UPLOAD}/status/${uploadId}`);
  },
};

/**
 * Feedback API client functions
 */
export const feedbackApi = {
  submitFeedback: async (
    sessionId: string,
    rating: 'thumbs_up' | 'thumbs_down',
    comment?: string
  ) => {
    return post(API_ENDPOINTS.FEEDBACK, {
      session_id: sessionId,
      rating,
      comment: comment || null,
    });
  },
};

/**
 * Health API client functions
 */
export const healthApi = {
  checkHealth: async () => {
    return get(API_ENDPOINTS.HEALTH);
  },
};

