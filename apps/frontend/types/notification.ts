export type NotificationPriority = 'High' | 'Medium' | 'Low';

export type NotificationCategory =
  | 'Jobs'
  | 'ATS'
  | 'Applications'
  | 'Recruiters'
  | 'Interviews'
  | 'Offers'
  | 'Resume'
  | 'System'
  | 'Security';

export type NotificationType =
  | 'New Jobs'
  | 'ATS Updates'
  | 'Recruiter Messages'
  | 'Interview Invites'
  | 'Offer Notifications'
  | 'Resume Reminder'
  | 'Application Status Updates'
  | 'Application Viewed'
  | 'Application Shortlisted'
  | 'Assessment Invitation'
  | 'Interview Reminder'
  | 'Offer Accepted'
  | 'Offer Rejected'
  | 'Profile Completion Reminder'
  | 'System Announcement'
  | 'Security Alert';

export interface Notification {
  id: string;
  type: NotificationType;
  category: NotificationCategory;
  priority: NotificationPriority;
  title: string;
  description: string;
  timestamp: string; // e.g. '5 min ago', '2026-07-26T12:00:00Z'
  read: boolean;
  archived?: boolean;
  relatedId?: string; // id of related entity e.g., jobId, applicationId
  relatedRoute?: string; // e.g., '/candidate/jobs/1'
  metadata?: Record<string, any>;
}

export interface NotificationFilter {
  search: string;
  readStatus: 'All' | 'Read' | 'Unread';
  category: string;
  priority: string;
  dateRange: 'All' | 'Today' | 'Last 7 Days' | 'Last 30 Days';
  sortBy: 'Newest' | 'Oldest';
}

export interface NotificationStats {
  total: number;
  unread: number;
  read: number;
  today: number;
  thisWeek: number;
  highPriority: number;
}

export interface NotificationAction {
  label: string;
  icon: string;
  action: (id: string) => void;
}
