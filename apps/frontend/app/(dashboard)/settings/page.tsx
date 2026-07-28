'use client';

import React, { useState } from 'react';
import { User, Lock, Bell, Palette, Shield, Eye, EyeOff, Camera, Trash2 } from 'lucide-react';

const tabs = [
  { id: 'profile', label: 'Profile', icon: User },
  { id: 'password', label: 'Password', icon: Lock },
  { id: 'notifications', label: 'Notifications', icon: Bell },
  { id: 'appearance', label: 'Appearance', icon: Palette },
  { id: 'account', label: 'Account', icon: Shield },
];

export default function Settings() {
  const [activeTab, setActiveTab] = useState('profile');
  const [showPass, setShowPass] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [compact, setCompact] = useState(false);

  const Toggle = ({ checked, onChange }: { checked: boolean; onChange: () => void }) => (
    <button
      onClick={onChange}
      className={`relative w-10 h-5.5 rounded-full transition-colors flex-shrink-0 cursor-pointer ${
        checked ? 'bg-[#2563EB]' : 'bg-[#CBD5E1]'
      }`}
      style={{ height: 22, width: 40 }}
    >
      <div
        className={`absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-all ${
          checked ? 'left-5' : 'left-0.5'
        }`}
      />
    </button>
  );

  return (
    <div className="p-6 space-y-5 max-w-4xl mx-auto">
      <div>
        <h1 className="text-xl font-bold text-[#0F172A]">Settings</h1>
        <p className="text-sm text-[#64748B] mt-0.5">Manage your account preferences and settings</p>
      </div>

      <div className="flex gap-6">
        {/* Sidebar tabs */}
        <div className="w-48 flex-shrink-0">
          <nav className="space-y-1">
            {tabs.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={`w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors cursor-pointer text-left ${
                  activeTab === id
                    ? 'bg-[#2563EB] text-white'
                    : 'text-[#64748B] hover:bg-[#F1F5F9] hover:text-[#0F172A]'
                }`}
              >
                <Icon size={16} />
                {label}
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="flex-1 space-y-5">
          {activeTab === 'profile' && (
            <div className="space-y-5">
              <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6">
                <h2 className="font-semibold text-[#0F172A] mb-5">Profile Information</h2>
                {/* Avatar */}
                <div className="flex items-center gap-4 mb-6">
                  <div className="relative">
                    <div className="w-16 h-16 rounded-full bg-[#2563EB] flex items-center justify-center text-white text-2xl font-bold">AJ</div>
                    <button className="absolute -bottom-1 -right-1 w-6 h-6 bg-white border border-[#E2E8F0] rounded-full flex items-center justify-center hover:bg-[#F8FAFC] shadow-sm cursor-pointer">
                      <Camera size={11} className="text-[#64748B]" />
                    </button>
                  </div>
                  <div>
                    <p className="font-medium text-[#0F172A] text-sm">Alex Johnson</p>
                    <p className="text-xs text-[#64748B]">Candidate</p>
                    <button className="text-xs text-[#2563EB] mt-1 hover:underline cursor-pointer">
                      Change photo
                    </button>
                  </div>
                </div>

                <div className="grid sm:grid-cols-2 gap-4">
                  {[
                    { label: 'First Name', val: 'Alex' },
                    { label: 'Last Name', val: 'Johnson' },
                    { label: 'Email Address', val: 'alex@example.com' },
                    { label: 'Phone Number', val: '+1 (555) 234-5678' },
                    { label: 'Location', val: 'San Francisco, CA' },
                    { label: 'LinkedIn', val: 'linkedin.com/in/alexjohnson' },
                  ].map(({ label, val }) => (
                    <div key={label}>
                      <label className="block text-xs font-medium text-[#64748B] mb-1.5">{label}</label>
                      <input
                        defaultValue={val}
                        className="w-full px-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-slate-900 placeholder-[#94A3B8] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-colors"
                      />
                    </div>
                  ))}
                </div>

                <div className="mt-4">
                  <label className="block text-xs font-medium text-[#64748B] mb-1.5">Bio</label>
                  <textarea
                    defaultValue="Senior Frontend Engineer with 5+ years building scalable React applications."
                    rows={3}
                    className="w-full px-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-slate-900 placeholder-[#94A3B8] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] resize-none"
                  />
                </div>

                <button className="mt-4 bg-[#2563EB] text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-[#1D4ED8] transition-colors cursor-pointer">
                  Save Changes
                </button>
              </div>
            </div>
          )}

          {activeTab === 'password' && (
            <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6">
              <h2 className="font-semibold text-[#0F172A] mb-5">Change Password</h2>
              <div className="space-y-4 max-w-sm">
                {['Current Password', 'New Password', 'Confirm New Password'].map((label) => (
                  <div key={label}>
                    <label className="block text-xs font-medium text-[#64748B] mb-1.5">{label}</label>
                    <div className="relative">
                      <input
                        type={showPass ? 'text' : 'password'}
                        placeholder="••••••••"
                        className="w-full px-3 py-2.5 pr-10 border border-[#E2E8F0] rounded-xl text-sm text-slate-900 placeholder-[#94A3B8] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB]"
                      />
                      <button
                        onClick={() => setShowPass(!showPass)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-[#94A3B8] cursor-pointer"
                      >
                        {showPass ? <EyeOff size={15} /> : <Eye size={15} />}
                      </button>
                    </div>
                  </div>
                ))}
                <button className="bg-[#2563EB] text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-[#1D4ED8] transition-colors cursor-pointer">
                  Update Password
                </button>
              </div>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6">
              <h2 className="font-semibold text-[#0F172A] mb-5">Notification Preferences</h2>
              <div className="space-y-4">
                {[
                  { label: 'New job matches', desc: 'Get notified when new jobs match your profile' },
                  { label: 'Application updates', desc: 'Status changes on your applications' },
                  { label: 'Interview reminders', desc: 'Reminders before scheduled interviews' },
                  { label: 'ATS score updates', desc: 'When your resume score changes' },
                  { label: 'Weekly digest', desc: 'Weekly summary of your job search activity' },
                  { label: 'Marketing emails', desc: 'Tips, news, and product updates' },
                ].map(({ label, desc }, i) => (
                  <div
                    key={label}
                    className="flex items-center justify-between py-2 border-b border-[#F8FAFC] last:border-0"
                  >
                    <div>
                      <p className="text-sm font-medium text-[#0F172A]">{label}</p>
                      <p className="text-xs text-[#64748B]">{desc}</p>
                    </div>
                    <Toggle checked={i < 4} onChange={() => {}} />
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'appearance' && (
            <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6">
              <h2 className="font-semibold text-[#0F172A] mb-5">Appearance</h2>
              <div className="space-y-5">
                <div>
                  <p className="text-sm font-medium text-[#0F172A] mb-3">Theme</p>
                  <div className="grid grid-cols-3 gap-3">
                    {[
                      { label: 'Light', bg: 'bg-white border-[#2563EB]', active: !darkMode },
                      { label: 'Dark', bg: 'bg-[#0F172A] border-[#E2E8F0]', active: darkMode },
                      {
                        label: 'System',
                        bg: 'bg-gradient-to-r from-white to-[#0F172A] border-[#E2E8F0]',
                        active: false,
                      },
                    ].map(({ label, bg, active }) => (
                      <button
                        key={label}
                        onClick={() => setDarkMode(label === 'Dark')}
                        className={`h-20 rounded-xl border-2 flex items-end p-2 cursor-pointer ${bg} ${
                          active ? 'border-[#2563EB]' : 'border-[#E2E8F0]'
                        }`}
                      >
                        <span
                          className={`text-xs font-medium ${
                            label === 'Dark' ? 'text-white' : 'text-[#0F172A]'
                          }`}
                        >
                          {label}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
                <div className="flex items-center justify-between py-3 border-t border-[#E2E8F0]">
                  <div>
                    <p className="text-sm font-medium text-[#0F172A]">Compact mode</p>
                    <p className="text-xs text-[#64748B]">Reduce spacing in the interface</p>
                  </div>
                  <Toggle checked={compact} onChange={() => setCompact(!compact)} />
                </div>
              </div>
            </div>
          )}

          {activeTab === 'account' && (
            <div className="space-y-5">
              <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6">
                <h2 className="font-semibold text-[#0F172A] mb-4">Account Information</h2>
                <div className="space-y-3 text-sm">
                  {[
                    { label: 'Account ID', val: 'usr_8Xk9mN2pQ' },
                    { label: 'Plan', val: 'Pro — $19/month' },
                    { label: 'Member since', val: 'January 15, 2025' },
                    { label: 'Last login', val: 'Today at 9:42 AM' },
                  ].map(({ label, val }) => (
                    <div
                      key={label}
                      className="flex justify-between py-2 border-b border-[#F8FAFC] last:border-0"
                    >
                      <span className="text-[#64748B]">{label}</span>
                      <span className="font-medium text-[#0F172A]">{val}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="bg-red-50 rounded-2xl border border-red-100 p-5">
                <h3 className="font-semibold text-[#EF4444] mb-2 flex items-center gap-2">
                  <Trash2 size={15} />
                  Delete Account
                </h3>
                <p className="text-xs text-red-700 mb-4">
                  This action is permanent and cannot be undone. All your data including applications,
                  resume analysis, and settings will be permanently deleted.
                </p>
                <button className="text-sm font-semibold text-[#EF4444] border border-[#EF4444] px-4 py-2 rounded-xl hover:bg-red-100 transition-colors cursor-pointer">
                  Delete My Account
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
