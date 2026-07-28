'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Sun, CloudSun, Moon, ShieldAlert, Sparkles, User, FileText, CheckCircle2 } from 'lucide-react';
import Link from 'next/link';

interface GreetingCardProps {
  name: string;
  profileCompletion: number;
  atsScore: number;
  careerScore: number;
  resumeScore: number;
}

export default function GreetingCard({
  name,
  profileCompletion,
  atsScore,
  careerScore,
  resumeScore,
}: GreetingCardProps) {
  const [time, setTime] = useState('');
  const [greeting, setGreeting] = useState('Welcome back');
  const [quote, setQuote] = useState('Your future is created by what you do today, not tomorrow.');

  const quotes = [
    'Your future is created by what you do today, not tomorrow.',
    'Opportunities don’t happen, you create them.',
    'It always seems impossible until it’s done.',
    'Action is the foundational key to all success.',
    'Believe you can and you’re halfway there.',
  ];

  useEffect(() => {
    // Clock
    const updateTime = () => {
      const now = new Date();
      setTime(
        now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true })
      );

      const hour = now.getHours();
      if (hour < 12) {
        setGreeting('Good Morning');
      } else if (hour < 18) {
        setGreeting('Good Afternoon');
      } else {
        setGreeting('Good Evening');
      }
    };

    updateTime();
    const interval = setInterval(updateTime, 1000);

    // Random Quote
    const randomQuoteIndex = Math.floor(Math.random() * quotes.length);
    setQuote(quotes[randomQuoteIndex]);

    return () => clearInterval(interval);
  }, []);

  const getGreetingIcon = () => {
    if (greeting === 'Good Morning') return <Sun className="text-amber-500 w-8 h-8 animate-pulse" />;
    if (greeting === 'Good Afternoon') return <CloudSun className="text-orange-400 w-8 h-8" />;
    return <Moon className="text-indigo-400 w-8 h-8" />;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="relative overflow-hidden bg-gradient-to-br from-[#0F172A] via-[#1E293B] to-[#0F172A] rounded-3xl p-6 text-white border border-slate-800 shadow-xl"
    >
      {/* Background radial highlight */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none" />

      <div className="flex flex-col lg:flex-row justify-between gap-6 relative z-10">
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-white/10 rounded-2xl flex items-center justify-center border border-white/10">
              {getGreetingIcon()}
            </div>
            <div>
              <h1 className="text-xl sm:text-2xl font-bold tracking-tight">
                {greeting}, <span className="bg-gradient-to-r from-blue-400 to-indigo-300 bg-clip-text text-transparent">{name}</span>
              </h1>
              <p className="text-xs text-slate-400 mt-0.5 font-medium">{time || '10:00 AM'}</p>
            </div>
          </div>

          <p className="text-xs sm:text-sm text-slate-300 max-w-lg italic font-medium leading-relaxed">
            "{quote}"
          </p>

          <div className="flex items-center gap-2 bg-white/5 border border-white/10 px-3 py-1.5 rounded-full w-fit">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
            <span className="text-[11px] text-slate-300 font-semibold">
              San Francisco, CA · 68°F · Sunny
            </span>
          </div>
        </div>

        {/* Progress Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-2 gap-3 min-w-[280px]">
          {/* Profile Completion */}
          <Link href="/candidate/profile" className="group">
            <div className="bg-white/5 hover:bg-white/10 border border-white/10 p-3 rounded-2xl transition-all duration-200 cursor-pointer">
              <div className="flex justify-between items-center mb-1">
                <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Profile</span>
                <User size={12} className="text-slate-400 group-hover:text-blue-400 transition-colors" />
              </div>
              <p className="text-lg font-bold text-slate-100">{profileCompletion}%</p>
              <div className="w-full bg-white/15 h-1.5 rounded-full mt-2 overflow-hidden">
                <div
                  className="bg-blue-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${profileCompletion}%` }}
                />
              </div>
            </div>
          </Link>

          {/* AI Career Score */}
          <Link href="/candidate/ai/career-score" className="group">
            <div className="bg-white/5 hover:bg-white/10 border border-white/10 p-3 rounded-2xl transition-all duration-200 cursor-pointer">
              <div className="flex justify-between items-center mb-1">
                <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Coach Score</span>
                <Sparkles size={12} className="text-slate-400 group-hover:text-indigo-400 transition-colors" />
              </div>
              <p className="text-lg font-bold text-slate-100">{careerScore}</p>
              <div className="w-full bg-white/15 h-1.5 rounded-full mt-2 overflow-hidden">
                <div
                  className="bg-indigo-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${careerScore}%` }}
                />
              </div>
            </div>
          </Link>

          {/* Resume Score */}
          <Link href="/candidate/resume" className="group">
            <div className="bg-white/5 hover:bg-white/10 border border-white/10 p-3 rounded-2xl transition-all duration-200 cursor-pointer">
              <div className="flex justify-between items-center mb-1">
                <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Resume</span>
                <FileText size={12} className="text-slate-400 group-hover:text-emerald-400 transition-colors" />
              </div>
              <p className="text-lg font-bold text-slate-100">{resumeScore}/100</p>
              <div className="w-full bg-white/15 h-1.5 rounded-full mt-2 overflow-hidden">
                <div
                  className="bg-emerald-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${resumeScore}%` }}
                />
              </div>
            </div>
          </Link>

          {/* ATS Score */}
          <Link href="/candidate/ats" className="group">
            <div className="bg-white/5 hover:bg-white/10 border border-white/10 p-3 rounded-2xl transition-all duration-200 cursor-pointer">
              <div className="flex justify-between items-center mb-1">
                <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">ATS Score</span>
                <CheckCircle2 size={12} className="text-slate-400 group-hover:text-rose-400 transition-colors" />
              </div>
              <p className="text-lg font-bold text-slate-100">{atsScore}%</p>
              <div className="w-full bg-white/15 h-1.5 rounded-full mt-2 overflow-hidden">
                <div
                  className="bg-rose-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${atsScore}%` }}
                />
              </div>
            </div>
          </Link>
        </div>
      </div>
    </motion.div>
  );
}
