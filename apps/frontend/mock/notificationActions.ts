import { NotificationAction } from '../types/notification';

export const MOCK_NOTIFICATION_ACTIONS: NotificationAction[] = [
  {
    label: 'Mark as Read',
    icon: 'Check',
    action: (id: string) => console.log(`Mark read: ${id}`),
  },
  {
    label: 'Delete',
    icon: 'Trash',
    action: (id: string) => console.log(`Delete: ${id}`),
  },
];
