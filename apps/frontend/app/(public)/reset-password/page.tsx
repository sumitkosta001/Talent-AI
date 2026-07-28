'use client';

import React from 'react';
import AuthLayout from '@/components/auth/AuthLayout';
import ResetPasswordForm from '@/components/auth/ResetPasswordForm';

export default function Page() {
  return (
    <AuthLayout
      title="Create New Password"
      subtitle="Choose a strong password meeting our enterprise security guidelines"
    >
      <ResetPasswordForm />
    </AuthLayout>
  );
}
