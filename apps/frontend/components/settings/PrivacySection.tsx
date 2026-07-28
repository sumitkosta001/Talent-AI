'use client';

import React from 'react';
import { PrivacySettings } from '@/types/settings';
import ToggleSetting from './ToggleSetting';

interface PrivacySectionProps {
  privacy?: PrivacySettings;
  onChange: (field: keyof PrivacySettings, value: any) => void;
}

export default function PrivacySection({ privacy, onChange }: PrivacySectionProps) {
  if (!privacy) return null;

  return (
    <div className="space-y-4 text-left">
      <div className="grid sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-bold text-[#475569] mb-1.5">Profile Discovery</label>
          <select
            value={privacy.profileVisibility}
            onChange={(e) => onChange('profileVisibility', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white cursor-pointer"
          >
            <option value="All">All Registered Users</option>
            <option value="Recruiters">Verified Recruiters</option>
            <option value="Connections">Connections Only</option>
            <option value="None">None (Only me)</option>
          </select>
        </div>

        <div>
          <label className="block text-xs font-bold text-[#475569] mb-1.5">Email Visibility</label>
          <select
            value={privacy.emailVisibility}
            onChange={(e) => onChange('emailVisibility', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white cursor-pointer"
          >
            <option value="All">All Users</option>
            <option value="Recruiters">Recruiters Only</option>
            <option value="None">Private (Hidden)</option>
          </select>
        </div>
      </div>

      <div className="border-t border-[#F1F5F9] pt-3 space-y-2">
        <ToggleSetting
          label="Search Engine Indexing"
          description="Allow public search index engine crawlers (Google, Bing) to index your profile."
          checked={privacy.searchEngineIndexing}
          onChange={(val) => onChange('searchEngineIndexing', val)}
        />
        <ToggleSetting
          label="Allow Company Invitations"
          description="Permit system matches to notify you about matching recruiter campaigns."
          checked={privacy.allowInvitations}
          onChange={(val) => onChange('allowInvitations', val)}
        />
        <ToggleSetting
          label="Allow AI Recommendations"
          description="Permit the TalentAI agent to match vacancies based on your parsed biography."
          checked={privacy.allowAiRecommendations}
          onChange={(val) => onChange('allowAiRecommendations', val)}
        />
        <ToggleSetting
          label="Allow Analytics Tracking"
          description="Contribute anonymous statistics regarding response metrics to build community salary reports."
          checked={privacy.allowAnalytics}
          onChange={(val) => onChange('allowAnalytics', val)}
        />
      </div>
    </div>
  );
}
