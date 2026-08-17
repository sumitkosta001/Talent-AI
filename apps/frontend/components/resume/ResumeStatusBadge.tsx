import React from 'react';
import { ResumeStatus } from '@/types/resume';
import { Loader2, CheckCircle2, AlertTriangle, UploadCloud } from 'lucide-react';

interface ResumeStatusBadgeProps {
  status: ResumeStatus | string;
  className?: string;
  showIcon?: boolean;
}

export default function ResumeStatusBadge({
  status,
  className = '',
  showIcon = true,
}: ResumeStatusBadgeProps) {
  const normalized = status.toLowerCase() as ResumeStatus;

  switch (normalized) {
    case 'processed':
      return (
        <span
          className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 ${className}`}
        >
          {showIcon && <CheckCircle2 size={12} className="text-emerald-600" />}
          Processed
        </span>
      );
    case 'processing':
      return (
        <span
          className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200 ${className}`}
        >
          {showIcon && <Loader2 size={12} className="animate-spin text-amber-600" />}
          Processing...
        </span>
      );
    case 'failed':
      return (
        <span
          className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200 ${className}`}
        >
          {showIcon && <AlertTriangle size={12} className="text-rose-600" />}
          Failed
        </span>
      );
    case 'uploaded':
    default:
      return (
        <span
          className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-sky-50 text-sky-700 border border-sky-200 ${className}`}
        >
          {showIcon && <UploadCloud size={12} className="text-sky-600" />}
          Uploaded
        </span>
      );
  }
}
