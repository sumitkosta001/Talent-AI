'use client';

import React, { useState } from 'react';
import { SocialLinks } from '@/types/settings';
import { Link2 } from 'lucide-react';

interface SocialLinksSectionProps {
  socials?: SocialLinks;
  onChange: (field: keyof SocialLinks, value: string) => void;
}

export default function SocialLinksSection({ socials, onChange }: SocialLinksSectionProps) {
  const [errors, setErrors] = useState<Record<string, string>>({});

  if (!socials) return null;

  const validateUrl = (field: keyof SocialLinks, val: string) => {
    if (!val) {
      setErrors(prev => {
        const next = { ...prev };
        delete next[field];
        return next;
      });
      onChange(field, val);
      return;
    }

    try {
      new URL(val);
      // Valid URL
      setErrors(prev => {
        const next = { ...prev };
        delete next[field];
        return next;
      });
    } catch {
      setErrors(prev => ({ ...prev, [field]: 'Please enter a valid absolute URL (e.g. https://...)' }));
    }

    onChange(field, val);
  };

  const fields: { id: keyof SocialLinks; label: string; placeholder: string }[] = [
    { id: 'linkedin', label: 'LinkedIn Profile URL', placeholder: 'https://linkedin.com/in/username' },
    { id: 'github', label: 'GitHub Profile URL', placeholder: 'https://github.com/username' },
    { id: 'portfolio', label: 'Portfolio Website', placeholder: 'https://portfolio.dev' },
    { id: 'leetcode', label: 'LeetCode Username/Link', placeholder: 'https://leetcode.com/username' },
    { id: 'stackoverflow', label: 'Stack Overflow Link', placeholder: 'https://stackoverflow.com/users/uid/username' },
    { id: 'twitter', label: 'Twitter/X Profile Link', placeholder: 'https://x.com/username' },
    { id: 'medium', label: 'Medium Blog Link', placeholder: 'https://medium.com/@username' },
  ];

  return (
    <div className="space-y-4 text-left">
      {fields.map(({ id, label, placeholder }) => (
        <div key={id}>
          <label className="block text-xs font-bold text-[#475569] mb-1.5">{label}</label>
          <div className="relative">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
              <Link2 size={14} />
            </span>
            <input
              type="text"
              value={socials[id] || ''}
              onChange={(e) => validateUrl(id, e.target.value)}
              placeholder={placeholder}
              className={`w-full pl-9 pr-3 py-2 border rounded-xl text-sm text-[#0F172A] focus:outline-none bg-white ${
                errors[id] ? 'border-red-300 focus:border-red-500' : 'border-[#E2E8F0] focus:border-blue-500'
              }`}
            />
          </div>
          {errors[id] && (
            <p className="text-[10px] text-red-500 font-semibold mt-1">{errors[id]}</p>
          )}
        </div>
      ))}
    </div>
  );
}
