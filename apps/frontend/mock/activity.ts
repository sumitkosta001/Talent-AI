export interface ActivityLog {
  id: string;
  description: string;
  timestamp: string;
}

export const MOCK_ACTIVITIES: ActivityLog[] = [
  { id: 'act-1', description: 'Updated primary resume document version to v2.1.', timestamp: 'Yesterday' },
  { id: 'act-2', description: 'Added a new project: TalentAI Recruitment Dashboard.', timestamp: '3 days ago' },
  { id: 'act-3', description: 'Applied to Google Senior Software Engineer (L5) position.', timestamp: '1 week ago' },
];
