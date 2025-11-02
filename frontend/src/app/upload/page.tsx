/**
 * Document upload page integrating FileUploader, FilePreview,
 * KnowledgeBaseSelector, and UploadProgress components
 */

'use client';

import Header from '@/layouts/Header';
import FileUploader from '@/components/DocumentUpload/FileUploader';
import FilePreview from '@/components/DocumentUpload/FilePreview';
import KnowledgeBaseSelector from '@/components/DocumentUpload/KnowledgeBaseSelector';
import UploadProgress from '@/components/DocumentUpload/UploadProgress';
import { UploadProvider } from '@/context/UploadContext';

export default function UploadPage() {
  return (
    <UploadProvider>
      <div className="flex flex-col min-h-screen">
        <Header />
        <div className="flex-1 overflow-y-auto">
          <div className="container mx-auto px-4 py-10 max-w-4xl">
            <div className="bg-white/75 backdrop-blur-xl border border-white/40 shadow-2xl rounded-3xl p-8 space-y-6">
              <div className="text-center space-y-2">
                <p className="text-sm uppercase tracking-[0.3em] text-primary font-semibold">
                  Knowledge Base Upload Portal
                </p>
                <h2 className="text-3xl font-bold text-gray-900">
                  Upload Documents
                </h2>
                <p className="text-sm text-gray-600 max-w-2xl mx-auto">
                  Drag and drop or browse to upload manuals, policies, contracts, and other resources.
                  Files larger than 20&nbsp;MB are automatically rejected.
                </p>
              </div>

              <div className="space-y-6">
                {/* Knowledge Base Selector */}
                <section className="bg-white/85 backdrop-blur-md border border-white/40 rounded-2xl shadow-lg p-6">
                  <KnowledgeBaseSelector />
                </section>
                
                {/* File Uploader */}
                <section className="bg-white/85 backdrop-blur-md border border-white/40 rounded-2xl shadow-lg p-6">
                  <FileUploader />
                </section>
                
                {/* File Preview */}
                <section className="bg-white/85 backdrop-blur-md border border-white/40 rounded-2xl shadow-lg p-6">
                  <FilePreview />
                </section>
                
                {/* Upload Progress */}
                <section className="bg-white/85 backdrop-blur-md border border-white/40 rounded-2xl shadow-lg p-6">
                  <UploadProgress />
                </section>
              </div>
            </div>
          </div>
        </div>
      </div>
    </UploadProvider>
  );
}

