'use client';

import React, { useEffect, useState } from 'react';
import { useResume } from '@/hooks/useResume';
import ResumeUploader from '@/components/resume/ResumeUploader';
import ResumeHistory from '@/components/resume/ResumeHistory';
import { CheckCircle, AlertTriangle, RefreshCw, X, Download, Loader2, FileText } from 'lucide-react';

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

  const [previewId, setPreviewId] = useState<string | null>(null);
  const [previewName, setPreviewName] = useState<string>('');

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const handleFileSelect = (file: File) => {
    uploadResumeFile(file);
  };

  const handleDeleteHistory = (id: string) => {
    deleteHistoryItem(id);
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

  const isDocx = previewName.toLowerCase().endsWith('.docx');

  return (
    <div className="p-4 sm:p-6 space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">Upload Resume</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-1">
          Upload your resume file to obtain AI-powered compatibility analysis and check ATS keyword scores.
        </p>
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
