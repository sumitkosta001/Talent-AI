import React from 'react';
import Link from 'next/link';
import { File, CheckCircle2, Eye, FileText, UploadCloud } from 'lucide-react';
import ResumeDropzone from './ResumeDropzone';

interface ResumeUploaderProps {
  isUploading: boolean;
  uploadProgress: number;
  isUploaded: boolean;
  uploadedFile: { name: string; size: string } | null;
  onFileSelect: (file: File) => void;
}

export default function ResumeUploader({
  isUploading,
  uploadProgress,
  isUploaded,
  uploadedFile,
  onFileSelect,
}: ResumeUploaderProps) {
  return (
    <div className="space-y-6">
      <ResumeDropzone
        onFileSelect={onFileSelect}
        isUploading={isUploading}
        uploadProgress={uploadProgress}
        uploadedFile={uploadedFile}
      />

      {isUploaded && uploadedFile && (
        <div className="bg-white rounded-2xl border border-emerald-200 p-5 shadow-sm animate-in fade-in slide-in-from-bottom-3 duration-300">
          <div className="flex items-center gap-3.5 mb-4">
            <div className="w-10 h-10 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center flex-shrink-0">
              <CheckCircle2 size={22} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-bold text-[#0F172A] truncate">{uploadedFile.name}</p>
              <p className="text-xs text-[#64748B]">{uploadedFile.size} · Upload complete</p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-3">
            <Link
              href="/candidate/resume"
              className="flex-1 flex items-center justify-center gap-2 bg-[#2563EB] text-white py-2.5 rounded-xl text-xs font-bold hover:bg-[#1D4ED8] transition-colors cursor-pointer shadow-xs"
            >
              <Eye size={15} />
              Manage in Resume Dashboard
            </Link>
            <Link
              href="/candidate/resume/analysis"
              className="flex-1 flex items-center justify-center gap-2 border border-[#CBD5E1] text-[#0F172A] py-2.5 rounded-xl text-xs font-semibold hover:bg-[#F8FAFC] transition-colors cursor-pointer"
            >
              <FileText size={15} />
              View AI Analysis
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
