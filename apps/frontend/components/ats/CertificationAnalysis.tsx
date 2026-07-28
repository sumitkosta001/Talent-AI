'use client';

import React from 'react';
import { Award, AlertCircle } from 'lucide-react';

interface CertificationAnalysisProps {
  suggestions?: string[];
}

export default function CertificationAnalysis({ suggestions = ['Add AWS Cloud Developer Associate to support cloud claims.'] }: CertificationAnalysisProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 rounded-xl bg-orange-50 text-orange-600 flex items-center justify-center flex-shrink-0">
          <Award size={20} />
        </div>
        <div>
          <h4 className="font-bold text-sm text-[#0F172A]">Professional Certifications</h4>
          <p className="text-xs text-[#64748B] font-medium mt-0.5">Industry-validated certifications</p>
        </div>
      </div>

      <div className="space-y-2">
        {suggestions.map((s, i) => (
          <div key={i} className="flex gap-2 p-3 bg-amber-50 border border-amber-100 rounded-xl text-xs text-amber-800">
            <AlertCircle size={14} className="text-amber-500 mt-0.5 flex-shrink-0" />
            <span>{s}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
