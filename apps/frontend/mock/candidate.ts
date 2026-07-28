export interface CandidateProfile {
  name: string;
  email: string;
  phone: string;
  university: string;
  branch: string;
  cgpa: string;
  resumeScore: number;
  atsScore: number;
  completion: number;
  location: string;
  skills: string[];
}

export const MOCK_CANDIDATE_PROFILE: CandidateProfile = {
  name: 'Sumit Kosta',
  email: 'sumit@example.com',
  phone: '+91 98765 43210',
  university: 'National Institute of Technology, Rourkela',
  branch: 'Computer Science & Engineering',
  cgpa: '8.7/10.0',
  resumeScore: 95,
  atsScore: 92,
  completion: 85,
  location: 'Bangalore, India',
  skills: ['React', 'TypeScript', 'Node.js', 'Next.js', 'System Design', 'Tailwind CSS'],
};
