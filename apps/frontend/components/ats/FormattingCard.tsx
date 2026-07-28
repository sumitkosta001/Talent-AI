'use client';

import React from 'react';
import { AlignLeft, FileText, CheckCircle } from 'lucide-react';
import { FormattingScore } from '@/types/ats';

interface FormattingCardProps {
  formatting: FormattingScore;
}

export default function FormattingCard({ formatting }: FormattingCardProps) {
  const traits = [
    { label: 'Margins', value: formatting.margins },
    { label: 'Typography / Font', value: formatting.font },
    { label: 'Line Spacing', value: formatting.spacing },
    { label: 'Section Headings', value: formatting.headings },
    { label: 'Bullet Points', value: formatting.bulletPoints },
    { label: 'Text Alignment', value: formatting.alignment },
    { label: 'Tables Check', value: formatting.tables },
    { label: 'Columns Layout', value: formatting.columns },
    { label: 'Icon Spacers', value: formatting.icons },
    { label: 'Graphic Charts', value: formatting.graphics },
  ];

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-4">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center">
          <FileText size={20} />
        </div>
        <div>
          <h3 className="font-semibold text-[#0F172A]">Formatting & Layout</h3>
          <p className="text-xs text-[#64748B]">{formatting.atsCompatibility}</p>
        </div>
      </div>

      <div className="grid sm:grid-cols-2 gap-3.5 pt-2">
        {traits.map(({ label, value }) => (
          <div key={label} className="p-3 bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl flex items-center justify-between gap-2">
            <span className="text-xs font-semibold text-[#64748B]">{label}</span>
            <span className="text-xs font-bold text-[#0F172A] text-right">{value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
