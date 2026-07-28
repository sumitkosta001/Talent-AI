'use client';

import React, { useState } from 'react';
import { useEducation } from '@/hooks/useEducation';
import { GraduationCap, Calendar, Award, Plus, Trash2 } from 'lucide-react';

export default function EducationSection() {
  const { education, addEducation, deleteEducation } = useEducation();

  const [school, setSchool] = useState('');
  const [degree, setDegree] = useState('');
  const [branch, setBranch] = useState('');
  const [gpa, setGpa] = useState('');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [desc, setDesc] = useState('');

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!school || !degree) return;
    const res = await addEducation({
      institutionName: school,
      degree,
      branch,
      cgpaOrPercentage: gpa,
      startYear: start,
      endYear: end,
      achievements: desc ? [desc] : [],
    });
    if (res) {
      setSchool('');
      setDegree('');
      setBranch('');
      setGpa('');
      setStart('');
      setEnd('');
      setDesc('');
    }
  };

  return (
    <div className="space-y-6 text-[#0F172A] text-left">
      {/* Add education form */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4">
        <h3 className="font-bold text-sm sm:text-base">Add Education Background</h3>

        <form onSubmit={handleAdd} className="space-y-3.5 text-xs font-semibold">
          <div className="grid sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Institution Name</label>
              <input
                type="text"
                value={school}
                onChange={(e) => setSchool(e.target.value)}
                placeholder="e.g. Stanford University"
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Degree Title</label>
              <input
                type="text"
                value={degree}
                onChange={(e) => setDegree(e.target.value)}
                placeholder="e.g. Bachelor of Science"
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
          </div>

          <div className="grid sm:grid-cols-4 gap-3">
            <div className="sm:col-span-2">
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Field of Study / Branch</label>
              <input
                type="text"
                value={branch}
                onChange={(e) => setBranch(e.target.value)}
                placeholder="e.g. Computer Science"
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">CGPA / Grade</label>
              <input
                type="text"
                value={gpa}
                onChange={(e) => setGpa(e.target.value)}
                placeholder="e.g. 3.9 GPA"
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Graduation Year</label>
              <input
                type="text"
                value={end}
                onChange={(e) => setEnd(e.target.value)}
                placeholder="e.g. 2024"
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Key Achievements & Activities</label>
            <input
              type="text"
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              placeholder="e.g. Gold Medalist, President of Tech Club"
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs px-4 py-2.5 rounded-xl transition-all cursor-pointer inline-flex items-center gap-1.5"
          >
            <Plus size={15} /> Add Education
          </button>
        </form>
      </div>

      {/* Education List */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-5">
        <h3 className="font-bold text-sm sm:text-base border-b border-[#F1F5F9] pb-3 flex items-center gap-1.5">
          <GraduationCap size={16} className="text-[#2563EB]" />
          Education Background
        </h3>

        {education.length === 0 ? (
          <div className="text-center p-8 text-xs text-[#64748B] font-semibold">
            No education background details added yet.
          </div>
        ) : (
          <div className="space-y-4">
            {education.map((edu) => (
              <div key={edu.id} className="p-4 border border-[#F1F5F9] bg-[#F8FAFC]/50 rounded-xl space-y-2 hover:shadow-sm transition-all flex justify-between items-start gap-4">
                <div className="space-y-1">
                  <h4 className="font-bold text-sm text-[#0F172A] leading-normal">{edu.institutionName}</h4>
                  <p className="text-xs text-slate-500 font-bold">
                    {edu.degree} in {edu.branch} · {edu.cgpaOrPercentage}
                  </p>
                  <span className="flex items-center gap-0.5 text-[10px] text-[#64748B] font-bold pt-1">
                    <Calendar size={12} /> Graduated {edu.endYear}
                  </span>
                  {edu.achievements && edu.achievements.length > 0 && (
                    <p className="text-xs text-slate-600 leading-relaxed font-semibold pt-1">
                      {edu.achievements[0]}
                    </p>
                  )}
                </div>

                <button
                  onClick={() => deleteEducation(edu.id)}
                  className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
                  title="Delete education block"
                >
                  <Trash2 size={13} />
                </button>
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
