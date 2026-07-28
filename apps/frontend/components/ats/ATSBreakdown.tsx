'use client';

import React from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer } from 'recharts';
import HorizontalProgress from './HorizontalProgress';

interface BreakdownItem {
  label: string;
  score: number;
  icon: string;
  color: string;
}

interface RadarItem {
  subject: string;
  score: number;
}

interface ATSBreakdownProps {
  scoreBreakdown: BreakdownItem[];
  radarData: RadarItem[];
}

export default function ATSBreakdown({ scoreBreakdown, radarData }: ATSBreakdownProps) {
  return (
    <div className="grid lg:grid-cols-2 gap-6">
      {/* Score breakdown */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm">
        <h2 className="font-semibold text-[#0F172A] mb-5">Score Breakdown</h2>
        <div className="space-y-4">
          {scoreBreakdown.map(({ label, score, icon, color }) => (
            <div key={label}>
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-base">{icon}</span>
                  <span className="text-sm font-medium text-[#0F172A]">{label}</span>
                </div>
                <span className="text-sm font-bold text-[#0F172A]">{score}%</span>
              </div>
              <HorizontalProgress value={score} color={color} />
            </div>
          ))}
        </div>
      </div>

      {/* Radar chart */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm flex flex-col justify-between">
        <h2 className="font-semibold text-[#0F172A] mb-3">Skill Radar</h2>
        <div className="w-full" style={{ height: 220 }}>
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
              <PolarGrid stroke="#E2E8F0" />
              <PolarAngleAxis dataKey="subject" tick={{ fontSize: 11, fill: '#64748B' }} />
              <Radar name="Score" dataKey="score" stroke="#2563EB" fill="#2563EB" fillOpacity={0.15} strokeWidth={2} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
