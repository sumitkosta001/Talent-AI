'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Eye, EyeOff, ArrowRight, User, Briefcase, Building2, Check } from 'lucide-react';
import PasswordStrength from './PasswordStrength';
import { authService } from '@/services/auth.service';

export default function RegisterForm() {
  const router = useRouter();
  const [role, setRole] = useState<'candidate' | 'recruiter' | 'company'>('candidate');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPass, setShowPass] = useState(false);
  const [agreeTerms, setAgreeTerms] = useState(false);
  const [newsletter, setNewsletter] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Full name is required');
      return;
    }
    if (!email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError('Valid email address is required');
      return;
    }
    if (!password || password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }
    if (!agreeTerms) {
      setError('You must accept the Terms of Service and Privacy Policy');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const res = await authService.register({ name, email, pass: password, role });
      if (res.success) {
        router.push('/verify-email');
      } else {
        setError(res.message);
      }
    } catch (err: any) {
      setError(err?.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full space-y-5 text-left">
      {error && (
        <div className="p-3 bg-rose-50 text-rose-600 dark:bg-rose-950/30 dark:text-rose-400 rounded-xl text-xs font-semibold border border-rose-100 dark:border-rose-900/50">
          {error}
        </div>
      )}

      <div>
        <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2 uppercase tracking-wider">
          Select Your Account Type
        </label>
        <div className="grid grid-cols-3 gap-2">
          {[
            { id: 'candidate', label: 'Candidate', icon: User },
            { id: 'recruiter', label: 'Recruiter', icon: Briefcase },
            { id: 'company', label: 'Company', icon: Building2 },
          ].map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              type="button"
              onClick={() => setRole(id as any)}
              className={`p-3 rounded-2xl border text-left transition-all cursor-pointer flex flex-col justify-between ${
                role === id
                  ? 'border-blue-600 bg-blue-50/50 dark:bg-blue-950/30 text-blue-600 dark:text-blue-400 shadow-xs'
                  : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:border-slate-300'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <Icon size={18} />
                {role === id && <Check size={14} className="text-blue-600 dark:text-blue-400" />}
              </div>
              <span className="text-xs font-extrabold">{label}</span>
            </button>
          ))}
        </div>
      </div>

      <form onSubmit={handleRegister} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-900 dark:text-slate-200 mb-1.5">
            Full Name
          </label>
          <input
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Alex Johnson"
            className="w-full px-3.5 py-2.5 border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:border-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-900 dark:text-slate-200 mb-1.5">
            Email Address
          </label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="alex@example.com"
            className="w-full px-3.5 py-2.5 border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:border-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-900 dark:text-slate-200 mb-1.5">
            Password
          </label>
          <div className="relative">
            <input
              type={showPass ? 'text' : 'password'}
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Create strong password"
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
          <PasswordStrength password={password} showRules={true} />
        </div>

        <div className="space-y-2 pt-1">
          <div className="flex items-start gap-2">
            <input
              type="checkbox"
              id="terms"
              checked={agreeTerms}
              onChange={(e) => setAgreeTerms(e.target.checked)}
              className="w-4 h-4 mt-0.5 rounded border-slate-300 dark:border-slate-700 text-blue-600 focus:ring-blue-500/20 cursor-pointer"
            />
            <label htmlFor="terms" className="text-xs text-slate-600 dark:text-slate-400 leading-normal cursor-pointer select-none">
              I agree to TalentAI&apos;s{' '}
              <a href="#" className="text-blue-600 dark:text-blue-400 underline font-semibold">Terms of Service</a>{' '}
              and{' '}
              <a href="#" className="text-blue-600 dark:text-blue-400 underline font-semibold">Privacy Policy</a>.
            </label>
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="newsletter"
              checked={newsletter}
              onChange={(e) => setNewsletter(e.target.checked)}
              className="w-4 h-4 rounded border-slate-300 dark:border-slate-700 text-blue-600 focus:ring-blue-500/20 cursor-pointer"
            />
            <label htmlFor="newsletter" className="text-xs text-slate-600 dark:text-slate-400 cursor-pointer select-none">
              Send me career insights and weekly AI job recommendations
            </label>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading || !agreeTerms}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl shadow-sm text-xs sm:text-sm transition-colors cursor-pointer disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {loading ? 'Creating Account...' : 'Create Account'}
          {!loading && <ArrowRight size={16} />}
        </button>
      </form>

      <p className="text-center text-xs sm:text-sm text-slate-500 dark:text-slate-400 pt-2">
        Already have an account?{' '}
        <Link href="/login" className="text-blue-600 dark:text-blue-400 font-bold hover:underline">
          Sign In
        </Link>
      </p>
    </div>
  );
}
