import React, { useEffect } from 'react';
import { FileText, X, Download, Loader2, AlertTriangle, RefreshCw } from 'lucide-react';

interface ResumePreviewModalProps {
  isOpen: boolean;
  resumeId: string | null;
  filename: string;
  blobUrl: string | null;
  isLoading: boolean;
  error: string | null;
  onClose: () => void;
  onDownload: (id: string, name: string) => void;
  onRetry: () => void;
}

export default function ResumePreviewModal({
  isOpen,
  resumeId,
  filename,
  blobUrl,
  isLoading,
  error,
  onClose,
  onDownload,
  onRetry,
}: ResumePreviewModalProps) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const isDocx = filename.toLowerCase().endsWith('.docx');
  const isPdf = filename.toLowerCase().endsWith('.pdf');

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="preview-modal-title"
      className="fixed inset-0 bg-[#0F172A]/75 backdrop-blur-xs z-50 flex items-center justify-center p-3 sm:p-6 transition-all duration-200 animate-in fade-in"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-2xl max-w-4xl w-full h-[85vh] flex flex-col shadow-2xl overflow-hidden border border-slate-200 animate-in zoom-in-95 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="px-5 py-4 border-b border-slate-100 bg-[#F8FAFC] flex justify-between items-center flex-shrink-0">
          <div className="flex items-center gap-3 min-w-0">
            <div
              className={`p-2 rounded-xl flex-shrink-0 ${
                isPdf ? 'bg-red-50 text-red-500' : 'bg-blue-50 text-blue-500'
              }`}
            >
              <FileText size={18} />
            </div>
            <div className="min-w-0">
              <h3 id="preview-modal-title" className="font-bold text-[#0F172A] text-sm sm:text-base truncate">
                {filename}
              </h3>
              <p className="text-[11px] text-[#64748B]">Secure Document Preview</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {resumeId && (
              <button
                onClick={() => onDownload(resumeId, filename)}
                className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-[#0F172A] bg-white border border-[#CBD5E1] hover:bg-[#F1F5F9] transition-colors cursor-pointer"
                title="Download file"
              >
                <Download size={14} className="text-[#059669]" />
                Download
              </button>
            )}
            <button
              onClick={onClose}
              className="p-1.5 hover:bg-[#E2E8F0] text-[#64748B] hover:text-[#0F172A] rounded-xl transition-colors cursor-pointer"
              title="Close Preview"
              aria-label="Close"
            >
              <X size={20} />
            </button>
          </div>
        </div>

        {/* Modal Body */}
        <div className="flex-1 bg-slate-50 flex flex-col justify-center items-center p-4 sm:p-6 overflow-hidden relative">
          {isLoading && (
            <div className="flex flex-col items-center gap-3 text-center">
              <Loader2 className="animate-spin text-[#2563EB]" size={36} />
              <p className="text-sm font-semibold text-[#64748B]">Loading document stream...</p>
            </div>
          )}

          {error && !isLoading && (
            <div className="flex flex-col items-center gap-4 text-center max-w-md p-6 bg-white rounded-2xl border border-red-200 shadow-xs">
              <div className="w-12 h-12 bg-red-50 text-red-500 rounded-2xl flex items-center justify-center">
                <AlertTriangle size={24} />
              </div>
              <div>
                <h4 className="font-bold text-[#0F172A] text-base">Unable to preview document</h4>
                <p className="text-xs text-[#64748B] mt-1.5 leading-relaxed">{error}</p>
              </div>
              <button
                onClick={onRetry}
                className="inline-flex items-center gap-2 bg-[#2563EB] text-white hover:bg-[#1D4ED8] font-semibold text-xs px-4 py-2 rounded-xl transition-all cursor-pointer shadow-xs"
              >
                <RefreshCw size={13} />
                Retry
              </button>
            </div>
          )}

          {!isLoading && !error && blobUrl && (
            isDocx ? (
              <div className="flex flex-col items-center gap-4 text-center max-w-md p-8 bg-white border border-[#E2E8F0] rounded-2xl shadow-sm">
                <div className="w-16 h-16 bg-blue-50 border border-blue-100 text-blue-600 rounded-2xl flex items-center justify-center shadow-inner">
                  <FileText size={32} />
                </div>
                <div>
                  <h4 className="font-bold text-[#0F172A] text-base">DOCX Preview Not Supported In-Browser</h4>
                  <p className="text-xs text-[#64748B] mt-1.5 leading-relaxed">
                    Standard browsers cannot render Microsoft Word files natively. You can download the verified document directly to view it on your device.
                  </p>
                </div>
                {resumeId && (
                  <button
                    onClick={() => onDownload(resumeId, filename)}
                    className="inline-flex items-center justify-center gap-2 bg-[#2563EB] text-white hover:bg-[#1D4ED8] font-bold text-xs px-5 py-2.5 rounded-xl transition-all cursor-pointer w-full shadow-sm"
                  >
                    <Download size={14} /> Download DOCX Document
                  </button>
                )}
              </div>
            ) : (
              <iframe
                src={blobUrl}
                className="w-full h-full border-0 rounded-xl shadow-inner bg-white"
                title="PDF Resume Preview"
              />
            )
          )}
        </div>
      </div>
    </div>
  );
}
