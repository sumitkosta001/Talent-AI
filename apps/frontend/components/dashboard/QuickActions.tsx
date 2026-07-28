'use client';

import React from 'react';
import { motion } from 'framer-motion';
import {
  Search,
  Upload,
  Shield,
  FileText,
  Mail,
  Video,
  Map,
  User,
  Bookmark,
  Bell,
  Sparkles,
} from 'lucide-react';
import Link from 'next/link';

export default function QuickActions() {
  const actions = [
    { label: 'Search Jobs', url: '/candidate/jobs', icon: Search, color: 'text-blue-500 bg-blue-50 border-blue-100 hover:bg-blue-100/50' },
    { label: 'Upload Resume', url: '/candidate/resume/upload', icon: Upload, color: 'text-emerald-500 bg-emerald-50 border-emerald-100 hover:bg-emerald-100/50' },
    { label: 'Improve ATS', url: '/candidate/ats', icon: Shield, color: 'text-rose-500 bg-rose-50 border-rose-100 hover:bg-rose-100/50' },
    { label: 'AI Resume Builder', url: '/candidate/ai/resume-builder', icon: Sparkles, color: 'text-indigo-500 bg-indigo-50 border-indigo-100 hover:bg-indigo-100/50' },
    { label: 'Cover Letter', url: '/candidate/ai/cover-letter', icon: Mail, color: 'text-amber-500 bg-amber-50 border-amber-100 hover:bg-amber-100/50' },
    { label: 'Mock Interview', url: '/candidate/ai/mock-interview', icon: Video, color: 'text-violet-500 bg-violet-50 border-violet-100 hover:bg-violet-100/50' },
    { label: 'Career Roadmap', url: '/candidate/ai/roadmap', icon: Map, color: 'text-cyan-500 bg-cyan-50 border-cyan-100 hover:bg-cyan-100/50' },
    { label: 'Edit Profile', url: '/candidate/profile', icon: User, color: 'text-purple-500 bg-purple-50 border-purple-100 hover:bg-purple-100/50' },
    { label: 'Saved Bookmarks', url: '/candidate/profile', icon: Bookmark, color: 'text-teal-500 bg-teal-50 border-teal-100 hover:bg-teal-100/50' },
    { label: 'Notifications', url: '/candidate/notifications', icon: Bell, color: 'text-pink-500 bg-pink-50 border-pink-100 hover:bg-pink-100/50' },
  ];

  return (
    <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <div className="border-b border-[#F1F5F9] pb-3">
        <h3 className="font-bold text-[#0F172A] text-base sm:text-lg">Quick Actions</h3>
        <p className="text-xs text-[#64748B] mt-0.5">Shortcuts to launch AI tools and manage applications</p>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {actions.map((item, idx) => {
          const Icon = item.icon;
          return (
            <Link key={idx} href={item.url}>
              <motion.div
                whileHover={{ scale: 1.01, y: -1 }}
                className={`p-3 border rounded-2xl flex items-center gap-2.5 transition-all duration-200 cursor-pointer ${item.color}`}
              >
                <div className="flex-shrink-0">
                  <Icon size={16} />
                </div>
                <span className="text-[11px] sm:text-xs font-bold text-[#334155] leading-tight truncate">
                  {item.label}
                </span>
              </motion.div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
