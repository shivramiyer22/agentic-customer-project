/**
 * File validation and handling utilities
 */

export interface FileValidationResult {
  isValid: boolean;
  error?: string;
}

/**
 * Supported file types for document upload
 */
export const SUPPORTED_FILE_TYPES = [
  'application/pdf',
  'text/plain',
  'text/markdown',
  'application/json',
] as const;

export const SUPPORTED_FILE_EXTENSIONS = [
  '.pdf',
  '.txt',
  '.md',
  '.json',
] as const;

/**
 * Maximum file size in bytes (limit: 20 MB per file)
 */
export const MAX_FILE_SIZE = 20 * 1024 * 1024; // 20 MB

/**
 * Maximum number of files per upload
 */
export const MAX_FILES_PER_UPLOAD = 10;

/**
 * Validates file format
 */
export function validateFileFormat(file: File): FileValidationResult {
  const fileExtension = file.name.toLowerCase().slice(file.name.lastIndexOf('.'));
  
  if (!SUPPORTED_FILE_EXTENSIONS.includes(fileExtension as any)) {
    return {
      isValid: false,
      error: `Unsupported file format. Supported formats: ${SUPPORTED_FILE_EXTENSIONS.join(', ')}`,
    };
  }
  
  if (!SUPPORTED_FILE_TYPES.includes(file.type as any)) {
    return {
      isValid: false,
      error: `Unsupported MIME type: ${file.type}`,
    };
  }
  
  return { isValid: true };
}

/**
 * Validates file size
 */
export function validateFileSize(file: File): FileValidationResult {
  if (file.size > MAX_FILE_SIZE) {
    return {
      isValid: false,
      error: `File size exceeds maximum allowed size of ${(MAX_FILE_SIZE / (1024 * 1024)).toFixed(0)} MB`,
    };
  }
  
  if (file.size === 0) {
    return {
      isValid: false,
      error: 'File is empty',
    };
  }
  
  return { isValid: true };
}

/**
 * Validates file for corruption (basic check)
 */
export function validateFileCorruption(file: File): Promise<FileValidationResult> {
  return new Promise((resolve) => {
    const reader = new FileReader();
    
    reader.onload = () => {
      if (reader.result && typeof reader.result === 'string') {
        // Basic validation: check if file can be read
        resolve({ isValid: true });
      } else {
        resolve({
          isValid: false,
          error: 'File appears to be corrupted or unreadable',
        });
      }
    };
    
    reader.onerror = () => {
      resolve({
        isValid: false,
        error: 'Error reading file. File may be corrupted.',
      });
    };
    
    reader.readAsText(file);
  });
}

/**
 * Validates a file completely (format, size, corruption)
 */
export async function validateFile(file: File): Promise<FileValidationResult> {
  // Validate format
  const formatCheck = validateFileFormat(file);
  if (!formatCheck.isValid) {
    return formatCheck;
  }
  
  // Validate size
  const sizeCheck = validateFileSize(file);
  if (!sizeCheck.isValid) {
    return sizeCheck;
  }
  
  // Validate corruption
  const corruptionCheck = await validateFileCorruption(file);
  if (!corruptionCheck.isValid) {
    return corruptionCheck;
  }
  
  return { isValid: true };
}

/**
 * Formats file size for display
 */
export function formatFileSize(bytes: number): string {
  if (bytes < 1024) {
    return `${bytes} B`;
  } else if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(2)} KB`;
  } else if (bytes < 1024 * 1024 * 1024) {
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  } else {
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
  }
}

/**
 * Gets file extension from filename
 */
export function getFileExtension(filename: string): string {
  return filename.toLowerCase().slice(filename.lastIndexOf('.'));
}

