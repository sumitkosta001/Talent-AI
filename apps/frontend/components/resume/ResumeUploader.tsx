import React from 'react';
import Link from 'next/link';
import { File, CheckCircle, Eye, FileText } from 'lucide-react';
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
      {!isUploading && !isUploaded && (
        <ResumeDropzone onFileSelect={onFileSelect} isUploading={isUploading} />
      )}

      {(isUploading || isUploaded) && uploadedFile && (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm animate-in fade-in slide-in-from-bottom-3 duration-300">
          <div className="flex items-center gap-3.5 mb-4">
            <div className="w-10 h-10 bg-red-50 rounded-xl flex items-center justify-center flex-shrink-0">
              <File size={20} className="text-red-500" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-bold text-[#0F172A] truncate">{uploadedFile.name}</p>
              <p className="text-xs text-[#64748B]">{uploadedFile.size}</p>
            </div>
            {isUploaded && (
              <div className="text-green-500 animate-bounce">
                <CheckCircle size={22} />
              </div>
            )}
          </div>

          {isUploading && (
            <div className="space-y-2">
              <div className="flex justify-between text-xs text-[#64748B] font-semibold">
                <span>Parsing & uploading...</span>
                <span>{uploadProgress}%</span>
              </div>
              <div className="w-full h-2 bg-[#F1F5F9] rounded-full overflow-hidden">
                <div
                  className="h-full bg-[#2563EB] rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
            </div>
          )}

          {isUploaded && (
            <div className="flex flex-col sm:flex-row gap-3 mt-4">
              <Link
                href="/candidate/resume/analysis"
                className="flex-1 flex items-center justify-center gap-2 bg-[#2563EB] text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-[#1D4ED8] transition-colors cursor-pointer"
              >
                <Eye size={15} />
                Analyze Resume
              </Link>
              <Link
                href="/candidate/ats"
                className="flex-1 flex items-center justify-center gap-2 border border-[#E2E8F0] text-[#0F172A] py-2.5 rounded-xl text-sm font-semibold hover:bg-[#F8FAFC] transition-colors cursor-pointer"
              >
                <FileText size={15} />
                Check ATS Score
              </Link>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
