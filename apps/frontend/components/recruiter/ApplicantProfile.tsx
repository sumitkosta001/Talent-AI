'use client';

import React, { useState } from 'react';
import { Applicant } from '@/types/applicant';
import { FileText, Calendar, Award, AlertCircle, Bot, Mail, Phone, BookOpen, Clock, Plus, Trash2 } from 'lucide-react';
import Link from 'next/link';

interface ApplicantProfileProps {
  applicant: Applicant;
  onStatusChange: (status: any) => void;
  onAddNote: (notes: string) => void;
}

export default function ApplicantProfile({ applicant, onStatusChange, onAddNote }: ApplicantProfileProps) {
  const { name, email, phone, atsScore, matchPercentage, experience, skills, status, bio, notes, timeline, jobTitle } = applicant;
  const [newNote, setNewNote] = useState(notes || '');

  const handleSaveNotes = (e: React.FormEvent) => {
    e.preventDefault();
    onAddNote(newNote);
    alert('Notes saved successfully');
  };

  const getStatusColor = (s: string) => {
    switch (s) {
      case 'Offer Sent':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'Interview Scheduled':
        return 'bg-violet-50 text-violet-700 border-violet-200';
      case 'Shortlisted':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'Rejected':
        return 'bg-red-50 text-red-700 border-red-200';
      default:
        return 'bg-slate-50 text-slate-600 border-slate-200';
    }
  };

  return (
    <div className="space-y-6 text-left text-[#0F172A]">
      {/* Header Panel */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex gap-4">
          <div className="w-14 h-14 rounded-full bg-[#2563EB] text-white font-black text-xl flex items-center justify-center border shadow-sm flex-shrink-0">
            {name.split(' ').map(n => n[0]).join('')}
          </div>
          <div>
            <h2 className="text-lg sm:text-xl font-bold">{name}</h2>
            <p className="text-xs text-[#64748B] mt-0.5">Applied for: <strong className="text-[#0F172A]">{jobTitle}</strong></p>
            <div className="flex flex-wrap items-center gap-3 mt-2 text-xs text-[#64748B] font-semibold">
              <span className="flex items-center gap-0.5"><Mail size={12} /> {email}</span>
              <span>·</span>
              <span className="flex items-center gap-0.5"><Phone size={12} /> {phone}</span>
            </div>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <span className={`text-[10px] font-bold px-3 py-1 rounded-full border uppercase tracking-wider ${getStatusColor(status)}`}>
            {status}
          </span>
          <span className="text-[10px] font-bold bg-green-50 text-green-700 border border-green-200 px-3 py-1 rounded-full uppercase tracking-wider">
            {matchPercentage}% match rate
          </span>
        </div>
      </div>

      {/* Main Grid splits columns */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left column info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Candidate Bio */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-3">
            <h4 className="font-bold text-sm text-[#0F172A] border-b border-[#F1F5F9] pb-2">Biography</h4>
            <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed">{bio || 'No bio provided.'}</p>
          </div>

          {/* Experience & Skills */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <h4 className="font-bold text-sm text-[#0F172A] border-b border-[#F1F5F9] pb-2">Professional Qualifications</h4>
            
            <div className="space-y-3 text-xs sm:text-sm">
              <div>
                <span className="font-semibold text-slate-500 block mb-0.5">Years of Experience</span>
                <span className="font-bold text-[#0F172A]">{experience}</span>
              </div>

              <div>
                <span className="font-semibold text-slate-500 block mb-1">Keywords & Skills Matching</span>
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {skills.map((skill) => (
                    <span key={skill} className="bg-slate-50 text-slate-700 border border-slate-100 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wide">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Timeline details stages */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <h4 className="font-bold text-sm text-[#0F172A] border-b border-[#F1F5F9] pb-2">Application Tracking Stages</h4>
            
            <div className="relative pl-6 space-y-5 text-xs">
              <div className="absolute left-[9px] top-2 bottom-2 w-0.5 bg-slate-200" />
              {timeline.map((t, idx) => (
                <div key={idx} className="relative flex flex-col sm:flex-row sm:items-start justify-between gap-2">
                  <div className="absolute left-[-23px] top-1 w-5.5 h-5.5 rounded-full bg-blue-50 border-2 border-blue-500 flex items-center justify-center text-[8px] font-black text-blue-600">
                    ✓
                  </div>
                  <div>
                    <h5 className="font-bold text-[#0F172A] text-xs sm:text-sm">{t.stage}</h5>
                    {t.notes && <p className="text-[10px] sm:text-xs text-[#64748B] mt-0.5 leading-relaxed">{t.notes}</p>}
                  </div>
                  <span className="text-[10px] text-[#64748B] font-bold whitespace-nowrap">{t.date}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right sidebar options actions */}
        <div className="space-y-6">
          {/* Action options buttons */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-3.5">
            <h4 className="font-bold text-sm text-[#0F172A]">Recruiter Actions</h4>
            
            <div className="flex flex-col gap-2">
              {status !== 'Shortlisted' && status !== 'Offer Sent' && status !== 'Interview Scheduled' && (
                <button
                  onClick={() => onStatusChange('Shortlisted')}
                  className="bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold text-xs py-2 rounded-xl transition-all cursor-pointer text-center"
                >
                  Shortlist Candidate
                </button>
              )}
              {status !== 'Interview Scheduled' && status !== 'Offer Sent' && (
                <button
                  onClick={() => onStatusChange('Interview Scheduled')}
                  className="bg-violet-600 hover:bg-violet-700 text-white font-bold text-xs py-2 rounded-xl transition-all cursor-pointer text-center"
                >
                  Schedule Coding Panel Loop
                </button>
              )}
              {status !== 'Offer Sent' && (
                <button
                  onClick={() => onStatusChange('Offer Sent')}
                  className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs py-2 rounded-xl transition-all cursor-pointer text-center"
                >
                  Send Written Job Offer
                </button>
              )}
              {status !== 'Rejected' && (
                <button
                  onClick={() => onStatusChange('Rejected')}
                  className="bg-red-50 hover:bg-red-100 text-red-700 border border-red-100 font-bold text-xs py-2 rounded-xl transition-all cursor-pointer text-center"
                >
                  Reject Candidate
                </button>
              )}
            </div>
          </div>

          {/* ATS report panel */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-3">
            <h4 className="font-bold text-sm text-[#0F172A] flex items-center gap-1.5">
              <Bot size={16} className="text-purple-600" />
              ATS Evaluation Index
            </h4>
            <div className="flex items-center gap-4">
              <div className="text-center bg-[#F8FAFC] border border-[#E2E8F0] px-4 py-2 rounded-xl flex-shrink-0">
                <span className="text-lg font-black text-[#0F172A]">{atsScore}%</span>
                <p className="text-[8px] text-[#64748B] font-bold mt-0.5 uppercase">ATS Score</p>
              </div>
              <p className="text-xs text-[#64748B] leading-relaxed">
                Matches required keywords for the integrations stack perfectly. Recommended for immediate fast-track loops.
              </p>
            </div>
          </div>

          {/* Recruiter notes field */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-3">
            <h4 className="font-bold text-sm text-[#0F172A]">Recruiter Notes</h4>
            <form onSubmit={handleSaveNotes} className="space-y-3">
              <textarea
                rows={3}
                value={newNote}
                onChange={(e) => setNewNote(e.target.value)}
                placeholder="Add private evaluation notes on the candidate..."
                className="w-full border border-[#E2E8F0] rounded-xl p-3 text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
              <button
                type="submit"
                className="bg-slate-800 hover:bg-slate-900 text-white font-bold text-xs px-3.5 py-2 rounded-xl cursor-pointer w-full text-center"
              >
                Save Candidate Notes
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
