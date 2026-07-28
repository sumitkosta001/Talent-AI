import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { CandidatePortfolioItem } from '@/types/portfolio';
import { MOCK_PORTFOLIO } from '@/mock/portfolio';

export class CandidatePortfolioService {
  static getLocalPortfolio(): CandidatePortfolioItem[] {
    if (typeof window === 'undefined') return MOCK_PORTFOLIO;
    const stored = localStorage.getItem('talentai_candidate_portfolio');
    if (!stored) {
      localStorage.setItem('talentai_candidate_portfolio', JSON.stringify(MOCK_PORTFOLIO));
      return MOCK_PORTFOLIO;
    }
    return JSON.parse(stored);
  }

  static saveLocalPortfolio(list: CandidatePortfolioItem[]) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_candidate_portfolio', JSON.stringify(list));
  }

  static async getPortfolio(): Promise<CandidatePortfolioItem[]> {
    if (DEV_MODE) {
      await mockDelay(200);
      return this.getLocalPortfolio();
    }

    const res = await fetch('/api/profile/portfolio');
    if (!res.ok) throw new Error('Failed to retrieve portfolio items');
    return res.json();
  }

  static async addPortfolioItem(item: Partial<CandidatePortfolioItem>): Promise<CandidatePortfolioItem> {
    if (DEV_MODE) {
      await mockDelay(300);
      const list = this.getLocalPortfolio();
      const newI: CandidatePortfolioItem = {
        id: `port-${Date.now()}`,
        type: item.type || 'Certificate',
        title: item.title || 'New Item',
        description: item.description || '',
        date: item.date || new Date().toISOString().split('T')[0],
        url: item.url || '',
      };
      list.unshift(newI);
      this.saveLocalPortfolio(list);
      return newI;
    }

    const res = await fetch('/api/profile/portfolio', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(item),
    });
    if (!res.ok) throw new Error('Failed to create portfolio item');
    return res.json();
  }

  static async deletePortfolioItem(id: string): Promise<boolean> {
    if (DEV_MODE) {
      await mockDelay(200);
      const list = this.getLocalPortfolio();
      const filtered = list.filter((i) => i.id !== id);
      this.saveLocalPortfolio(filtered);
      return true;
    }

    const res = await fetch(`/api/profile/portfolio/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete portfolio item');
    return true;
  }
}
