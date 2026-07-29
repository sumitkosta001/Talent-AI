'use client';

import React, { useState, useEffect } from 'react';
import { CompanyService } from '@/services/company.service';
import { Company } from '@/types/company';
import { Eye, Building, Trash2, ShieldAlert } from 'lucide-react';
import Link from 'next/link';
import { Loader2 } from 'lucide-react';

export default function AdminCompaniesListPage() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadData() {
    try {
      const items = await CompanyService.getCompanies();
      setCompanies(items);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  const handleDelete = (id: string) => {
    const ok = window.confirm('Are you sure you want to delete this company profile?');
    if (ok) {
      setCompanies((prev) => prev.filter(c => c.id !== id));
      alert('Company profile removed successfully.');
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading corporate accounts profiles...</p>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto text-[#0F172A]">
      <div className="text-left">
        <h1 className="text-xl sm:text-2xl font-bold">Manage Companies Profiles</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">Edit, delete, or inspect platform corporate organizations.</p>
      </div>

      <div className="bg-white rounded-2xl border border-[#E2E8F0] overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-[#F8FAFC] border-b border-[#E2E8F0] text-xs font-bold text-[#64748B] uppercase tracking-wider">
              <tr>
                <th className="px-5 py-3">Company Logo</th>
                <th className="px-5 py-3">Industry</th>
                <th className="px-5 py-3">Headcount Size</th>
                <th className="px-5 py-3">Headquarters</th>
                <th className="px-5 py-3">Open Positions</th>
                <th className="px-5 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#F1F5F9] text-xs sm:text-sm">
              {companies.map((comp) => (
                <tr key={comp.id} className="hover:bg-[#F8FAFC]/50 transition-colors">
                  <td className="px-5 py-4 flex items-center gap-3">
                    <div className={`w-8 h-8 rounded-lg ${comp.logoColor} flex items-center justify-center text-white font-bold text-xs flex-shrink-0`}>
                      {comp.logo}
                    </div>
                    <div>
                      <Link href={`/admin/companies/${comp.id}`} className="font-bold text-[#0F172A] hover:text-blue-600 transition-colors">
                        {comp.name}
                      </Link>
                      <p className="text-[10px] text-[#64748B] font-semibold mt-0.5">{comp.website}</p>
                    </div>
                  </td>
                  <td className="px-5 py-4 font-semibold text-slate-700">{comp.industry}</td>
                  <td className="px-5 py-4 font-semibold text-slate-600">{comp.employees}</td>
                  <td className="px-5 py-4 font-semibold text-slate-700">{comp.headquarters}</td>
                  <td className="px-5 py-4 font-bold text-[#0F172A]">{comp.openPositions} jobs</td>
                  <td className="px-5 py-4 text-right">
                    <div className="flex items-center justify-end gap-1.5">
                      <Link
                        href={`/admin/companies/${comp.id}`}
                        className="p-1 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
                        title="View company details"
                      >
                        <Eye size={14} />
                      </Link>
                      <button
                        onClick={() => handleDelete(comp.id)}
                        className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
                        title="Delete Company"
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
