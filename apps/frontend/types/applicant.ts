export type ApplicantStatus =
  | 'Applied'
  | 'Under Review'
  | 'Shortlisted'
  | 'Interview Scheduled'
  | 'Offer Sent'
  | 'Rejected'
  | 'Archived';

export interface Applicant {
  id: string;
  jobId: string;
  jobTitle: string;
  name: string;
  email: string;
  phone: string;
  avatarUrl?: string;
  atsScore: number;
  matchPercentage: number;
  experience: string;
  skills: string[];
  status: ApplicantStatus;
  appliedDate: string;
  bio?: string;
  resumeUrl?: string;
  notes?: string;
  timeline: {
    stage: string;
    date: string;
    notes?: string;
  }[];
}
