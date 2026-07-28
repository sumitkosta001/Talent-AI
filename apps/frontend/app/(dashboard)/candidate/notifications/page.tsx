'use client';

import React, { useState, useEffect } from 'react';
import { useNotifications } from '@/hooks/useNotifications';
import NotificationsHeader from '@/components/notifications/NotificationsHeader';
import NotificationStats from '@/components/notifications/NotificationStats';
import NotificationTabs from '@/components/notifications/NotificationTabs';
import NotificationSearch from '@/components/notifications/NotificationSearch';
import NotificationFilters from '@/components/notifications/NotificationFilters';
import NotificationList from '@/components/notifications/NotificationList';
import NotificationDetails from '@/components/notifications/NotificationDetails';
import EmptyNotifications from '@/components/notifications/EmptyNotifications';
import { Loader2 } from 'lucide-react';
import { Notification } from '@/types/notification';

export default function CandidateNotificationsPage() {
  const {
    notifications,
    rawNotifications,
    stats,
    loading,
    error,
    filters,
    updateFilter,
    resetFilters,
    markRead,
    markAllRead,
    deleteNotification,
    clearAll,
    refetch,
  } = useNotifications();

  const [activeTab, setActiveTab] = useState('All');
  const [selectedNotification, setSelectedNotification] = useState<Notification | null>(null);

  // Sync selected notification on initial load or category tab change
  useEffect(() => {
    if (notifications.length > 0) {
      setSelectedNotification(notifications[0]);
    } else {
      setSelectedNotification(null);
    }
  }, [notifications, activeTab]);

  // Handle Tab Switch Filter triggers
  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    if (tab === 'All') {
      updateFilter('readStatus', 'All');
      updateFilter('category', 'All');
    } else if (tab === 'Unread') {
      updateFilter('readStatus', 'Unread');
      updateFilter('category', 'All');
    } else {
      updateFilter('readStatus', 'All');
      updateFilter('category', tab);
    }
  };

  // Compile tab counters dynamically from rawNotifications list
  const getTabUnreadCounts = () => {
    const counts: Record<string, number> = {
      all: rawNotifications.filter((n) => !n.read).length,
      unread: rawNotifications.filter((n) => !n.read).length,
    };
    rawNotifications.forEach((n) => {
      if (!n.read) {
        counts[n.category] = (counts[n.category] || 0) + 1;
      }
    });
    return counts;
  };

  const handleSelectNotification = (n: Notification) => {
    setSelectedNotification(n);
    // Mark as read automatically when selected previewed
    if (!n.read) {
      markRead(n.id, true);
    }
  };

  if (loading && rawNotifications.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-[#2563EB]" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading notifications...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Error Loading Notifications</h3>
        <p className="text-sm text-[#64748B]">{error}</p>
        <button
          onClick={refetch}
          className="bg-[#2563EB] text-white px-4 py-2 rounded-xl text-sm font-semibold cursor-pointer"
        >
          Retry Fetching
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto text-[#0F172A]">
      {/* Header operations row */}
      <NotificationsHeader
        onMarkAllRead={markAllRead}
        onClearAll={clearAll}
        onRefresh={refetch}
      />

      {/* Counters Stats blocks */}
      <NotificationStats stats={stats} />

      {/* Search and Filters selectors row */}
      <div className="flex flex-col md:flex-row gap-3">
        <NotificationSearch
          value={filters.search}
          onChange={(val) => updateFilter('search', val)}
        />
      </div>

      <NotificationFilters
        filters={filters}
        updateFilter={updateFilter}
        resetFilters={resetFilters}
      />

      {/* Horizontal Tabs selection row */}
      <NotificationTabs
        activeTab={activeTab}
        onTabChange={handleTabChange}
        unreadCounts={getTabUnreadCounts()}
      />

      {/* Split/Double columns list layout */}
      {notifications.length === 0 ? (
        <EmptyNotifications />
      ) : (
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Left Column list */}
          <div className="lg:col-span-2 space-y-3">
            <NotificationList
              notifications={notifications}
              onMarkRead={markRead}
              onDelete={deleteNotification}
              onSelect={handleSelectNotification}
              activeId={selectedNotification?.id}
            />
          </div>

          {/* Right Column preview block */}
          <div className="hidden lg:block h-fit sticky top-6">
            <NotificationDetails notification={selectedNotification} />
          </div>
        </div>
      )}
    </div>
  );
}
