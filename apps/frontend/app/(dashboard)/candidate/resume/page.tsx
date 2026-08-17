'use client';

import React, { useState, useRef } from 'react';
import { useResume } from '@/hooks/useResume';
import { useToast } from '@/hooks/useToast';
import ResumeCurrentCard from '@/components/resume/ResumeCurrentCard';
import ResumeDropzone from '@/components/resume/ResumeDropzone';
import ResumeList from '@/components/resume/ResumeList';
import ResumePreviewModal from '@/components/resume/ResumePreviewModal';
import ResumeDeleteDialog from '@/components/resume/ResumeDeleteDialog';
import ResumeRestoreDialog from '@/components/resume/ResumeRestoreDialog';
import ResumeSkeleton from '@/components/resume/ResumeSkeleton';
import ResumeEmptyState from '@/components/resume/ResumeEmptyState';
import { BackendResume } from '@/types/resume';
import {
  FileText,
  AlertTriangle,
  RefreshCw,
  Sparkles,
  ShieldCheck,
  CheckCircle2,
  HardDrive,
} from 'lucide-react';

export default function ResumePage() {
  const {
    resumes,
    currentResume,
    pagination,
    sortBy,
    sortOrder,
    loading,
    isRefreshing,
    error,
    isUploading,
    uploadProgress,
    uploadedFile,
    actionLoading,
    previewBlobUrl,
    previewLoading,
    previewError,
    uploadResumeFile,
    deleteResume,
    restoreVersion,
    retryProcessing,
    processResume,
    setPage,
    setSorting,
    refreshAll,
    previewResumeFile,
    downloadResumeFile,
    clearPreview,
  } = useResume();

  const { success: showSuccess, error: showError } = useToast();

  // Modal and Dialog states
  const [previewId, setPreviewId] = useState<string | null>(null);
  const [previewName, setPreviewName] = useState<string>('');
  const [deleteTarget, setDeleteTarget] = useState<BackendResume | null>(null);
  const [restoreTarget, setRestoreTarget] = useState<BackendResume | null>(null);

  const dropzoneRef = useRef<HTMLDivElement>(null);

  // Upload handler
  const handleFileUpload = async (file: File) => {
    try {
      const uploaded = await uploadResumeFile(file);
      showSuccess(
        'Resume uploaded successfully!',
        `${file.name} is now stored securely in MinIO.`
      );
    } catch (err: any) {
      showError('Upload Failed', err?.message || 'Failed to upload resume document.');
    }
  };

  // Preview handler
  const handleOpenPreview = async (id: string, name: string) => {
    setPreviewId(id);
    setPreviewName(name);
    await previewResumeFile(id);
  };

  const handleClosePreview = () => {
    setPreviewId(null);
    setPreviewName('');
    clearPreview();
  };

  // Delete handlers
  const handleOpenDelete = (resume: BackendResume) => {
    setDeleteTarget(resume);
  };

  const handleConfirmDelete = async () => {
    if (!deleteTarget) return;
    try {
      await deleteResume(deleteTarget.id);
      showSuccess('Resume deleted', `${deleteTarget.original_filename} (v${deleteTarget.version}) was removed.`);
      setDeleteTarget(null);
    } catch (err: any) {
      showError('Delete Failed', err?.message || 'Could not delete resume.');
    }
  };

  // Restore handlers
  const handleOpenRestore = (resume: BackendResume) => {
    setRestoreTarget(resume);
  };

  const handleConfirmRestore = async () => {
    if (!restoreTarget) return;
    try {
      await restoreVersion(restoreTarget.id);
      showSuccess(
        'Version Restored',
        `Version ${restoreTarget.version} (${restoreTarget.original_filename}) is now your active resume.`
      );
      setRestoreTarget(null);
    } catch (err: any) {
      showError('Restore Failed', err?.message || 'Could not restore resume version.');
    }
  };

  // Retry processing
  const handleRetryProcessing = async (id: string) => {
    try {
      await retryProcessing(id);
      showSuccess('Processing Started', 'Resume processing has been restarted.');
    } catch (err: any) {
      showError('Retry Failed', err?.message || 'Could not restart processing.');
    }
  };

  // Trigger processing
  const handleProcess = async (id: string) => {
    try {
      await processResume(id);
      showSuccess('Processing Complete', 'Resume parsed and verified.');
    } catch (err: any) {
      showError('Processing Failed', err?.message || 'Could not process resume.');
    }
  };

  const scrollToUpload = () => {
    dropzoneRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  if (loading) {
    return (
      <div className="p-4 sm:p-6 max-w-6xl mx-auto">
        <ResumeSkeleton />
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-6 space-y-6 max-w-6xl mx-auto text-[#0F172A]">
      {/* Header section */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A] tracking-tight">
            Resumes
          </h1>
          <p className="text-xs sm:text-sm text-[#64748B] mt-1">
            Upload, manage, preview, version and organize your professional resumes.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => refreshAll()}
            disabled={isRefreshing}
            className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold text-[#475569] bg-white border border-[#CBD5E1] hover:bg-[#F8FAFC] transition-colors cursor-pointer disabled:opacity-50"
            title="Refresh list"
          >
            <RefreshCw size={13} className={isRefreshing ? 'animate-spin text-[#2563EB]' : ''} />
            {isRefreshing ? 'Syncing...' : 'Sync'}
          </button>
        </div>
      </div>

      {/* Global Error Banner if any */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-4 flex items-center justify-between gap-3 text-xs sm:text-sm text-red-800 animate-in fade-in">
          <div className="flex items-center gap-2.5">
            <AlertTriangle size={18} className="text-red-600 flex-shrink-0" />
            <span>{error}</span>
          </div>
          <button
            onClick={() => refreshAll()}
            className="px-3 py-1 bg-red-100 hover:bg-red-200 text-red-900 rounded-lg font-bold text-xs transition-colors cursor-pointer"
          >
            Retry
          </button>
        </div>
      )}

      {/* Main Content Layout */}
      {resumes.length === 0 ? (
        <div className="space-y-6">
          <ResumeEmptyState onUploadClick={scrollToUpload} />

          <div ref={dropzoneRef} className="max-w-2xl mx-auto">
            <ResumeDropzone
              onFileSelect={handleFileUpload}
              isUploading={isUploading}
              uploadProgress={uploadProgress}
              uploadedFile={uploadedFile}
            />
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Current Active Resume Card */}
          {currentResume && (
            <ResumeCurrentCard
              resume={currentResume}
              onPreview={handleOpenPreview}
              onDownload={downloadResumeFile}
              onDelete={handleOpenDelete}
              onRetry={handleRetryProcessing}
              isActionLoading={!!actionLoading[currentResume.id]}
            />
          )}

          {/* Grid: Upload Dropzone & Storage Security Info */}
          <div className="grid lg:grid-cols-3 gap-6">
            <div ref={dropzoneRef} className="lg:col-span-2">
              <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="font-bold text-sm text-[#0F172A]">Upload New Version</h3>
                  <span className="text-[11px] text-[#64748B]">Auto-increments version</span>
                </div>
                <ResumeDropzone
                  onFileSelect={handleFileUpload}
                  isUploading={isUploading}
                  uploadProgress={uploadProgress}
                  uploadedFile={uploadedFile}
                />
              </div>
            </div>

            {/* Storage & Versioning Feature Card */}
            <div className="bg-gradient-to-br from-slate-900 to-slate-800 text-white rounded-2xl p-5 shadow-sm flex flex-col justify-between space-y-4">
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center">
                    <ShieldCheck size={18} />
                  </div>
                  <h4 className="font-bold text-sm">Enterprise Storage</h4>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Documents are encrypted in private MinIO object storage with automatic rollback compensation and SHA-256 integrity checks.
                </p>
                <ul className="space-y-1.5 text-xs text-slate-300">
                  <li className="flex items-center gap-1.5">
                    <CheckCircle2 size={13} className="text-emerald-400" />
                    <span>Automatic version numbering</span>
                  </li>
                  <li className="flex items-center gap-1.5">
                    <CheckCircle2 size={13} className="text-emerald-400" />
                    <span>One-click instant version restore</span>
                  </li>
                  <li className="flex items-center gap-1.5">
                    <CheckCircle2 size={13} className="text-emerald-400" />
                    <span>Zero public credential exposure</span>
                  </li>
                </ul>
              </div>

              <div className="pt-3 border-t border-slate-700/60 flex items-center justify-between text-[11px] text-slate-400">
                <span>Active versions: {resumes.length}</span>
                <span className="text-emerald-400 font-semibold">Protected</span>
              </div>
            </div>
          </div>

          {/* All Uploads & Version History Table */}
          <ResumeList
            resumes={resumes}
            pagination={pagination}
            sortBy={sortBy}
            sortOrder={sortOrder}
            actionLoading={actionLoading}
            onPageChange={setPage}
            onSortChange={setSorting}
            onPreview={handleOpenPreview}
            onDownload={downloadResumeFile}
            onRestore={handleOpenRestore}
            onDelete={handleOpenDelete}
            onRetry={handleRetryProcessing}
            onProcess={handleProcess}
          />
        </div>
      )}

      {/* Preview Modal */}
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

      {/* Delete Confirmation Dialog */}
      <ResumeDeleteDialog
        isOpen={!!deleteTarget}
        resume={deleteTarget}
        isLoading={deleteTarget ? actionLoading[deleteTarget.id] === 'delete' : false}
        onClose={() => setDeleteTarget(null)}
        onConfirm={handleConfirmDelete}
      />

      {/* Restore Confirmation Dialog */}
      <ResumeRestoreDialog
        isOpen={!!restoreTarget}
        resume={restoreTarget}
        isLoading={restoreTarget ? actionLoading[restoreTarget.id] === 'restore' : false}
        onClose={() => setRestoreTarget(null)}
        onConfirm={handleConfirmRestore}
      />
    </div>
  );
}
