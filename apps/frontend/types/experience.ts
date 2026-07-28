export interface CandidateExperience {
  id: string;
  companyName: string;
  companyLogo?: string;
  jobTitle: string;
  employmentType: 'Full-time' | 'Part-time' | 'Contract' | 'Internship';
  location: string;
  startDate: string;
  endDate: string;
  isCurrentJob: boolean;
  description: string;
  achievements?: string[];
  technologiesUsed?: string[];
}
