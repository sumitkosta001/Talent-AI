import React from 'react';
import { Resume } from '../../types/resume';
import ResumeSummary from './ResumeSummary';
import ExperienceCard from './ExperienceCard';
import ProjectCard from './ProjectCard';
import EducationCard from './EducationCard';
import CertificateCard from './CertificateCard';
import SkillSection from './SkillSection';
import ResumeCard from './ResumeCard';
import { Briefcase, FolderOpen, GraduationCap, Award, Code, Globe, Trophy } from 'lucide-react';

interface ResumeViewerProps {
  resume: Resume;
}

export default function ResumeViewer({ resume }: ResumeViewerProps) {
  const {
    summary,
    experience,
    projects,
    education,
    certificates,
    skills,
    languages,
    achievements,
  } = resume;

  return (
    <div className="grid lg:grid-cols-3 gap-6 animate-in fade-in duration-300">
      {/* Left side: Contact & Skills Info */}
      <div className="space-y-6">
        <ResumeCard resume={resume} />
        
        {/* Skills Card */}
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <Code size={18} className="text-[#2563EB]" />
            <h2 className="font-bold text-[#0F172A] text-base sm:text-lg">Skills Inventory</h2>
          </div>
          <SkillSection skills={skills} />
        </div>

        {/* Languages Card */}
        {languages && languages.length > 0 && (
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm">
            <div className="flex items-center gap-2 mb-3.5">
              <Globe size={18} className="text-[#2563EB]" />
              <h2 className="font-bold text-[#0F172A] text-base sm:text-lg">Languages</h2>
            </div>
            <div className="flex flex-wrap gap-2">
              {languages.map((lang) => (
                <span
                  key={lang}
                  className="text-xs font-semibold bg-[#F8FAFC] border border-[#E2E8F0] text-[#475569] px-3 py-1 rounded-full"
                >
                  {lang}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Right side: Professional Details */}
      <div className="lg:col-span-2 space-y-6">
        {/* Summary */}
        <ResumeSummary summary={summary} />

        {/* Work Experience */}
        {experience && experience.length > 0 && (
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <div className="flex items-center gap-2 pb-1 border-b border-[#E2E8F0]/60">
              <Briefcase size={18} className="text-[#2563EB]" />
              <h2 className="font-bold text-[#0F172A] text-base sm:text-lg">Work Experience</h2>
            </div>
            <div className="space-y-4">
              {experience.map((exp) => (
                <ExperienceCard key={exp.id} experience={exp} />
              ))}
            </div>
          </div>
        )}

        {/* Projects */}
        {projects && projects.length > 0 && (
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <div className="flex items-center gap-2 pb-1 border-b border-[#E2E8F0]/60">
              <FolderOpen size={18} className="text-[#2563EB]" />
              <h2 className="font-bold text-[#0F172A] text-base sm:text-lg">Projects</h2>
            </div>
            <div className="grid grid-cols-1 gap-4">
              {projects.map((proj) => (
                <ProjectCard key={proj.id} project={proj} />
              ))}
            </div>
          </div>
        )}

        {/* Education */}
        {education && education.length > 0 && (
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <div className="flex items-center gap-2 pb-1 border-b border-[#E2E8F0]/60">
              <GraduationCap size={18} className="text-[#2563EB]" />
              <h2 className="font-bold text-[#0F172A] text-base sm:text-lg">Education</h2>
            </div>
            <div className="space-y-3.5">
              {education.map((edu) => (
                <EducationCard key={edu.id} education={edu} />
              ))}
            </div>
          </div>
        )}

        {/* Certificates */}
        {certificates && certificates.length > 0 && (
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <div className="flex items-center gap-2 pb-1 border-b border-[#E2E8F0]/60">
              <Award size={18} className="text-[#2563EB]" />
              <h2 className="font-bold text-[#0F172A] text-base sm:text-lg">Certifications</h2>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {certificates.map((cert) => (
                <CertificateCard key={cert.id} certificate={cert} />
              ))}
            </div>
          </div>
        )}

        {/* Achievements */}
        {achievements && achievements.length > 0 && (
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <div className="flex items-center gap-2 pb-1 border-b border-[#E2E8F0]/60">
              <Trophy size={18} className="text-[#2563EB]" />
              <h2 className="font-bold text-[#0F172A] text-base sm:text-lg">Achievements</h2>
            </div>
            <ul className="space-y-3">
              {achievements.map((ach, idx) => (
                <li key={idx} className="flex gap-3 items-start text-xs sm:text-sm text-[#64748B]">
                  <div className="w-1.5 h-1.5 rounded-full bg-[#2563EB] mt-2 flex-shrink-0" />
                  <span className="leading-relaxed">{ach}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
