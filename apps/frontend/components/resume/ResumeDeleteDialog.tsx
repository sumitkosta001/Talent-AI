import React, { useEffect } from 'react';
import { BackendResume } from '@/types/resume';
import { AlertTriangle, Trash2, X, Loader2 } from 'lucide-react';

interface ResumeDeleteDialogProps {
  isOpen: boolean;
  resume: BackendResume | null;
  isLoading: boolean;
  onClose: () => void;
  onConfirm: () => void;
}

export default function ResumeDeleteDialog({
  isOpen,
  resume,
  isLoading,
  onClose,
  onConfirm,
}: ResumeDeleteDialogProps) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && !isLoading) onClose();
    };
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, isLoading, onClose]);

  if (!isOpen || !resume) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="delete-dialog-title"
      className="fixed inset-0 bg-[#0F172A]/70 backdrop-blur-xs z-50 flex items-center justify-center p-4 transition-all duration-200 animate-in fade-in"
      onClick={() => !isLoading && onClose()}
    >
      <div
        className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-100 animate-in zoom-in-95 duration-200 space-y-5"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-2xl bg-red-50 text-red-600 flex items-center justify-center flex-shrink-0 border border-red-100">
            <AlertTriangle size={24} />
          </div>
          <div className="space-y-1">
            <h3 id="delete-dialog-title" className="font-bold text-[#0F172A] text-lg leading-tight">
              Delete Resume?
            </h3>
            <p className="text-xs text-[#64748B] leading-relaxed">
              Are you sure you want to delete <span className="font-bold text-[#0F172A]">v{resume.version} — {resume.original_filename}</span>?
            </p>
          </div>
        </div>

        {resume.is_current && (
          <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 leading-normal">
            <span className="font-bold">Note: </span>
            This is currently your active resume. Deleting it will automatically make your most recent previous version active.
          </div>
        )}

        <div className="flex items-center justify-end gap-3 pt-2">
          <button
            onClick={onClose}
            disabled={isLoading}
            className="px-4 py-2.5 rounded-xl text-xs font-semibold text-[#64748B] hover:bg-[#F1F5F9] transition-colors cursor-pointer disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            disabled={isLoading}
            className="inline-flex items-center justify-center gap-2 bg-red-600 hover:bg-red-700 text-white px-5 py-2.5 rounded-xl text-xs font-bold transition-colors cursor-pointer shadow-xs disabled:opacity-50"
          >
            {isLoading ? (
              <>
                <Loader2 size={14} className="animate-spin" />
                Deleting...
              </>
            ) : (
              <>
                <Trash2 size={14} />
                Delete Resume
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
