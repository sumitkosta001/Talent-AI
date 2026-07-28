export interface RecentActivityItem {
  id: string;
  type:
    | 'applied'
    | 'resume_updated'
    | 'ats_improved'
    | 'interview_scheduled'
    | 'offer_received'
    | 'profile_updated'
    | 'company_followed'
    | 'certificate_added'
    | 'project_added'
    | 'skill_added';
  title: string;
  timestamp: string;
  description: string;
  actionUrl?: string;
  actionText?: string;
}
