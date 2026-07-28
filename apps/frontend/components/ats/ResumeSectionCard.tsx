'use client';

import React, { useState } from 'react';
import { SectionAnalysis, ATSResult } from '@/types/ats';
import SkillAnalysis from './SkillAnalysis';
import EducationAnalysis from './EducationAnalysis';
import ExperienceAnalysis from './ExperienceAnalysis';
import ProjectsAnalysis from './ProjectsAnalysis';
import AchievementsAnalysis from './AchievementsAnalysis';
import CertificationAnalysis from './CertificationAnalysis';

interface ResumeSectionCardProps {
  sections: SectionAnalysis[];
  result: ATSResult;
}

export default function ResumeSectionCard({ sections, result }: ResumeSectionCardProps) {
  const [activeTab, setActiveTab] = useState<string>('Skills');

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'excellent': return 'bg-green-50 text-green-700 border-green-200';
      case 'good': return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'average': return 'bg-amber-50 text-amber-700 border-amber-200';
      default: return 'bg-red-50 text-red-700 border-red-200';
    }
  };

  const renderSectionContent = () => {
    switch (activeTab) {
      case 'Skills':
        return <SkillAnalysis skills={result.skills} />;
      case 'Education':
        return <EducationAnalysis education={result.education} />;
      case 'Experience':
        return <ExperienceAnalysis experience={result.experience} />;
      case 'Projects':
        return <ProjectsAnalysis projects={result.projects} />;
      case 'Achievements':
        return <AchievementsAnalysis />;
      case 'Certifications':
        return <CertificationAnalysis suggestions={result.education.suggestions} />;
      default:
        return (
          <p className="text-sm text-[#64748B] leading-relaxed">
            {sections.find(s => s.sectionName === activeTab)?.suggestion || 'Analysis details are not available for this section.'}
          </p>
        );
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-6">
      <div>
        <h2 className="font-semibold text-lg text-[#0F172A]">Resume Section Analysis</h2>
        <p className="text-xs text-[#64748B] mt-0.5">Evaluation of structural sections of the parsed resume profile.</p>
      </div>

      <div className="flex flex-col md:flex-row gap-6">
        {/* Left Section List */}
        <div className="md:w-1/3 flex flex-row md:flex-col gap-1.5 overflow-x-auto pb-2 md:pb-0 md:border-r border-[#E2E8F0] md:pr-4">
          {sections.map(({ sectionName, score, status }) => (
            <button
              key={sectionName}
              onClick={() => setActiveTab(sectionName)}
              className={`flex items-center justify-between gap-3 text-left px-3.5 py-2.5 rounded-xl text-sm font-semibold transition-all cursor-pointer whitespace-nowrap md:whitespace-normal w-full ${
                activeTab === sectionName
                  ? 'bg-blue-50 text-[#2563EB]'
                  : 'text-[#64748B] hover:bg-[#F8FAFC]'
              }`}
            >
              <span>{sectionName}</span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getStatusColor(status)}`}>
                {score}%
              </span>
            </button>
          ))}
        </div>

        {/* Right Content Area */}
        <div className="flex-1 min-w-0">
          <div className="border-b border-[#F1F5F9] pb-4 mb-4 flex items-center justify-between">
            <h3 className="font-bold text-[#0F172A] text-base">{activeTab} Details</h3>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full border ${
              getStatusColor(sections.find(s => s.sectionName === activeTab)?.status || 'good')
            }`}>
              {sections.find(s => s.sectionName === activeTab)?.status}
            </span>
          </div>
          <div className="animate-in fade-in duration-300">
            {renderSectionContent()}
          </div>
        </div>
      </div>
    </div>
  );
}
