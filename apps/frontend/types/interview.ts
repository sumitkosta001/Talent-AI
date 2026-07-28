export interface RecruiterInterview {
  jobId: string;
  applicantId: string;
  date: string;
  time: string;
  type: 'Online' | 'Offline';
  panelMembers: string[];
  meetingLink?: string;
  notes?: string;
}
