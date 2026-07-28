export interface BookmarkItem {
  id: string;
  type: 'job' | 'company' | 'article' | 'learning';
  title: string;
  subtitle: string;
  url: string;
  savedDate: string;
  metadata?: Record<string, any>;
}
