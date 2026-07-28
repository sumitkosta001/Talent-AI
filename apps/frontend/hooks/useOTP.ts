'use client';

import { useState, useRef, useEffect } from 'react';
import { otpService } from '@/services/otp.service';

export function useOTP(length = 6, onComplete?: (code: string) => void) {
  const [digits, setDigits] = useState<string[]>(Array(length).fill(''));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [countdown, setCountdown] = useState(30);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    if (countdown <= 0) return;
    const timer = setInterval(() => {
      setCountdown((prev) => prev - 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [countdown]);

  const handleChange = (index: number, value: string) => {
    if (!/^\d*$/.test(value)) return;
    const newDigits = [...digits];
    newDigits[index] = value.slice(-1);
    setDigits(newDigits);
    setError('');

    if (value && index < length - 1) {
      inputRefs.current[index + 1]?.focus();
    }

    const fullCode = newDigits.join('');
    if (fullCode.length === length && !newDigits.includes('')) {
      if (onComplete) onComplete(fullCode);
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace') {
      if (!digits[index] && index > 0) {
        inputRefs.current[index - 1]?.focus();
      }
    }
  };

  const handlePaste = (e: React.ClipboardEvent<HTMLInputElement>) => {
    e.preventDefault();
    const pasted = e.clipboardData.getData('text').trim();
    if (!/^\d+$/.test(pasted)) return;
    const pastedDigits = pasted.slice(0, length).split('');
    const newDigits = [...digits];
    pastedDigits.forEach((d, i) => {
      newDigits[i] = d;
    });
    setDigits(newDigits);
    setError('');
    
    const nextEmpty = newDigits.findIndex((d) => !d);
    if (nextEmpty !== -1) {
      inputRefs.current[nextEmpty]?.focus();
    } else {
      inputRefs.current[length - 1]?.focus();
      if (onComplete) onComplete(newDigits.join(''));
    }
  };

  const verify = async (codeOverride?: string) => {
    const code = codeOverride || digits.join('');
    if (code.length !== length) {
      setError(`Please enter all ${length} digits`);
      return false;
    }
    setLoading(true);
    setError('');
    try {
      const res = await otpService.verifyOTP(code);
      if (res.success) {
        setSuccess(true);
        return true;
      } else {
        setError(res.message || 'Verification failed');
        return false;
      }
    } catch {
      setError('System verification error. Try again.');
      return false;
    } finally {
      setLoading(false);
    }
  };

  const resend = async (target?: string) => {
    if (countdown > 0) return;
    setLoading(true);
    try {
      await otpService.resendOTP(target);
      setCountdown(30);
      setDigits(Array(length).fill(''));
      setError('');
    } finally {
      setLoading(false);
    }
  };

  return {
    digits,
    loading,
    error,
    success,
    countdown,
    inputRefs,
    handleChange,
    handleKeyDown,
    handlePaste,
    verify,
    resend,
  };
}
