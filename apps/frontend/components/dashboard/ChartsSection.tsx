'use client';

import React, { useState, useEffect } from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  Legend,
} from 'recharts';
import {
  MOCK_APPLICATIONS_PER_MONTH,
  MOCK_SKILL_GROWTH,
} from '@/mock/charts';
import { TrendingUp, Award, BarChart3 } from 'lucide-react';

export default function ChartsSection() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 h-72 animate-pulse" />
        <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 h-72 animate-pulse" />
      </div>
    );
  }

  return (
    <div className="grid md:grid-cols-2 gap-6 text-left">
      {/* Applications Per Month */}
      <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-3">
          <div className="flex items-center gap-2">
            <TrendingUp size={18} className="text-blue-500" />
            <div>
              <h3 className="font-bold text-[#0F172A] text-sm sm:text-base">Applications Activity</h3>
              <p className="text-[10px] text-[#64748B]">Trend of jobs applied vs technical interviews</p>
            </div>
          </div>
        </div>

        <div className="h-60 w-full text-xs">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={MOCK_APPLICATIONS_PER_MONTH} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorApps" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="colorInts" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
              <XAxis dataKey="month" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0F172A',
                  border: 'none',
                  borderRadius: '12px',
                  color: '#fff',
                  fontSize: '11px',
                }}
              />
              <Area type="monotone" dataKey="applications" stroke="#3B82F6" strokeWidth={2} fillOpacity={1} fill="url(#colorApps)" name="Applied" />
              <Area type="monotone" dataKey="interviews" stroke="#8B5CF6" strokeWidth={2} fillOpacity={1} fill="url(#colorInts)" name="Interviews" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Skill Gap Analysis Radar */}
      <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-3">
          <div className="flex items-center gap-2">
            <Award size={18} className="text-indigo-500" />
            <div>
              <h3 className="font-bold text-[#0F172A] text-sm sm:text-base">Skill Matching Inventory</h3>
              <p className="text-[10px] text-[#64748B]">Comparison of current levels vs industry targets</p>
            </div>
          </div>
        </div>

        <div className="h-60 w-full text-xs flex justify-center items-center">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="75%" data={MOCK_SKILL_GROWTH}>
              <PolarGrid stroke="#F1F5F9" />
              <PolarAngleAxis dataKey="subject" stroke="#94A3B8" />
              <Radar name="Current level" dataKey="current" stroke="#635BFF" fill="#635BFF" fillOpacity={0.25} />
              <Radar name="Required" dataKey="required" stroke="#94A3B8" fill="#94A3B8" fillOpacity={0.05} />
              <Legend verticalAlign="bottom" height={24} iconSize={8} iconType="circle" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0F172A',
                  border: 'none',
                  borderRadius: '12px',
                  color: '#fff',
                  fontSize: '11px',
                }}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
