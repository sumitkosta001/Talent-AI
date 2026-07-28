'use client';

import React, { useState } from 'react';
import { useSkills } from '@/hooks/useSkills';
import { Search, Plus, Trash2, ShieldCheck } from 'lucide-react';

export default function SkillsSection() {
  const { skills, addSkill, deleteSkill } = useSkills();

  const [query, setQuery] = useState('');
  const [newName, setNewName] = useState('');
  const [newLevel, setNewLevel] = useState<'Beginner' | 'Intermediate' | 'Expert'>('Expert');
  const [newExp, setNewExp] = useState(3);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;
    const res = await addSkill(newName.trim(), newLevel, newExp);
    if (res) {
      setNewName('');
    }
  };

  const filtered = skills.filter((s) => s.name.toLowerCase().includes(query.toLowerCase()));

  return (
    <div className="space-y-6 text-[#0F172A] text-left">
      {/* Search and add forms */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4">
        <h3 className="font-bold text-sm sm:text-base">Technical skills</h3>

        <div className="flex relative">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search keywords skill tags..."
            className="w-full pl-9 pr-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
          />
        </div>

        {/* Add skill inline form fields */}
        <form onSubmit={handleAdd} className="grid grid-cols-1 sm:grid-cols-4 gap-3 pt-3 border-t border-[#F1F5F9] items-end text-xs">
          <div className="sm:col-span-2">
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Skill Name</label>
            <input
              type="text"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              placeholder="e.g. React, Docker, Python"
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white font-semibold"
            />
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Level</label>
            <select
              value={newLevel}
              onChange={(e) => setNewLevel(e.target.value as any)}
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer font-bold"
            >
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Expert">Expert</option>
            </select>
          </div>

          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs py-2 rounded-xl transition-all cursor-pointer inline-flex items-center justify-center gap-1"
          >
            <Plus size={14} /> Add Skill
          </button>
        </form>
      </div>

      {/* Skills Grid */}
      <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
        {filtered.map((skill) => (
          <div key={skill.id} className="bg-white border border-[#E2E8F0] rounded-2xl p-4.5 shadow-sm flex items-start justify-between gap-3 hover:shadow-md transition-all">
            <div className="space-y-1">
              <h4 className="font-bold text-sm text-[#0F172A]">{skill.name}</h4>
              <p className="text-[10px] text-[#64748B] font-bold">
                {skill.level} · {skill.yearsOfExperience} years experience
              </p>
              {skill.endorsementsCount !== undefined && skill.endorsementsCount > 0 && (
                <span className="inline-flex items-center gap-0.5 text-[9px] font-semibold text-slate-500 pt-1">
                  <ShieldCheck size={11} className="text-blue-500" />
                  {skill.endorsementsCount} endorsements
                </span>
              )}
            </div>

            <button
              onClick={() => deleteSkill(skill.id)}
              className="p-1 text-slate-400 hover:text-red-600 rounded-lg hover:bg-red-50 transition-colors cursor-pointer"
              title="Delete skill"
            >
              <Trash2 size={13} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
