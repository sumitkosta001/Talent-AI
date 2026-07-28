export interface CandidatePortfolioItem {
  id: string;
  type: 'Certificate' | 'Award' | 'Hackathon' | 'Research Paper' | 'Blog' | 'Video';
  title: string;
  description: string;
  date: string;
  url?: string;
}
