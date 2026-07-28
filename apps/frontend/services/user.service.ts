import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { AdminUser, UserRole, UserStatus } from '@/types/user';
import { MOCK_ADMIN_USERS } from '@/mock/users';

export class AdminUserService {
  static getLocalUsers(): AdminUser[] {
    if (typeof window === 'undefined') return MOCK_ADMIN_USERS;
    const stored = localStorage.getItem('talentai_admin_users');
    if (!stored) {
      localStorage.setItem('talentai_admin_users', JSON.stringify(MOCK_ADMIN_USERS));
      return MOCK_ADMIN_USERS;
    }
    return JSON.parse(stored);
  }

  static saveLocalUsers(users: AdminUser[]) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_admin_users', JSON.stringify(users));
  }

  static async getUsers(): Promise<AdminUser[]> {
    if (DEV_MODE) {
      await mockDelay(300);
      return this.getLocalUsers();
    }

    const res = await fetch('/api/admin/users');
    if (!res.ok) throw new Error('Failed to retrieve user accounts');
    return res.json();
  }

  static async getUserById(id: string): Promise<AdminUser | null> {
    if (DEV_MODE) {
      await mockDelay(200);
      const items = this.getLocalUsers();
      return items.find((u) => u.id === id) || null;
    }

    const res = await fetch(`/api/admin/users/${id}`);
    if (!res.ok) throw new Error('Failed to retrieve user data profile');
    return res.json();
  }

  static async updateStatus(id: string, status: UserStatus): Promise<AdminUser> {
    if (DEV_MODE) {
      await mockDelay(300);
      const items = this.getLocalUsers();
      const idx = items.findIndex((u) => u.id === id);
      if (idx === -1) throw new Error('User account not found');

      items[idx].status = status;
      this.saveLocalUsers(items);
      return items[idx];
    }

    const res = await fetch(`/api/admin/users/${id}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    if (!res.ok) throw new Error('Failed to change account status');
    return res.json();
  }

  static async updateRole(id: string, role: UserRole): Promise<AdminUser> {
    if (DEV_MODE) {
      await mockDelay(300);
      const items = this.getLocalUsers();
      const idx = items.findIndex((u) => u.id === id);
      if (idx === -1) throw new Error('User account not found');

      items[idx].role = role;
      this.saveLocalUsers(items);
      return items[idx];
    }

    const res = await fetch(`/api/admin/users/${id}/role`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role }),
    });
    if (!res.ok) throw new Error('Failed to change user role');
    return res.json();
  }

  static async deleteUser(id: string): Promise<boolean> {
    if (DEV_MODE) {
      await mockDelay(200);
      const items = this.getLocalUsers();
      const filtered = items.filter((u) => u.id !== id);
      this.saveLocalUsers(filtered);
      return true;
    }

    const res = await fetch(`/api/admin/users/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to remove user account');
    return true;
  }
}
