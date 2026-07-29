'use client';

import React from 'react';
import { useUsers } from '@/hooks/useUsers';
import UsersTable from '@/components/admin/UsersTable';
import { Loader2, Search } from 'lucide-react';

export default function AdminUsersListPage() {
  const {
    users,
    loading,
    error,
    search,
    setSearch,
    roleFilter,
    setRoleFilter,
    statusFilter,
    setStatusFilter,
    sortBy,
    setSortBy,
    deleteUser,
    updateStatus,
    updateRole,
  } = useUsers();

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading platform accounts directory...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Error Loading Users</h3>
        <p className="text-sm text-[#64748B]">{error}</p>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto text-[#0F172A]">
      {/* Title */}
      <div className="text-left">
        <h1 className="text-xl sm:text-2xl font-bold">Platform Users Directory</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">Moderate roles, edit settings, delete profiles, or suspend candidates/recruiters.</p>
      </div>

      {/* Filters Card */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-4 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="flex-1 relative">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search user by name, email, or country..."
              className="w-full pl-9 pr-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div className="w-full md:w-48">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="w-full px-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
            >
              <option value="newest">Newest Registered</option>
              <option value="oldest">Oldest Registered</option>
              <option value="ats">Highest ATS Score</option>
              <option value="alphabetical">Alphabetical</option>
            </select>
          </div>
        </div>

        {/* Dropdowns */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-2 border-t border-[#F1F5F9] items-center text-left">
          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">User Role</label>
            <select
              value={roleFilter}
              onChange={(e) => setRoleFilter(e.target.value)}
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
            >
              <option value="">All Roles</option>
              <option value="Candidate">Candidate</option>
              <option value="Recruiter">Recruiter</option>
              <option value="Super Admin">Super Admin</option>
            </select>
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Status State</label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
            >
              <option value="">All Statuses</option>
              <option value="Active">Active</option>
              <option value="Suspended">Suspended</option>
            </select>
          </div>
        </div>
      </div>

      {/* Users table list */}
      {users.length === 0 ? (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-12 text-center shadow-sm">
          <p className="text-sm text-[#64748B] font-semibold">No platform accounts matched your criteria.</p>
        </div>
      ) : (
        <UsersTable
          users={users}
          onRoleChange={updateRole}
          onStatusChange={updateStatus}
          onDelete={deleteUser}
        />
      )}
    </div>
  );
}
