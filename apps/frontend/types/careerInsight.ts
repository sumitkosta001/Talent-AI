export interface CareerInsightCard {
  id: string;
  type:
    | 'resume'
    | 'profile'
    | 'skill'
    | 'ats'
    | 'portfolio'
    | 'interview'
    | 'job'
    | 'company'
    | 'certification';
  title: string;
  priority: 'high' | 'medium' | 'low';
  reason: string;
  actionText: string;
  actionUrl: string;
  metadata?: Record<string, any>;
}
