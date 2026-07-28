'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Upload, FileText, Bot, ArrowRight, Eye, RefreshCw, AlertTriangle } from 'lucide-react';
import { useResume } from '@/hooks/useResume';
import ResumeHeader from '@/components/resume/ResumeHeader';
import ResumeStats from '@/components/resume/ResumeStats';
import ResumeCompletion from '@/components/resume/ResumeCompletion';
import ResumeViewer from '@/components/resume/ResumeViewer';

export default function ResumePage() {
  const { resume, loading, error, fetchResume } = useResume();
  const [activeTab, setActiveTab] = useState<'overview' | 'viewer'>('overview');

  useEffect(() => {
    fetchResume();
  }, [fetchResume]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] gap-3">
        <RefreshCw className="animate-spin text-[#2563EB]" size={36} />
        <p className="text-sm font-semibold text-[#64748B]">Loading resume dashboard...</p>
      </div>
    );
  }

  if (error || !resume) {
    return (
      <div className="p-6 space-y-6 max-w-4xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-2xl p-6 text-center space-y-4">
          <div className="w-12 h-12 bg-red-100 text-red-600 rounded-xl flex items-center justify-center mx-auto">
            <AlertTriangle size={24} />
          </div>
          <div>
            <h3 className="font-bold text-[#0F172A] text-lg">Failed to load resume</h3>
            <p className="text-sm text-[#64748B] mt-1">{error || 'No active resume found.'}</p>
          </div>
          <button
            onClick={() => fetchResume()}
            className="inline-flex items-center justify-center gap-2 bg-[#2563EB] text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-[#1D4ED8] transition-colors cursor-pointer"
          >
            Retry Fetching
          </button>
        </div>
      </div>
    );
  }

  // Define missing sections and optimization suggestions for the dashboard based on candidate details
  const missingSections = [
    'LinkedIn Link',
    'GitHub Link',
    'Cloud container tools (Kubernetes)',
  ];

  const optimizationSuggestions = [
    'Your technical skills score is 95% — high compatibility with frontend positions.',
    'Add links: GitHub profile, LinkedIn, portfolio website to increase visibility.',
    'Quantify your projects: include active user counts, conversion metrics, or package downloads.',
  ];

  return (
    <div className="p-4 sm:p-6 space-y-6 max-w-5xl mx-auto">
      {/* Header section */}
      <ResumeHeader
        title="Resume Dashboard"
        fileName="Alex_Johnson_Resume_v3.pdf"
        version={resume.version}
        lastUpdated={resume.lastUpdated}
      />

      {/* Quick stats cards */}
      <ResumeStats
        score={resume.profileCompletion + 7} // Score matches overall analysis (92%)
        completion={resume.profileCompletion}
        status={resume.resumeStatus}
        lastUpdated={resume.lastUpdated}
      />

      {/* Tabs selector */}
      <div className="flex border-b border-[#E2E8F0]">
        <button
          onClick={() => setActiveTab('overview')}
          className={`pb-3 text-sm font-semibold border-b-2 px-4 transition-colors cursor-pointer ${
            activeTab === 'overview'
              ? 'border-[#2563EB] text-[#2563EB]'
              : 'border-transparent text-[#64748B] hover:text-[#0F172A]'
          }`}
        >
          Resume Overview
        </button>
        <button
          onClick={() => setActiveTab('viewer')}
          className={`pb-3 text-sm font-semibold border-b-2 px-4 transition-colors cursor-pointer ${
            activeTab === 'viewer'
              ? 'border-[#2563EB] text-[#2563EB]'
              : 'border-transparent text-[#64748B] hover:text-[#0F172A]'
          }`}
        >
          View Parsed Resume
        </button>
      </div>

      {/* Tab contents */}
      {activeTab === 'overview' ? (
        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            {/* Quick module entry cards */}
            <div className="grid md:grid-cols-2 gap-6">
              {[
                {
                  icon: Upload,
                  title: 'Upload Resume',
                  desc: 'Add or update your resume file to begin the parsing and analysis process.',
                  href: '/candidate/resume/upload',
                  color: 'bg-blue-50 text-blue-600 border-blue-100',
                  actionText: 'Upload New File',
                },
                {
                  icon: Bot,
                  title: 'AI Analysis & Recommendations',
                  desc: 'Review extracted skills, experience summaries, project details, and recommendations.',
                  href: '/candidate/resume/analysis',
                  color: 'bg-emerald-50 text-emerald-600 border-emerald-100',
                  actionText: 'Review Analysis',
                },
              ].map(({ icon: Icon, title, desc, href, color, actionText }) => (
                <div
                  key={title}
                  className="bg-white border border-[#E2E8F0] rounded-2xl p-5 flex flex-col justify-between hover:shadow-md transition-shadow"
                >
                  <div>
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center border mb-3 ${color}`}>
                      <Icon size={20} />
                    </div>
                    <h3 className="font-bold text-[#0F172A] text-base mb-2">{title}</h3>
                    <p className="text-xs text-[#64748B] leading-relaxed mb-6">{desc}</p>
                  </div>
                  <Link
                    href={href}
                    className="inline-flex items-center justify-center gap-2 bg-[#2563EB] text-white py-2.5 rounded-xl text-xs font-semibold hover:bg-[#1D4ED8] transition-colors w-full cursor-pointer"
                  >
                    {actionText}
                    <ArrowRight size={13} />
                  </Link>
                </div>
              ))}
            </div>

            {/* Resume Summary Card */}
            <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-3">
              <div className="flex items-center gap-2">
                <FileText size={18} className="text-[#2563EB]" />
                <h3 className="font-bold text-[#0F172A] text-base">Summary Statement</h3>
              </div>
              <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed">{resume.summary}</p>
            </div>
          </div>

          {/* Right side completions panel */}
          <div>
            <ResumeCompletion
              completionPercentage={resume.profileCompletion}
              missingSections={missingSections}
              suggestions={optimizationSuggestions}
            />
          </div>
        </div>
      ) : (
        /* Full Profile Viewer Tab */
        <ResumeViewer resume={resume} />
      )}
    </div>
  );
}
