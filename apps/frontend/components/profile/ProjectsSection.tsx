'use client';

import React, { useState } from 'react';
import { useProjects } from '@/hooks/useProjects';
import { Briefcase, Code, Plus, Trash2, Globe, ExternalLink } from 'lucide-react';

export default function ProjectsSection() {
  const { projects, addProject, deleteProject } = useProjects();

  const [projectName, setProjectName] = useState('');
  const [desc, setDesc] = useState('');
  const [tech, setTech] = useState('');
  const [role, setRole] = useState('');
  const [duration, setDuration] = useState('');
  const [git, setGit] = useState('');
  const [live, setLive] = useState('');

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!projectName) return;
    const res = await addProject({
      projectName,
      description: desc,
      technologies: tech ? tech.split(',').map((s) => s.trim()) : [],
      role,
      duration,
      githubUrl: git,
      liveUrl: live,
    });
    if (res) {
      setProjectName('');
      setDesc('');
      setTech('');
      setRole('');
      setDuration('');
      setGit('');
      setLive('');
    }
  };

  return (
    <div className="space-y-6 text-[#0F172A] text-left">
      {/* Add project form */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4">
        <h3 className="font-bold text-sm sm:text-base">Add Project Details</h3>

        <form onSubmit={handleAdd} className="space-y-3.5 text-xs font-semibold">
          <div className="grid sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Project Name</label>
              <input
                type="text"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="e.g. TalentAI Dashboard"
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Your Role</label>
              <input
                type="text"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                placeholder="e.g. Frontend Lead, Fullstack Architect"
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
          </div>

          <div className="grid sm:grid-cols-3 gap-3">
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Duration</label>
              <input
                type="text"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                placeholder="e.g. 3 months, 1 year"
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">GitHub Repository Link</label>
              <input
                type="text"
                value={git}
                onChange={(e) => setGit(e.target.value)}
                placeholder="e.g. https://github.com/..."
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Live Demo Link</label>
              <input
                type="text"
                value={live}
                onChange={(e) => setLive(e.target.value)}
                placeholder="e.g. https://talentai.co"
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Technologies Used (comma separated)</label>
            <input
              type="text"
              value={tech}
              onChange={(e) => setTech(e.target.value)}
              placeholder="e.g. Next.js, React, Tailwind, PostgreSQL"
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Project Description Summary</label>
            <textarea
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              rows={3}
              placeholder="Detail the project goals, framework integrations, and scaling limits..."
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs px-4 py-2.5 rounded-xl transition-all cursor-pointer inline-flex items-center gap-1.5"
          >
            <Plus size={15} /> Add Project
          </button>
        </form>
      </div>

      {/* Projects Grid List */}
      <div className="space-y-4">
        {projects.length === 0 ? (
          <div className="bg-white border border-[#E2E8F0] rounded-2xl p-8 text-center text-xs text-[#64748B] font-semibold shadow-sm">
            No projects added to your profile portfolio yet.
          </div>
        ) : (
          projects.map((proj) => (
            <div key={proj.id} className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-3.5 hover:shadow-md transition-all flex flex-col justify-between">
              <div className="flex justify-between items-start gap-4">
                <div>
                  <h4 className="font-bold text-sm text-[#0F172A] leading-normal">{proj.projectName}</h4>
                  <p className="text-[10px] text-[#64748B] font-bold mt-0.5">Role: {proj.role} · Duration: {proj.duration}</p>
                </div>

                <button
                  onClick={() => deleteProject(proj.id)}
                  className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
                  title="Delete project item"
                >
                  <Trash2 size={13} />
                </button>
              </div>

              <p className="text-xs text-slate-600 leading-relaxed font-semibold">
                {proj.description}
              </p>

              {/* Technologies tags */}
              {proj.technologies && proj.technologies.length > 0 && (
                <div className="flex flex-wrap gap-1 pt-1.5">
                  {proj.technologies.map((t) => (
                    <span key={t} className="bg-slate-50 border border-slate-100 text-slate-600 text-[9px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wide">
                      {t}
                    </span>
                  ))}
                </div>
              )}

              {/* Links */}
              <div className="flex items-center gap-3 pt-2 border-t border-[#F8FAFC] text-[11px] text-[#64748B] font-bold">
                {proj.githubUrl && (
                  <a href={proj.githubUrl} target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-slate-900">
                    <Code size={13} /> Code Repository <ExternalLink size={10} />
                  </a>
                )}
                {proj.liveUrl && (
                  <a href={proj.liveUrl} target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-slate-900">
                    <Globe size={13} /> Live Demo <ExternalLink size={10} />
                  </a>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
