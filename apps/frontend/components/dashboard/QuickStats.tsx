'use client';

import React from 'react';
import { motion } from 'framer-motion';
import {
  FileText,
  Briefcase,
  Calendar,
  Award,
  Bookmark,
  Building2,
  Eye,
  UserCheck,
  Sparkles,
  ShieldCheck,
} from 'lucide-react';
import { DashboardStats } from '@/types/dashboard';
import StatCard from './StatCard';

interface QuickStatsProps {
  stats: DashboardStats;
}

export default function QuickStats({ stats }: QuickStatsProps) {
  const statItems = [
    {
      label: 'Applications',
      value: stats.applications,
      icon: Briefcase,
      color: 'text-blue-500 bg-blue-50 border-blue-100',
    },
    {
      label: 'Interviews',
      value: stats.interviews,
      icon: Calendar,
      color: 'text-indigo-500 bg-indigo-50 border-indigo-100',
    },
    {
      label: 'Offers',
      value: stats.offers,
      icon: Award,
      color: 'text-emerald-500 bg-emerald-50 border-emerald-100',
    },
    {
      label: 'Bookmarks',
      value: stats.bookmarks,
      icon: Bookmark,
      color: 'text-violet-500 bg-violet-50 border-violet-100',
    },
    {
      label: 'Saved Jobs',
      value: stats.savedJobs,
      icon: FileText,
      color: 'text-amber-500 bg-amber-50 border-amber-100',
    },
    {
      label: 'Companies Followed',
      value: stats.companiesFollowed,
      icon: Building2,
      color: 'text-cyan-500 bg-cyan-50 border-cyan-100',
    },
    {
      label: 'Resume Views',
      value: stats.resumeViews,
      icon: Eye,
      color: 'text-teal-500 bg-teal-50 border-teal-100',
    },
    {
      label: 'Profile Views',
      value: stats.profileViews,
      icon: UserCheck,
      color: 'text-purple-500 bg-purple-50 border-purple-100',
    },
    {
      label: 'Career Score',
      value: stats.careerScore,
      icon: Sparkles,
      color: 'text-orange-500 bg-orange-50 border-orange-100',
    },
    {
      label: 'ATS Score',
      value: `${stats.atsScore}%`,
      icon: ShieldCheck,
      color: 'text-rose-500 bg-rose-50 border-rose-100',
    },
  ];

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.05,
      },
    },
  };

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4"
    >
      {statItems.map((item, index) => (
        <StatCard
          key={index}
          label={item.label}
          value={item.value}
          icon={item.icon}
          color={item.color}
        />
      ))}
    </motion.div>
  );
}
