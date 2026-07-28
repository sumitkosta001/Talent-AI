'use client';

import React, { useState } from 'react';
import { useExperience } from '@/hooks/useExperience';
import { Briefcase, Calendar, MapPin, Plus, Trash2, Globe } from 'lucide-react';

export default function ExperienceSection() {
  const { experience, addExperience, deleteExperience } = useExperience();

  const [companyName, setCompanyName] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [empType, setEmpType] = useState<'Full-time' | 'Part-time' | 'Contract' | 'Internship'>('Full-time');
  const [loc, setLoc] = useState('');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [current, setCurrent] = useState(false);
  const [desc, setDesc] = useState('');

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!companyName || !jobTitle) return;
    const res = await addExperience({
      companyName,
      jobTitle,
      employmentType: empType,
      location: loc,
      startDate: start,
      endDate: current ? 'Present' : end,
      isCurrentJob: current,
      description: desc,
    });
    if (res) {
      setCompanyName('');
      setJobTitle('');
      setLoc('');
      setStart('');
      setEnd('');
      setDesc('');
      setCurrent(false);
    }
  };

  return (
    <div className="space-y-6 text-[#0F172A] text-left">
      {/* Add experiences form */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4">
        <h3 className="font-bold text-sm sm:text-base">Add Professional Experience</h3>

        <form onSubmit={handleAdd} className="space-y-3.5 text-xs font-semibold">
          <div className="grid sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Company Name</label>
              <input
                type="text"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                placeholder="e.g. Stripe, Google"
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Job Title</label>
              <input
                type="text"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                placeholder="e.g. Senior Software Engineer"
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
          </div>

          <div className="grid sm:grid-cols-3 gap-3">
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Employment Type</label>
              <select
                value={empType}
                onChange={(e) => setEmpType(e.target.value as any)}
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
              >
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Contract">Contract</option>
                <option value="Internship">Internship</option>
              </select>
            </div>
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Location</label>
              <input
                type="text"
                value={loc}
                onChange={(e) => setLoc(e.target.value)}
                placeholder="e.g. San Francisco, CA"
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Start Date</label>
              <input
                type="month"
                value={start}
                onChange={(e) => setStart(e.target.value)}
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
              />
            </div>
          </div>

          <div className="flex items-center gap-2 py-1">
            <input
              type="checkbox"
              id="isCurrent"
              checked={current}
              onChange={(e) => setCurrent(e.target.checked)}
              className="w-4 h-4 text-blue-600 border-[#E2E8F0] rounded focus:ring-blue-500 cursor-pointer"
            />
            <label htmlFor="isCurrent" className="text-xs text-slate-700 cursor-pointer">I am currently working in this role</label>
          </div>

          {!current && (
            <div className="w-full sm:w-1/2">
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">End Date</label>
              <input
                type="month"
                value={end}
                onChange={(e) => setEnd(e.target.value)}
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
              />
            </div>
          )}

          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Description & Role Responsibilities</label>
            <textarea
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              rows={3}
              placeholder="Detail your roles, projects, and tech frameworks used..."
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs px-4 py-2.5 rounded-xl transition-all cursor-pointer inline-flex items-center gap-1.5"
          >
            <Plus size={15} /> Add Experience
          </button>
        </form>
      </div>

      {/* Experience Timeline */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-5">
        <h3 className="font-bold text-sm sm:text-base border-b border-[#F1F5F9] pb-3 flex items-center gap-1.5">
          <Briefcase size={16} className="text-[#2563EB]" />
          Experience Timeline
        </h3>

        {experience.length === 0 ? (
          <div className="text-center p-8 text-xs text-[#64748B] font-semibold">
            No professional experience added yet.
          </div>
        ) : (
          <div className="space-y-6">
            {experience.map((exp) => (
              <div key={exp.id} className="flex gap-4 border-l-2 border-[#F1F5F9] pl-5 relative ml-3">
                {/* Node icon */}
                <div className="absolute -left-2 top-1.5 w-3.5 h-3.5 bg-blue-600 rounded-full border-4 border-white shadow-sm flex-shrink-0" />
                <div className="flex-1 space-y-1.5">
                  <div className="flex justify-between items-start gap-4">
                    <div>
                      <h4 className="font-bold text-sm text-[#0F172A] leading-normal">{exp.jobTitle}</h4>
                      <p className="text-xs text-slate-500 font-bold mt-0.5">
                        {exp.companyName} · {exp.employmentType}
                      </p>
                    </div>

                    <button
                      onClick={() => deleteExperience(exp.id)}
                      className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
                      title="Delete experience item"
                    >
                      <Trash2 size={13} />
                    </button>
                  </div>

                  <div className="flex flex-wrap items-center gap-3 text-[10px] text-[#64748B] font-bold">
                    <span className="flex items-center gap-0.5"><Calendar size={12} /> {exp.startDate} - {exp.isCurrentJob ? 'Present' : exp.endDate}</span>
                    <span className="flex items-center gap-0.5"><MapPin size={12} /> {exp.location}</span>
                  </div>

                  <p className="text-xs text-slate-600 leading-relaxed font-semibold">
                    {exp.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
export type UserStatus = 'Active' | 'Suspended' | 'Deactivated';
export type UserRole = 'Super Admin' | 'Admin' | 'Moderator' | 'Support' | 'Candidate' | 'Recruiter';
