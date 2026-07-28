'use client';

import React from 'react';
import { RecentActivityItem } from '@/types/activity';
import RecentActivity from './RecentActivity';

interface ActivityTimelineProps {
  activities: RecentActivityItem[];
}

export default function ActivityTimeline({ activities }: ActivityTimelineProps) {
  return <RecentActivity activities={activities} />;
}
