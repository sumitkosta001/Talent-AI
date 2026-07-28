'use client';

import React, { useState } from 'react';
import { useApplications } from '@/hooks/useApplications';
import ApplicationsHeader from '@/components/applications/ApplicationsHeader';
import StatsCards from '@/components/applications/StatsCards';
import SearchFilterBar from '@/components/applications/SearchFilterBar';
import ApplicationCard from '@/components/applications/ApplicationCard';
import EmptyApplications from '@/components/applications/EmptyApplications';
import ApplicationAnalytics from '@/components/applications/ApplicationAnalytics';
import { Loader2 } from 'lucide-react';

export default function CandidateApplicationsPage() {
  const {
    applications,
    rawApplications,
    analytics,
    loading,
    error,
    filters,
    sortBy,
    setSortBy,
    updateFilter,
    resetFilters,
    archive,
    restore,
  } = useApplications();

  const [showArchived, setShowArchived] = useState(false);

  // Split into active and archived lists
  const activeApps = applications.filter((a) => !a.archived);
  const archivedApps = applications.filter((a) => a.archived);

  const displayList = showArchived ? archivedApps : activeApps;

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading your application history...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3">
        <div className="text-red-500 font-bold text-lg">Error Loading Applications</div>
        <p className="text-sm text-[#64748B]">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="bg-blue-600 text-white px-4 py-2 rounded-xl text-sm font-semibold cursor-pointer"
        >
          Retry
        </button>
      </div>
    );
  }

  const offersCount = rawApplications.filter((a) => a.status === 'Offer Received' || a.status === 'Offer Accepted').length;

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto text-[#0F172A]">
      {/* Header */}
      <ApplicationsHeader totalCount={rawApplications.length} offersCount={offersCount} />

      {/* Stats Counter Blocks */}
      <StatsCards applications={rawApplications.filter((a) => !a.archived)} />

      {/* Analytics Dashboard */}
      {analytics && <ApplicationAnalytics analytics={analytics} />}

      {/* Filters & Sorting */}
      <SearchFilterBar
        filters={filters}
        updateFilter={updateFilter}
        resetFilters={resetFilters}
        sortBy={sortBy}
        setSortBy={setSortBy}
        showArchived={showArchived}
        setShowArchived={setShowArchived}
      />

      {/* Application lists */}
      <div className="space-y-4">
        <h2 className="font-bold text-sm text-[#0F172A] uppercase tracking-wide text-left">
          {showArchived ? 'Archived Applications' : 'Active Applications'} ({displayList.length})
        </h2>

        {displayList.length === 0 ? (
          <EmptyApplications />
        ) : (
          <div className="grid gap-4">
            {displayList.map((app) => (
              <ApplicationCard
                key={app.id}
                application={app}
                onArchive={archive}
                onRestore={restore}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
