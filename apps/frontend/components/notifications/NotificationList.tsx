'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Notification } from '@/types/notification';
import NotificationCard from './NotificationCard';

interface NotificationListProps {
  notifications: Notification[];
  onMarkRead: (id: string, read: boolean) => void;
  onDelete: (id: string) => void;
  onSelect: (notification: Notification) => void;
  activeId?: string;
}

export default function NotificationList({
  notifications,
  onMarkRead,
  onDelete,
  onSelect,
  activeId,
}: NotificationListProps) {
  return (
    <div className="space-y-3">
      <AnimatePresence initial={false}>
        {notifications.map((item) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.15 }}
          >
            <NotificationCard
              notification={item}
              onMarkRead={onMarkRead}
              onDelete={onDelete}
              onSelect={onSelect}
              isActive={item.id === activeId}
            />
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
