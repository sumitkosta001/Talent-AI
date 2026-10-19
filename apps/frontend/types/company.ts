export interface Company {
  id: string;
  name: string;
  description?: string | null;
  location?: string | null;
  website?: string | null;
  logo_url?: string | null;
  industry?: string | null;
  logo?: string;
  logoColor?: string;
  employees?: string;
  rating?: number;
  openPositions?: number;
  about?: string;
  founded?: string;
  headquarters?: string;
  stage?: string;
  totalRaised?: string;
  valuation?: string;
  techStack?: string[];
}

export interface CompanyDetail {
  name: string;
  logo: string;
  logoColor: string;
  bannerUrl?: string;
  about: string;
  industry: string;
  website: string;
  location: string;
  employees: string;
  founded: string;
  culture: string[];
  benefits: string[];
  hiringTeam: {
    name: string;
    role: string;
    avatar?: string;
  }[];
  socials: {
    linkedin?: string;
    twitter?: string;
    github?: string;
  };
}
