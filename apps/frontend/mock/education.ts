import { CandidateEducation } from '../types/education';

export const MOCK_EDUCATION: CandidateEducation[] = [
  {
    id: 'edu-1',
    institutionName: 'Stanford University',
    degree: 'Master of Science',
    branch: 'Computer Science',
    cgpaOrPercentage: '3.9 GPA',
    startYear: '2020',
    endYear: '2021',
    achievements: ['Specialized in Human-Computer Interaction.', 'Graduate teaching assistant for Web Technologies.'],
    relevantCoursework: ['Advanced UI Architecture', 'System Scaling', 'Databases Systems'],
  },
];
