export interface CandidateSkill {
  id: string;
  name: string;
  level: 'Beginner' | 'Intermediate' | 'Expert';
  yearsOfExperience: number;
  endorsementsCount?: number;
}
