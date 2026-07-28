'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useSettings } from '@/hooks/useSettings';
import SettingsHeader from '@/components/settings/SettingsHeader';
import SettingsSidebar from '@/components/settings/SettingsSidebar';
import SettingsSearch from '@/components/settings/SettingsSearch';
import SettingsCard from '@/components/settings/SettingsCard';
import ProfileSection from '@/components/settings/ProfileSection';
import PasswordSection from '@/components/settings/PasswordSection';
import SocialLinksSection from '@/components/settings/SocialLinksSection';
import ResumeVisibilitySection from '@/components/settings/ResumeVisibilitySection';
import PrivacySection from '@/components/settings/PrivacySection';
import NotificationSettingsSection from '@/components/settings/NotificationSettingsSection';
import ThemeSection from '@/components/settings/ThemeSection';
import LanguageSection from '@/components/settings/LanguageSection';
import DeleteAccountSection from '@/components/settings/DeleteAccountSection';
import SaveChangesBar from '@/components/settings/SaveChangesBar';
import SettingsToast from '@/components/settings/SettingsToast';
import { Loader2 } from 'lucide-react';

export default function CandidateSettingsPage() {
  const {
    settings,
    loading,
    saving,
    error,
    success,
    updateSettingNode,
    hasUnsavedChanges,
    discardChanges,
    saveSettings,
    changePassword,
    deleteAccount,
  } = useSettings();

  const [activeSection, setActiveSection] = useState('profile');
  const contentAreaRef = useRef<HTMLDivElement>(null);

  // Jump to section helper (for search index navigation clicks)
  const handleJumpToSection = (sectionId: string) => {
    setActiveSection(sectionId);
    // Smooth scroll the content area
    if (contentAreaRef.current) {
      contentAreaRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const getSectionTitleAndDesc = (sectionId: string) => {
    switch (sectionId) {
      case 'password':
        return {
          title: 'Account Password & Credentials Security',
          desc: 'Keep your account secure by rotating passwords regularly.',
        };
      case 'socials':
        return {
          title: 'Social Network Integrations',
          desc: 'Link your developer profiles to stand out on search listings.',
        };
      case 'resume':
        return {
          title: 'Resume Index Visibility settings',
          desc: 'Control how registered organizations see your parsed qualifications resume files.',
        };
      case 'privacy':
        return {
          title: 'Personal Privacy Control panel',
          desc: 'Configure email and phone indexing rules.',
        };
      case 'notifications':
        return {
          title: 'Notifications & Alerts Preferences',
          desc: 'Select which channel digests and alerts to receive.',
        };
      case 'theme':
        return {
          title: 'Interface Themes',
          desc: 'Personalize colors, contrast, and layout visibility styles.',
        };
      case 'language':
        return {
          title: 'Language Parameters',
          desc: 'Update menu parameters display languages.',
        };
      case 'delete':
        return {
          title: 'Danger Zone: Account Deletion',
          desc: 'Permanent profiling cleanup.',
        };
      default:
        return {
          title: 'Profile Personal Information',
          desc: 'Update your display biography and career specifications.',
        };
    }
  };

  const renderActiveSectionContent = () => {
    if (!settings) return null;
    switch (activeSection) {
      case 'password':
        return <PasswordSection onSave={changePassword} />;
      case 'socials':
        return (
          <SocialLinksSection
            socials={settings.socials}
            onChange={(field, val) => updateSettingNode('socials', field, val)}
          />
        );
      case 'resume':
        return (
          <ResumeVisibilitySection
            resume={settings.resume}
            onChange={(field, val) => updateSettingNode('resume', field, val)}
          />
        );
      case 'privacy':
        return (
          <PrivacySection
            privacy={settings.privacy}
            onChange={(field, val) => updateSettingNode('privacy', field, val)}
          />
        );
      case 'notifications':
        return (
          <NotificationSettingsSection
            notifications={settings.notifications}
            onChange={(field, val) => updateSettingNode('notifications', field, val)}
          />
        );
      case 'theme':
        return (
          <ThemeSection
            theme={settings.theme}
            onChange={(val) => updateSettingNode('theme', '', val)}
          />
        );
      case 'language':
        return (
          <LanguageSection
            language={settings.language}
            onChange={(val) => updateSettingNode('language', '', val)}
          />
        );
      case 'delete':
        return <DeleteAccountSection onConfirmDelete={deleteAccount} />;
      default:
        return (
          <ProfileSection
            profile={settings.profile}
            onChange={(field, val) => updateSettingNode('profile', field, val)}
          />
        );
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading account settings...</p>
      </div>
    );
  }

  const { title, desc } = getSectionTitleAndDesc(activeSection);

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto text-[#0F172A]">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <SettingsHeader />
        <SettingsSearch onJumpToSection={handleJumpToSection} />
      </div>

      {/* Split Columns Grid Layout */}
      <div className="grid md:grid-cols-4 gap-6">
        {/* Sidebar Nav */}
        <div className="md:col-span-1">
          <SettingsSidebar activeSection={activeSection} onSectionChange={setActiveSection} />
        </div>

        {/* Content Box */}
        <div ref={contentAreaRef} className="md:col-span-3">
          <SettingsCard title={title} description={desc}>
            {renderActiveSectionContent()}
          </SettingsCard>
        </div>
      </div>

      {/* Save changes footer bar */}
      <SaveChangesBar
        isVisible={hasUnsavedChanges}
        onSave={saveSettings}
        onDiscard={discardChanges}
        saving={saving}
      />

      {/* Success/Error Alerts Toasts */}
      <SettingsToast message={success} type="success" />
      <SettingsToast message={error} type="error" />
    </div>
  );
}
