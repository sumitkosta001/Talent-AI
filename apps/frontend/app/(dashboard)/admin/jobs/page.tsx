'use client';

import React, { useState, useEffect } from 'react';
import { RecruiterJobsService } from '@/services/jobs.service';
import { RecruiterJob } from '@/types/job';
import { Eye, Briefcase, Trash2, MapPin, DollarSign } from 'lucide-react';
import Link from 'next/link';
import { Loader2 } from 'lucide-react';

export default function AdminJobsListPage() {
  const [jobs, setJobs] = useState<RecruiterJob[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadData() {
    try {
      const items = await RecruiterJobsService.getJobs();
      setJobs(items);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  const handleDelete = async (id: string) => {
    const ok = window.confirm('Are you sure you want to delete this job post from the platform?');
    if (ok) {
      const res = await RecruiterJobsService.deleteJob(id);
      if (res) {
        setJobs((prev) => prev.filter(j => j.id !== id));
        alert('Job post deleted successfully.');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading platform job listings...</p>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto text-[#0F172A]">
      <div className="text-left">
        <h1 className="text-xl sm:text-2xl font-bold">Manage Platform Job Listings</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">Track, edit, delete, or inspect active job openings globally.</p>
      </div>

      <div className="bg-white rounded-2xl border border-[#E2E8F0] overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-[#F8FAFC] border-b border-[#E2E8F0] text-xs font-bold text-[#64748B] uppercase tracking-wider">
              <tr>
                <th className="px-5 py-3">Job Role</th>
                <th className="px-5 py-3">Department</th>
                <th className="px-5 py-3">Employer</th>
                <th className="px-5 py-3">Status</th>
                <th className="px-5 py-3">Applications</th>
                <th className="px-5 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#F1F5F9] text-xs sm:text-sm">
              {jobs.map((job) => (
                <tr key={job.id} className="hover:bg-[#F8FAFC]/50 transition-colors">
                  <td className="px-5 py-4 flex items-center gap-3">
                    <div className={`w-8 h-8 rounded-lg ${job.logoColor} flex items-center justify-center text-white font-bold text-xs flex-shrink-0`}>
                      {job.logo}
                    </div>
                    <div>
                      <Link href={`/admin/jobs/${job.id}`} className="font-bold text-[#0F172A] hover:text-blue-600 transition-colors">
                        {job.role}
                      </Link>
                      <p className="text-[10px] text-[#64748B] font-semibold mt-0.5">{job.location} · {job.employmentType}</p>
                    </div>
                  </td>
                  <td className="px-5 py-4 font-semibold text-slate-700">{job.department}</td>
                  <td className="px-5 py-4 font-bold text-slate-700">{job.company}</td>
                  <td className="px-5 py-4">
                    <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${
                      job.status === 'Published' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-red-50 text-red-700 border-red-200'
                    }`}>
                      {job.status}
                    </span>
                  </td>
                  <td className="px-5 py-4 font-semibold text-slate-600">
                    <strong>{job.applicationsCount}</strong> candidates
                  </td>
                  <td className="px-5 py-4 text-right">
                    <div className="flex items-center justify-end gap-1.5">
                      <Link
                        href={`/admin/jobs/${job.id}`}
                        className="p-1 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
                        title="View job statistics"
                      >
                        <Eye size={14} />
                      </Link>
                      <button
                        onClick={() => handleDelete(job.id)}
                        className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
                        title="Delete job posting"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
