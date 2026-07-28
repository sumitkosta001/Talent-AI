import { Metadata } from 'next';

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://talentai.com';

interface SEOOptions {
  title: string;
  description: string;
  keywords?: string[];
  canonicalPath?: string;
  ogImage?: string;
  noIndex?: boolean;
}

export function buildMetadata({
  title,
  description,
  keywords = [],
  canonicalPath = '',
  ogImage = '/og-image.png',
  noIndex = false,
}: SEOOptions): Metadata {
  const fullTitle = `${title} | TalentAI - Enterprise Recruitment & AI Career Tools`;
  const canonicalUrl = `${BASE_URL}${canonicalPath}`;
  const defaultKeywords = [
    'TalentAI', 'AI Recruitment', 'ATS Resume Optimization', 'AI Career Coach',
    'Tech Hiring Platform', 'Job Board', 'Smart Candidate Matching',
  ];
  const allKeywords = Array.from(new Set([...defaultKeywords, ...keywords]));

  return {
    title: fullTitle,
    description,
    keywords: allKeywords,
    alternates: {
      canonical: canonicalUrl,
    },
    openGraph: {
      title: fullTitle,
      description,
      url: canonicalUrl,
      siteName: 'TalentAI',
      images: [
        {
          url: `${BASE_URL}${ogImage}`,
          width: 1200,
          height: 630,
          alt: title,
        },
      ],
      type: 'website',
    },
    twitter: {
      card: 'summary_large_image',
      title: fullTitle,
      description,
      images: [`${BASE_URL}${ogImage}`],
      creator: '@TalentAI',
    },
    robots: {
      index: !noIndex,
      follow: !noIndex,
    },
  };
}

export function buildJobPostingSchema(job: {
  title: string;
  description: string;
  companyName: string;
  location: string;
  salary?: string;
  datePosted?: string;
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'JobPosting',
    title: job.title,
    description: job.description,
    hiringOrganization: {
      '@type': 'Organization',
      name: job.companyName,
    },
    jobLocation: {
      '@type': 'Place',
      address: {
        '@type': 'PostalAddress',
        addressLocality: job.location,
      },
    },
    datePosted: job.datePosted || new Date().toISOString(),
  };
}

export function buildOrganizationSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'TalentAI',
    url: BASE_URL,
    logo: `${BASE_URL}/logo.png`,
    sameAs: [
      'https://twitter.com/talentai',
      'https://linkedin.com/company/talentai',
      'https://github.com/talentai',
    ],
  };
}
