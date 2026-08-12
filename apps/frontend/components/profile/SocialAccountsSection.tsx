'use client';

import React, { useState, useEffect } from 'react';
import { useProfile } from '@/hooks/useProfile';
import { User, Code, Globe, Cpu, Save } from 'lucide-react';

export default function SocialAccountsSection() {
  const { profile, updateProfile } = useProfile();

  const [linkedin, setLinkedin] = useState('');
  const [github, setGithub] = useState('');
  const [portfolio, setPortfolio] = useState('');
  const [x, setX] = useState('');

  useEffect(() => {
    if (profile) {
      setLinkedin(profile.linkedinUrl || '');
      setGithub(profile.githubUrl || '');
      setPortfolio(profile.portfolioUrl || '');
    }
  }, [profile]);

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
    if (portfolio && !urlPattern.test(portfolio)) {
      alert('Please enter a valid Portfolio / Website URL.');
      return;
    }

    const ok = await updateProfile({
      linkedinUrl: linkedin,
      githubUrl: github,
      portfolioUrl: portfolio,
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

          {/* Portfolio Website */}
          <div className="space-y-1.5">
            <label className="text-[10px] font-bold text-[#64748B] uppercase tracking-wide flex items-center gap-1">
              <Globe size={13} className="text-blue-500" /> Portfolio / Website URL
            </label>
            <input
              type="text"
              value={portfolio}
              onChange={(e) => setPortfolio(e.target.value)}
              placeholder="https://portfolio.dev"
              className="w-full px-3 py-2.5 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          {/* Twitter/X */}
          <div className="space-y-1.5">
            <label className="text-[10px] font-bold text-[#64748B] uppercase tracking-wide flex items-center gap-1">
              <Globe size={13} className="text-sky-500" /> Twitter / X URL (Optional)
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
