/**
 * FilePreview component to preview selected files with names, sizes, and remove buttons
 */

'use client';

import { useUploadContext } from '@/context/UploadContext';
import { cn } from '@/utils/cn';

export default function FilePreview() {
  const { uploadState, removeFile, formatFileSize } = useUploadContext();

  if (uploadState.files.length === 0) {
    return null;
  }

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-semibold text-gray-700">
        Selected Files ({uploadState.files.length})
      </h3>
      <div className="space-y-2 max-h-64 overflow-y-auto">
        {uploadState.files.map((file) => (
          <div
            key={file.id}
            className={cn(
              'flex items-center justify-between p-3 rounded-lg border',
              file.status === 'error'
                ? 'bg-red-50 border-red-200'
                : file.status === 'success'
                ? 'bg-green-50 border-green-200'
                : 'bg-gray-50 border-gray-200'
            )}
          >
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {file.file.name}
              </p>
              <p className="text-xs text-gray-500">
                {formatFileSize(file.file.size)} • {file.status}
                {file.chunksCount && ` • ${file.chunksCount} chunks`}
              </p>
              {file.targetCollection && (
                <p className="text-xs font-semibold text-primary mt-1">
                  📁 Collection: {file.targetCollection.replace(/_/g, ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                </p>
              )}
              {!file.targetCollection && (file.status === 'success' || file.status === 'uploading') && (
                <p className="text-xs text-gray-400 mt-1 italic">
                  Collection: Determining...
                </p>
              )}
              {file.error && (
                <p className="text-xs text-red-600 mt-1">{file.error}</p>
              )}
              {file.status === 'uploading' && file.progress > 0 && (
                <p className="text-xs text-blue-600 mt-1">
                  Progress: {file.progress.toFixed(0)}%
                </p>
              )}
            </div>
            {file.status !== 'uploading' && (
              <button
                onClick={() => removeFile(file.id)}
                className="ml-3 p-1 text-gray-400 hover:text-red-600 transition-colors"
                aria-label={`Remove ${file.file.name}`}
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

