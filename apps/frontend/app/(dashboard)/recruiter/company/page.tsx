'use client';

import React, { useState, useEffect } from 'react';
import { useCompany } from '@/hooks/useCompany';
import { Loader2, Save, Building, MapPin, Globe, Users, Briefcase } from 'lucide-react';

export default function RecruiterCompanyPage() {
  const { company, loading, error, updateCompany } = useCompany();

  const [name, setName] = useState('');
  const [industry, setIndustry] = useState('');
  const [about, setAbout] = useState('');
  const [location, setLocation] = useState('');
  const [website, setWebsite] = useState('');
  const [employees, setEmployees] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (company) {
      setName(company.name || '');
      setIndustry(company.industry || '');
      setAbout(company.about || '');
      setLocation(company.location || '');
      setWebsite(company.website || '');
      setEmployees(company.employees || '');
    }
  }, [company]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!company) return;
    if (!name.trim()) {
      alert('Company Name is required.');
      return;
    }
    setSaving(true);
    try {
      const success = await updateCompany({
        ...company,
        name: name.trim(),
        industry: industry.trim(),
        about: about.trim(),
        location: location.trim(),
        website: website.trim(),
        employees: employees.trim(),
      });
      if (success) {
        alert('Company profile saved successfully!');
      } else {
        alert('Failed to save company profile.');
      }
    } catch (err: any) {
      alert(err?.message || 'Failed to save company profile.');
    } finally {
      setSaving(false);
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

  if (error || !company) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Error Loading Company Profile</h3>
        <p className="text-sm text-[#64748B]">{error || 'Failed load'}</p>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-4xl mx-auto text-[#0F172A] text-left">
      <div className="border-b border-[#E2E8F0] pb-5">
        <h1 className="text-xl sm:text-2xl font-bold">Company Profile</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">Manage details displayed on job advertisements and listing listings.</p>
      </div>

      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-6">
        <div className="flex gap-4">
          <div className={`w-14 h-14 rounded-2xl ${company.logoColor || 'bg-blue-600'} flex items-center justify-center text-white font-black text-xl shadow-sm flex-shrink-0`}>
            {name ? name.charAt(0).toUpperCase() : 'C'}
          </div>
          <div>
            <h2 className="text-lg font-bold">{name || company.name}</h2>
            <p className="text-xs text-[#64748B] mt-0.5">Founded in {company.founded} · {industry || company.industry}</p>
          </div>
        </div>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 sm:p-6 shadow-sm space-y-4">
          <h3 className="font-bold text-xs uppercase tracking-wider text-[#64748B]">Information Fields</h3>

          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-[#475569] mb-1.5 flex items-center gap-1">
                <Building size={12} /> Company Name *
              </label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Company Name"
                className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-[#475569] mb-1.5 flex items-center gap-1">
                <Briefcase size={12} /> Industry Sector
              </label>
              <input
                type="text"
                value={industry}
                onChange={(e) => setIndustry(e.target.value)}
                placeholder="Software and Technology"
                className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-[#475569] mb-1.5 flex items-center gap-1">
                <MapPin size={12} /> Office Location
              </label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="San Francisco, CA (Remote)"
                className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-[#475569] mb-1.5 flex items-center gap-1">
                <Globe size={12} /> Company URL Website
              </label>
              <input
                type="text"
                value={website}
                onChange={(e) => setWebsite(e.target.value)}
                placeholder="https://example.com"
                className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-[#475569] mb-1.5 flex items-center gap-1">
                <Users size={12} /> Headcount size range
              </label>
              <input
                type="text"
                value={employees}
                onChange={(e) => setEmployees(e.target.value)}
                placeholder="50 - 200 Employees"
                className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
          </div>

          <div className="pt-2">
            <label className="block text-xs font-bold text-[#475569] mb-1.5">About Corporate Summary</label>
            <textarea
              rows={4}
              value={about}
              onChange={(e) => setAbout(e.target.value)}
              placeholder="Describe your company mission and domain..."
              className="w-full px-3.5 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white resize-none"
            />
          </div>
        </div>

        {/* Culture & Benefits details cards */}
        <div className="grid sm:grid-cols-2 gap-6">
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-3">
            <h4 className="font-bold text-xs uppercase tracking-wider text-[#64748B] border-b border-[#F1F5F9] pb-2">
              Corporate Culture pillars
            </h4>
            <ul className="space-y-2 text-xs text-slate-600">
              {company.culture.map(c => (
                <li key={c} className="flex items-start gap-1.5">
                  <span className="text-blue-500 font-bold">•</span>
                  <span>{c}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-3">
            <h4 className="font-bold text-xs uppercase tracking-wider text-[#64748B] border-b border-[#F1F5F9] pb-2">
              Hiring Perks & Benefits
            </h4>
            <ul className="space-y-2 text-xs text-slate-600">
              {company.benefits.map(b => (
                <li key={b} className="flex items-start gap-1.5">
                  <span className="text-green-500 font-bold">•</span>
                  <span>{b}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={saving}
            className="inline-flex items-center gap-1.5 bg-[#2563EB] hover:bg-[#1D4ED8] disabled:opacity-50 text-white font-bold text-xs px-4 py-2.5 rounded-xl transition-colors cursor-pointer"
          >
            {saving ? <Loader2 size={14} className="animate-spin" /> : <Save size={14} />}
            {saving ? 'Saving...' : 'Save Profile'}
          </button>
        </div>
      </form>
    </div>
  );
}
