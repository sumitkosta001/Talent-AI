'use client';

import React, { useState } from 'react';
import { useResume } from '@/hooks/useResume';
import { FileText, Download, AlertCircle, Bot, Loader2, Eye, X, AlertTriangle } from 'lucide-react';

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
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-8 text-center text-xs text-[#64748B] font-semibold shadow-sm">
        No primary resume file uploaded. Please upload a PDF or DOCX in the Resume module.
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

  const isDocx = previewName.toLowerCase().endsWith('.docx');

  return (
    <div className="space-y-6 text-[#0F172A] text-left">
      {/* Resume Card Details */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4">
        <h3 className="font-bold text-sm sm:text-base">Primary Resume</h3>

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

      {/* Preview Modal Overlay */}
      {previewId && (
        <div className="fixed inset-0 bg-[#0F172A]/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 transition-all duration-300">
          <div className="bg-white rounded-2xl max-w-4xl w-full h-[80vh] flex flex-col shadow-2xl overflow-hidden border border-slate-100 animate-in zoom-in-95 duration-200">
            {/* Modal Header */}
            <div className="px-5 py-4 border-b border-slate-100 bg-[#F8FAFC] flex justify-between items-center flex-shrink-0">
              <div className="flex items-center gap-2.5 min-w-0">
                <div className="p-2 bg-red-50 text-red-500 rounded-lg flex-shrink-0">
                  <FileText size={16} />
                </div>
                <h3 className="font-bold text-[#0F172A] text-sm sm:text-base truncate">{previewName}</h3>
              </div>
              <button
                onClick={handleClosePreview}
                className="p-1.5 hover:bg-[#E2E8F0] text-[#64748B] hover:text-[#0F172A] rounded-lg transition-colors cursor-pointer"
                title="Close"
              >
                <X size={18} />
              </button>
            </div>

            {/* Modal Body / Viewer */}
            <div className="flex-1 bg-slate-50 flex flex-col justify-center items-center p-6 overflow-hidden relative">
              {previewLoading && (
                <div className="flex flex-col items-center gap-3">
                  <Loader2 className="animate-spin text-[#2563EB]" size={36} />
                  <p className="text-sm text-[#64748B] font-semibold">Decrypting document stream...</p>
                </div>
              )}

              {previewError && (
                <div className="flex flex-col items-center gap-4 text-center max-w-md">
                  <div className="w-12 h-12 bg-red-50 border border-red-100 text-red-500 rounded-2xl flex items-center justify-center">
                    <AlertTriangle size={24} />
                  </div>
                  <div>
                    <h4 className="font-bold text-[#0F172A] text-base">Unable to preview document</h4>
                    <p className="text-xs sm:text-sm text-[#64748B] mt-1 leading-normal">{previewError}</p>
                  </div>
                  <button
                    onClick={() => handlePreview(previewId, previewName)}
                    className="bg-[#2563EB] text-white hover:bg-[#1D4ED8] font-bold text-xs px-4 py-2 rounded-xl transition-all cursor-pointer inline-flex items-center gap-1.5"
                  >
                    Retry Loading
                  </button>
                </div>
              )}

              {!previewLoading && !previewError && previewBlobUrl && (
                isDocx ? (
                  /* DOCX Fallback display */
                  <div className="flex flex-col items-center gap-4 text-center max-w-md p-6 bg-white border border-[#E2E8F0] rounded-2xl shadow-sm">
                    <div className="w-14 h-14 bg-blue-50 border border-blue-100 text-blue-600 rounded-2xl flex items-center justify-center">
                      <FileText size={30} />
                    </div>
                    <div>
                      <h4 className="font-bold text-[#0F172A] text-base">Microsoft Word Preview Unsupported</h4>
                      <p className="text-xs sm:text-sm text-[#64748B] mt-1.5 leading-relaxed">
                        Browser engines cannot render DOCX files natively. Download the document to review its contents.
                      </p>
                    </div>
                    <button
                      onClick={() => downloadResumeFile(previewId, previewName)}
                      className="bg-[#2563EB] text-white hover:bg-[#1D4ED8] font-bold text-xs px-4 py-2.5 rounded-xl transition-all cursor-pointer inline-flex items-center gap-1.5 w-full justify-center"
                    >
                      <Download size={14} /> Download DOCX File
                    </button>
                  </div>
                ) : (
                  /* PDF Frame display */
                  <iframe
                    src={previewBlobUrl}
                    className="w-full h-full border-0 rounded-lg shadow-inner bg-white"
                    title="PDF Resume Preview"
                  />
                )
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
