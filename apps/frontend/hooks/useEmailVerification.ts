'use client';

import { useState, useEffect } from 'react';
import { VerificationStatus } from '@/types/verification';
import { verificationService } from '@/services/verification.service';

export function useEmailVerification(initialEmail = 'alex@example.com') {
  const [email, setEmail] = useState(initialEmail);
  const [status, setStatus] = useState<VerificationStatus>('Pending');
  const [countdown, setCountdown] = useState(60);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (countdown <= 0) return;
    const timer = setInterval(() => {
      setCountdown((prev) => prev - 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [countdown]);

  const resend = async (targetEmail?: string) => {
    if (countdown > 0) return;
    const e = targetEmail || email;
    setLoading(true);
    try {
      const res = await verificationService.resendVerificationEmail(e);
      setMessage(res.message);
      setCountdown(60);
    } finally {
      setLoading(false);
    }
  };

  return {
    email,
    setEmail,
    status,
    setStatus,
    countdown,
    loading,
    message,
    resend,
  };
}
