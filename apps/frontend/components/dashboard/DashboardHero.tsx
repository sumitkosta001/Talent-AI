'use client';

import React from 'react';
import GreetingCard from './GreetingCard';
import QuickStats from './QuickStats';
import { DashboardOverview } from '@/types/dashboard';

interface DashboardHeroProps {
  overview: DashboardOverview;
}

export default function DashboardHero({ overview }: DashboardHeroProps) {
  return (
    <div className="space-y-6">
      <GreetingCard
        name={overview.candidateName}
        profileCompletion={overview.profileCompletion}
        atsScore={overview.atsScore}
        careerScore={overview.careerScore}
        resumeScore={overview.resumeScore}
      />
      <QuickStats stats={overview.stats} />
    </div>
  );
}
