/**
 * SSE (Server-Sent Events) stream parsing utilities
 */

export interface StreamMessage {
  type: 'message' | 'error' | 'done' | 'metadata';
  content?: string;
  data?: any;
}

/**
 * Parses SSE stream data
 */
export function parseSSEMessage(line: string): StreamMessage | null {
  if (!line.trim()) {
    return null;
  }
  
  // Parse SSE format: "data: {json}" or "event: type\ndata: {json}"
  if (line.startsWith('data:')) {
    const content = line.slice(5).trim();
    
    if (content === '[DONE]') {
      return { type: 'done' };
    }
    
    try {
      const parsed = JSON.parse(content);
      
      // Handle different message formats
      if (parsed.content || parsed.message) {
        return {
          type: 'message',
          content: parsed.content || parsed.message,
          data: parsed,
        };
      }
      
      if (parsed.metadata) {
        return {
          type: 'metadata',
          data: parsed.metadata,
        };
      }
      
      return {
        type: 'message',
        content: content,
        data: parsed,
      };
    } catch {
      // If not JSON, return as plain text
      return {
        type: 'message',
        content: content,
      };
    }
  }
  
  if (line.startsWith('event:')) {
    const eventType = line.slice(6).trim();
    return {
      type: eventType === 'error' ? 'error' : 'message',
    };
  }
  
  return null;
}

/**
 * Reads SSE stream and calls callback for each message
 */
export async function readSSEStream(
  reader: ReadableStreamDefaultReader<Uint8Array>,
  onMessage: (message: StreamMessage) => void,
  onError?: (error: Error) => void,
  onDone?: () => void
): Promise<void> {
  const decoder = new TextDecoder();
  let buffer = '';
  
  try {
    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        // Process remaining buffer
        if (buffer.trim()) {
          const lines = buffer.split('\n');
          for (const line of lines) {
            const message = parseSSEMessage(line);
            if (message) {
              onMessage(message);
            }
          }
        }
        
        onDone?.();
        break;
      }
      
      // Decode chunk and add to buffer
      buffer += decoder.decode(value, { stream: true });
      
      // Process complete lines
      const lines = buffer.split('\n');
      buffer = lines.pop() || ''; // Keep incomplete line in buffer
      
      for (const line of lines) {
        const message = parseSSEMessage(line);
        if (message) {
          onMessage(message);
          
          if (message.type === 'done') {
            onDone?.();
            return;
          }
          
          if (message.type === 'error') {
            onError?.(new Error(message.content || 'Stream error'));
            return;
          }
        }
      }
    }
  } catch (error) {
    onError?.(error instanceof Error ? error : new Error('Unknown stream error'));
  }
}

