'use client';

import React, { useState } from 'react';
import { Bell, CheckCheck, Trash2, Briefcase, UserCheck, Calendar, Bot, Clock } from 'lucide-react';

const allNotifications = [
  { id: 1, type: 'interview', icon: Calendar, title: 'Interview Scheduled', msg: 'Stripe has scheduled a technical interview for Jul 18, 2025 at 2:00 PM PST.', time: '2 hours ago', read: false, color: 'bg-blue-100 text-blue-600' },
  { id: 2, type: 'application', icon: UserCheck, title: 'Application Shortlisted', msg: 'Linear has shortlisted your application for Product Designer.', time: '5 hours ago', read: false, color: 'bg-green-100 text-green-600' },
  { id: 3, type: 'job', icon: Briefcase, title: 'New Job Match', msg: '3 new jobs match your profile: React Engineer at Figma, Staff SWE at Vercel, and more.', time: '1 day ago', read: false, color: 'bg-violet-100 text-violet-600' },
  { id: 4, type: 'ats', icon: Bot, title: 'ATS Analysis Complete', msg: 'Your resume scored 92/100. View detailed suggestions to improve further.', time: '2 days ago', read: true, color: 'bg-amber-100 text-amber-600' },
  { id: 5, type: 'application', icon: Trash2, title: 'Application Update', msg: 'Your application at Notion has been closed. Keep applying!', time: '3 days ago', read: true, color: 'bg-red-100 text-red-600' },
  { id: 6, type: 'job', icon: Briefcase, title: 'Saved Job Closing Soon', msg: 'The DevOps Engineer role at GitHub closes in 3 days. Apply now!', time: '4 days ago', read: true, color: 'bg-orange-100 text-orange-600' },
  { id: 7, type: 'interview', icon: Calendar, title: 'Interview Reminder', msg: 'You have a phone screen with Supabase tomorrow at 10:00 AM PST.', time: '1 week ago', read: true, color: 'bg-blue-100 text-blue-600' },
];

export default function Notifications() {
  const [notifications, setNotifications] = useState(allNotifications);
  const [filter, setFilter] = useState('all');

  const unreadCount = notifications.filter(n => !n.read).length;

  const markAllRead = () => setNotifications(n => n.map(x => ({ ...x, read: true })));
  const markRead = (id: number) => setNotifications(n => n.map(x => x.id === id ? { ...x, read: true } : x));
  const deleteOne = (id: number) => setNotifications(n => n.filter(x => x.id !== id));

  const filtered = notifications.filter(n => {
    if (filter === 'unread') return !n.read;
    if (filter === 'read') return n.read;
    return true;
  });

  return (
    <div className="p-6 space-y-5 max-w-2xl mx-auto">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-xl font-bold text-[#0F172A]">Notifications</h1>
          {unreadCount > 0 && (
            <span className="text-xs font-semibold bg-[#EF4444] text-white px-2 py-0.5 rounded-full">{unreadCount}</span>
          )}
        </div>
        <button onClick={markAllRead} className="flex items-center gap-1.5 text-sm text-[#2563EB] hover:underline font-medium cursor-pointer">
          <CheckCheck size={15} />
          Mark all read
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-1 bg-[#F1F5F9] p-1 rounded-xl w-fit">
        {[['all', 'All'], ['unread', 'Unread'], ['read', 'Read']].map(([val, label]) => (
          <button
            key={val}
            onClick={() => setFilter(val)}
            className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors cursor-pointer ${filter === val ? 'bg-white text-[#0F172A] shadow-sm' : 'text-[#64748B] hover:text-[#0F172A]'}`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Notification list */}
      <div className="space-y-2">
        {filtered.length === 0 ? (
          <div className="text-center py-16">
            <Bell size={40} className="mx-auto text-[#E2E8F0] mb-3" />
            <p className="text-[#64748B] font-medium">No notifications</p>
            <p className="text-xs text-[#94A3B8] mt-1">You're all caught up!</p>
          </div>
        ) : filtered.map(({ id, icon: Icon, title, msg, time, read, color }) => (
          <div
            key={id}
            className={`flex items-start gap-4 p-4 rounded-2xl border transition-all ${
              read ? 'bg-white border-[#E2E8F0]' : 'bg-blue-50/50 border-blue-100'
            }`}
          >
            <div className={`w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 ${color}`}>
              <Icon size={16} />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between gap-2">
                <p className={`text-sm font-semibold ${read ? 'text-[#64748B]' : 'text-[#0F172A]'}`}>{title}</p>
                {!read && <div className="w-2 h-2 rounded-full bg-[#2563EB] mt-1.5 flex-shrink-0" />}
              </div>
              <p className="text-xs text-[#64748B] mt-0.5 leading-relaxed">{msg}</p>
              <p className="text-xs text-[#94A3B8] mt-1.5 flex items-center gap-1"><Clock size={10} />{time}</p>
            </div>
            <div className="flex items-center gap-1 flex-shrink-0">
              {!read && (
                <button onClick={() => markRead(id)} className="p-1.5 text-[#94A3B8] hover:text-[#2563EB] rounded-lg hover:bg-blue-50 transition-colors cursor-pointer" title="Mark as read">
                  <CheckCheck size={14} />
                </button>
              )}
              <button onClick={() => deleteOne(id)} className="p-1.5 text-[#94A3B8] hover:text-[#EF4444] rounded-lg hover:bg-red-50 transition-colors cursor-pointer">
                <Trash2 size={14} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
