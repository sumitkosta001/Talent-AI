'use client';

import React from 'react';
import { useResume } from '@/hooks/useResume';
import { FileText, Download, AlertCircle, Bot, Loader2 } from 'lucide-react';

export default function ResumeSection() {
  const { resume, loading } = useResume();

  if (loading) {
    return (
      <div className="flex justify-center p-8">
        <Loader2 className="animate-spin text-blue-600" size={24} />
      </div>
    );
  }

  if (!resume) {
    return (
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-8 text-center text-xs text-[#64748B] font-semibold shadow-sm">
        No primary resume file uploaded. Please upload a PDF in the Resume module.
      </div>
    );
  }

  const handleDownload = () => {
    alert(`Downloading resume document: ${resume.name}`);
  };

  return (
    <div className="space-y-6 text-[#0F172A] text-left">
      {/* Resume Card Details */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4">
        <h3 className="font-bold text-sm sm:text-base">Primary Resume</h3>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 border border-[#F1F5F9] bg-[#F8FAFC]/50 rounded-xl">
          <div className="flex items-start gap-3">
            <div className="p-2.5 bg-blue-50 text-blue-600 rounded-xl flex-shrink-0">
              <FileText size={20} />
            </div>
            <div className="text-xs font-semibold">
              <h4 className="font-bold text-[#0F172A] text-sm leading-normal">{resume.name}</h4>
              <p className="text-[#64748B] mt-0.5">Version: {resume.version} · Uploaded: {resume.uploadDate}</p>
            </div>
          </div>

          <button
            onClick={handleDownload}
            className="bg-white border border-[#E2E8F0] hover:bg-[#F8FAFC] text-slate-700 font-bold text-xs px-3.5 py-2 rounded-xl transition-all cursor-pointer inline-flex items-center gap-1.5 self-end sm:self-center"
          >
            <Download size={14} /> Download PDF
          </button>
        </div>
      </div>

      {/* ATS score overview */}
      {resume.atsScore && (
        <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-3">
          <h4 className="font-bold text-sm text-[#0F172A] flex items-center gap-1.5">
            <Bot size={16} className="text-purple-600 animate-pulse" />
            AI Resume Parsing Score
          </h4>
          <div className="flex flex-col sm:flex-row sm:items-center gap-4">
            <div className="text-center bg-[#F8FAFC] border border-[#E2E8F0] px-5 py-3 rounded-2xl flex-shrink-0 w-28 mx-auto sm:mx-0">
              <span className="text-2xl font-black text-[#0F172A]">{resume.atsScore}%</span>
              <p className="text-[8px] text-[#64748B] font-bold mt-0.5 uppercase tracking-wider">ATS Score</p>
            </div>
            <div className="text-xs text-slate-500 font-semibold space-y-1.5">
              <p className="leading-relaxed text-slate-600">
                Your resume keywords matches represent a high alignment rate of **87%** with core SDE roles.
              </p>
              <div className="flex items-start gap-1 text-[11px] text-[#64748B]">
                <AlertCircle size={13} className="text-blue-500 flex-shrink-0 mt-0.5" />
                <p>To exceed 90%, integrate keywords like System Operations and access Management.</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
