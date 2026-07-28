import { SearchResultItem } from '@/types/search';
import { MOCK_SEARCH_ITEMS } from '@/mock/search';
import { mockDelay } from '@/lib/mockDelay';

export class SearchService {
  static async search(query: string, category?: string): Promise<SearchResultItem[]> {
    await mockDelay(150);
    const cleaned = query.trim().toLowerCase();
    if (!cleaned) return [];

    return MOCK_SEARCH_ITEMS.filter((item) => {
      const matchesQuery =
        item.title.toLowerCase().includes(cleaned) ||
        item.subtitle.toLowerCase().includes(cleaned);
      const matchesCategory = !category || category === 'all' || item.category === category;
      return matchesQuery && matchesCategory;
    });
  }
}
