import React from 'react';
import { FileText, Award, Percent, Calendar } from 'lucide-react';

interface ResumeStatsProps {
  score: number;
  completion: number;
  status: string;
  lastUpdated: string;
}

export default function ResumeStats({ score, completion, status, lastUpdated }: ResumeStatsProps) {
  const stats = [
    {
      icon: Award,
      label: 'Resume Score',
      value: `${score}/100`,
      color: 'bg-violet-50 text-violet-600 border-violet-100',
      description: 'Excellent match rating',
    },
    {
      icon: Percent,
      label: 'Profile Completion',
      value: `${completion}%`,
      color: 'bg-[#2563EB]/5 text-[#2563EB] border-[#2563EB]/10',
      description: 'Missing sections impact score',
    },
    {
      icon: FileText,
      label: 'Resume Status',
      value: status,
      color: 'bg-emerald-50 text-emerald-600 border-emerald-100',
      description: 'Ready for job screening',
    },
    {
      icon: Calendar,
      label: 'Last Updated',
      value: lastUpdated,
      color: 'bg-amber-50 text-amber-600 border-amber-100',
      description: 'Keep resume fresh',
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map(({ icon: Icon, label, value, color, description }) => (
        <div
          key={label}
          className="bg-white rounded-2xl border border-[#E2E8F0] p-4 flex flex-col hover:shadow-md transition-shadow duration-200"
        >
          <div className={`w-9 h-9 rounded-xl flex items-center justify-center border mb-3 ${color}`}>
            <Icon size={16} />
          </div>
          <p className="text-2xl font-bold text-[#0F172A]">{value}</p>
          <p className="text-xs font-bold text-[#0F172A] mt-0.5">{label}</p>
          <p className="text-[10px] text-[#64748B] mt-0.5">{description}</p>
        </div>
      ))}
    </div>
  );
}
