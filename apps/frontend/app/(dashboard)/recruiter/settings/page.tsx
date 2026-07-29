'use client';

import React, { useState } from 'react';
import { Save, User, Bell, Clock, Paintbrush } from 'lucide-react';

export default function RecruiterSettingsPage() {
  const [name, setName] = useState('Sarah Mitchell');
  const [role, setRole] = useState('Principal Talent Acquisition Lead');
  const [email, setEmail] = useState('sarah.mitchell@talentai.co');
  
  const [emailAlerts, setEmailAlerts] = useState(true);
  const [atsAlerts, setAtsAlerts] = useState(true);
  const [weeklyDigest, setWeeklyDigest] = useState(true);
  
  const [duration, setDuration] = useState('45');
  const [brandColor, setBrandColor] = useState('Blue');

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    alert('Recruiter profile settings changes saved successfully!');
  };

  return (
    <div className="p-6 space-y-6 max-w-4xl mx-auto text-[#0F172A] text-left">
      <div className="border-b border-[#E2E8F0] pb-5">
        <h1 className="text-xl sm:text-2xl font-bold">Recruiter Settings</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">Configure your recruiter profile details and notification parameters.</p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Profile Card */}
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 sm:p-6 shadow-sm space-y-4">
          <h3 className="font-bold text-xs uppercase tracking-wider text-[#64748B] border-b border-[#F1F5F9] pb-2 flex items-center gap-1.5">
            <User size={14} /> Profile Information
          </h3>

          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-[#475569] mb-1.5">Display Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-[#475569] mb-1.5">Corporate Role</label>
              <input
                type="text"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>

            <div className="sm:col-span-2">
              <label className="block text-xs font-bold text-[#475569] mb-1.5">Email Address</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
          </div>
        </div>

        {/* Notifications & Prefs */}
        <div className="grid sm:grid-cols-2 gap-6">
          {/* Notifications config */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <h3 className="font-bold text-xs uppercase tracking-wider text-[#64748B] border-b border-[#F1F5F9] pb-2 flex items-center gap-1.5">
              <Bell size={14} /> Notifications Alerts
            </h3>
            
            <div className="space-y-3.5">
              {[
                { label: 'Email Notifications', desc: 'Alert me whenever new candidates apply.', checked: emailAlerts, set: setEmailAlerts },
                { label: 'ATS Score Matches', desc: 'Alert me of applicants scoring 90% or above.', checked: atsAlerts, set: setAtsAlerts },
                { label: 'Weekly Summary Digest', desc: 'Consolidated weekend recruitment report.', checked: weeklyDigest, set: setWeeklyDigest },
              ].map(({ label, desc, checked, set }) => (
                <div key={label} className="flex items-start justify-between gap-4 py-1 text-xs">
                  <div>
                    <span className="font-bold text-slate-800">{label}</span>
                    <p className="text-[10px] text-slate-500 mt-0.5 leading-relaxed">{desc}</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={checked}
                    onChange={(e) => set(e.target.checked)}
                    className="w-4.5 h-4.5 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer"
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Hiring preferences */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <h3 className="font-bold text-xs uppercase tracking-wider text-[#64748B] border-b border-[#F1F5F9] pb-2 flex items-center gap-1.5">
              <Clock size={14} /> Interview Schedules
            </h3>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-[#475569] mb-1.5">Default Slot Duration</label>
                <select
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                  className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
                >
                  <option value="30">30 minutes</option>
                  <option value="45">45 minutes</option>
                  <option value="60">60 minutes</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#475569] mb-1.5">Mock Branding Accent</label>
                <select
                  value={brandColor}
                  onChange={(e) => setBrandColor(e.target.value)}
                  className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
                >
                  <option value="Blue">Classic Blue (Default)</option>
                  <option value="Emerald">Forest Green</option>
                  <option value="Violet">Deep Violet</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            className="inline-flex items-center gap-1.5 bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold text-xs px-4 py-2.5 rounded-xl transition-colors cursor-pointer"
          >
            <Save size={14} />
            Save Settings
          </button>
        </div>
      </form>
    </div>
  );
}
