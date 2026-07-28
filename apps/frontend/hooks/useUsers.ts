'use client';

import { useState, useEffect, useCallback } from 'react';
import { AdminUser, UserRole, UserStatus } from '@/types/user';
import { AdminUserService } from '@/services/user.service';

export function useUsers() {
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'ats' | 'alphabetical'>('newest');

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const items = await AdminUserService.getUsers();
      setUsers(items);
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch platform accounts directory');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  const handleDelete = useCallback(async (id: string) => {
    try {
      await AdminUserService.deleteUser(id);
      setUsers((prev) => prev.filter((u) => u.id !== id));
      return true;
    } catch {
      return false;
    }
  }, []);

  const handleUpdateStatus = useCallback(async (id: string, newStatus: UserStatus) => {
    try {
      const updated = await AdminUserService.updateStatus(id, newStatus);
      setUsers((prev) => prev.map((u) => (u.id === id ? updated : u)));
      return true;
    } catch {
      return false;
    }
  }, []);

  const handleUpdateRole = useCallback(async (id: string, newRole: UserRole) => {
    try {
      const updated = await AdminUserService.updateRole(id, newRole);
      setUsers((prev) => prev.map((u) => (u.id === id ? updated : u)));
      return true;
    } catch {
      return false;
    }
  }, []);

  const getFilteredAndSorted = useCallback(() => {
    let result = [...users];

    // Search matching
    if (search) {
      const q = search.toLowerCase();
      result = result.filter(
        (u) =>
          u.name.toLowerCase().includes(q) ||
          u.email.toLowerCase().includes(q) ||
          u.country.toLowerCase().includes(q)
      );
    }

    // Role filter
    if (roleFilter) {
      result = result.filter((u) => u.role === roleFilter);
    }

    // Status filter
    if (statusFilter) {
      result = result.filter((u) => u.status === statusFilter);
    }

    // Sorting
    if (sortBy === 'newest') {
      result.sort((a, b) => new Date(b.registrationDate).getTime() - new Date(a.registrationDate).getTime());
    } else if (sortBy === 'oldest') {
      result.sort((a, b) => new Date(a.registrationDate).getTime() - new Date(b.registrationDate).getTime());
    } else if (sortBy === 'ats') {
      result.sort((a, b) => (b.atsScore || 0) - (a.atsScore || 0));
    } else if (sortBy === 'alphabetical') {
      result.sort((a, b) => a.name.localeCompare(b.name));
    }

    return result;
  }, [users, search, roleFilter, statusFilter, sortBy]);

  return {
    users: getFilteredAndSorted(),
    rawUsers: users,
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
    deleteUser: handleDelete,
    updateStatus: handleUpdateStatus,
    updateRole: handleUpdateRole,
    refetch: fetchUsers,
  };
}
