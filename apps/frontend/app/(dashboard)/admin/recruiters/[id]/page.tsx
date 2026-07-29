'use client';

import React, { use, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { AdminUserService } from '@/services/user.service';
import { AdminUser, UserStatus } from '@/types/user';
import { Loader2, ArrowLeft, Mail, Phone, MapPin, ShieldAlert } from 'lucide-react';
import Link from 'next/link';

interface AdminRecruiterDetailPageProps {
  params: Promise<{ id: string }>;
}

export default function AdminRecruiterDetailPage({ params }: AdminRecruiterDetailPageProps) {
  const { id } = use(params);
  const router = useRouter();

  const [user, setUser] = useState<AdminUser | null>(null);
  const [loading, setLoading] = useState(true);

  async function loadData() {
    try {
      const match = await AdminUserService.getUserById(id);
      if (match && match.role === 'Recruiter') {
        setUser(match);
      } else {
        setUser(null);
      }
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
      alert(`Recruiter status updated to ${status}!`);
      loadData();
    }
  };

  const handleDelete = async () => {
    if (!user) return;
    const ok = window.confirm('Are you sure you want to delete this recruiter account?');
    if (ok) {
      const res = await AdminUserService.deleteUser(user.id);
      if (res) {
        alert('Recruiter account deleted successfully.');
        router.push('/admin/recruiters');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading recruiter credentials...</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Recruiter Not Found</h3>
        <Link href="/admin/recruiters" className="inline-block bg-blue-600 text-white px-4 py-2 rounded-xl text-xs font-semibold">
          Back to Directory
        </Link>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-4xl mx-auto text-[#0F172A] text-left">
      <div className="flex items-center gap-3">
        <Link href="/admin/recruiters" className="text-slate-400 hover:text-[#0F172A] cursor-pointer">
          <ArrowLeft size={18} />
        </Link>
        <h2 className="text-lg font-bold">Recruiter Account evaluation</h2>
      </div>

      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex gap-4">
          <div className="w-14 h-14 rounded-full bg-blue-500 text-white font-bold text-xl flex items-center justify-center border shadow-sm flex-shrink-0">
            {user.name.split(' ').map((n) => n[0]).join('')}
          </div>
          <div>
            <h2 className="text-lg font-bold">{user.name}</h2>
            <p className="text-xs text-[#64748B] mt-0.5">Recruiting expertise: <strong className="text-blue-600">{user.experience}</strong></p>
            <div className="flex flex-wrap items-center gap-3 mt-2 text-xs text-[#64748B] font-semibold">
              <span className="flex items-center gap-0.5"><Mail size={12} /> {user.email}</span>
              <span className="flex items-center gap-0.5"><MapPin size={12} /> {user.country}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className={`text-[10px] font-bold px-3 py-1 rounded-full border uppercase tracking-wider ${
            user.status === 'Active' ? 'text-emerald-700 bg-emerald-50 border-emerald-200' : 'text-amber-700 bg-amber-50 border-amber-200'
          }`}>
            {user.status}
          </span>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2 bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-3">
          <h4 className="font-bold text-xs uppercase tracking-wider text-[#64748B] border-b border-[#F1F5F9] pb-2">Biography details</h4>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">{user.bio || 'No biography written.'}</p>
        </div>

        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
          <h4 className="font-bold text-sm text-[#0F172A] border-b border-[#F1F5F9] pb-2 flex items-center gap-1.5">
            <ShieldAlert size={16} className="text-red-500" />
            Recruiter Actions
          </h4>

          <div className="flex flex-col gap-2">
            {user.status === 'Active' ? (
              <button
                onClick={() => handleStatusToggle('Suspended')}
                className="bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs py-2 rounded-xl transition-all cursor-pointer text-center"
              >
                Suspend Recruiter
              </button>
            ) : (
              <button
                onClick={() => handleStatusToggle('Active')}
                className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs py-2 rounded-xl transition-all cursor-pointer text-center"
              >
                Activate Recruiter
              </button>
            )}

            <button
              onClick={handleDelete}
              className="bg-red-600 hover:bg-red-700 text-white font-bold text-xs py-2 rounded-xl transition-all cursor-pointer text-center"
            >
              Delete Recruiter Account
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
