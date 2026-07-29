'use client';

import React, { use, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { AdminUserService } from '@/services/user.service';
import { AdminUser, UserRole, UserStatus } from '@/types/user';
import { Loader2, ArrowLeft, Mail, Phone, MapPin, Calendar, Clock, Award, ShieldAlert, Bot } from 'lucide-react';
import Link from 'next/link';

interface AdminUserDetailPageProps {
  params: Promise<{ id: string }>;
}

export default function AdminUserDetailPage({ params }: AdminUserDetailPageProps) {
  const { id } = use(params);
  const router = useRouter();

  const [user, setUser] = useState<AdminUser | null>(null);
  const [loading, setLoading] = useState(true);

  async function loadData() {
    try {
      const match = await AdminUserService.getUserById(id);
      setUser(match);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, [id]);

  const handleStatusToggle = async (status: UserStatus) => {
    if (!user) return;
    const res = await AdminUserService.updateStatus(user.id, status);
    if (res) {
      alert(`User status updated to ${status}!`);
      loadData();
    }
  };

  const handleRoleChange = async (role: UserRole) => {
    if (!user) return;
    const res = await AdminUserService.updateRole(user.id, role);
    if (res) {
      alert(`User role promoted/demoted to ${role}!`);
      loadData();
    }
  };

  const handleDelete = async () => {
    if (!user) return;
    const ok = window.confirm('Are you sure you want to permanently delete this user account?');
    if (ok) {
      const res = await AdminUserService.deleteUser(user.id);
      if (res) {
        alert('User account deleted successfully.');
        router.push('/admin/users');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading user details profile...</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">User Account Not Found</h3>
        <Link href="/admin/users" className="inline-block bg-blue-600 text-white px-4 py-2 rounded-xl text-xs font-semibold">
          Back to Directory
        </Link>
      </div>
    );
  }

  const getStatusColor = (s: string) => {
    if (s === 'Active') return 'text-emerald-700 bg-emerald-50 border-emerald-200';
    return 'text-amber-700 bg-amber-50 border-amber-200';
  };

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto text-[#0F172A] text-left">
      {/* Header */}
      <div className="flex items-center gap-3">
        <Link href="/admin/users" className="text-slate-400 hover:text-[#0F172A] cursor-pointer">
          <ArrowLeft size={18} />
        </Link>
        <h2 className="text-lg font-bold">User Audit Inspector</h2>
      </div>

      {/* Info card */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex gap-4">
          <div className="w-14 h-14 rounded-full bg-blue-500 text-white font-bold text-xl flex items-center justify-center border shadow-sm flex-shrink-0">
            {user.name.split(' ').map((n) => n[0]).join('')}
          </div>
          <div>
            <h2 className="text-lg font-bold">{user.name}</h2>
            <p className="text-xs text-[#64748B] mt-0.5">Role level: <strong className="text-blue-600">{user.role}</strong></p>
            <div className="flex flex-wrap items-center gap-3 mt-2 text-xs text-[#64748B] font-semibold">
              <span className="flex items-center gap-0.5"><Mail size={12} /> {user.email}</span>
              <span className="flex items-center gap-0.5"><MapPin size={12} /> {user.country}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className={`text-[10px] font-bold px-3 py-1 rounded-full border uppercase tracking-wider ${getStatusColor(user.status)}`}>
            {user.status}
          </span>
        </div>
      </div>

      {/* Columns splits */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left biography & qualifications */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-3">
            <h4 className="font-bold text-sm text-[#0F172A] border-b border-[#F1F5F9] pb-2">Biography summary</h4>
            <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed">{user.bio || 'No biography written.'}</p>
          </div>

          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <h4 className="font-bold text-sm text-[#0F172A] border-b border-[#F1F5F9] pb-2">Experience & Skills</h4>
            <div className="space-y-3 text-xs sm:text-sm">
              <div>
                <span className="font-semibold text-slate-500 block mb-0.5">Years of Experience</span>
                <span className="font-bold text-[#0F172A]">{user.experience || 'Not declared'}</span>
              </div>
              {user.skills && (
                <div>
                  <span className="font-semibold text-slate-500 block mb-1">Keywords Skills index</span>
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {user.skills.map((s) => (
                      <span key={s} className="bg-slate-50 text-slate-700 border border-slate-100 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wide">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Admin Controls Panel */}
        <div className="space-y-6">
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <h4 className="font-bold text-sm text-[#0F172A] border-b border-[#F1F5F9] pb-2 flex items-center gap-1.5">
              <ShieldAlert size={16} className="text-red-500" />
              Administrative Actions
            </h4>

            <div className="flex flex-col gap-2">
              {user.status === 'Active' ? (
                <button
                  onClick={() => handleStatusToggle('Suspended')}
                  className="bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs py-2 rounded-xl transition-all cursor-pointer text-center"
                >
                  Suspend User Account
                </button>
              ) : (
                <button
                  onClick={() => handleStatusToggle('Active')}
                  className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs py-2 rounded-xl transition-all cursor-pointer text-center"
                >
                  Activate User Account
                </button>
              )}

              {user.role !== 'Admin' && (
                <button
                  onClick={() => handleRoleChange('Admin')}
                  className="bg-slate-800 hover:bg-slate-900 text-white font-bold text-xs py-2 rounded-xl transition-all cursor-pointer text-center"
                >
                  Promote to Platform Admin
                </button>
              )}

              {user.role !== 'Candidate' && (
                <button
                  onClick={() => handleRoleChange('Candidate')}
                  className="bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 font-bold text-xs py-2 rounded-xl transition-all cursor-pointer text-center"
                >
                  Demote to Candidate
                </button>
              )}

              <button
                onClick={handleDelete}
                className="bg-red-600 hover:bg-red-700 text-white font-bold text-xs py-2 rounded-xl transition-all cursor-pointer text-center"
              >
                Delete Account Permanently
              </button>
            </div>
          </div>

          {user.atsScore && (
            <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-3">
              <h4 className="font-bold text-sm text-[#0F172A] flex items-center gap-1.5">
                <Bot size={16} className="text-purple-600" />
                Resume Parsing Evaluation
              </h4>
              <div className="flex items-center gap-4">
                <div className="text-center bg-[#F8FAFC] border border-[#E2E8F0] px-4 py-2 rounded-xl flex-shrink-0">
                  <span className="text-lg font-black text-[#0F172A]">{user.atsScore}%</span>
                  <p className="text-[8px] text-[#64748B] font-bold mt-0.5 uppercase">ATS SCORE</p>
                </div>
                <p className="text-xs text-[#64748B] leading-relaxed">
                  Candidate resume parser evaluation details. Checked keywords matching.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
