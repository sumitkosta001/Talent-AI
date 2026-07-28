'use client';

import React, { useState } from 'react';
import { useProfile } from '@/hooks/useProfile';
import ProfileBanner from '@/components/profile/ProfileBanner';
import ProfileHeader from '@/components/profile/ProfileHeader';
import ProfileSidebar from '@/components/profile/ProfileSidebar';
import ProfileOverview from '@/components/profile/ProfileOverview';
import ExperienceSection from '@/components/profile/ExperienceSection';
import EducationSection from '@/components/profile/EducationSection';
import ProjectsSection from '@/components/profile/ProjectsSection';
import SkillsSection from '@/components/profile/SkillsSection';
import PortfolioSection from '@/components/profile/PortfolioSection';
import SocialAccountsSection from '@/components/profile/SocialAccountsSection';
import ResumeSection from '@/components/profile/ResumeSection';
import ActivityTimeline from '@/components/profile/ActivityTimeline';
import { Loader2 } from 'lucide-react';

type ProfileTab = 'overview' | 'experience' | 'education' | 'projects' | 'skills' | 'portfolio' | 'socials' | 'resume' | 'activity';

export default function CandidateProfilePage() {
  const { profile, loading, error, updateProfile } = useProfile();
  const [activeTab, setActiveTab] = useState<ProfileTab>('overview');

  const [isEditing, setIsEditing] = useState(false);

  // Edit fields state
  const [name, setName] = useState('');
  const [headline, setHeadline] = useState('');
  const [loc, setLoc] = useState('');
  const [bio, setBio] = useState('');

  // Pre-populate fields on edit toggle
  const handleEditToggle = () => {
    if (profile) {
      setName(profile.name);
      setHeadline(profile.headline);
      setLoc(profile.location);
      setBio(profile.bio);
    }
    setIsEditing(!isEditing);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    const ok = await updateProfile({
      name,
      headline,
      location: loc,
      bio,
    });
    if (ok) {
      alert('Profile details saved successfully.');
      setIsEditing(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading your candidate portfolio...</p>
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12 text-[#0F172A]">
        <h3 className="text-red-500 font-bold text-lg">Error Loading Profile</h3>
        <p className="text-sm text-[#64748B]">{error || 'Profile loading failed'}</p>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-6xl mx-auto text-[#0F172A] text-left space-y-6">
      {/* Header and Banner */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] overflow-hidden shadow-sm">
        <ProfileBanner />
        <ProfileHeader profile={profile} onEditToggle={handleEditToggle} />
      </div>

      {/* Edit Dialog Drawer */}
      {isEditing && (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-xs sm:text-sm">
          <h3 className="font-bold text-sm sm:text-base border-b border-[#F1F5F9] pb-2">Edit Header Information</h3>
          <form onSubmit={handleSave} className="space-y-4 font-semibold">
            <div className="grid sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Full Name</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
                />
              </div>
              <div>
                <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Headline</label>
                <input
                  type="text"
                  value={headline}
                  onChange={(e) => setHeadline(e.target.value)}
                  className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
                />
              </div>
            </div>

            <div className="grid sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Location Headquarters</label>
                <input
                  type="text"
                  value={loc}
                  onChange={(e) => setLoc(e.target.value)}
                  className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
                />
              </div>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Summary Biography</label>
              <textarea
                value={bio}
                onChange={(e) => setBio(e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>

            <div className="flex justify-end gap-2 pt-2 border-t border-[#F1F5F9]">
              <button
                type="button"
                onClick={() => setIsEditing(false)}
                className="px-4 py-2 border border-[#E2E8F0] rounded-xl text-xs text-slate-600 hover:bg-slate-50 cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs px-4 py-2 rounded-xl cursor-pointer"
              >
                Save Details
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Two columns split */}
      <div className="grid lg:grid-cols-3 gap-6 items-start">
        {/* Left main content columns */}
        <div className="lg:col-span-2 space-y-6">
          {/* Tabs navigation list */}
          <div className="flex gap-2.5 overflow-x-auto pb-1 border-b border-[#E2E8F0] text-xs sm:text-sm">
            {[
              { id: 'overview', label: 'Overview' },
              { id: 'experience', label: 'Experience' },
              { id: 'education', label: 'Education' },
              { id: 'projects', label: 'Projects' },
              { id: 'skills', label: 'Skills' },
              { id: 'portfolio', label: 'Portfolio' },
              { id: 'socials', label: 'Social Accounts' },
              { id: 'resume', label: 'Resume' },
              { id: 'activity', label: 'Activity Feed' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as ProfileTab)}
                className={`
                  pb-3 font-bold border-b-2 transition-all cursor-pointer whitespace-nowrap px-1
                  ${
                    activeTab === tab.id
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-[#64748B] hover:text-[#0F172A]'
                  }
                `}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Active Tab Panel */}
          <div className="min-h-[220px]">
            {activeTab === 'overview' && <ProfileOverview profile={profile} />}
            {activeTab === 'experience' && <ExperienceSection />}
            {activeTab === 'education' && <EducationSection />}
            {activeTab === 'projects' && <ProjectsSection />}
            {activeTab === 'skills' && <SkillsSection />}
            {activeTab === 'portfolio' && <PortfolioSection />}
            {activeTab === 'socials' && <SocialAccountsSection />}
            {activeTab === 'resume' && <ResumeSection />}
            {activeTab === 'activity' && <ActivityTimeline />}
          </div>
        </div>

        {/* Right completeness and visibility options */}
        <div className="space-y-6 lg:sticky lg:top-6">
          <ProfileSidebar
            profile={profile}
            onVisibilityChange={(v) => updateProfile({ visibility: v })}
          />
        </div>
      </div>
    </div>
  );
}
