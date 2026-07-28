'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronRight, Home } from 'lucide-react';

export default function Breadcrumbs() {
  const pathname = usePathname();
  
  if (pathname === '/' || pathname === '/login' || pathname === '/register') {
    return null;
  }

  const segments = pathname.split('/').filter(Boolean);

  const getLabel = (segment: string) => {
    if (segment === 'candidate') return 'Dashboard';
    if (segment === 'recruiter') return 'Recruiter Portal';
    if (segment === 'admin') return 'Admin Portal';
    if (segment === 'ai') return 'AI Tools';
    
    return segment
      .split('-')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <nav className="flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400 font-semibold py-2 overflow-x-auto whitespace-nowrap">
      <Link href="/" className="hover:text-slate-800 dark:hover:text-slate-200 flex items-center transition-colors">
        <Home size={12} className="mr-1" />
        Home
      </Link>
      {segments.map((seg, idx) => {
        const href = '/' + segments.slice(0, idx + 1).join('/');
        const isLast = idx === segments.length - 1;
        const label = getLabel(seg);

        return (
          <React.Fragment key={href}>
            <ChevronRight size={12} className="text-slate-400 dark:text-slate-650 flex-shrink-0" />
            {isLast ? (
              <span className="text-slate-800 dark:text-slate-100 font-extrabold truncate max-w-[200px]">
                {label}
              </span>
            ) : (
              <Link href={href} className="hover:text-slate-800 dark:hover:text-slate-200 transition-colors truncate max-w-[150px]">
                {label}
              </Link>
            )}
          </React.Fragment>
        );
      })}
    </nav>
  );
}
