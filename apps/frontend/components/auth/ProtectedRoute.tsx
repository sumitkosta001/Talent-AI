'use client';

import React from 'react';
import AuthGuard from './AuthGuard';
import RoleGuard from './RoleGuard';

interface ProtectedRouteProps {
  children: React.ReactNode;
  roles?: ('candidate' | 'recruiter' | 'admin')[];
}

export default function ProtectedRoute({ children, roles }: ProtectedRouteProps) {
  if (roles && roles.length > 0) {
    return (
      <AuthGuard>
        <RoleGuard allowedRoles={roles}>{children}</RoleGuard>
      </AuthGuard>
    );
  }

  return <AuthGuard>{children}</AuthGuard>;
}
