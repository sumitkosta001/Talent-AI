import { BookmarkItem } from '@/types/bookmark';
import { MOCK_BOOKMARKS } from '@/mock/bookmarks';
import { mockDelay } from '@/lib/mockDelay';

const STORAGE_KEY = 'talentai_candidate_bookmarks';

export class BookmarkService {
  static getLocalBookmarks(): BookmarkItem[] {
    if (typeof window === 'undefined') return MOCK_BOOKMARKS;
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(MOCK_BOOKMARKS));
      return MOCK_BOOKMARKS;
    }
    try {
      return JSON.parse(stored);
    } catch {
      return MOCK_BOOKMARKS;
    }
  }

  static async getBookmarks(): Promise<BookmarkItem[]> {
    await mockDelay(100);
    return this.getLocalBookmarks();
  }

  static async addBookmark(item: Omit<BookmarkItem, 'id' | 'savedDate'>): Promise<BookmarkItem> {
    await mockDelay(100);
    const list = this.getLocalBookmarks();
    const newItem: BookmarkItem = {
      ...item,
      id: `book-${Date.now()}`,
      savedDate: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
    };
    list.unshift(newItem);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
    return newItem;
  }

  static async removeBookmark(id: string): Promise<boolean> {
    await mockDelay(100);
    const list = this.getLocalBookmarks();
    const filtered = list.filter((item) => item.id !== id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
    return true;
  }
}
