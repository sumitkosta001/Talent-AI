import { Timeline } from '../types/ats';

export const MOCK_TIMELINE: Timeline[] = [
  { step: 1, title: 'Improve Resume Summary', description: 'Rewrite summary using strong action hooks and direct years of experience.', status: 'completed' },
  { step: 2, title: 'Inject Quantified Metrics', description: 'Modify work experience points to include numbers, percentages, and metrics.', status: 'in-progress' },
  { step: 3, title: 'Optimize Tech Stack Keywords', description: 'Add Kubernetes, Terraform, and GraphQL keywords into project details.', status: 'pending' },
  { step: 4, title: 'Update Formatting Details', description: 'Align margins, verify standard typography, and clean redundant spacers.', status: 'pending' },
  { step: 5, title: 'Increase ATS Score', description: 'Run validation checks to verify score raises above 95/100.', status: 'pending' }
];
