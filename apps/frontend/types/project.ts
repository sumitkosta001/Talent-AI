export interface CandidateProject {
  id: string;
  projectName: string;
  description: string;
  technologies: string[];
  role: string;
  duration: string;
  githubUrl?: string;
  liveUrl?: string;
  achievements?: string[];
}
