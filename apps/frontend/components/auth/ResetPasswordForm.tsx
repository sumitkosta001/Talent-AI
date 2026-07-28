'use client';

import React, { useState } from 'react';
import { Eye, EyeOff, CheckCircle2, ArrowRight } from 'lucide-react';
import Link from 'next/link';
import PasswordStrength from './PasswordStrength';
import { passwordService } from '@/services/password.service';

export default function ResetPasswordForm() {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPassword) {
      setError('Password is required');
      return;
    }
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    const { rules } = passwordService.evaluateStrength(newPassword);
    if (!rules.minLength || !rules.hasNumber) {
      setError('Please fulfill all password security rules');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const res = await passwordService.resetPassword('mock-token', newPassword);
      if (res.success) {
        setSuccess(true);
      } else {
        setError(res.message);
      }
    } catch {
      setError('Failed to reset password. Link may be expired.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-5 text-left">
      {success ? (
        <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 text-center space-y-4">
          <div className="w-14 h-14 bg-emerald-50 dark:bg-emerald-950/30 text-emerald-500 border border-emerald-100 dark:border-emerald-900/50 rounded-2xl flex items-center justify-center mx-auto">
            <CheckCircle2 size={28} />
          </div>
          <h3 className="text-lg font-black text-slate-900 dark:text-slate-100">
            Password Reset Complete
          </h3>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
            Your password has been securely updated. You can now log into your account with your new credentials.
          </p>
          <Link href="/login">
            <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl text-xs sm:text-sm transition-colors cursor-pointer mt-2">
              Back to Login
            </button>
          </Link>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="p-3 bg-rose-50 text-rose-600 dark:bg-rose-950/30 dark:text-rose-400 rounded-xl text-xs font-semibold border border-rose-100 dark:border-rose-900/50">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-slate-900 dark:text-slate-200 mb-1.5">
              New Password
            </label>
            <div className="relative">
              <input
                type={showPass ? 'text' : 'password'}
                required
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="Enter new password"
                className="w-full px-3.5 py-2.5 pr-10 border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:border-blue-500"
              />
              <button
                type="button"
                onClick={() => setShowPass(!showPass)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 cursor-pointer"
              >
                {showPass ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
            <PasswordStrength password={newPassword} showRules={true} />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-900 dark:text-slate-200 mb-1.5">
              Confirm New Password
            </label>
            <input
              type={showPass ? 'text' : 'password'}
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Re-enter new password"
              className="w-full px-3.5 py-2.5 border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:border-blue-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading || !newPassword || newPassword !== confirmPassword}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl shadow-sm text-xs sm:text-sm transition-colors cursor-pointer disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {loading ? 'Resetting Password...' : 'Reset Password'}
            {!loading && <ArrowRight size={16} />}
          </button>
        </form>
      )}
    </div>
  );
}
