import { Mail, Phone, MapPin, Globe, User } from 'lucide-react';
import { Resume } from '../../types/resume';

const GithubIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    viewBox="0 0 24 24"
    width="14"
    height="14"
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

const LinkedinIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    viewBox="0 0 24 24"
    width="14"
    height="14"
    stroke="currentColor"
    strokeWidth="2"
    fill="none"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...props}
  >
    <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z" />
    <rect x="2" y="9" width="4" height="12" />
    <circle cx="4" cy="4" r="2" />
  </svg>
);

interface ResumeCardProps {
  resume: Resume;
}

export default function ResumeCard({ resume }: ResumeCardProps) {
  const {
    candidateName,
    email,
    phone,
    location,
    website,
    github,
    linkedin,
  } = resume;

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-5">
      <div className="flex items-center gap-3.5 pb-4 border-b border-[#E2E8F0]/60">
        <div className="w-12 h-12 bg-blue-50 text-[#2563EB] rounded-2xl flex items-center justify-center">
          <User size={24} />
        </div>
        <div>
          <h2 className="font-bold text-[#0F172A] text-lg leading-snug">{candidateName}</h2>
          <p className="text-xs text-[#64748B] flex items-center gap-1 mt-0.5">
            <MapPin size={12} />
            {location}
          </p>
        </div>
      </div>

      <div className="space-y-3 text-xs sm:text-sm">
        <div className="flex items-center gap-2.5 text-[#64748B]">
          <Mail size={16} className="text-[#94A3B8]" />
          <a href={`mailto:${email}`} className="hover:text-[#2563EB] font-medium transition-colors truncate">
            {email}
          </a>
        </div>
        <div className="flex items-center gap-2.5 text-[#64748B]">
          <Phone size={16} className="text-[#94A3B8]" />
          <span className="font-medium">{phone}</span>
        </div>
        {website && (
          <div className="flex items-center gap-2.5 text-[#64748B]">
            <Globe size={16} className="text-[#94A3B8]" />
            <a
              href={website}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-[#2563EB] font-medium transition-colors truncate"
            >
              {website.replace(/(^\w+:|^)\/\//, '')}
            </a>
          </div>
        )}
      </div>

      <div className="flex items-center gap-2 pt-4 border-t border-[#E2E8F0]/60">
        {github && (
          <a
            href={github}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 inline-flex items-center justify-center gap-1.5 py-2 px-3 border border-[#E2E8F0] rounded-xl text-xs font-semibold text-[#64748B] hover:text-[#0F172A] hover:bg-[#F8FAFC] transition-colors"
          >
            <GithubIcon />
            GitHub
          </a>
        )}
        {linkedin && (
          <a
            href={linkedin}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 inline-flex items-center justify-center gap-1.5 py-2 px-3 border border-[#E2E8F0] rounded-xl text-xs font-semibold text-[#64748B] hover:text-[#2563EB] hover:bg-[#F8FAFC] transition-colors"
          >
            <LinkedinIcon />
            LinkedIn
          </a>
        )}
      </div>
    </div>
  );
}
