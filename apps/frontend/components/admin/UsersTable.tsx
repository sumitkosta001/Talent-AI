'use client';

import React from 'react';
import Link from 'next/link';
import { AdminUser, UserRole, UserStatus } from '@/types/user';
import { Eye, ArrowUp, ToggleLeft, ToggleRight, Trash2 } from 'lucide-react';

interface UsersTableProps {
  users: AdminUser[];
  onRoleChange: (id: string, role: UserRole) => void;
  onStatusChange: (id: string, status: UserStatus) => void;
  onDelete: (id: string) => void;
}

export default function UsersTable({ users, onRoleChange, onStatusChange, onDelete }: UsersTableProps) {
  const getStatusColor = (s: string) => {
    switch (s) {
      case 'Active':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'Suspended':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      default:
        return 'bg-slate-50 text-slate-600 border-slate-200';
    }
  };

  const getRoleColor = (r: string) => {
    if (r === 'Super Admin') return 'bg-red-50 text-red-700 border-red-200';
    if (r === 'Recruiter') return 'bg-violet-50 text-violet-700 border-violet-200';
    return 'bg-blue-50 text-blue-700 border-blue-200';
  };

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] overflow-hidden shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead className="bg-[#F8FAFC] border-b border-[#E2E8F0] text-xs font-bold text-[#64748B] uppercase tracking-wider">
            <tr>
              <th className="px-5 py-3">User Profile</th>
              <th className="px-5 py-3">Role</th>
              <th className="px-5 py-3">Status</th>
              <th className="px-5 py-3">Country</th>
              <th className="px-5 py-3">Last Login</th>
              <th className="px-5 py-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#F1F5F9] text-xs sm:text-sm">
            {users.map((user) => (
              <tr key={user.id} className="hover:bg-[#F8FAFC]/50 transition-colors">
                <td className="px-5 py-4">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-blue-500 text-white font-bold flex items-center justify-center text-xs flex-shrink-0">
                      {user.name.split(' ').map((n) => n[0]).join('')}
                    </div>
                    <div>
                      <Link href={`/admin/users/${user.id}`} className="font-bold text-[#0F172A] hover:text-blue-600 transition-colors">
                        {user.name}
                      </Link>
                      <p className="text-[10px] text-[#64748B] font-semibold mt-0.5">{user.email}</p>
                    </div>
                  </div>
                </td>

                <td className="px-5 py-4">
                  <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${getRoleColor(user.role)}`}>
                    {user.role}
                  </span>
                </td>

                <td className="px-5 py-4">
                  <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${getStatusColor(user.status)}`}>
                    {user.status}
                  </span>
                </td>

                <td className="px-5 py-4 font-semibold text-slate-700">{user.country}</td>
                <td className="px-5 py-4 font-semibold text-slate-500">{user.lastLogin}</td>

                <td className="px-5 py-4 text-right">
                  <div className="flex items-center justify-end gap-1.5">
                    <Link
                      href={`/admin/users/${user.id}`}
                      className="p-1 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
                      title="Inspect user details"
                    >
                      <Eye size={14} />
                    </Link>
                    {user.role !== 'Super Admin' && (
                      <>
                        <button
                          onClick={() => onRoleChange(user.id, 'Admin')}
                          className="p-1 text-slate-400 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors cursor-pointer"
                          title="Promote to admin"
                        >
                          <ArrowUp size={14} />
                        </button>
                        {user.status === 'Active' ? (
                          <button
                            onClick={() => onStatusChange(user.id, 'Suspended')}
                            className="p-1 text-slate-400 hover:text-amber-600 hover:bg-amber-50 rounded-lg transition-colors cursor-pointer"
                            title="Suspend user"
                          >
                            <ToggleLeft size={14} />
                          </button>
                        ) : (
                          <button
                            onClick={() => onStatusChange(user.id, 'Active')}
                            className="p-1 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors cursor-pointer"
                            title="Activate user"
                          >
                            <ToggleRight size={14} />
                          </button>
                        )}
                        <button
                          onClick={() => onDelete(user.id)}
                          className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
                          title="Remove user account"
                        >
                          <Trash2 size={14} />
                        </button>
                      </>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
