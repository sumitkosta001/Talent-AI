'use client';

import React, { useState } from 'react';
import { RecruiterJob } from '@/types/job';
import { Save, Eye, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

interface JobFormProps {
  initialJob?: Partial<RecruiterJob>;
  onSubmit: (job: Partial<RecruiterJob>) => void;
  onPreview?: (job: Partial<RecruiterJob>) => void;
  isEdit?: boolean;
}

export default function JobForm({ initialJob, onSubmit, onPreview, isEdit }: JobFormProps) {
  const [role, setRole] = useState(initialJob?.role || '');
  const [department, setDepartment] = useState(initialJob?.department || 'Engineering');
  const [employmentType, setEmploymentType] = useState<any>(initialJob?.employmentType || 'Full-time');
  const [workMode, setWorkMode] = useState<any>(initialJob?.workMode || 'Remote');
  const [experience, setExperience] = useState(initialJob?.experience || '');
  const [salary, setSalary] = useState(initialJob?.salary || '');
  const [location, setLocation] = useState(initialJob?.location || '');
  const [openings, setOpenings] = useState(initialJob?.openings || 1);
  const [deadline, setDeadline] = useState(initialJob?.deadline || '');
  const [hiringManager, setHiringManager] = useState(initialJob?.hiringManager || '');
  const [description, setDescription] = useState(initialJob?.description || '');
  const [status, setStatus] = useState<any>(initialJob?.status || 'Published');

  const [skillsStr, setSkillsStr] = useState(initialJob?.skills?.join(', ') || '');
  const [responsibilitiesStr, setResponsibilitiesStr] = useState(initialJob?.responsibilities?.join('\n') || '');
  const [requirementsStr, setRequirementsStr] = useState(initialJob?.requirements?.join('\n') || '');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!role || !experience || !salary || !location || !deadline) {
      alert('Please fill out all required fields');
      return;
    }

    const payload: Partial<RecruiterJob> = {
      role,
      department,
      employmentType,
      workMode,
      experience,
      salary,
      location,
      openings,
      deadline,
      hiringManager,
      description,
      status,
      skills: skillsStr.split(',').map(s => s.trim()).filter(Boolean),
      responsibilities: responsibilitiesStr.split('\n').map(r => r.trim()).filter(Boolean),
      requirements: requirementsStr.split('\n').map(r => r.trim()).filter(Boolean),
    };

    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 text-left text-[#0F172A]">
      <div className="flex items-center gap-3">
        <Link href="/recruiter/jobs" className="text-slate-400 hover:text-[#0F172A] cursor-pointer">
          <ArrowLeft size={18} />
        </Link>
        <h2 className="text-lg font-bold">{isEdit ? 'Edit Job Posting' : 'Post a New Position'}</h2>
      </div>

      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 sm:p-6 shadow-sm space-y-4">
        <h3 className="font-bold text-xs uppercase tracking-wider text-[#64748B] border-b border-[#F1F5F9] pb-2">
          Basic Information
        </h3>

        <div className="grid sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Job Title *</label>
            <input
              required
              type="text"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              placeholder="e.g. Senior Backend Developer"
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Department</label>
            <input
              type="text"
              value={department}
              onChange={(e) => setDepartment(e.target.value)}
              placeholder="e.g. Engineering, Sales"
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Employment Type</label>
            <select
              value={employmentType}
              onChange={(e) => setEmploymentType(e.target.value as any)}
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white cursor-pointer"
            >
              <option value="Full-time">Full-time</option>
              <option value="Part-time">Part-time</option>
              <option value="Contract">Contract</option>
              <option value="Internship">Internship</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Work Mode</label>
            <select
              value={workMode}
              onChange={(e) => setWorkMode(e.target.value as any)}
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white cursor-pointer"
            >
              <option value="Remote">Remote</option>
              <option value="Hybrid">Hybrid</option>
              <option value="On-site">On-site</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Experience Range *</label>
            <input
              required
              type="text"
              value={experience}
              onChange={(e) => setExperience(e.target.value)}
              placeholder="e.g. 3 - 6 years"
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Salary Range *</label>
            <input
              required
              type="text"
              value={salary}
              onChange={(e) => setSalary(e.target.value)}
              placeholder="e.g. $140K - $180K"
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Location *</label>
            <input
              required
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g. San Francisco, CA"
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Openings</label>
            <input
              type="number"
              value={openings}
              onChange={(e) => setOpenings(parseInt(e.target.value) || 1)}
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Application Deadline *</label>
            <input
              required
              type="date"
              value={deadline}
              onChange={(e) => setDeadline(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Hiring Manager</label>
            <input
              type="text"
              value={hiringManager}
              onChange={(e) => setHiringManager(e.target.value)}
              placeholder="e.g. Marcus Aurelius"
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 sm:p-6 shadow-sm space-y-4">
        <h3 className="font-bold text-xs uppercase tracking-wider text-[#64748B] border-b border-[#F1F5F9] pb-2">
          Skills & Specifications
        </h3>

        <div className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Required Skills (Comma separated)</label>
            <input
              type="text"
              value={skillsStr}
              onChange={(e) => setSkillsStr(e.target.value)}
              placeholder="e.g. React, Next.js, Node.js, TypeScript"
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Job Description Summary</label>
            <textarea
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Provide a general summary of the position..."
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white resize-none"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Responsibilities (One per line)</label>
            <textarea
              rows={3}
              value={responsibilitiesStr}
              onChange={(e) => setResponsibilitiesStr(e.target.value)}
              placeholder="e.g. Design, build, and optimize backend payment gateways."
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white resize-none"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Requirements (One per line)</label>
            <textarea
              rows={3}
              value={requirementsStr}
              onChange={(e) => setRequirementsStr(e.target.value)}
              placeholder="e.g. Strong foundations in graph traversals and relational databases."
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white resize-none"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#475569] mb-1.5">Posting Status</label>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value as any)}
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:border-blue-500 bg-white cursor-pointer"
            >
              <option value="Published">Publish Immediately</option>
              <option value="Draft">Draft Mode</option>
              <option value="Closed">Closed</option>
            </select>
          </div>
        </div>
      </div>

      {/* Buttons */}
      <div className="flex justify-end gap-3 pt-2">
        <button
          type="submit"
          className="inline-flex items-center gap-1.5 bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold text-xs px-4 py-2.5 rounded-xl transition-colors cursor-pointer"
        >
          <Save size={14} />
          {isEdit ? 'Save Changes' : 'Publish Job'}
        </button>
      </div>
    </form>
  );
}
