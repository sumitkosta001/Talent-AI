'use client';

import React from 'react';
import { MOCK_NOTIFICATION_CATEGORIES } from '@/mock/notificationCategories';

interface NotificationTabsProps {
  activeTab: string;
  onTabChange: (category: string) => void;
  unreadCounts: Record<string, number>;
}

export default function NotificationTabs({
  activeTab,
  onTabChange,
  unreadCounts,
}: NotificationTabsProps) {
  const tabs = ['All', 'Unread', ...MOCK_NOTIFICATION_CATEGORIES];

  const getUnreadCount = (tab: string) => {
    if (tab === 'All') return unreadCounts.all;
    if (tab === 'Unread') return unreadCounts.unread;
    return unreadCounts[tab] || 0;
  };

  return (
    <div className="flex border-b border-[#E2E8F0] overflow-x-auto scrollbar-none gap-2 pb-px select-none">
      {tabs.map((tab) => {
        const count = getUnreadCount(tab);
        const isActive = activeTab === tab;

        return (
          <button
            key={tab}
            onClick={() => onTabChange(tab)}
            className={`
              pb-3 px-3 text-xs sm:text-sm font-semibold border-b-2 transition-all cursor-pointer whitespace-nowrap flex items-center gap-1.5
              ${isActive
                ? 'border-[#2563EB] text-[#2563EB]'
                : 'border-transparent text-[#64748B] hover:text-[#0F172A]'
              }
            `}
          >
            {tab}
            {count > 0 && (
              <span className={`text-[10px] px-1.5 py-0.5 rounded-full font-bold ${
                isActive ? 'bg-blue-50 text-[#2563EB]' : 'bg-slate-100 text-[#64748B]'
              }`}>
                {count}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}
