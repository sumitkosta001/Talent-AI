export interface SearchResultItem {
  id: string;
  title: string;
  subtitle: string;
  category: 'jobs' | 'companies' | 'candidates' | 'recruiters' | 'applications' | 'interviews' | 'skills' | 'projects' | 'resumes' | 'tools' | 'bookmarks' | 'notifications' | 'settings';
  route: string;
  metadata?: Record<string, any>;
}

export interface GroupedSearchResults {
  category: string;
  items: SearchResultItem[];
}
