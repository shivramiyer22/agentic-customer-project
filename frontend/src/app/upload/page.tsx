'use client';

import Header from '@/layouts/Header';
import FileUploader from '@/components/DocumentUpload/FileUploader';
import FilePreview from '@/components/DocumentUpload/FilePreview';
import KnowledgeBaseSelector from '@/components/DocumentUpload/KnowledgeBaseSelector';
import UploadProgress from '@/components/DocumentUpload/UploadProgress';
import { UploadProvider } from '@/context/UploadContext';
import { SessionProvider } from '@/context/SessionContext';

export default function UploadPage() {
  return (
    <SessionProvider>
      <UploadProvider>
        <div className="flex flex-col min-h-screen">
          <Header />
          <div className="flex-1 overflow-y-auto flex items-start justify-center px-4 pt-12">
            <div className="container mx-auto py-10 max-w-5xl w-full">
              <div className="bg-white/75 backdrop-blur-xl border border-white/40 shadow-2xl rounded-3xl p-10 space-y-8">
                <div className="text-center space-y-3">
                  <p className="text-base uppercase tracking-[0.3em] text-primary font-semibold">
                    Knowledge Base Upload Portal
                  </p>
                  <h2 className="text-4xl font-bold text-gray-900">
                    Upload Documents
                  </h2>
                  <p className="text-base text-gray-600 max-w-2xl mx-auto">
                    Drag and drop or browse to upload manuals, policies, contracts, and other resources.
                    Files larger than 20&nbsp;MB are automatically rejected.
                  </p>
                </div>

                <div className="space-y-8">
                  {/* Knowledge Base Selector */}
                  <section className="bg-white/85 backdrop-blur-md border border-white/40 rounded-2xl shadow-lg p-8">
                    <KnowledgeBaseSelector />
                  </section>
                  
                  {/* File Uploader */}
                  <section className="bg-white/85 backdrop-blur-md border border-white/40 rounded-2xl shadow-lg p-8">
                    <FileUploader />
                  </section>
                  
                  {/* File Preview */}
                  <section className="bg-white/85 backdrop-blur-md border border-white/40 rounded-2xl shadow-lg p-8">
                    <FilePreview />
                  </section>
                  
                  {/* Upload Progress */}
                  <section className="bg-white/85 backdrop-blur-md border border-white/40 rounded-2xl shadow-lg p-8">
                    <UploadProgress />
                  </section>
                </div>
              </div>
            </div>
          </div>
        </div>
      </UploadProvider>
    </SessionProvider>
  );
}

