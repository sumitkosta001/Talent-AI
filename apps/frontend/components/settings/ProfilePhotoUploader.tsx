'use client';

import React, { useState } from 'react';
import { Camera, RefreshCw, Trash2 } from 'lucide-react';

interface ProfilePhotoUploaderProps {
  initialPic?: string;
  onUpdate: (pic: string) => void;
}

export default function ProfilePhotoUploader({ initialPic, onUpdate }: ProfilePhotoUploaderProps) {
  const [preview, setPreview] = useState<string | null>(initialPic || null);

  const handleUpload = () => {
    // Mock upload simulation
    const mockImages = ['AJ', 'Sarah', 'Alex', 'John'];
    const chosen = mockImages[Math.floor(Math.random() * mockImages.length)];
    setPreview(chosen);
    onUpdate(chosen);
    alert('Simulated profile picture uploaded successfully!');
  };

  const handleRemove = () => {
    setPreview(null);
    onUpdate('');
  };

  return (
    <div className="flex flex-col sm:flex-row items-center gap-4 text-left border-b border-[#F1F5F9] pb-5">
      <div className="w-16 h-16 rounded-full bg-[#2563EB] text-white font-black text-lg flex items-center justify-center border shadow-sm flex-shrink-0">
        {preview ? preview.slice(0, 2).toUpperCase() : 'AJ'}
      </div>
      
      <div className="space-y-1.5 text-center sm:text-left">
        <h4 className="font-bold text-xs sm:text-sm text-[#0F172A]">Profile Avatar Photo</h4>
        <p className="text-[10px] sm:text-xs text-[#64748B] leading-relaxed">
          Supports PNG, JPG, or GIF. Max filesize limit 2MB.
        </p>

        <div className="flex items-center gap-2 pt-1 justify-center sm:justify-start">
          <button
            type="button"
            onClick={handleUpload}
            className="inline-flex items-center gap-1.5 bg-[#2563EB] hover:bg-[#1D4ED8] text-white px-3 py-1.5 rounded-xl text-[10px] sm:text-xs font-semibold cursor-pointer transition-colors"
          >
            <Camera size={12} />
            Upload Photo
          </button>
          {preview && (
            <button
              type="button"
              onClick={handleRemove}
              className="inline-flex items-center gap-1.5 bg-red-50 hover:bg-red-100 text-red-600 px-3 py-1.5 rounded-xl text-[10px] sm:text-xs font-semibold cursor-pointer transition-colors border border-red-100"
            >
              <Trash2 size={12} />
              Remove
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
