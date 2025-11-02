/**
 * UploadProgress component to display upload progress (percentage and file-by-file status)
 */

'use client';

import { useUploadContext } from '@/context/UploadContext';
import { cn } from '@/utils/cn';

export default function UploadProgress() {
  const { uploadState, uploadFiles, clearCompletedFiles } = useUploadContext();

  const pendingFiles = uploadState.files.filter((f) => f.status === 'pending');
  const uploadingFiles = uploadState.files.filter((f) => f.status === 'uploading');
  const successFiles = uploadState.files.filter((f) => f.status === 'success');
  const errorFiles = uploadState.files.filter((f) => f.status === 'error');

  const totalFiles = uploadState.files.length;
  const completedFiles = successFiles.length + errorFiles.length;
  // Use overall progress from state if available, otherwise calculate
  const progressPercentage = uploadState.overallProgress > 0 
    ? uploadState.overallProgress 
    : (totalFiles > 0 ? (completedFiles / totalFiles) * 100 : 0);

  if (totalFiles === 0) {
    return null;
  }

  return (
    <div className="space-y-4">
      {/* Overall Progress */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-gray-700">Upload Progress</h3>
          <span className="text-sm text-gray-600">
            {completedFiles} / {totalFiles} files
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={cn(
              'h-2 rounded-full transition-all duration-300',
              uploadState.isUploading ? 'bg-primary' : 'bg-green-500'
            )}
            style={{ width: `${progressPercentage}%` }}
            role="progressbar"
            aria-valuenow={progressPercentage}
            aria-valuemin={0}
            aria-valuemax={100}
          />
        </div>
        <p className="text-xs text-gray-600">{progressPercentage.toFixed(0)}% complete</p>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-2">
        {pendingFiles.length > 0 && (
          <button
            onClick={uploadFiles}
            disabled={uploadState.isUploading}
            className={cn(
              'px-4 py-2 rounded-lg font-semibold transition-colors',
              'bg-primary text-white hover:bg-primary-dark',
              'disabled:bg-gray-300 disabled:cursor-not-allowed'
            )}
          >
            {uploadState.isUploading ? 'Uploading...' : `Upload ${pendingFiles.length} File(s)`}
          </button>
        )}
        {successFiles.length > 0 && (
          <button
            onClick={clearCompletedFiles}
            className="px-4 py-2 rounded-lg font-semibold border border-gray-300 text-gray-700 hover:bg-gray-50"
          >
            Clear Completed
          </button>
        )}
      </div>

      {/* File-by-file Status */}
      {uploadState.files.length > 0 && (
        <div className="space-y-1 max-h-40 overflow-y-auto">
          {uploadState.files.map((file) => (
            <div
              key={file.id}
              className={cn(
                'flex items-center gap-2 text-xs p-2 rounded',
                file.status === 'success' && 'bg-green-50 text-green-700',
                file.status === 'error' && 'bg-red-50 text-red-700',
                file.status === 'uploading' && 'bg-blue-50 text-blue-700',
                file.status === 'pending' && 'bg-gray-50 text-gray-700'
              )}
            >
              <span className="flex-1 truncate">{file.file.name}</span>
              {file.targetCollection && (
                <span className="text-xs mr-2 font-semibold">
                  📁 {file.targetCollection.replace(/_/g, ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                </span>
              )}
              {!file.targetCollection && (file.status === 'success' || file.status === 'uploading') && (
                <span className="text-xs mr-2 text-gray-400 italic">
                  Determining collection...
                </span>
              )}
              <span className="font-medium capitalize">{file.status}</span>
              {file.status === 'uploading' && file.progress > 0 && (
                <span className="text-xs">{file.progress.toFixed(0)}%</span>
              )}
              {file.status === 'uploading' && (
                <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
              )}
              {file.status === 'success' && file.chunksCount && (
                <span className="text-xs">({file.chunksCount} chunks)</span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

