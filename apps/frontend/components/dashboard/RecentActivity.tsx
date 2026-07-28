'use client';

import React from 'react';
import { motion } from 'framer-motion';
import {
  Briefcase,
  FileText,
  Shield,
  Calendar,
  Award,
  User,
  Plus,
  ArrowUpRight,
} from 'lucide-react';
import { RecentActivityItem } from '@/types/activity';
import Link from 'next/link';

interface RecentActivityProps {
  activities: RecentActivityItem[];
}

export default function RecentActivity({ activities }: RecentActivityProps) {
  const getActivityIcon = (type: RecentActivityItem['type']) => {
    switch (type) {
      case 'applied':
        return { icon: Briefcase, color: 'text-blue-500 bg-blue-50 border-blue-100' };
      case 'resume_updated':
        return { icon: FileText, color: 'text-emerald-500 bg-emerald-50 border-emerald-100' };
      case 'ats_improved':
        return { icon: Shield, color: 'text-indigo-500 bg-indigo-50 border-indigo-100' };
      case 'interview_scheduled':
        return { icon: Calendar, color: 'text-violet-500 bg-violet-50 border-violet-100' };
      case 'offer_received':
        return { icon: Award, color: 'text-amber-500 bg-amber-50 border-amber-100' };
      case 'profile_updated':
      case 'skill_added':
      case 'project_added':
      case 'certificate_added':
        return { icon: User, color: 'text-pink-500 bg-pink-50 border-pink-100' };
      default:
        return { icon: Plus, color: 'text-slate-500 bg-slate-50 border-slate-100' };
    }
  };

  return (
    <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <div className="border-b border-[#F1F5F9] pb-3">
        <h3 className="font-bold text-[#0F172A] text-base sm:text-lg">Recent Activities</h3>
        <p className="text-xs text-[#64748B] mt-0.5">Keep track of your latest movements and integrations</p>
      </div>

      <div className="relative pl-4 space-y-5 border-l-2 border-[#E2E8F0]">
        {activities.map((item, idx) => {
          const config = getActivityIcon(item.type);
          const Icon = config.icon;

          return (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.05 }}
              className="relative group"
            >
              {/* Timeline bubble */}
              <div className="absolute -left-[30px] top-1.5 w-6 h-6 rounded-full bg-white border-2 border-[#E2E8F0] flex items-center justify-center flex-shrink-0">
                <div className="w-2 h-2 rounded-full bg-blue-500" />
              </div>

              <div className="flex items-start justify-between gap-4 p-3 rounded-2xl border border-transparent hover:border-[#E2E8F0]/80 hover:bg-[#F8FAFC]/50 transition-all duration-200">
                <div className="flex gap-3 min-w-0">
                  <div className={`w-9 h-9 rounded-xl flex items-center justify-center border flex-shrink-0 ${config.color}`}>
                    <Icon size={16} />
                  </div>
                  <div className="min-w-0">
                    <h4 className="font-bold text-[#0F172A] text-sm truncate leading-tight">
                      {item.title}
                    </h4>
                    <p className="text-xs text-[#64748B] leading-relaxed mt-1">
                      {item.description}
                    </p>
                    <span className="text-[10px] font-bold text-[#94A3B8] block mt-1.5 uppercase tracking-wide">
                      {item.timestamp}
                    </span>
                  </div>
                </div>

                {item.actionText && item.actionUrl && (
                  <Link href={item.actionUrl}>
                    <button className="flex items-center gap-1 py-1.5 px-2.5 bg-white hover:bg-slate-50 border border-[#E2E8F0] rounded-xl text-xs font-bold text-[#475569] transition-all whitespace-nowrap">
                      {item.actionText}
                      <ArrowUpRight size={12} className="text-[#94A3B8]" />
                    </button>
                  </Link>
                )}
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
