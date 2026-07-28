export interface CandidateEducation {
  id: string;
  institutionName: string;
  degree: string;
  branch: string;
  cgpaOrPercentage: string;
  startYear: string;
  endYear: string;
  achievements?: string[];
  relevantCoursework?: string[];
}
