export type UserRole = 'Super Admin' | 'Admin' | 'Moderator' | 'Support' | 'Candidate' | 'Recruiter';
export type UserStatus = 'Active' | 'Suspended' | 'Deactivated';

export interface AdminUser {
  id: string;
  name: string;
  email: string;
  phone: string;
  role: UserRole;
  status: UserStatus;
  country: string;
  registrationDate: string;
  lastLogin: string;
  resumeUploaded: boolean;
  atsScore?: number;
  applicationsCount: number;
  bio?: string;
  experience?: string;
  skills?: string[];
  education?: string[];
}
