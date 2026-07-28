'use client';

import { useState } from 'react';
import { TwoFactorMethod } from '@/types/twoFactor';
import { twoFactorService } from '@/services/twoFactor.service';

export function useTwoFactor() {
  const [method, setMethod] = useState<TwoFactorMethod>('authenticator');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const verifyCode = async (code: string, rememberDevice = false) => {
    setLoading(true);
    setError('');
    try {
      const res = await twoFactorService.verifyTwoFactor(code, method, rememberDevice);
      if (res.success) {
        setSuccess(true);
        return true;
      } else {
        setError(res.message);
        return false;
      }
    } catch {
      setError('2FA verification failed');
      return false;
    } finally {
      setLoading(false);
    }
  };

  return {
    method,
    setMethod,
    loading,
    error,
    success,
    verifyCode,
  };
}
