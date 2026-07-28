import React from 'react';
import RegisterForm from '@/components/auth/RegisterForm';
import AuthLayout from '@/components/auth/AuthLayout';

export default function Page() {
  return (
    <AuthLayout
      title="Create your account"
      subtitle="Join TalentAI to access smart candidate matching and resume ATS scoring"
    >
      <RegisterForm />
    </AuthLayout>
  );
}
