'use client';

import React from 'react';
import { CompanyGalleryImage } from '@/types/companyGallery';

interface CompanyGalleryProps {
  gallery: CompanyGalleryImage[];
}

export default function CompanyGallery({ gallery }: CompanyGalleryProps) {
  return (
    <div className="space-y-5 text-left text-[#0F172A]">
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm">
        <h3 className="font-bold text-sm sm:text-base mb-1">HQ Campus Gallery</h3>
        <p className="text-xs text-[#64748B] font-semibold">Workspace environments, meeting lounges, and campus environments.</p>
      </div>

      {gallery.length === 0 ? (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-8 text-center text-xs text-slate-500 font-semibold shadow-sm">
          No office gallery images available.
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
          {gallery.map((img) => (
            <div key={img.id} className="bg-white rounded-2xl border border-[#E2E8F0] p-2.5 shadow-sm space-y-2">
              <img
                src={img.url}
                alt={img.caption}
                className="w-full h-44 object-cover rounded-xl border border-slate-100 hover:scale-[1.01] transition-transform duration-150"
              />
              <p className="text-[10px] text-slate-500 font-bold px-1.5">{img.caption}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
