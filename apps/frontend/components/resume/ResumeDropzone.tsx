import React, { useState, useRef } from 'react';
import { Upload } from 'lucide-react';

interface ResumeDropzoneProps {
  onFileSelect: (file: File) => void;
  isUploading?: boolean;
}

export default function ResumeDropzone({ onFileSelect, isUploading = false }: ResumeDropzoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    if (!isUploading) setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (isUploading) return;
    const file = e.dataTransfer.files[0];
    if (file && isValidFile(file)) {
      onFileSelect(file);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (isUploading) return;
    const file = e.target.files?.[0];
    if (file && isValidFile(file)) {
      onFileSelect(file);
    }
  };

  const isValidFile = (file: File) => {
    const validExtensions = ['.pdf', '.docx', '.doc'];
    const filename = file.name.toLowerCase();
    const isValidExt = validExtensions.some((ext) => filename.endsWith(ext));
    const isValidSize = file.size <= 10 * 1024 * 1024; // 10 MB limit
    return isValidExt && isValidSize;
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={() => !isUploading && fileInputRef.current?.click()}
      className={`
        relative border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-300
        ${
          isDragging
            ? 'border-[#2563EB] bg-blue-50/70 scale-[0.99]'
            : isUploading
            ? 'border-gray-200 bg-gray-50/50 cursor-not-allowed'
            : 'border-[#E2E8F0] hover:border-[#2563EB] hover:bg-[#F8FAFC]'
        }
      `}
    >
      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        accept=".pdf,.docx,.doc"
        onChange={handleFileChange}
        disabled={isUploading}
      />
      <div className="flex flex-col items-center gap-4">
        <div
          className={`w-16 h-16 rounded-2xl flex items-center justify-center transition-colors duration-200 ${
            isDragging ? 'bg-[#2563EB] text-white' : 'bg-[#F1F5F9] text-[#64748B]'
          }`}
        >
          <Upload size={28} />
        </div>
        <div>
          <p className="font-bold text-[#0F172A] text-lg">
            {isDragging ? 'Drop your resume here' : 'Drag & drop your resume'}
          </p>
          <p className="text-[#64748B] text-sm mt-1">
            or <span className="text-[#2563EB] font-bold">click to browse</span> from your device
          </p>
        </div>
        <div className="flex items-center gap-3">
          {[
            { label: 'PDF', color: 'bg-red-50 text-red-600 border-red-100' },
            { label: 'DOCX', color: 'bg-blue-50 text-blue-600 border-blue-100' },
            { label: 'DOC', color: 'bg-violet-50 text-violet-600 border-violet-100' },
          ].map(({ label, color }) => (
            <span
              key={label}
              className={`text-xs font-semibold px-3 py-0.5 rounded-full border ${color}`}
            >
              {label}
            </span>
          ))}
        </div>
        <p className="text-xs text-[#94A3B8]">Maximum file size: 10 MB</p>
      </div>
    </div>
  );
}
