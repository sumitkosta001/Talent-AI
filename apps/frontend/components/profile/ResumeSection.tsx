'use client';

import React, { useState } from 'react';
import { useResume } from '@/hooks/useResume';
import ResumePreviewModal from '@/components/resume/ResumePreviewModal';
import { FileText, Download, AlertCircle, Bot, Loader2, Eye } from 'lucide-react';
import Link from 'next/link';

export default function ResumeSection() {
  const {
    resume,
    loading,
    previewBlobUrl,
    previewLoading,
    previewError,
    previewResumeFile,
    downloadResumeFile,
    clearPreview,
  } = useResume();

  const [previewId, setPreviewId] = useState<string | null>(null);
  const [previewName, setPreviewName] = useState<string>('');

  if (loading) {
    return (
      <div className="flex justify-center p-8">
        <Loader2 className="animate-spin text-blue-600" size={24} />
      </div>
    );
  }

  if (!resume || resume.name === 'No resume uploaded' || !resume.id) {
    return (
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-8 text-center text-xs text-[#64748B] font-semibold shadow-sm space-y-3">
        <p>No primary resume file uploaded.</p>
        <Link
          href="/candidate/resume"
          className="inline-flex items-center justify-center gap-1.5 bg-[#2563EB] text-white px-4 py-2 rounded-xl text-xs font-bold hover:bg-[#1D4ED8] transition-colors"
        >
          Go to Resume Dashboard
        </Link>
      </div>
    );
  }

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
    <div className="space-y-6 text-[#0F172A] text-left">
      {/* Resume Card Details */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-sm sm:text-base">Primary Resume</h3>
          <Link
            href="/candidate/resume"
            className="text-xs text-[#2563EB] font-bold hover:underline"
          >
            Manage Versions →
          </Link>
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 border border-[#F1F5F9] bg-[#F8FAFC]/50 rounded-xl">
          <div className="flex items-start gap-3">
            <div className="p-2.5 bg-blue-50 text-blue-600 rounded-xl flex-shrink-0">
              <FileText size={20} />
            </div>
            <div className="text-xs font-semibold">
              <h4 className="font-bold text-[#0F172A] text-sm leading-normal">{resume.name}</h4>
              <p className="text-[#64748B] mt-0.5">Version: {resume.version} · Uploaded: {resume.uploadDate}</p>
            </div>
          </div>

          <div className="flex items-center gap-2 self-end sm:self-center">
            <button
              onClick={() => handlePreview(resume.id, resume.name)}
              className="bg-white border border-[#E2E8F0] hover:bg-[#F8FAFC] text-slate-700 font-bold text-xs px-3.5 py-2 rounded-xl transition-all cursor-pointer inline-flex items-center gap-1.5"
            >
              <Eye size={14} /> Preview
            </button>
            <button
              onClick={() => downloadResumeFile(resume.id, resume.name)}
              className="bg-white border border-[#E2E8F0] hover:bg-[#F8FAFC] text-slate-700 font-bold text-xs px-3.5 py-2 rounded-xl transition-all cursor-pointer inline-flex items-center gap-1.5"
            >
              <Download size={14} /> Download
            </button>
          </div>
        </div>
      </div>

      {/* ATS score overview */}
      {resume.atsScore && (
        <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-3">
          <h4 className="font-bold text-sm text-[#0F172A] flex items-center gap-1.5">
            <Bot size={16} className="text-purple-600 animate-pulse" />
            AI Resume Parsing Score
          </h4>
          <div className="flex flex-col sm:flex-row sm:items-center gap-4">
            <div className="text-center bg-[#F8FAFC] border border-[#E2E8F0] px-5 py-3 rounded-2xl flex-shrink-0 w-28 mx-auto sm:mx-0">
              <span className="text-2xl font-black text-[#0F172A]">{resume.atsScore}%</span>
              <p className="text-[8px] text-[#64748B] font-bold mt-0.5 uppercase tracking-wider">ATS Score</p>
            </div>
            <div className="text-xs text-slate-500 font-semibold space-y-1.5">
              <p className="leading-relaxed text-slate-600">
                Your resume keywords matches represent a high alignment rate of **87%** with core SDE roles.
              </p>
              <div className="flex items-start gap-1 text-[11px] text-[#64748B]">
                <AlertCircle size={13} className="text-blue-500 flex-shrink-0 mt-0.5" />
                <p>To exceed 90%, integrate keywords like System Operations and access Management.</p>
              </div>
            </div>
          </div>
        </div>
      )}

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
