'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Activity, AlertTriangle, RefreshCw } from 'lucide-react';

// Hooks
import { useDashboard } from '@/hooks/useDashboard';
import { useCalendar } from '@/hooks/useCalendar';
import { useActivity } from '@/hooks/useActivity';
import { useBookmarks } from '@/hooks/useBookmarks';
import { useRecentSearches } from '@/hooks/useRecentSearches';
import { useWeeklyReport } from '@/hooks/useWeeklyReport';
import { useCareerInsights } from '@/hooks/useCareerInsights';

// Reusable Components
import DashboardHero from '@/components/dashboard/DashboardHero';
import DashboardSearch from '@/components/dashboard/DashboardSearch';
import DashboardFilters, { TimeFilter, ModuleFilter } from '@/components/dashboard/DashboardFilters';
import ChartsSection from '@/components/dashboard/ChartsSection';
import WeeklyReport from '@/components/dashboard/WeeklyReport';
import RecentActivity from '@/components/dashboard/RecentActivity';
import QuickActions from '@/components/dashboard/QuickActions';
import ProductivityGoals from '@/components/dashboard/ProductivityGoals';
import CalendarWidget from '@/components/dashboard/CalendarWidget';
import UpcomingInterviews from '@/components/dashboard/UpcomingInterviews';
import ApplicationDeadlines from '@/components/dashboard/ApplicationDeadlines';
import CareerInsights from '@/components/dashboard/CareerInsights';
import Bookmarks from '@/components/dashboard/Bookmarks';
import RecentSearches from '@/components/dashboard/RecentSearches';
import NotificationPreview from '@/components/dashboard/NotificationPreview';

export default function CandidateDashboardPage() {
  // Global States
  const [searchQuery, setSearchQuery] = useState('');
  const [timeFilter, setTimeFilter] = useState<TimeFilter>('week');
  const [moduleFilter, setModuleFilter] = useState<ModuleFilter>('all');

  // Hooks bindings
  const { overview, interviews, deadlines, goals, loading: dashLoading, error: dashError, refetch: refetchDash } = useDashboard();
  const { events, loading: calLoading, refetch: refetchCal } = useCalendar();
  const { activities, loading: actLoading, refetch: refetchAct } = useActivity();
  const { bookmarks, removeBookmark, loading: bookLoading, refetch: refetchBook } = useBookmarks();
  const { searches, addSearch, deleteSearch, clearHistory } = useRecentSearches();
  const { reportData, loading: reportLoading, refetch: refetchReport } = useWeeklyReport();
  const { insights, dismissInsight, loading: insightsLoading, refetch: refetchInsights } = useCareerInsights();

  const handleSearchSelect = (query: string) => {
    setSearchQuery(query);
    addSearch(query, 'jobs');
  };

  const handleGlobalSearchSubmit = (val: string) => {
    setSearchQuery(val);
    if (val.trim()) {
      addSearch(val, 'jobs');
    }
  };

  const handleReloadAll = () => {
    refetchDash();
    refetchCal();
    refetchAct();
    refetchBook();
    refetchReport();
    refetchInsights();
  };

  const isLoading = dashLoading || calLoading || actLoading || bookLoading || reportLoading || insightsLoading;

  if (dashError) {
    return (
      <div className="p-6 text-center max-w-lg mx-auto mt-20 space-y-4">
        <div className="w-16 h-16 bg-red-50 text-red-500 rounded-2xl flex items-center justify-center mx-auto border border-red-100">
          <AlertTriangle size={28} />
        </div>
        <h2 className="text-xl font-bold text-slate-800">Failed to load Dashboard</h2>
        <p className="text-sm text-slate-500 leading-relaxed">{dashError}</p>
        <button
          onClick={handleReloadAll}
          className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-5 rounded-2xl shadow-sm transition-all"
        >
          <RefreshCw size={14} />
          Retry Connection
        </button>
      </div>
    );
  }

  // Helper filters visibility checks
  const isSectionVisible = (secName: ModuleFilter) => {
    if (moduleFilter === 'all') return true;
    return moduleFilter === secName;
  };

  return (
    <div className="p-4 sm:p-6 space-y-6 max-w-[1600px] mx-auto text-left">
      {/* Search and control filters bar */}
      <div className="flex flex-col lg:flex-row justify-between gap-4">
        <DashboardSearch value={searchQuery} onChange={handleGlobalSearchSubmit} />
        <DashboardFilters
          timeFilter={timeFilter}
          setTimeFilter={setTimeFilter}
          moduleFilter={moduleFilter}
          setModuleFilter={setModuleFilter}
        />
      </div>

      {isLoading && !overview ? (
        <div className="space-y-6 animate-pulse">
          <div className="bg-slate-200 h-48 rounded-3xl" />
          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <div className="bg-slate-200 h-64 rounded-3xl" />
              <div className="bg-slate-200 h-64 rounded-3xl" />
            </div>
            <div className="space-y-6">
              <div className="bg-slate-200 h-72 rounded-3xl" />
              <div className="bg-slate-200 h-72 rounded-3xl" />
            </div>
          </div>
        </div>
      ) : (
        <div className="grid lg:grid-cols-3 gap-6 items-start">
          {/* Main workspace column (2 cols on large screen) */}
          <div className="lg:col-span-2 space-y-6">
            {overview && (
              <DashboardHero overview={overview} />
            )}

            {isSectionVisible('all') && (
              <ChartsSection />
            )}

            {isSectionVisible('all') && reportData && (
              <WeeklyReport report={reportData} />
            )}

            {isSectionVisible('all') && (
              <RecentActivity activities={activities} />
            )}
          </div>

          {/* Right Sidebar column (1 col on large screen) */}
          <div className="space-y-6">
            {/* Quick launch shortcuts */}
            <QuickActions />

            {/* Target progress rings */}
            <ProductivityGoals goals={goals} />

            {/* Monthly calendar agenda planner */}
            {isSectionVisible('interviews') && (
              <CalendarWidget events={events} />
            )}

            {/* Countdown items for upcoming screening calls */}
            {isSectionVisible('interviews') && (
              <UpcomingInterviews interviews={interviews} />
            )}

            {/* Application deadlines countdown bars */}
            {isSectionVisible('apps') && (
              <ApplicationDeadlines deadlines={deadlines} />
            )}

            {/* AI Mentoring Coach Insights recommendations */}
            <CareerInsights insights={insights} onDismiss={dismissInsight} />

            {/* Persisted saved resources bookmarks */}
            {isSectionVisible('bookmarks') && (
              <Bookmarks bookmarks={bookmarks} onRemove={removeBookmark} />
            )}

            {/* Relaunch searches logs */}
            <RecentSearches
              searches={searches}
              onDelete={deleteSearch}
              onClear={clearHistory}
              onSelect={handleSearchSelect}
            />

            {/* Recent alerts preview list */}
            {isSectionVisible('notifications') && (
              <NotificationPreview />
            )}
          </div>
        </div>
      )}
    </div>
  );
}
