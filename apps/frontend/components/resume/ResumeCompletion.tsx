import React from 'react';
import { CheckCircle, AlertCircle, Plus } from 'lucide-react';
import ResumeProgress from './ResumeProgress';

interface ResumeCompletionProps {
  completionPercentage: number;
  missingSections: string[];
  suggestions: string[];
}

export default function ResumeCompletion({
  completionPercentage,
  missingSections,
  suggestions,
}: ResumeCompletionProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-6">
      <div className="flex flex-col sm:flex-row items-center gap-6 pb-5 border-b border-[#E2E8F0]/60">
        <div className="flex-shrink-0">
          <ResumeProgress percentage={completionPercentage} type="circle" size={110} strokeWidth={8} />
        </div>
        <div className="flex-1 text-center sm:text-left space-y-1">
          <h3 className="font-bold text-[#0F172A] text-base sm:text-lg">Optimize Your Profile</h3>
          <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed">
            Completing these sections increases your likelihood of matching candidate screens by up to 40%.
          </p>
        </div>
      </div>

      {missingSections.length > 0 && (
        <div>
          <h4 className="text-xs font-bold text-[#EF4444] uppercase tracking-wider mb-3 flex items-center gap-1.5">
            <AlertCircle size={14} /> Missing Resume Sections ({missingSections.length})
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {missingSections.map((sec) => (
              <div
                key={sec}
                className="flex items-center justify-between p-3 bg-red-50/40 border border-red-100 rounded-xl"
              >
                <span className="text-xs sm:text-sm font-semibold text-red-800">{sec}</span>
                <button
                  className="p-1 bg-white border border-red-200 text-red-600 rounded-lg hover:bg-red-50 transition-colors flex items-center justify-center cursor-pointer"
                  title={`Add ${sec}`}
                >
                  <Plus size={13} />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {suggestions.length > 0 && (
        <div className="pt-2">
          <h4 className="text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-3 flex items-center gap-1.5">
            <CheckCircle size={14} /> Optimization Suggestions
          </h4>
          <ul className="space-y-2.5">
            {suggestions.map((sug, idx) => (
              <li key={idx} className="flex gap-2.5 items-start text-xs sm:text-sm text-[#64748B]">
                <div className="w-1.5 h-1.5 rounded-full bg-[#2563EB] mt-2 flex-shrink-0" />
                <span className="leading-relaxed">{sug}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
