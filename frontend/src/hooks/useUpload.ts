/**
 * Custom hook for document upload with progress tracking
 */

import { useState, useCallback, useEffect, useRef } from 'react';
import { uploadApi } from '@/services/api-client';
import { formatFileSize } from '@/utils/file-handlers';

export interface UploadFile {
  file: File;
  id: string;
  status: 'pending' | 'uploading' | 'success' | 'error';
  progress: number;
  error?: string;
  uploadId?: string;
  chunksCount?: number;
}

export interface UploadState {
  files: UploadFile[];
  targetCollection: string | null;
  isUploading: boolean;
  overallProgress: number;
  currentUploadId?: string;
}

export function useUpload() {
  const [uploadState, setUploadState] = useState<UploadState>({
    files: [],
    targetCollection: null,
    isUploading: false,
    overallProgress: 0,
  });
  
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const addFiles = useCallback((files: File[]) => {
    const newFiles: UploadFile[] = files.map((file) => ({
      file,
      id: `file-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      status: 'pending',
      progress: 0,
    }));

    setUploadState((prev) => ({
      ...prev,
      files: [...prev.files, ...newFiles],
    }));
  }, []);

  const removeFile = useCallback((fileId: string) => {
    setUploadState((prev) => ({
      ...prev,
      files: prev.files.filter((f) => f.id !== fileId),
    }));
  }, []);

  const setTargetCollection = useCallback((collection: string | null) => {
    setUploadState((prev) => ({
      ...prev,
      targetCollection: collection,
    }));
  }, []);

  const pollUploadStatus = useCallback(async (uploadId: string) => {
    try {
      const status = await uploadApi.getUploadStatus(uploadId);
      
      setUploadState((prev) => {
        // Map server statuses to frontend statuses
        const statusMap: Record<string, 'pending' | 'uploading' | 'success' | 'error'> = {
          'queued': 'pending',
          'processing': 'uploading',
          'completed': 'success',
          'failed': 'error',
        };
        
        const updatedFiles = prev.files.map((file) => {
          const serverFile = status.files.find((sf) => sf.file_name === file.file.name);
          if (!serverFile) return file;
          
          const frontendStatus = statusMap[serverFile.status] || 'pending';
          
          return {
            ...file,
            status: frontendStatus,
            progress: serverFile.progress,
            error: serverFile.error,
            chunksCount: serverFile.chunks_count,
            uploadId,
          };
        });
        
        // Stop polling if all files are completed or failed
        const allFinished = updatedFiles.every(
          (f) => f.status === 'success' || f.status === 'error'
        );
        
        if (allFinished) {
          if (pollingIntervalRef.current) {
            clearInterval(pollingIntervalRef.current);
            pollingIntervalRef.current = null;
          }
        }
        
        return {
          ...prev,
          files: updatedFiles,
          overallProgress: status.overall_progress,
          isUploading: status.status === 'processing' || status.status === 'queued',
        };
      });
    } catch (error) {
      console.error('Error polling upload status:', error);
    }
  }, []);

  const uploadFiles = useCallback(async () => {
    const filesToUpload = uploadState.files.filter(
      (f) => f.status === 'pending' || f.status === 'error'
    );

    if (filesToUpload.length === 0) {
      return;
    }

    setUploadState((prev) => ({
      ...prev,
      isUploading: true,
      overallProgress: 0,
    }));

    try {
      // Update files to uploading status
      setUploadState((prev) => ({
        ...prev,
        files: prev.files.map((f) =>
          filesToUpload.some((ftu) => ftu.id === f.id)
            ? { ...f, status: 'uploading', progress: 0 }
            : f
        ),
      }));

      // Upload files
      const fileList = filesToUpload.map((f) => f.file);
      const result = await uploadApi.uploadFiles(
        fileList,
        uploadState.targetCollection || undefined
      );

      // Store upload ID
      setUploadState((prev) => ({
        ...prev,
        currentUploadId: result.upload_id,
      }));

      // Start polling for progress
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
      
      pollingIntervalRef.current = setInterval(() => {
        pollUploadStatus(result.upload_id);
      }, 1000); // Poll every second

      // Initial status update
      await pollUploadStatus(result.upload_id);

      return result;
    } catch (error) {
      console.error('Upload error:', error);
      
      // Stop polling
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
        pollingIntervalRef.current = null;
      }
      
      // Update files to error status
      setUploadState((prev) => ({
        ...prev,
        files: prev.files.map((f) =>
          filesToUpload.some((ftu) => ftu.id === f.id)
            ? {
                ...f,
                status: 'error',
                error: error instanceof Error ? error.message : 'Upload failed',
              }
            : f
        ),
        isUploading: false,
      }));

      throw error;
    }
  }, [uploadState.files, uploadState.targetCollection, pollUploadStatus]);

  // Cleanup polling on unmount
  useEffect(() => {
    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
    };
  }, []);

  const clearFiles = useCallback(() => {
    setUploadState({
      files: [],
      targetCollection: null,
      isUploading: false,
      overallProgress: 0,
    });
  }, []);

  const clearCompletedFiles = useCallback(() => {
    setUploadState((prev) => ({
      ...prev,
      files: prev.files.filter((f) => f.status !== 'success'),
    }));
  }, []);

  return {
    uploadState,
    addFiles,
    removeFile,
    setTargetCollection,
    uploadFiles,
    clearFiles,
    clearCompletedFiles,
    formatFileSize,
  };
}

