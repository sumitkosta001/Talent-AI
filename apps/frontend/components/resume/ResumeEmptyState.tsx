import React from 'react';
import { FileUp, Sparkles } from 'lucide-react';

interface ResumeEmptyStateProps {
  onUploadClick?: () => void;
}

export default function ResumeEmptyState({ onUploadClick }: ResumeEmptyStateProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-10 sm:p-14 text-center space-y-5 shadow-xs">
      <div className="w-16 h-16 rounded-2xl bg-blue-50 text-[#2563EB] flex items-center justify-center mx-auto shadow-inner">
        <FileUp size={32} />
      </div>

      <div className="max-w-md mx-auto space-y-2">
        <h3 className="font-bold text-lg sm:text-xl text-[#0F172A]">No Resumes Uploaded Yet</h3>
        <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed">
          Upload your resume in PDF or Word DOCX format. Your resume will be stored securely in MinIO, versioned automatically, and ready for instant previews and job applications.
        </p>
      </div>

      {onUploadClick && (
        <button
          onClick={onUploadClick}
          className="inline-flex items-center justify-center gap-2 bg-[#2563EB] hover:bg-[#1D4ED8] text-white px-6 py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer shadow-sm"
        >
          <Sparkles size={14} className="text-yellow-300" />
          Upload Your First Resume
        </button>
      )}
    </div>
  );
}
