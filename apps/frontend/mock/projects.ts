import { CandidateProject } from '../types/project';

export const MOCK_PROJECTS: CandidateProject[] = [
  {
    id: 'proj-1',
    projectName: 'TalentAI Recruitment Dashboard',
    description: 'An AI-powered applicant evaluation portal integrating resume analysis, real-time pipelines, and diagnostic trackers.',
    technologies: ['Next.js', 'React', 'Tailwind CSS', 'Recharts'],
    role: 'Lead Architect',
    duration: '3 months',
    githubUrl: 'https://github.com/alexjohnson/talentai-frontend',
    liveUrl: 'https://talentai.co',
    achievements: ['Designed HSL color responsive sidebar system.', 'Aggregated system KPIs grids dashboards.'],
  },
];
