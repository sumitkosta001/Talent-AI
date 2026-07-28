import React from 'react';
import { Project } from '../../types/resume';
import { ExternalLink } from 'lucide-react';

const GithubIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    viewBox="0 0 24 24"
    width="16"
    height="16"
    stroke="currentColor"
    strokeWidth="2"
    fill="none"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...props}
  >
    <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22" />
  </svg>
);

interface ProjectCardProps {
  project: Project;
}

export default function ProjectCard({ project }: ProjectCardProps) {
  const { name, description, techStack, github, liveLink, duration } = project;

  return (
    <div className="bg-[#F8FAFC] rounded-xl border border-[#E2E8F0] p-4 hover:shadow-sm transition-all duration-200">
      <div className="flex items-center justify-between gap-3 mb-2">
        <h3 className="font-bold text-[#0F172A] text-sm sm:text-base">{name}</h3>
        <span className="text-xs text-[#94A3B8] font-medium">{duration}</span>
      </div>
      <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed mb-3">{description}</p>
      
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-2 border-t border-[#E2E8F0]/60">
        <div className="flex flex-wrap gap-1.5">
          {techStack.map((tech) => (
            <span
              key={tech}
              className="text-[10px] bg-white border border-[#E2E8F0] text-[#64748B] px-2 py-0.5 rounded-full font-medium"
            >
              {tech}
            </span>
          ))}
        </div>
        <div className="flex items-center gap-3">
          {github && (
            <a
              href={github}
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#64748B] hover:text-[#0F172A] transition-colors p-1"
              aria-label="View Source on GitHub"
            >
              <GithubIcon />
            </a>
          )}
          {liveLink && (
            <a
              href={liveLink}
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#64748B] hover:text-[#2563EB] transition-colors p-1"
              aria-label="View Live Deployment"
            >
              <ExternalLink size={16} />
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
