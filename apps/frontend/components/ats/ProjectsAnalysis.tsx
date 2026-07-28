'use client';

import React from 'react';
import { Layers, CheckCircle2, XCircle, AlertCircle } from 'lucide-react';
import { ProjectAnalysis as ProjectType } from '@/types/ats';

interface ProjectsAnalysisProps {
  projects: ProjectType;
}

export default function ProjectsAnalysis({ projects }: ProjectsAnalysisProps) {
  const flags = [
    { label: 'GitHub Repository', status: projects.hasGithub },
    { label: 'Live Deploy Link', status: projects.hasLiveDemo },
    { label: 'Project Documentation', status: projects.hasDocumentation },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center flex-shrink-0">
          <Layers size={20} />
        </div>
        <div>
          <h4 className="font-bold text-sm text-[#0F172A]">Project Complexity: {projects.complexity}</h4>
          <p className="text-xs text-[#64748B] font-medium mt-0.5">Innovation Score: {projects.innovationScore}/100</p>
        </div>
      </div>

      <div className="space-y-2">
        {flags.map(({ label, status }) => (
          <div key={label} className="flex items-center justify-between text-xs font-semibold py-1">
            <span className="text-[#64748B]">{label}</span>
            {status ? (
              <span className="flex items-center gap-1 text-green-600"><CheckCircle2 size={13} /> Found</span>
            ) : (
              <span className="flex items-center gap-1 text-red-500"><XCircle size={13} /> Missing</span>
            )}
          </div>
        ))}
      </div>

      {projects.suggestions.map((s, i) => (
        <div key={i} className="flex gap-2 p-3 bg-amber-50 border border-amber-100 rounded-xl text-xs text-amber-800">
          <AlertCircle size={14} className="text-amber-500 mt-0.5 flex-shrink-0" />
          <span>{s}</span>
        </div>
      ))}
    </div>
  );
}
