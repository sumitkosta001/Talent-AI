export interface CultureValue {
  title: string;
  desc: string;
}

export const MOCK_COMPANY_CULTURE: Record<string, CultureValue[]> = {
  stripe: [
    { title: 'Users First', desc: 'We build economic infrastructure for real people run by real businesses.' },
    { title: 'Rigorous Thinking', desc: 'We solve hard problems from first principles, writing down clear rationales.' },
    { title: 'Optimistic Builders', desc: 'We believe the internet GDP is tiny compared to what it will become.' },
  ],
  vercel: [
    { title: 'Developer Obsession', desc: 'We design software that makes developers faster and happier.' },
    { title: 'Speed & Simplicity', desc: 'Fast pages, clean interfaces, and frictionless deploys.' },
  ],
};
