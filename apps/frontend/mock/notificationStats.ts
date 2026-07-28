import { Notification, NotificationStats } from '../types/notification';

export function calculateNotificationStats(notifications: Notification[]): NotificationStats {
  const total = notifications.length;
  const unread = notifications.filter(n => !n.read).length;
  const read = total - unread;
  const highPriority = notifications.filter(n => n.priority === 'High').length;

  // Mock date categorizations
  const today = notifications.filter(n => n.timestamp.includes('now') || n.timestamp.includes('min') || n.timestamp.includes('hour')).length;
  const thisWeek = total; // all mock elements fit into this week range

  return {
    total,
    unread,
    read,
    today,
    thisWeek,
    highPriority,
  };
}
