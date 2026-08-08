'use client';

import { useState, useEffect, useRef } from 'react';
import { VerificationStatus } from '@/types/verification';
import { verificationService } from '@/services/verification.service';

// Module-level cache to track verified/in-flight tokens and prevent duplicate requests during page lifecycle
const verifiedTokens = new Set<string>();

export function useEmailVerification(initialEmail: string = '', token: string | null = null) {
  const [email, setEmail] = useState(initialEmail);
  const [status, setStatus] = useState<VerificationStatus>('Pending');
  const [countdown, setCountdown] = useState(60);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const verifyAttempted = useRef(false);

  // Keep email in sync if initialEmail updates (e.g., searchParams are parsed after mount)
  useEffect(() => {
    if (initialEmail) {
      setEmail(initialEmail);
    }
  }, [initialEmail]);

  // Effect to automatically run token verification
  useEffect(() => {
    if (!token || verifyAttempted.current || verifiedTokens.has(token)) return;

    verifyAttempted.current = true;
    verifiedTokens.add(token);

    const verifyToken = async () => {
      setLoading(true);
      setError('');
      setMessage('');
      try {
        const res = await verificationService.verifyEmail(token);
        if (res.success) {
          if (res.email) {
            setEmail(res.email);
          }
          if (res.message === 'Email address is already verified.') {
            setStatus('AlreadyVerified');
            setMessage(res.message);
          } else {
            setStatus('Verified');
            setMessage(res.message || 'Email verified successfully.');
          }
        } else {
          setStatus('Failed');
          setError(res.message || 'Email verification failed.');
        }
      } catch (err: any) {
        const errMsg = err?.message || '';
        if (errMsg.includes('expired') || errMsg.includes('Expired')) {
          setStatus('Expired');
        } else if (errMsg.includes('already verified') || errMsg.includes('Already verified')) {
          setStatus('AlreadyVerified');
        } else {
          setStatus('Failed');
        }
        setError(errMsg || 'Email verification failed.');
      } finally {
        setLoading(false);
      }
    };

    verifyToken();
  }, [token]);

  useEffect(() => {
    if (countdown <= 0) return;
    const timer = setInterval(() => {
      setCountdown((prev) => prev - 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [countdown]);

  const resend = async (targetEmail?: string) => {
    const e = targetEmail || email;
    if (!e) {
      setError('Email address is required to resend verification.');
      return;
    }
    setLoading(true);
    setError('');
    setMessage('');
    try {
      const res = await verificationService.resendVerificationEmail(e);
      setMessage(res.message || `Verification link sent to ${e}`);
      setCountdown(60);
    } catch (err: any) {
      setError(err?.message || 'Failed to resend verification email.');
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
    error,
    setError,
    resend,
  };
}
