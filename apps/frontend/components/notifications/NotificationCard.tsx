'use client';

import React from 'react';
import Link from 'next/link';
import { Mail, MailOpen, Trash2, CheckCircle2, AlertOctagon, Briefcase, Bot, User, Award, ShieldAlert, AlertCircle } from 'lucide-react';
import { Notification } from '@/types/notification';
import NotificationBadge from './NotificationBadge';
import NotificationPriorityBadge from './NotificationPriorityBadge';
import UnreadIndicator from './UnreadIndicator';

interface NotificationCardProps {
  notification: Notification;
  onMarkRead: (id: string, read: boolean) => void;
  onDelete: (id: string) => void;
  onSelect: (notification: Notification) => void;
  isActive: boolean;
}

export default function NotificationCard({
  notification,
  onMarkRead,
  onDelete,
  onSelect,
  isActive,
}: NotificationCardProps) {
  const { id, title, description, timestamp, category, priority, read, relatedRoute } = notification;

  const getCategoryIcon = (cat: string) => {
    switch (cat) {
      case 'Jobs':
        return <Briefcase size={16} className="text-blue-600" />;
      case 'ATS':
        return <Bot size={16} className="text-purple-600" />;
      case 'Applications':
        return <CheckCircle2 size={16} className="text-orange-600" />;
      case 'Recruiters':
        return <User size={16} className="text-pink-600" />;
      case 'Offers':
        return <Award size={16} className="text-emerald-600" />;
      case 'Security':
        return <ShieldAlert size={16} className="text-red-600" />;
      default:
        return <AlertCircle size={16} className="text-slate-500" />;
    }
  };

  const handleMarkReadToggle = (e: React.MouseEvent) => {
    e.stopPropagation();
    onMarkRead(id, !read);
  };

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    onDelete(id);
  };

  return (
    <div
      onClick={() => onSelect(notification)}
      className={`
        border border-[#E2E8F0] p-4 rounded-2xl flex gap-4 transition-all relative text-left cursor-pointer hover:shadow-sm
        ${read ? 'bg-white' : 'bg-blue-50/20 border-blue-100'}
        ${isActive ? 'ring-2 ring-blue-500 border-transparent shadow-sm' : ''}
      `}
    >
      {/* Read/Unread indicator */}
      {!read && (
        <div className="absolute top-4 right-4">
          <UnreadIndicator />
        </div>
      )}

      {/* Leading Category icon */}
      <div className={`w-9 h-9 rounded-xl flex items-center justify-center border flex-shrink-0 bg-[#F8FAFC]`}>
        {getCategoryIcon(category)}
      </div>

      {/* Main Info */}
      <div className="flex-1 space-y-1.5 min-w-0 pr-4">
        <div className="flex items-center gap-2 flex-wrap">
          <NotificationBadge category={category} />
          <NotificationPriorityBadge priority={priority} />
          <span className="text-[10px] text-[#64748B] font-semibold ml-auto">{timestamp}</span>
        </div>

        <h4 className={`text-xs sm:text-sm font-bold text-[#0F172A] line-clamp-1 ${read ? '' : 'font-extrabold'}`}>
          {title}
        </h4>
        <p className="text-xs text-[#64748B] line-clamp-2 leading-relaxed">{description}</p>

        <div className="flex items-center justify-between pt-1">
          {relatedRoute ? (
            <Link
              href={relatedRoute}
              onClick={(e) => {
                e.stopPropagation();
                onMarkRead(id, true);
              }}
              className="text-[10px] font-bold text-blue-600 hover:underline inline-flex items-center gap-0.5"
            >
              Action Needed
            </Link>
          ) : (
            <div />
          )}

          {/* Inline option Actions */}
          <div className="flex items-center gap-1">
            <button
              onClick={handleMarkReadToggle}
              className="p-1 text-slate-400 hover:text-[#2563EB] hover:bg-[#F1F5F9] rounded-lg transition-colors cursor-pointer"
              title={read ? 'Mark as unread' : 'Mark as read'}
            >
              {read ? <Mail size={13} /> : <MailOpen size={13} />}
            </button>
            <button
              onClick={handleDelete}
              className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
              title="Delete notification"
            >
              <Trash2 size={13} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
