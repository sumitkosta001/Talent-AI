import React from 'react';
import { BackendResume } from '@/types/resume';
import ResumeStatusBadge from './ResumeStatusBadge';
import {
  FileText,
  Eye,
  Download,
  Trash2,
  RotateCcw,
  RefreshCw,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
  AlertCircle,
  Loader2,
  CheckCircle,
  Play,
} from 'lucide-react';

interface ResumeListProps {
  resumes: BackendResume[];
  pagination: {
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
    hasNext: boolean;
    hasPrevious: boolean;
  };
  sortBy: string;
  sortOrder: 'asc' | 'desc';
  actionLoading: { [id: string]: string };
  onPageChange: (page: number) => void;
  onSortChange: (field: string, order: 'asc' | 'desc') => void;
  onPreview: (id: string, name: string) => void;
  onDownload: (id: string, name: string) => void;
  onRestore: (resume: BackendResume) => void;
  onDelete: (resume: BackendResume) => void;
  onRetry: (id: string) => void;
  onProcess?: (id: string) => void;
}

export default function ResumeList({
  resumes,
  pagination,
  sortBy,
  sortOrder,
  actionLoading,
  onPageChange,
  onSortChange,
  onPreview,
  onDownload,
  onRestore,
  onDelete,
  onRetry,
  onProcess,
}: ResumeListProps) {
  const handleSortSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    const [field, order] = val.split(':');
    onSortChange(field, order as 'asc' | 'desc');
  };

  const currentSortVal = `${sortBy}:${sortOrder}`;

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] shadow-sm overflow-hidden space-y-0">
      {/* Table Header Controls */}
      <div className="p-5 border-b border-[#E2E8F0] flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-[#F8FAFC]">
        <div>
          <h3 className="font-bold text-[#0F172A] text-base">Version History & All Uploads</h3>
          <p className="text-xs text-[#64748B] mt-0.5">
            Showing {resumes.length} of {pagination.total} total documents
          </p>
        </div>

        {/* Sort selector */}
        <div className="flex items-center gap-2">
          <label htmlFor="sort-select" className="text-xs font-semibold text-[#64748B] flex items-center gap-1">
            <ArrowUpDown size={13} />
            Sort:
          </label>
          <select
            id="sort-select"
            value={currentSortVal}
            onChange={handleSortSelect}
            className="bg-white border border-[#CBD5E1] text-xs font-semibold rounded-xl px-3 py-1.5 text-[#0F172A] focus:outline-hidden focus:ring-2 focus:ring-[#2563EB] cursor-pointer"
          >
            <option value="uploaded_at:desc">Newest First</option>
            <option value="uploaded_at:asc">Oldest First</option>
            <option value="file_size_bytes:desc">File Size (Largest)</option>
            <option value="file_size_bytes:asc">File Size (Smallest)</option>
            <option value="status:asc">Status</option>
          </select>
        </div>
      </div>

      {/* Desktop / Tablet Table */}
      <div className="hidden md:block overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-[#E2E8F0] bg-[#FAFAFA] text-[11px] font-bold text-[#64748B] uppercase tracking-wider">
              <th className="py-3 px-5">Version</th>
              <th className="py-3 px-5">Document</th>
              <th className="py-3 px-5">Size</th>
              <th className="py-3 px-5">Uploaded</th>
              <th className="py-3 px-5">Status</th>
              <th className="py-3 px-5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#F1F5F9] text-xs">
            {resumes.map((item) => {
              const sizeKb = (item.file_size_bytes || 0) / 1024;
              const sizeStr = sizeKb > 1024 ? `${(sizeKb / 1024).toFixed(1)} MB` : `${sizeKb.toFixed(1)} KB`;
              const isPdf = item.original_filename.toLowerCase().endsWith('.pdf');
              const isCurrent = item.is_current;
              const currentAction = actionLoading[item.id];
              const formattedDate = item.uploaded_at
                ? new Date(item.uploaded_at).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric',
                  })
                : 'N/A';

              return (
                <tr
                  key={item.id}
                  className={`hover:bg-[#F8FAFC] transition-colors ${
                    isCurrent ? 'bg-blue-50/30' : ''
                  }`}
                >
                  {/* Version Column */}
                  <td className="py-3.5 px-5 font-bold text-[#0F172A] whitespace-nowrap">
                    <div className="flex items-center gap-1.5">
                      <span className="bg-slate-100 text-slate-700 font-bold px-2 py-0.5 rounded-md border border-slate-200">
                        v{item.version}
                      </span>
                      {isCurrent && (
                        <span className="text-[10px] font-bold uppercase bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">
                          Current
                        </span>
                      )}
                    </div>
                  </td>

                  {/* Document Column */}
                  <td className="py-3.5 px-5">
                    <div className="flex items-center gap-2.5 max-w-xs">
                      <div
                        className={`w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 ${
                          isPdf ? 'bg-red-50 text-red-600' : 'bg-blue-50 text-blue-600'
                        }`}
                      >
                        <FileText size={15} />
                      </div>
                      <div className="min-w-0">
                        <p className="font-semibold text-[#0F172A] truncate" title={item.original_filename}>
                          {item.original_filename}
                        </p>
                        {item.failure_reason && item.status === 'failed' && (
                          <p className="text-[10px] text-red-600 truncate flex items-center gap-1 mt-0.5" title={item.failure_reason}>
                            <AlertCircle size={10} />
                            {item.failure_reason}
                          </p>
                        )}
                      </div>
                    </div>
                  </td>

                  {/* Size */}
                  <td className="py-3.5 px-5 text-[#64748B] whitespace-nowrap">{sizeStr}</td>

                  {/* Date */}
                  <td className="py-3.5 px-5 text-[#64748B] whitespace-nowrap">{formattedDate}</td>

                  {/* Status */}
                  <td className="py-3.5 px-5 whitespace-nowrap">
                    <ResumeStatusBadge status={item.status} />
                  </td>

                  {/* Actions */}
                  <td className="py-3.5 px-5 text-right whitespace-nowrap">
                    <div className="inline-flex items-center gap-1">
                      {/* Preview Button */}
                      <button
                        onClick={() => onPreview(item.id, item.original_filename)}
                        className="p-1.5 text-[#64748B] hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
                        title="Preview Document"
                        disabled={!!currentAction}
                      >
                        <Eye size={15} />
                      </button>

                      {/* Download Button */}
                      <button
                        onClick={() => onDownload(item.id, item.original_filename)}
                        className="p-1.5 text-[#64748B] hover:text-[#059669] hover:bg-emerald-50 rounded-lg transition-colors cursor-pointer"
                        title="Download Document"
                        disabled={!!currentAction}
                      >
                        <Download size={15} />
                      </button>

                      {/* Process button (if uploaded state) */}
                      {item.status === 'uploaded' && onProcess && (
                        <button
                          onClick={() => onProcess(item.id)}
                          className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
                          title="Trigger Processing"
                          disabled={!!currentAction}
                        >
                          {currentAction === 'process' ? <Loader2 size={15} className="animate-spin" /> : <Play size={15} />}
                        </button>
                      )}

                      {/* Retry Button (if failed) */}
                      {item.status === 'failed' && (
                        <button
                          onClick={() => onRetry(item.id)}
                          className="p-1.5 text-amber-600 hover:bg-amber-50 rounded-lg transition-colors cursor-pointer"
                          title="Retry Processing"
                          disabled={!!currentAction}
                        >
                          {currentAction === 'retry' ? <Loader2 size={15} className="animate-spin" /> : <RefreshCw size={15} />}
                        </button>
                      )}

                      {/* Restore Button (if not current) */}
                      {!isCurrent && (
                        <button
                          onClick={() => onRestore(item)}
                          className="p-1.5 text-[#475569] hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
                          title="Make this version active"
                          disabled={!!currentAction}
                        >
                          {currentAction === 'restore' ? <Loader2 size={15} className="animate-spin" /> : <RotateCcw size={15} />}
                        </button>
                      )}

                      {/* Delete Button */}
                      <button
                        onClick={() => onDelete(item)}
                        className="p-1.5 text-[#64748B] hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
                        title="Delete Resume"
                        disabled={!!currentAction}
                      >
                        {currentAction === 'delete' ? <Loader2 size={15} className="animate-spin text-red-600" /> : <Trash2 size={15} />}
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Mobile Stacked Card View */}
      <div className="block md:hidden divide-y divide-[#F1F5F9]">
        {resumes.map((item) => {
          const sizeKb = (item.file_size_bytes || 0) / 1024;
          const sizeStr = sizeKb > 1024 ? `${(sizeKb / 1024).toFixed(1)} MB` : `${sizeKb.toFixed(1)} KB`;
          const isCurrent = item.is_current;
          const currentAction = actionLoading[item.id];

          return (
            <div key={item.id} className={`p-4 space-y-3 ${isCurrent ? 'bg-blue-50/20' : ''}`}>
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="bg-slate-100 text-slate-700 font-bold px-2 py-0.5 rounded-md text-xs border border-slate-200">
                    v{item.version}
                  </span>
                  <p className="font-bold text-sm text-[#0F172A] truncate">{item.original_filename}</p>
                </div>
                {isCurrent && (
                  <span className="text-[9px] font-bold uppercase bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full flex-shrink-0">
                    Current
                  </span>
                )}
              </div>

              <div className="flex items-center justify-between text-xs text-[#64748B]">
                <span>{sizeStr}</span>
                <ResumeStatusBadge status={item.status} />
              </div>

              {item.failure_reason && item.status === 'failed' && (
                <div className="text-xs text-red-600 bg-red-50 p-2 rounded-lg">
                  {item.failure_reason}
                </div>
              )}

              {/* Action row on mobile */}
              <div className="flex items-center justify-end gap-1 pt-1 border-t border-slate-100">
                <button
                  onClick={() => onPreview(item.id, item.original_filename)}
                  className="px-2.5 py-1.5 text-xs text-[#0F172A] bg-slate-100 rounded-lg flex items-center gap-1 font-semibold"
                >
                  <Eye size={12} /> Preview
                </button>
                <button
                  onClick={() => onDownload(item.id, item.original_filename)}
                  className="px-2.5 py-1.5 text-xs text-[#0F172A] bg-slate-100 rounded-lg flex items-center gap-1 font-semibold"
                >
                  <Download size={12} /> Download
                </button>
                {item.status === 'failed' && (
                  <button
                    onClick={() => onRetry(item.id)}
                    className="px-2.5 py-1.5 text-xs text-amber-700 bg-amber-50 rounded-lg flex items-center gap-1 font-semibold"
                  >
                    <RefreshCw size={12} /> Retry
                  </button>
                )}
                {!isCurrent && (
                  <button
                    onClick={() => onRestore(item)}
                    className="px-2.5 py-1.5 text-xs text-blue-700 bg-blue-50 rounded-lg flex items-center gap-1 font-semibold"
                  >
                    <RotateCcw size={12} /> Restore
                  </button>
                )}
                <button
                  onClick={() => onDelete(item)}
                  className="p-1.5 text-red-600 bg-red-50 rounded-lg"
                  title="Delete"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Pagination Footer */}
      {pagination.totalPages > 1 && (
        <div className="p-4 border-t border-[#E2E8F0] flex items-center justify-between bg-[#F8FAFC]">
          <span className="text-xs text-[#64748B] font-semibold">
            Page {pagination.page} of {pagination.totalPages}
          </span>

          <div className="flex items-center gap-1.5">
            <button
              onClick={() => onPageChange(pagination.page - 1)}
              disabled={!pagination.hasPrevious}
              className="p-1.5 rounded-lg border border-[#CBD5E1] bg-white text-[#0F172A] hover:bg-[#F1F5F9] disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
              title="Previous Page"
            >
              <ChevronLeft size={16} />
            </button>
            <button
              onClick={() => onPageChange(pagination.page + 1)}
              disabled={!pagination.hasNext}
              className="p-1.5 rounded-lg border border-[#CBD5E1] bg-white text-[#0F172A] hover:bg-[#F1F5F9] disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
              title="Next Page"
            >
              <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
