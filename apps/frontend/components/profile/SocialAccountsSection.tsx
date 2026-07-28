'use client';

import React, { useState } from 'react';
import { useProfile } from '@/hooks/useProfile';
import { User, Code, Globe, Cpu, Save } from 'lucide-react';

export default function SocialAccountsSection() {
  const { profile, updateProfile } = useProfile();

  const [linkedin, setLinkedin] = useState(profile?.portfolioUrl || 'https://linkedin.com/in/alex-johnson');
  const [github, setGithub] = useState(profile?.personalWebsite || 'https://github.com/alexjohnson');
  const [leetcode, setLeetcode] = useState('https://leetcode.com/alexjohnson');
  const [x, setX] = useState('https://twitter.com/alexjohnson');

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    const urlPattern = /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([\/\w .-]*)*\/?$/;

    if (linkedin && !urlPattern.test(linkedin)) {
      alert('Please enter a valid LinkedIn URL.');
      return;
    }
    if (github && !urlPattern.test(github)) {
      alert('Please enter a valid GitHub URL.');
      return;
    }

    const ok = await updateProfile({
      portfolioUrl: linkedin,
      personalWebsite: github,
    });
    if (ok) {
      alert('Social profile URLs saved successfully.');
    }
  };

  return (
    <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4 text-left text-[#0F172A]">
      <h3 className="font-bold text-sm sm:text-base">Linked Social Accounts</h3>

      <form onSubmit={handleSave} className="space-y-4 text-xs font-semibold">
        <div className="space-y-3">
          {/* LinkedIn */}
          <div className="space-y-1.5">
            <label className="text-[10px] font-bold text-[#64748B] uppercase tracking-wide flex items-center gap-1">
              <User size={13} className="text-[#0A66C2]" /> LinkedIn URL
            </label>
            <input
              type="text"
              value={linkedin}
              onChange={(e) => setLinkedin(e.target.value)}
              placeholder="https://linkedin.com/in/username"
              className="w-full px-3 py-2.5 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          {/* GitHub */}
          <div className="space-y-1.5">
            <label className="text-[10px] font-bold text-[#64748B] uppercase tracking-wide flex items-center gap-1">
              <Code size={13} className="text-[#181717]" /> GitHub URL
            </label>
            <input
              type="text"
              value={github}
              onChange={(e) => setGithub(e.target.value)}
              placeholder="https://github.com/username"
              className="w-full px-3 py-2.5 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          {/* LeetCode */}
          <div className="space-y-1.5">
            <label className="text-[10px] font-bold text-[#64748B] uppercase tracking-wide flex items-center gap-1">
              <Cpu size={13} className="text-amber-500" /> LeetCode profile URL
            </label>
            <input
              type="text"
              value={leetcode}
              onChange={(e) => setLeetcode(e.target.value)}
              placeholder="https://leetcode.com/username"
              className="w-full px-3 py-2.5 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          {/* Twitter/X */}
          <div className="space-y-1.5">
            <label className="text-[10px] font-bold text-[#64748B] uppercase tracking-wide flex items-center gap-1">
              <Globe size={13} className="text-sky-500" /> Twitter / X URL
            </label>
            <input
              type="text"
              value={x}
              onChange={(e) => setX(e.target.value)}
              placeholder="https://x.com/username"
              className="w-full px-3 py-2.5 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>
        </div>

        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs px-4.5 py-2.5 rounded-xl transition-all cursor-pointer inline-flex items-center gap-1.5"
        >
          <Save size={15} /> Save Social Accounts
        </button>
      </form>
    </div>
  );
}
