'use client';

import React from 'react';
import { ResumeVisibility } from '@/types/settings';
import ToggleSetting from './ToggleSetting';

interface ResumeVisibilitySectionProps {
  resume?: ResumeVisibility;
  onChange: (field: keyof ResumeVisibility, value: any) => void;
}

export default function ResumeVisibilitySection({ resume, onChange }: ResumeVisibilitySectionProps) {
  if (!resume) return null;

  return (
    <div className="space-y-4 text-left">
      <div>
        <label className="block text-xs font-bold text-[#475569] mb-1.5">Resume Search Visibility Status</label>
        <select
          value={resume.status}
          onChange={(e) => onChange('status', e.target.value)}
          className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white cursor-pointer"
        >
          <option value="Public">Public (Any registered company can find you)</option>
          <option value="Recruiters Only">Recruiters Only (Only verified staffing roles see you)</option>
          <option value="Private">Private (Invisible on recruiter searches)</option>
        </select>
        <p className="text-[10px] text-[#64748B] mt-1.5 leading-relaxed">
          Public resumes receive up to 5x more company interview invitations. Private resumes can only be submitted to jobs manually.
        </p>
      </div>

      <div className="border-t border-[#F1F5F9] pt-3 space-y-2">
        <ToggleSetting
          label="Hide Contact Information"
          description="Remove email and phone number details from the parsed search index until you apply."
          checked={resume.hideContactInfo}
          onChange={(val) => onChange('hideContactInfo', val)}
        />
        <ToggleSetting
          label="Allow Resume Download"
          description="Let matched companies download a PDF copy of your parsed profile resume."
          checked={resume.allowDownload}
          onChange={(val) => onChange('allowDownload', val)}
        />
        <ToggleSetting
          label="Allow Resume Search"
          description="Permit system index algorithms to rank your resume profile match score."
          checked={resume.allowSearch}
          onChange={(val) => onChange('allowSearch', val)}
        />
        <ToggleSetting
          label="Allow Recruiter Contact"
          description="Permit recruiters to send messages directly to your dashboard alerts."
          checked={resume.allowContact}
          onChange={(val) => onChange('allowContact', val)}
        />
      </div>
    </div>
  );
}
