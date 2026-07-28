'use client';

import React from 'react';

export default function SettingsHeader() {
  return (
    <div className="border-b border-[#E2E8F0] pb-5 text-left">
      <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">Account Settings</h1>
      <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">
        Manage your profile details, passwords, visibility criteria, and notification options.
      </p>
    </div>
  );
}
