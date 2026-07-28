'use client';

import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  icon?: LucideIcon;
  label: string;
  value: string | number;
  subValue?: string;
  iconColor?: string;
  iconBgColor?: string;
}

export default function MetricCard({
  icon: Icon,
  label,
  value,
  subValue,
  iconColor = 'text-blue-600',
  iconBgColor = 'bg-blue-50',
}: MetricCardProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 flex items-center gap-4">
      {Icon && (
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${iconBgColor} ${iconColor} flex-shrink-0`}>
          <Icon size={22} />
        </div>
      )}
      <div>
        <p className="text-2xl font-bold text-[#0F172A]">{value}</p>
        <p className="text-sm font-medium text-[#0F172A] mt-0.5">{label}</p>
        {subValue && <p className="text-xs text-[#64748B] mt-0.5">{subValue}</p>}
      </div>
    </div>
  );
}
