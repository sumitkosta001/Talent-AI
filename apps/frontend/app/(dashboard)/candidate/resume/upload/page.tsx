'use client';

import React, { useEffect, useState } from 'react';
import { useResume } from '@/hooks/useResume';
import { useToast } from '@/hooks/useToast';
import ResumeUploader from '@/components/resume/ResumeUploader';
import ResumeHistory from '@/components/resume/ResumeHistory';
import ResumePreviewModal from '@/components/resume/ResumePreviewModal';
import { CheckCircle, AlertTriangle, RefreshCw } from 'lucide-react';
import Link from 'next/link';

export default function ResumeUploadPage() {
  const {
    history,
    loading,
    error,
    isUploading,
    uploadProgress,
    isUploaded,
    uploadedFile,
    previewBlobUrl,
    previewLoading,
    previewError,
    fetchHistory,
    uploadResumeFile,
    deleteHistoryItem,
    previewResumeFile,
    downloadResumeFile,
    clearPreview,
  } = useResume();

  const { success: showSuccess, error: showError } = useToast();

  const [previewId, setPreviewId] = useState<string | null>(null);
  const [previewName, setPreviewName] = useState<string>('');

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const handleFileSelect = async (file: File) => {
    try {
      await uploadResumeFile(file);
      showSuccess('Resume Uploaded', `${file.name} is stored and registered.`);
    } catch (err: any) {
      showError('Upload Failed', err?.message || 'Failed to upload resume file.');
    }
  };

  const handleDeleteHistory = async (id: string) => {
    try {
      await deleteHistoryItem(id);
      showSuccess('Resume Deleted', 'The resume document has been removed.');
    } catch (err: any) {
      showError('Delete Failed', err?.message || 'Could not delete resume.');
    }
  };

  const handlePreview = async (id: string, name: string) => {
    setPreviewId(id);
    setPreviewName(name);
    await previewResumeFile(id);
  };

  const handleClosePreview = () => {
    setPreviewId(null);
    setPreviewName('');
    clearPreview();
  };

  return (
    <div className="p-4 sm:p-6 space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">Upload Resume</h1>
          <p className="text-xs sm:text-sm text-[#64748B] mt-1">
            Upload your resume file to obtain AI-powered compatibility analysis and check ATS keyword scores.
          </p>
        </div>
        <Link
          href="/candidate/resume"
          className="text-xs font-bold text-[#2563EB] hover:underline"
        >
          ← Resume Dashboard
        </Link>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex gap-3 items-center text-xs sm:text-sm text-red-800 animate-in fade-in duration-200">
          <AlertTriangle size={18} className="flex-shrink-0" />
          <p className="leading-snug">{error}</p>
        </div>
      )}

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left column: Drag-drop & tips */}
        <div className="lg:col-span-2 space-y-6">
          <ResumeUploader
            isUploading={isUploading}
            uploadProgress={uploadProgress}
            isUploaded={isUploaded}
            uploadedFile={uploadedFile}
            onFileSelect={handleFileSelect}
          />

          {/* Guidelines / Tips card */}
          <div className="bg-blue-50/50 rounded-2xl border border-blue-100 p-5 space-y-3.5">
            <h3 className="text-sm font-bold text-[#2563EB]">Tips for high compatibility</h3>
            <ul className="space-y-2">
              {[
                'Use clear, standard section headings (Work Experience, Education, Technical Skills).',
                'Quantify achievements where possible (e.g., "$100K budget managed", "35% faster load speeds").',
                'Integrate target job terms directly into your role summaries and project stack descriptions.',
                'Keep formatting structural — avoid complex visual layout columns, side tables, or charts.',
                'Save and export as PDF to maintain formatting integrity during automated parsing.',
              ].map((tip) => (
                <li key={tip} className="flex items-start gap-2 text-xs sm:text-sm text-[#2563EB]/90">
                  <CheckCircle size={14} className="mt-0.5 flex-shrink-0 text-[#2563EB]" />
                  <span className="leading-relaxed">{tip}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Right column: Upload history list */}
        <div>
          {loading && history.length === 0 ? (
            <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 flex flex-col items-center justify-center gap-2">
              <RefreshCw className="animate-spin text-[#2563EB]" size={20} />
              <p className="text-xs text-[#64748B] font-semibold">Syncing history...</p>
            </div>
          ) : (
            <ResumeHistory
              history={history}
              onDelete={handleDeleteHistory}
              onPreview={handlePreview}
              onDownload={downloadResumeFile}
            />
          )}
        </div>
      </div>

      {/* Shared Preview Modal */}
      <ResumePreviewModal
        isOpen={!!previewId}
        resumeId={previewId}
        filename={previewName}
        blobUrl={previewBlobUrl}
        isLoading={previewLoading}
        error={previewError}
        onClose={handleClosePreview}
        onDownload={downloadResumeFile}
        onRetry={() => previewId && previewResumeFile(previewId)}
      />
    </div>
  );
}
