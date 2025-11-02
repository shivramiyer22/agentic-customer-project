/**
 * FileUploader component with drag-and-drop file picker supporting multiple file selection
 */

'use client';

import { useRef, useState, DragEvent, ChangeEvent } from 'react';
import { useUploadContext } from '@/context/UploadContext';
import { cn } from '@/utils/cn';

export default function FileUploader() {
  const { addFiles } = useUploadContext();
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const dragCounterRef = useRef(0);

  const handleFiles = (files: FileList | null) => {
    console.log('[FileUploader] ========================================');
    console.log('[FileUploader] 📎 handleFiles called with', files?.length || 0, 'file(s)');
    
    if (!files || files.length === 0) {
      console.warn('[FileUploader] ⚠️ No files provided');
      return;
    }
    
    const fileArray = Array.from(files);
    console.log('[FileUploader] 📋 File details:');
    fileArray.forEach((file, index) => {
      console.log(`[FileUploader]   ${index + 1}. ${file.name}`);
      console.log(`[FileUploader]      Size: ${(file.size / 1024).toFixed(2)} KB`);
      console.log(`[FileUploader]      Type: ${file.type || 'unknown'}`);
      console.log(`[FileUploader]      Last Modified: ${new Date(file.lastModified).toLocaleString()}`);
    });
    
    try {
      addFiles(fileArray);
      console.log('[FileUploader] ✅ Successfully added files to upload state');
      console.log('[FileUploader] ⏳ Files are now pending upload');
      console.log('[FileUploader] ========================================');
    } catch (error) {
      console.error('[FileUploader] ❌ Error adding files:', error);
      console.log('[FileUploader] ========================================');
    }
  };

  const handleDragEnter = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounterRef.current++;
    
    console.log('[FileUploader] 🖱️ Drag enter event, counter:', dragCounterRef.current);
    console.log('[FileUploader] DataTransfer types:', e.dataTransfer?.types);
    
    if (e.dataTransfer?.types.includes('Files')) {
      setIsDragging(true);
      console.log('[FileUploader] ✅ Files detected - drag state activated');
    } else {
      console.log('[FileUploader] ⚠️ Not a file drag - types:', Array.from(e.dataTransfer?.types || []));
    }
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.dataTransfer) {
      e.dataTransfer.dropEffect = 'copy';
    }
    
    // Keep dragging state active
    if (!isDragging && e.dataTransfer?.types.includes('Files')) {
      setIsDragging(true);
    }
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounterRef.current--;
    
    console.log('[FileUploader] Drag leave, counter:', dragCounterRef.current);
    
    // Only set dragging to false when we've truly left the drop zone
    if (dragCounterRef.current === 0) {
      setIsDragging(false);
      console.log('[FileUploader] Drag state set to false (left drop zone)');
    }
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    dragCounterRef.current = 0;

    console.log('[FileUploader] ========================================');
    console.log('[FileUploader] 📦 Drop event triggered');
    
    const files = e.dataTransfer?.files;
    console.log('[FileUploader] Files in drop:', files?.length || 0);
    console.log('[FileUploader] DataTransfer items:', e.dataTransfer?.items.length || 0);
    
    if (files && files.length > 0) {
      console.log('[FileUploader] ✅ Processing dropped files');
      handleFiles(files);
    } else {
      console.warn('[FileUploader] ⚠️ No files in drop event');
      console.log('[FileUploader] ========================================');
    }
  };

  const handleFileSelect = (e: ChangeEvent<HTMLInputElement>) => {
    console.log('[FileUploader] ========================================');
    console.log('[FileUploader] 📂 File select event triggered (dialog)');
    
    const files = e.target.files;
    console.log('[FileUploader] Selected files count:', files?.length || 0);
    
    if (files && files.length > 0) {
      console.log('[FileUploader] ✅ Processing selected files');
      handleFiles(files);
    } else {
      console.warn('[FileUploader] ⚠️ No files selected or dialog cancelled');
      console.log('[FileUploader] ========================================');
    }
    
    // Reset input to allow selecting same file again
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleClick = () => {
    console.log('[FileUploader] 🖱️ Click event triggered - opening file dialog');
    fileInputRef.current?.click();
  };

  return (
    <div
      onDragEnter={handleDragEnter}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={handleClick}
      className={cn(
        'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors',
        isDragging
          ? 'border-primary bg-primary/10'
          : 'border-gray-300 hover:border-primary hover:bg-gray-50'
      )}
      role="button"
      tabIndex={0}
      aria-label="File upload area"
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleClick();
        }
      }}
    >
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".pdf,.txt,.md,.json"
        onChange={handleFileSelect}
        className="hidden"
        aria-label="File input"
      />
      <div className="flex flex-col items-center gap-4 pointer-events-none">
        <svg
          className="w-12 h-12 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
        <div>
          <p className="text-lg font-semibold text-gray-700">
            {isDragging ? 'Drop files here' : 'Click to upload or drag and drop'}
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Supported formats: PDF, TXT, Markdown, JSON (Max 20 MB per file)
          </p>
          <p className="text-xs text-red-600 mt-2 font-semibold">
            ⚠️ Each file must be 20 MB or smaller. Larger files will be rejected automatically.
          </p>
        </div>
      </div>
    </div>
  );
}

