'use client';

import React, { use, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { CompanyService } from '@/services/company.service';
import { Company } from '@/types/company';
import { Loader2, ArrowLeft, Globe, MapPin, Users, Calendar, Award } from 'lucide-react';
import Link from 'next/link';

interface AdminCompanyDetailPageProps {
  params: Promise<{ id: string }>;
}

export default function AdminCompanyDetailPage({ params }: AdminCompanyDetailPageProps) {
  const { id } = use(params);
  const router = useRouter();

  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(true);

  async function loadData() {
    try {
      const match = await CompanyService.getCompanyById(id);
      setCompany(match);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, [id]);

  const handleDelete = () => {
    if (!company) return;
    const ok = window.confirm('Are you sure you want to delete this company?');
    if (ok) {
      alert('Company profile removed successfully.');
      router.push('/admin/companies');
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading company configuration profile...</p>
      </div>
    );
  }

  if (!company) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Company Profile Not Found</h3>
        <Link href="/admin/companies" className="inline-block bg-blue-600 text-white px-4 py-2 rounded-xl text-xs font-semibold">
          Back to list
        </Link>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-4xl mx-auto text-[#0F172A] text-left">
      <div className="flex items-center gap-3">
        <Link href="/admin/companies" className="text-slate-400 hover:text-[#0F172A] cursor-pointer">
          <ArrowLeft size={18} />
        </Link>
        <h2 className="text-lg font-bold">Company profile inspector</h2>
      </div>

      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex gap-4">
          <div className={`w-14 h-14 rounded-2xl ${company.logoColor} flex items-center justify-center text-white font-black text-xl shadow-sm flex-shrink-0`}>
            {company.logo}
          </div>
          <div>
            <h2 className="text-lg font-bold">{company.name}</h2>
            <p className="text-xs text-[#64748B] mt-0.5">Founded in {company.founded} · {company.industry}</p>
          </div>
        </div>

        <button
          onClick={handleDelete}
          className="bg-red-600 hover:bg-red-700 text-white font-bold text-xs px-4 py-2 rounded-xl transition-all cursor-pointer"
        >
          Delete Company
        </button>
      </div>

      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 sm:p-6 shadow-sm space-y-4">
        <h3 className="font-bold text-xs uppercase tracking-wider text-[#64748B] border-b border-[#F1F5F9] pb-2">
          Corporate specifications
        </h3>

        <div className="grid sm:grid-cols-2 gap-4 text-xs sm:text-sm">
          <div>
            <span className="font-semibold text-slate-500 block mb-0.5">Headquarters Location</span>
            <span className="font-bold text-[#0F172A] flex items-center gap-1"><MapPin size={12} /> {company.headquarters}</span>
          </div>
          <div>
            <span className="font-semibold text-slate-500 block mb-0.5">Corporate Website</span>
            <span className="font-bold text-[#0F172A] flex items-center gap-1"><Globe size={12} /> {company.website}</span>
          </div>
          <div>
            <span className="font-semibold text-slate-500 block mb-0.5">Employees size</span>
            <span className="font-bold text-[#0F172A] flex items-center gap-1"><Users size={12} /> {company.employees}</span>
          </div>
          <div>
            <span className="font-semibold text-slate-500 block mb-0.5">Platforms jobs posted</span>
            <span className="font-bold text-blue-600">{company.openPositions} active listings</span>
          </div>
        </div>

        <div className="pt-2">
          <span className="font-semibold text-slate-500 block mb-1">About Summary</span>
          <p className="text-xs text-slate-600 leading-relaxed">{company.about}</p>
        </div>
      </div>
    </div>
  );
}
