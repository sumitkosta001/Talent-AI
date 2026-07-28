'use client';

import React from 'react';
import { NotificationSettings } from '@/types/settings';
import ToggleSetting from './ToggleSetting';

interface NotificationSettingsSectionProps {
  notifications?: NotificationSettings;
  onChange: (field: keyof NotificationSettings, value: boolean) => void;
}

export default function NotificationSettingsSection({
  notifications,
  onChange,
}: NotificationSettingsSectionProps) {
  if (!notifications) return null;

  return (
    <div className="space-y-4 text-left">
      <div className="space-y-2">
        <h4 className="text-xs font-bold text-[#64748B] uppercase tracking-wide">Category Updates</h4>
        <ToggleSetting
          label="Job Recommendations"
          description="Alert me whenever a new job matches my parsed skills index."
          checked={notifications.jobRecommendations}
          onChange={(val) => onChange('jobRecommendations', val)}
        />
        <ToggleSetting
          label="ATS Updates"
          description="Alert me whenever my ATS score improves or profile optimization suggestions change."
          checked={notifications.atsUpdates}
          onChange={(val) => onChange('atsUpdates', val)}
        />
        <ToggleSetting
          label="Recruiter Messages"
          description="Notify me instantly when a hiring coordinator messages my profile."
          checked={notifications.recruiterMessages}
          onChange={(val) => onChange('recruiterMessages', val)}
        />
        <ToggleSetting
          label="Interview Reminders"
          description="Notify me of scheduled coding panels 24 hours in advance."
          checked={notifications.interviewReminders}
          onChange={(val) => onChange('interviewReminders', val)}
        />
        <ToggleSetting
          label="Offer Notifications"
          description="Alert me instantly when a company issues a written job offer letter."
          checked={notifications.offerNotifications}
          onChange={(val) => onChange('offerNotifications', val)}
        />
        <ToggleSetting
          label="Resume Reminders"
          description="Notify me if my uploaded resume file has been inactive for over 90 days."
          checked={notifications.resumeReminder}
          onChange={(val) => onChange('resumeReminder', val)}
        />
      </div>

      <div className="border-t border-[#F1F5F9] pt-4 space-y-2">
        <h4 className="text-xs font-bold text-[#64748B] uppercase tracking-wide">Delivery Channels</h4>
        <ToggleSetting
          label="Email Notifications"
          description="Receive matching summaries, letters, and interview details directly at your inbox."
          checked={notifications.email}
          onChange={(val) => onChange('email', val)}
        />
        <ToggleSetting
          label="Push Notifications"
          description="Receive browser alerts for recruiter messages and updates."
          checked={notifications.push}
          onChange={(val) => onChange('push', val)}
        />
        <ToggleSetting
          label="SMS Text Alerts"
          description="Receive urgent mobile notifications for interview slots."
          checked={notifications.sms}
          onChange={(val) => onChange('sms', val)}
        />
      </div>

      <div className="border-t border-[#F1F5F9] pt-4 space-y-2">
        <h4 className="text-xs font-bold text-[#64748B] uppercase tracking-wide">Digest Settings</h4>
        <ToggleSetting
          label="Weekly Digest"
          description="Receive a consolidated weekend summary of applications progress."
          checked={notifications.weeklyDigest}
          onChange={(val) => onChange('weeklyDigest', val)}
        />
        <ToggleSetting
          label="Monthly Report"
          description="Receive a monthly statistical review of response ratios."
          checked={notifications.monthlyReport}
          onChange={(val) => onChange('monthlyReport', val)}
        />
      </div>
    </div>
  );
}
