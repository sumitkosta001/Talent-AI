'use client';

import React, { useState, useEffect } from 'react';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import {
  Home, User, Upload, Briefcase, Building, Bell, Settings,
  BarChart2, Search, LogOut, FileText, ChevronLeft, ChevronRight,
  Menu, X, Bot, ChevronDown, Users, Activity, FileSpreadsheet
} from 'lucide-react';
import Breadcrumbs from '@/components/global/Breadcrumbs';
import ThemeSwitcher from '@/components/global/ThemeSwitcher';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const candidateNav = [
  { id: 'dashboard', label: 'Dashboard', icon: Home, href: '/candidate' },
  { id: 'resume-upload', label: 'Upload Resume', icon: Upload, href: '/candidate/resume/upload' },
  { id: 'resume-analysis', label: 'Resume Analysis', icon: FileText, href: '/candidate/resume/analysis' },
  { id: 'ats-score', label: 'ATS Score', icon: Bot, href: '/candidate/ats' },
  { id: 'job-listing', label: 'Browse Jobs', icon: Briefcase, href: '/candidate/jobs' },
  { id: 'my-applications', label: 'My Applications', icon: FileText, href: '/candidate/applications' },
  { id: 'notifications', label: 'Notifications', icon: Bell, href: '/candidate/notifications' },
  { id: 'settings', label: 'Settings', icon: Settings, href: '/candidate/settings' },
];

const recruiterNav = [
  { id: 'recruiter-dashboard', label: 'Dashboard', icon: Home, href: '/recruiter' },
  { id: 'job-listing', label: 'Job Listings', icon: Briefcase, href: '/recruiter/jobs' },
  { id: 'recruiter-applicants', label: 'Applicants', icon: Users, href: '/recruiter/applicants' },
  { id: 'company-profile', label: 'Company Profile', icon: Building, href: '/recruiter/company' },
  { id: 'analytics', label: 'Analytics', icon: BarChart2, href: '/recruiter/analytics' },
  { id: 'settings', label: 'Settings', icon: Settings, href: '/recruiter/settings' },
];

const adminNav = [
  { id: 'admin-dashboard', label: 'Dashboard', icon: Home, href: '/admin' },
  { id: 'admin-users', label: 'Users', icon: Users, href: '/admin/users' },
  { id: 'admin-recruiters', label: 'Recruiters', icon: User, href: '/admin/recruiters' },
  { id: 'admin-companies', label: 'Companies', icon: Building, href: '/admin/companies' },
  { id: 'admin-jobs', label: 'Jobs', icon: Briefcase, href: '/admin/jobs' },
  { id: 'admin-reports', label: 'Reports', icon: FileSpreadsheet, href: '/admin/reports' },
  { id: 'admin-analytics', label: 'Analytics', icon: BarChart2, href: '/admin/analytics' },
  { id: 'admin-system', label: 'System Health', icon: Activity, href: '/admin/system' },
  { id: 'admin-settings', label: 'Settings', icon: Settings, href: '/admin/settings' },
];

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const pathname = usePathname();
  const router = useRouter();

  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);

  useEffect(() => {
    setMobileOpen(false);
  }, [pathname]);

  const isAdmin = pathname.startsWith('/admin');
  const isRecruiter = pathname.startsWith('/recruiter');
  const navItems = isAdmin ? adminNav : isRecruiter ? recruiterNav : candidateNav;

  const userName = isAdmin ? 'Sarah Mitchell' : isRecruiter ? 'Sarah Mitchell' : 'Alex Johnson';
  const userRole = isAdmin ? 'Super Admin' : isRecruiter ? 'Recruiter' : 'Candidate';
  const userInitials = isAdmin ? 'SM' : isRecruiter ? 'SM' : 'AJ';

  const handleLogout = () => {
    alert('Logging out...');
    router.push('/login');
  };

  const isItemActive = (href: string) => {
    if (href === '/admin') {
      return pathname === '/admin';
    }
    if (href === '/candidate') {
      return pathname === '/candidate';
    }
    if (href === '/recruiter') {
      return pathname === '/recruiter';
    }
    if (href === '/candidate/resume/upload' || href === '/candidate/resume/analysis') {
      return pathname === href;
    }
    if (href === '/candidate/applications') {
      return pathname.startsWith('/candidate/applications');
    }
    return pathname.startsWith(href);
  };

  return (
    <div className="flex h-screen bg-[#F8FAFC] dark:bg-[#090D16] overflow-hidden text-[#0F172A] dark:text-[#F8FAFC]">
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-[40] lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:relative z-[50] h-full bg-white dark:bg-[#1E293B] border-r border-[#E2E8F0] dark:border-slate-800 flex flex-col
          transition-all duration-300 ease-in-out
          ${collapsed ? 'w-16' : 'w-60'}
          ${mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
      >
        {/* Logo */}
        <div className={`flex items-center gap-2.5 p-4 border-b border-[#E2E8F0] dark:border-slate-800 ${collapsed ? 'justify-center' : ''}`}>
          <div className="w-8 h-8 bg-[#2563EB] rounded-lg flex items-center justify-center flex-shrink-0 animate-pulse">
            <Bot size={16} className="text-white" />
          </div>
          {!collapsed && (
            <span className="font-bold text-[#0F172A] dark:text-white text-lg tracking-tight">TalentAI</span>
          )}
        </div>

        {/* Nav items */}
        <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
          {navItems.map(({ id, label, icon: Icon, href }) => {
            const targetHref = (label === 'My Applications' ? '/candidate/applications' : href) || '#';
            const active = isItemActive(targetHref);
            
            return (
              <Link
                key={id}
                href={targetHref}
                className={`
                  flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium
                  transition-all duration-155 group w-full text-left cursor-pointer
                  ${active
                    ? 'bg-[#2563EB] text-white shadow-sm font-bold animate-none'
                    : 'text-[#64748B] dark:text-[#94A3B8] hover:bg-[#F1F5F9] dark:hover:bg-slate-800 hover:text-[#0F172A] dark:hover:text-white'
                  }
                  ${collapsed ? 'justify-center' : ''}
                `}
                title={collapsed ? label : undefined}
              >
                <Icon size={18} className="flex-shrink-0" />
                {!collapsed && <span>{label}</span>}
              </Link>
            );
          })}
        </nav>

        {/* Collapse & Logout footer */}
        <div className="p-3 border-t border-[#E2E8F0] dark:border-slate-800 space-y-2">
          {!collapsed && (
            <div className="flex items-center justify-between px-3 py-1 bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-850 rounded-2xl">
              <span className="text-[10px] font-black text-slate-400 uppercase tracking-wider">Theme</span>
              <ThemeSwitcher />
            </div>
          )}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="hidden lg:flex w-full items-center gap-2 px-3 py-2.5 rounded-lg text-[#64748B] dark:text-[#94A3B8] hover:bg-[#F1F5F9] dark:hover:bg-slate-800 text-sm transition-colors cursor-pointer"
          >
            {collapsed ? <ChevronRight size={16} /> : <><ChevronLeft size={16} /><span>Collapse</span></>}
          </button>
          <button
            onClick={handleLogout}
            className={`flex items-center gap-2 px-3 py-2.5 rounded-lg text-[#EF4444] hover:bg-red-50 dark:hover:bg-red-950/20 text-sm w-full transition-colors cursor-pointer ${collapsed ? 'justify-center' : ''}`}
          >
            <LogOut size={16} />
            {!collapsed && <span>Log Out</span>}
          </button>
        </div>
      </aside>

      {/* Main content body */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Navbar */}
        <header className="h-14 bg-white dark:bg-[#1E293B] border-b border-[#E2E8F0] dark:border-slate-800 flex items-center px-4 gap-4 flex-shrink-0 z-[30]">
          <button
            className="lg:hidden p-1.5 rounded-lg hover:bg-[#F1F5F9] dark:hover:bg-slate-850 text-[#64748B] cursor-pointer"
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <X size={20} /> : <Menu size={20} />}
          </button>

          {/* Dynamic Breadcrumbs */}
          <div className="hidden md:block flex-shrink-0">
            <Breadcrumbs />
          </div>

          {/* Global Search trigger bar */}
          <button
            onClick={() => {
              const trigger = document.getElementById('talentai-search-trigger');
              if (trigger) trigger.click();
            }}
            className="flex-1 max-w-xs sm:max-w-md text-left flex items-center gap-2 px-3 py-1.5 bg-[#F8FAFC] dark:bg-slate-800/60 border border-[#E2E8F0] dark:border-slate-700 rounded-lg text-sm text-[#94A3B8] hover:text-[#64748B] cursor-pointer shadow-xs whitespace-nowrap ml-2"
          >
            <Search size={16} />
            <span className="truncate">Search everywhere (⌘ + K)...</span>
          </button>

          <div className="flex items-center gap-2 ml-auto">
            {/* Notification bell badge */}
            <Link
              href={isRecruiter ? '/admin/notifications' : '/candidate/notifications'}
              className="relative p-2 rounded-lg hover:bg-[#F1F5F9] dark:hover:bg-slate-800 text-[#64748B] dark:text-[#94A3B8] cursor-pointer block"
            >
              <Bell size={18} />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-[#EF4444] rounded-full animate-pulse" />
            </Link>

            {/* Profile Avatar Dropdown */}
            <div className="relative">
              <button
                onClick={() => setProfileOpen(!profileOpen)}
                className="flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-[#F1F5F9] dark:hover:bg-slate-800 transition-colors cursor-pointer"
              >
                <div className="w-7 h-7 rounded-full bg-[#2563EB] flex items-center justify-center text-white text-xs font-semibold animate-pulse">
                  {userInitials}
                </div>
                <div className="hidden sm:block text-left">
                  <p className="text-xs font-semibold text-[#0F172A] dark:text-[#F8FAFC]">{userName}</p>
                  <p className="text-[10px] text-[#64748B] dark:text-[#94A3B8]">{userRole}</p>
                </div>
                <ChevronDown size={14} className="text-[#64748B]" />
              </button>

              {profileOpen && (
                <>
                  <div className="fixed inset-0 z-30" onClick={() => setProfileOpen(false)} />
                  <div className="absolute right-0 top-10 w-48 bg-white dark:bg-[#1E293B] border border-[#E2E8F0] dark:border-slate-850 rounded-xl shadow-lg py-1 z-40 animate-in fade-in slide-in-from-top-2 duration-150">
                    <Link
                      href={isAdmin ? '/admin/settings' : isRecruiter ? '/recruiter/settings' : '/candidate/profile'}
                      onClick={() => setProfileOpen(false)}
                      className="flex items-center gap-2 w-full px-3 py-2 text-sm text-[#0F172A] dark:text-[#F8FAFC] hover:bg-[#F8FAFC] dark:hover:bg-slate-800"
                    >
                      <User size={14} /> Profile
                    </Link>
                    <Link
                      href={isAdmin ? '/admin/settings' : isRecruiter ? '/recruiter/settings' : '/candidate/settings'}
                      onClick={() => setProfileOpen(false)}
                      className="flex items-center gap-2 w-full px-3 py-2 text-sm text-[#0F172A] dark:text-[#F8FAFC] hover:bg-[#F8FAFC] dark:hover:bg-slate-800"
                    >
                      <Settings size={14} /> Settings
                    </Link>
                    <div className="border-t border-[#E2E8F0] dark:border-slate-800 my-1" />
                    <button
                      onClick={handleLogout}
                      className="flex items-center gap-2 w-full px-3 py-2 text-sm text-[#EF4444] hover:bg-red-50 dark:hover:bg-red-950/20 cursor-pointer text-left"
                    >
                      <LogOut size={14} /> Log Out
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        </header>

        {/* Dynamic page main content container */}
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}

