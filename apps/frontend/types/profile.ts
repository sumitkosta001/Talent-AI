export type ProfileVisibility = 'Public' | 'Recruiters Only' | 'Private';

export interface CandidateProfile {
  id: string;
  name: string;
  firstName?: string;
  lastName?: string;
  profilePic?: string;
  headline: string;
  currentRole: string;
  location: string;
  email: string;
  phone: string;
  alternatePhone?: string;
  visibility: ProfileVisibility;
  isOpenToWork: boolean;
  availabilityStatus: string;
  completionPercentage: number;
  bio: string;
  gender?: string;
  dob?: string;
  nationality?: string;
  address?: string;
  city?: string;
  state?: string;
  country?: string;
  postalCode?: string;
  portfolioUrl?: string;
  personalWebsite?: string;
  preferredRole?: string;
  preferredWorkMode?: 'Remote' | 'Hybrid' | 'On-site';
  expectedSalary?: string;
  careerObjective?: string;
  yearsOfExperience?: number;
}
