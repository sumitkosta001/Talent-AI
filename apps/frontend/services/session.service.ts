import { SessionStatus } from '@/types/session';
import { MOCK_SESSION_STATUS } from '@/mock/session';

const DEV_MODE = true;

export const sessionService = {
  async getSessionStatus(): Promise<SessionStatus> {
    if (DEV_MODE) {
      await new Promise((r) => setTimeout(r, 200));
      return MOCK_SESSION_STATUS;
    }
    const res = await fetch('/api/auth/session');
    return res.json();
  },

  async extendSession(): Promise<{ success: boolean; message: string }> {
    if (DEV_MODE) {
      await new Promise((r) => setTimeout(r, 300));
      return { success: true, message: 'Session extended by 30 minutes' };
    }
    const res = await fetch('/api/auth/session/refresh', { method: 'POST' });
    return res.json();
  },
};
