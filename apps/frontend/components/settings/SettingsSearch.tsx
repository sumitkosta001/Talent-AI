'use client';

import React, { useState, useEffect } from 'react';
import { Search, ChevronRight } from 'lucide-react';

interface SettingsSearchProps {
  onJumpToSection: (sectionId: string) => void;
}

const SECTION_KEYWORDS = [
  { id: 'profile', keywords: ['profile', 'name', 'headline', 'bio', 'phone', 'city', 'location', 'avatar', 'upload', 'personal'] },
  { id: 'password', keywords: ['password', 'security', 'strength', 'authentication', 'requirements'] },
  { id: 'socials', keywords: ['socials', 'linkedin', 'github', 'portfolio', 'leetcode', 'website', 'twitter', 'medium'] },
  { id: 'resume', keywords: ['resume', 'visibility', 'public', 'private', 'download', 'search', 'recruiters'] },
  { id: 'privacy', keywords: ['privacy', 'indexing', 'recommendations', 'analytics', 'tracking'] },
  { id: 'notifications', keywords: ['notifications', 'email', 'push', 'sms', 'digest', 'reminders'] },
  { id: 'theme', keywords: ['theme', 'dark', 'light', 'system', 'appearance'] },
  { id: 'language', keywords: ['language', 'english', 'hindi', 'spanish', 'french', 'german', 'japanese', 'chinese'] },
  { id: 'delete', keywords: ['delete', 'remove', 'danger', 'erase', 'cancel'] },
];

export default function SettingsSearch({ onJumpToSection }: SettingsSearchProps) {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<{ id: string; label: string }[]>([]);

  useEffect(() => {
    if (!query.trim()) {
      setSuggestions([]);
      return;
    }

    const q = query.toLowerCase();
    const matched = SECTION_KEYWORDS.filter((sec) =>
      sec.keywords.some((k) => k.includes(q))
    ).map((sec) => {
      // Map back to a human-readable title
      let label = sec.id.charAt(0).toUpperCase() + sec.id.slice(1);
      if (sec.id === 'socials') label = 'Social Links';
      if (sec.id === 'resume') label = 'Resume Visibility';
      if (sec.id === 'delete') label = 'Delete Account';
      return { id: sec.id, label };
    });

    setSuggestions(matched);
  }, [query]);

  const handleJump = (sectionId: string) => {
    onJumpToSection(sectionId);
    setQuery('');
  };

  return (
    <div className="relative flex-1 text-left">
      <div className="relative">
        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search settings..."
          className="w-full pl-9 pr-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
        />
      </div>

      {suggestions.length > 0 && (
        <div className="absolute left-0 right-0 top-12 bg-white border border-[#E2E8F0] rounded-xl shadow-lg py-1.5 z-40">
          {suggestions.map((s) => (
            <button
              key={s.id}
              onClick={() => handleJump(s.id)}
              className="w-full px-3 py-2 text-xs sm:text-sm text-[#0F172A] hover:bg-[#F8FAFC] flex items-center justify-between text-left cursor-pointer"
            >
              <span>Jump to: <strong className="font-bold text-blue-600">{s.label}</strong></span>
              <ChevronRight size={13} className="text-slate-400" />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
