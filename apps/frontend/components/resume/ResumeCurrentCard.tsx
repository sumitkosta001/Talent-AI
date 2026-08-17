import React from 'react';
import { BackendResume } from '@/types/resume';
import ResumeStatusBadge from './ResumeStatusBadge';
import {
  FileText,
  Eye,
  Download,
  Trash2,
  Calendar,
  HardDrive,
  Sparkles,
  RefreshCw,
  AlertCircle,
} from 'lucide-react';

interface ResumeCurrentCardProps {
  resume: BackendResume | null;
  onPreview: (id: string, name: string) => void;
  onDownload: (id: string, name: string) => void;
  onDelete: (resume: BackendResume) => void;
  onRetry?: (id: string) => void;
  isActionLoading?: boolean;
}

export default function ResumeCurrentCard({
  resume,
  onPreview,
  onDownload,
  onDelete,
  onRetry,
  isActionLoading = false,
}: ResumeCurrentCardProps) {
  if (!resume) return null;

  const sizeKb = (resume.file_size_bytes || 0) / 1024;
  const sizeFormatted =
    sizeKb > 1024 ? `${(sizeKb / 1024).toFixed(1)} MB` : `${sizeKb.toFixed(1)} KB`;
  const isPdf = resume.original_filename.toLowerCase().endsWith('.pdf');
  const isFailed = resume.status === 'failed';

  const formattedDate = resume.uploaded_at
    ? new Date(resume.uploaded_at).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    : 'N/A';

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] shadow-sm overflow-hidden transition-all hover:shadow-md">
      {/* Header ribbon */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-3 text-white flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sparkles size={16} className="text-yellow-300 animate-pulse" />
          <span className="text-xs font-bold uppercase tracking-wider">Active Resume (Default)</span>
        </div>
        <span className="text-xs font-semibold bg-white/20 backdrop-blur-xs px-2.5 py-0.5 rounded-full">
          Version {resume.version}
        </span>
      </div>

      <div className="p-6">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          {/* File information */}
          <div className="flex items-start gap-4 min-w-0">
            <div
              className={`w-14 h-14 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-inner ${
                isPdf ? 'bg-red-50 text-red-600 border border-red-100' : 'bg-blue-50 text-blue-600 border border-blue-100'
              }`}
            >
              <FileText size={28} />
            </div>

            <div className="min-w-0 space-y-1.5">
              <div className="flex flex-wrap items-center gap-2">
                <h3 className="font-bold text-lg text-[#0F172A] truncate" title={resume.original_filename}>
                  {resume.original_filename}
                </h3>
                <ResumeStatusBadge status={resume.status} />
              </div>

              <div className="flex flex-wrap items-center gap-y-1 gap-x-4 text-xs text-[#64748B]">
                <span className="flex items-center gap-1">
                  <HardDrive size={13} className="text-[#94A3B8]" />
                  {sizeFormatted}
                </span>
                <span className="flex items-center gap-1">
                  <Calendar size={13} className="text-[#94A3B8]" />
                  Uploaded {formattedDate}
                </span>
              </div>
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex flex-wrap items-center gap-2.5 self-start lg:self-center">
            <button
              onClick={() => onPreview(resume.id, resume.original_filename)}
              disabled={isActionLoading}
              className="inline-flex items-center justify-center gap-2 bg-[#F8FAFC] hover:bg-[#F1F5F9] text-[#0F172A] border border-[#CBD5E1] px-4 py-2.5 rounded-xl text-xs font-semibold transition-all hover:border-[#94A3B8] cursor-pointer shadow-xs disabled:opacity-50"
            >
              <Eye size={14} className="text-[#2563EB]" />
              Preview
            </button>

            <button
              onClick={() => onDownload(resume.id, resume.original_filename)}
              disabled={isActionLoading}
              className="inline-flex items-center justify-center gap-2 bg-[#F8FAFC] hover:bg-[#F1F5F9] text-[#0F172A] border border-[#CBD5E1] px-4 py-2.5 rounded-xl text-xs font-semibold transition-all hover:border-[#94A3B8] cursor-pointer shadow-xs disabled:opacity-50"
            >
              <Download size={14} className="text-[#059669]" />
              Download
            </button>

            {isFailed && onRetry && (
              <button
                onClick={() => onRetry(resume.id)}
                disabled={isActionLoading}
                className="inline-flex items-center justify-center gap-2 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-300 px-4 py-2.5 rounded-xl text-xs font-semibold transition-all cursor-pointer shadow-xs disabled:opacity-50"
              >
                <RefreshCw size={14} className="text-amber-600" />
                Retry Processing
              </button>
            )}

            <button
              onClick={() => onDelete(resume)}
              disabled={isActionLoading}
              className="inline-flex items-center justify-center gap-2 bg-white hover:bg-red-50 text-red-600 border border-red-200 px-4 py-2.5 rounded-xl text-xs font-semibold transition-all hover:border-red-300 cursor-pointer shadow-xs disabled:opacity-50"
            >
              <Trash2 size={14} />
              Delete
            </button>
          </div>
        </div>

        {/* Failed reason banner if present */}
        {isFailed && resume.failure_reason && (
          <div className="mt-4 p-3 bg-red-50/70 border border-red-200 rounded-xl flex items-start gap-2.5 text-xs text-red-800">
            <AlertCircle size={15} className="text-red-500 mt-0.5 flex-shrink-0" />
            <div>
              <span className="font-bold">Failure details: </span>
              <span>{resume.failure_reason}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
