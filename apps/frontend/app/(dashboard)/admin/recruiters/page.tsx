'use client';

import React from 'react';
import { useUsers } from '@/hooks/useUsers';
import { Eye, ToggleLeft, ToggleRight, Trash2, ShieldAlert } from 'lucide-react';
import Link from 'next/link';
import { Loader2 } from 'lucide-react';

export default function AdminRecruitersListPage() {
  const { users, loading, error, updateStatus, deleteUser } = useUsers();

  const recruiters = users.filter((u) => u.role === 'Recruiter');

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading active recruiter profiles...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Error Loading Recruiters</h3>
        <p className="text-sm text-[#64748B]">{error}</p>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto text-[#0F172A]">
      {/* Title */}
      <div className="text-left">
        <h1 className="text-xl sm:text-2xl font-bold">Manage Platform Recruiters</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">Suspend, delete, or inspect active recruiter credentials.</p>
      </div>

      {/* Recruiter table list */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-[#F8FAFC] border-b border-[#E2E8F0] text-xs font-bold text-[#64748B] uppercase tracking-wider">
              <tr>
                <th className="px-5 py-3">Recruiter Profile</th>
                <th className="px-5 py-3">Email Address</th>
                <th className="px-5 py-3">Status</th>
                <th className="px-5 py-3">Country</th>
                <th className="px-5 py-3">Last Login</th>
                <th className="px-5 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#F1F5F9] text-xs sm:text-sm">
              {recruiters.map((user) => (
                <tr key={user.id} className="hover:bg-[#F8FAFC]/50 transition-colors">
                  <td className="px-5 py-4 font-bold text-[#0F172A] flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-blue-500 text-white font-bold flex items-center justify-center text-xs flex-shrink-0">
                      {user.name.split(' ').map(n => n[0]).join('')}
                    </div>
                    <div>
                      <span>{user.name}</span>
                      <p className="text-[10px] text-[#64748B] font-semibold mt-0.5">{user.experience}</p>
                    </div>
                  </td>
                  <td className="px-5 py-4 font-semibold text-slate-700">{user.email}</td>
                  <td className="px-5 py-4">
                    <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${
                      user.status === 'Active' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-amber-50 text-amber-700 border-amber-200'
                    }`}>
                      {user.status}
                    </span>
                  </td>
                  <td className="px-5 py-4 font-semibold text-slate-700">{user.country}</td>
                  <td className="px-5 py-4 font-semibold text-slate-500">{user.lastLogin}</td>
                  <td className="px-5 py-4 text-right">
                    <div className="flex items-center justify-end gap-1.5">
                      <Link
                        href={`/admin/recruiters/${user.id}`}
                        className="p-1 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
                        title="Inspect Recruiter"
                      >
                        <Eye size={14} />
                      </Link>
                      {user.status === 'Active' ? (
                        <button
                          onClick={() => updateStatus(user.id, 'Suspended')}
                          className="p-1 text-slate-400 hover:text-amber-600 hover:bg-amber-50 rounded-lg transition-colors cursor-pointer"
                          title="Suspend recruiter"
                        >
                          <ToggleLeft size={14} />
                        </button>
                      ) : (
                        <button
                          onClick={() => updateStatus(user.id, 'Active')}
                          className="p-1 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors cursor-pointer"
                          title="Activate recruiter"
                        >
                          <ToggleRight size={14} />
                        </button>
                      )}
                      <button
                        onClick={() => deleteUser(user.id)}
                        className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
                        title="Delete Recruiter"
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
export type UserStatus = 'Active' | 'Suspended' | 'Deactivated';
