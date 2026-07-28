'use client';

import React from 'react';
import { User, Key, Link2, Eye, Shield, Bell, EyeOff, Globe, Trash2, SunMoon } from 'lucide-react';

interface SettingsSidebarProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
}

export default function SettingsSidebar({ activeSection, onSectionChange }: SettingsSidebarProps) {
  const sections = [
    { id: 'profile', label: 'Profile Information', icon: User },
    { id: 'password', label: 'Security & Password', icon: Key },
    { id: 'socials', label: 'Social Networks', icon: Link2 },
    { id: 'resume', label: 'Resume Visibility', icon: Eye },
    { id: 'privacy', label: 'Privacy Control', icon: Shield },
    { id: 'notifications', label: 'Notification Settings', icon: Bell },
    { id: 'theme', label: 'Visual Interface Theme', icon: SunMoon },
    { id: 'language', label: 'Language Select', icon: Globe },
    { id: 'delete', label: 'Delete Account', icon: Trash2, danger: true },
  ];

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-3 shadow-sm space-y-1 text-left h-fit">
      {sections.map(({ id, label, icon: Icon, danger }) => {
        const isActive = activeSection === id;
        return (
          <button
            key={id}
            onClick={() => onSectionChange(id)}
            className={`
              w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs sm:text-sm font-semibold
              transition-all duration-150 cursor-pointer text-left
              ${isActive
                ? 'bg-blue-50 text-[#2563EB] font-bold border-l-2 border-[#2563EB] pl-3'
                : danger
                  ? 'text-red-500 hover:bg-red-50'
                  : 'text-[#64748B] hover:bg-[#F8FAFC] hover:text-[#0F172A]'
              }
            `}
          >
            <Icon size={16} className="flex-shrink-0" />
            <span className="truncate">{label}</span>
          </button>
        );
      })}
    </div>
  );
}
