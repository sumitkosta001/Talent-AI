import React from 'react';
import ForgotPasswordForm from '@/components/auth/ForgotPasswordForm';
import AuthLayout from '@/components/auth/AuthLayout';

export default function Page() {
  return (
    <AuthLayout
      title="Reset Password"
      subtitle="Enter your email to receive password reset instructions"
    >
      <ForgotPasswordForm />
    </AuthLayout>
  );
}
