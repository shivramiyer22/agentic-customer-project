'use client';

/**
 * Upload context provider for upload state management
 */

import React, { createContext, useContext, useState, useCallback, useEffect, useRef } from 'react';
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
  targetCollection?: string;
}

export interface UploadState {
  files: UploadFile[];
  targetCollection: string | null;
  isUploading: boolean;
  overallProgress: number;
  currentUploadId?: string;
}

export interface UploadContextType {
  uploadState: UploadState;
  addFiles: (files: File[]) => void;
  removeFile: (fileId: string) => void;
  setTargetCollection: (collection: string | null) => void;
  uploadFiles: () => Promise<any>;
  clearFiles: () => void;
  clearCompletedFiles: () => void;
  formatFileSize: (bytes: number) => string;
}

const UploadContext = createContext<UploadContextType | undefined>(undefined);

export function UploadProvider({ children }: { children: React.ReactNode }) {
  const [uploadState, setUploadState] = useState<UploadState>({
    files: [],
    targetCollection: null,
    isUploading: false,
    overallProgress: 0,
  });
  
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const addFiles = useCallback((files: File[]) => {
    console.log('[UploadContext] addFiles called with', files.length, 'files');
    
    if (!files || files.length === 0) {
      console.warn('[UploadContext] No files provided to addFiles');
      return;
    }

    const newFiles: UploadFile[] = files.map((file) => ({
      file,
      id: `file-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      status: 'pending',
      progress: 0,
    }));

    console.log('[UploadContext] Created', newFiles.length, 'upload file objects');
    console.log('[UploadContext] Files:', newFiles.map(f => ({ name: f.file.name, size: f.file.size })));

    setUploadState((prev) => {
      const updated = {
        ...prev,
        files: [...prev.files, ...newFiles],
      };
      console.log('[UploadContext] Updated state with', updated.files.length, 'total files');
      return updated;
    });
  }, []);

  const removeFile = useCallback((fileId: string) => {
    console.log('[UploadContext] removeFile called for', fileId);
    setUploadState((prev) => ({
      ...prev,
      files: prev.files.filter((f) => f.id !== fileId),
    }));
  }, []);

  const setTargetCollection = useCallback((collection: string | null) => {
    console.log('[UploadContext] 🎯 Target collection set to:', collection || 'auto-map');
    setUploadState((prev) => ({
      ...prev,
      targetCollection: collection,
    }));
  }, []);

  const pollUploadStatus = useCallback(async (uploadId: string) => {
    try {
      const status = await uploadApi.getUploadStatus(uploadId);
      console.log('[UploadContext] Poll status response:', {
        upload_id: status.upload_id,
        status: status.status,
        overall_progress: status.overall_progress,
        files: status.files.map(f => ({
          name: f.file_name,
          status: f.status,
          progress: f.progress,
          target_collection: f.target_collection,
          chunks: f.chunks_count
        }))
      });
      
      // Map server statuses to frontend statuses
      const statusMap: Record<string, 'pending' | 'uploading' | 'success' | 'error'> = {
        'queued': 'pending',
        'processing': 'uploading',
        'completed': 'success',
        'failed': 'error',
      };
      
      setUploadState((prev) => {
        const updatedFiles = prev.files.map((file) => {
          const serverFile = status.files.find((sf) => sf.file_name === file.file.name);
          if (!serverFile) return file;
          
          const frontendStatus = statusMap[serverFile.status] || 'pending';
          
          const collectionName = serverFile.target_collection 
            ? serverFile.target_collection.replace(/_/g, ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
            : 'Unknown';
          
          console.log(`[UploadContext] 📄 File: "${file.file.name}"`);
          console.log(`[UploadContext]    → Status: ${frontendStatus}`);
          console.log(`[UploadContext]    → Progress: ${serverFile.progress}%`);
          console.log(`[UploadContext]    → Collection: 📁 ${collectionName}`);
          console.log(`[UploadContext]    → Chunks: ${serverFile.chunks_count || 0}`);
          
          return {
            ...file,
            status: frontendStatus,
            progress: serverFile.progress,
            error: serverFile.error,
            chunksCount: serverFile.chunks_count,
            targetCollection: serverFile.target_collection,
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
          
          const successCount = updatedFiles.filter(f => f.status === 'success').length;
          const errorCount = updatedFiles.filter(f => f.status === 'error').length;
          
          console.log('[UploadContext] ========================================');
          console.log(`[UploadContext] ✅ UPLOAD COMPLETE`);
          console.log(`[UploadContext]   Total files: ${updatedFiles.length}`);
          console.log(`[UploadContext]   ✅ Successful: ${successCount}`);
          console.log(`[UploadContext]   ❌ Errors: ${errorCount}`);
          console.log('[UploadContext]');
          console.log('[UploadContext] 📁 FINAL COLLECTION MAPPING:');
          
          // Log final collection mapping with detailed info
          updatedFiles.forEach((f, index) => {
            if (f.status === 'success') {
              const collectionName = f.targetCollection 
                ? f.targetCollection.replace(/_/g, ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
                : 'Unknown';
              console.log(`[UploadContext]   ${index + 1}. "${f.file.name}"`);
              console.log(`[UploadContext]      → Collection: 📁 ${collectionName}`);
              console.log(`[UploadContext]      → Chunks: ${f.chunksCount || 0}`);
              console.log(`[UploadContext]      → Status: ✅ Success`);
            } else if (f.status === 'error') {
              console.log(`[UploadContext]   ${index + 1}. "${f.file.name}"`);
              console.log(`[UploadContext]      → Status: ❌ Error`);
              console.log(`[UploadContext]      → Error: ${f.error || 'Unknown error'}`);
            }
          });
          console.log('[UploadContext] ========================================');
        }
        
        return {
          ...prev,
          files: updatedFiles,
          overallProgress: status.overall_progress,
          isUploading: status.status === 'processing' || status.status === 'queued',
        };
      });
    } catch (error) {
      console.error('[UploadContext] Error polling upload status:', error);
    }
  }, []);

  const uploadFiles = useCallback(async () => {
    const filesToUpload = uploadState.files.filter(
      (f) => f.status === 'pending' || f.status === 'error'
    );

    if (filesToUpload.length === 0) {
      console.warn('[UploadContext] No files to upload');
      return;
    }

    console.log('[UploadContext] 🚀 Starting upload of', filesToUpload.length, 'files');
    console.log('[UploadContext] 🎯 Target collection:', uploadState.targetCollection || 'auto-map');
    console.log('[UploadContext] 📦 Files to upload:', filesToUpload.map(f => ({
      name: f.file.name,
      size: f.file.size,
      type: f.file.type,
    })));

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
      const targetCollection = uploadState.targetCollection || 'auto-map';
      
      console.log('[UploadContext] ========================================');
      console.log('[UploadContext] 📤 STARTING UPLOAD');
      console.log('[UploadContext] Files to upload:', fileList.map(f => f.name));
      console.log('[UploadContext] Target collection:', targetCollection);
      console.log('[UploadContext] File count:', fileList.length);
      console.log('[UploadContext] ========================================');
      
      const result = await uploadApi.uploadFiles(
        fileList,
        uploadState.targetCollection || undefined
      );

      console.log('[UploadContext] ========================================');
      console.log('[UploadContext] ✅ UPLOAD INITIATED SUCCESSFULLY!');
      console.log('[UploadContext] Upload ID:', result.upload_id);
      console.log('[UploadContext] Initial status:', result.status);
      console.log('[UploadContext] Files in upload response:', result.files.length);
      console.log('[UploadContext]');
      console.log('[UploadContext] 📋 Upload Details:');
      result.files.forEach((file, index) => {
        console.log(`[UploadContext]   ${index + 1}. ${file.file_name}`);
        console.log(`[UploadContext]      Status: ${file.status}`);
        console.log(`[UploadContext]      Progress: ${file.progress}%`);
        console.log(`[UploadContext]      Target Collection: ${file.target_collection || 'auto-map (will be determined)'}`);
        console.log(`[UploadContext]      Chunks: ${file.chunks_count || 'pending'}`);
      });
      console.log('[UploadContext] ========================================');

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
      console.error('[UploadContext] Upload error:', error);
      
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
    console.log('[UploadContext] clearFiles called');
    setUploadState({
      files: [],
      targetCollection: null,
      isUploading: false,
      overallProgress: 0,
    });
  }, []);

  const clearCompletedFiles = useCallback(() => {
    console.log('[UploadContext] clearCompletedFiles called');
    setUploadState((prev) => ({
      ...prev,
      files: prev.files.filter((f) => f.status !== 'success'),
    }));
  }, []);

  return (
    <UploadContext.Provider
      value={{
        uploadState,
        addFiles,
        removeFile,
        setTargetCollection,
        uploadFiles,
        clearFiles,
        clearCompletedFiles,
        formatFileSize,
      }}
    >
      {children}
    </UploadContext.Provider>
  );
}

export function useUploadContext() {
  const context = useContext(UploadContext);
  if (context === undefined) {
    throw new Error('useUploadContext must be used within an UploadProvider');
  }
  return context;
}

