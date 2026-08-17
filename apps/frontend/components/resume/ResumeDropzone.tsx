import React, { useState, useRef } from 'react';
import { Upload, Loader2, AlertTriangle, FileText, CheckCircle2 } from 'lucide-react';

interface ResumeDropzoneProps {
  onFileSelect: (file: File) => void;
  isUploading?: boolean;
  uploadProgress?: number;
  uploadedFile?: { name: string; size: string } | null;
}

export default function ResumeDropzone({
  onFileSelect,
  isUploading = false,
  uploadProgress = 0,
  uploadedFile = null,
}: ResumeDropzoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    if (!isUploading) setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const validateAndSelect = (file: File) => {
    setValidationError(null);

    const validExtensions = ['.pdf', '.docx'];
    const filename = file.name.toLowerCase();
    const hasValidExt = validExtensions.some((ext) => filename.endsWith(ext));

    if (!hasValidExt) {
      setValidationError('Only .PDF and .DOCX resume documents are supported.');
      return;
    }

    const maxSize = 10 * 1024 * 1024; // 10 MB
    if (file.size > maxSize) {
      setValidationError('File size exceeds the 10 MB maximum limit.');
      return;
    }

    if (file.size === 0) {
      setValidationError('The selected file is empty.');
      return;
    }

    onFileSelect(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (isUploading) return;
    const file = e.dataTransfer.files[0];
    if (file) {
      validateAndSelect(file);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (isUploading) return;
    const file = e.target.files?.[0];
    if (file) {
      validateAndSelect(file);
    }
    // Reset input so re-selecting same file triggers onChange
    if (e.target) e.target.value = '';
  };

  return (
    <div className="space-y-3">
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !isUploading && fileInputRef.current?.click()}
        className={`
          relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-300
          ${
            isDragging
              ? 'border-[#2563EB] bg-blue-50/80 scale-[0.99] ring-4 ring-blue-100'
              : isUploading
              ? 'border-blue-300 bg-blue-50/30 cursor-wait'
              : 'border-[#CBD5E1] bg-white hover:border-[#2563EB] hover:bg-[#F8FAFC]'
          }
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          onChange={handleFileChange}
          disabled={isUploading}
        />

        {isUploading ? (
          <div className="flex flex-col items-center gap-3 py-2">
            <div className="w-14 h-14 rounded-2xl bg-blue-100 text-blue-600 flex items-center justify-center">
              <Loader2 size={28} className="animate-spin" />
            </div>
            <div>
              <p className="font-bold text-[#0F172A] text-base">Uploading & Registering Resume...</p>
              <p className="text-xs text-[#64748B] mt-1">Transmitting document to secure storage</p>
            </div>
            {/* Progress bar */}
            <div className="w-full max-w-xs bg-slate-200 h-2 rounded-full overflow-hidden mt-1">
              <div
                className="bg-[#2563EB] h-full transition-all duration-300 rounded-full"
                style={{ width: `${Math.max(uploadProgress, 20)}%` }}
              />
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-3.5">
            <div
              className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-colors duration-200 ${
                isDragging ? 'bg-[#2563EB] text-white shadow-md' : 'bg-[#F1F5F9] text-[#475569]'
              }`}
            >
              <Upload size={26} />
            </div>

            <div>
              <p className="font-bold text-[#0F172A] text-base">
                {isDragging ? 'Drop your resume here' : 'Drag & drop your resume here'}
              </p>
              <p className="text-[#64748B] text-xs mt-1">
                or <span className="text-[#2563EB] font-bold underline">browse files</span> from your computer
              </p>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full border bg-red-50 text-red-700 border-red-200">
                PDF
              </span>
              <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full border bg-blue-50 text-blue-700 border-blue-200">
                DOCX
              </span>
              <span className="text-[11px] text-[#94A3B8] font-medium ml-1">Up to 10 MB</span>
            </div>
          </div>
        )}
      </div>

      {validationError && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-3 flex items-center gap-2.5 text-xs text-red-700 animate-in fade-in">
          <AlertTriangle size={16} className="text-red-500 flex-shrink-0" />
          <span>{validationError}</span>
        </div>
      )}
    </div>
  );
}
