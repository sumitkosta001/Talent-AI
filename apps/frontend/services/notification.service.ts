import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { Notification, NotificationStats } from '@/types/notification';
import { MOCK_NOTIFICATIONS } from '@/mock/notifications';
import { calculateNotificationStats } from '@/mock/notificationStats';

export class NotificationService {
  static getLocalNotifications(): Notification[] {
    if (typeof window === 'undefined') return MOCK_NOTIFICATIONS;
    const stored = localStorage.getItem('talentai_notifications');
    if (!stored) {
      localStorage.setItem('talentai_notifications', JSON.stringify(MOCK_NOTIFICATIONS));
      return MOCK_NOTIFICATIONS;
    }
    return JSON.parse(stored);
  }

  static saveLocalNotifications(notifs: Notification[]) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_notifications', JSON.stringify(notifs));
  }

  static async getNotifications(): Promise<Notification[]> {
    if (DEV_MODE) {
      await mockDelay(200);
      return this.getLocalNotifications();
    }

    const res = await fetch('/api/notifications');
    if (!res.ok) throw new Error('Failed to fetch notifications');
    return res.json();
  }

  static async getNotificationById(id: string): Promise<Notification | null> {
    if (DEV_MODE) {
      await mockDelay(100);
      const notifs = this.getLocalNotifications();
      return notifs.find(n => n.id === id) || null;
    }

    const res = await fetch(`/api/notifications/${id}`);
    if (!res.ok) throw new Error('Failed to fetch notification detail');
    return res.json();
  }

  static async toggleRead(id: string, read: boolean): Promise<Notification> {
    if (DEV_MODE) {
      await mockDelay(100);
      const notifs = this.getLocalNotifications();
      const idx = notifs.findIndex(n => n.id === id);
      if (idx === -1) throw new Error('Notification not found');
      notifs[idx].read = read;
      this.saveLocalNotifications(notifs);
      return notifs[idx];
    }

    const res = await fetch(`/api/notifications/${id}/read`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ read }),
    });
    if (!res.ok) throw new Error('Failed to toggle read state');
    return res.json();
  }

  static async markAllRead(): Promise<Notification[]> {
    if (DEV_MODE) {
      await mockDelay(300);
      const notifs = this.getLocalNotifications();
      const updated = notifs.map(n => ({ ...n, read: true }));
      this.saveLocalNotifications(updated);
      return updated;
    }

    const res = await fetch('/api/notifications/read-all', { method: 'PATCH' });
    if (!res.ok) throw new Error('Failed to mark all read');
    return res.json();
  }

  static async deleteNotification(id: string): Promise<boolean> {
    if (DEV_MODE) {
      await mockDelay(200);
      const notifs = this.getLocalNotifications();
      const filtered = notifs.filter(n => n.id !== id);
      this.saveLocalNotifications(filtered);
      return true;
    }

    const res = await fetch(`/api/notifications/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete notification');
    return true;
  }

  static async clearAll(): Promise<boolean> {
    if (DEV_MODE) {
      await mockDelay(200);
      this.saveLocalNotifications([]);
      return true;
    }

    const res = await fetch('/api/notifications', { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to clear notifications');
    return true;
  }

  static async getStats(): Promise<NotificationStats> {
    if (DEV_MODE) {
      await mockDelay(200);
      const notifs = this.getLocalNotifications();
      return calculateNotificationStats(notifs);
    }

    const res = await fetch('/api/notifications/stats');
    if (!res.ok) throw new Error('Failed to fetch stats');
    return res.json();
  }
}
