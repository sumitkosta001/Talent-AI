import React from 'react';
import Link from 'next/link';
import Logo from '@/components/common/Logo';

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 border-b border-[#E2E8F0] bg-white/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center gap-6">
        <Link href="/">
          <Logo />
        </Link>

        <div className="hidden md:flex items-center gap-6 ml-6">
          {['Features', 'How it Works', 'Pricing', 'About'].map((item) => (
            <Link
              key={item}
              href={`#${item.toLowerCase().replace(/\s+/g, '-')}`}
              className="text-sm text-[#64748B] hover:text-[#0F172A] transition-colors"
            >
              {item}
            </Link>
          ))}
        </div>

        <div className="flex items-center gap-3 ml-auto">
          <Link
            href="/login"
            className="text-sm font-medium text-[#0F172A] hover:text-[#2563EB] transition-colors px-3 py-2"
          >
            Login
          </Link>
          <Link
            href="/register"
            className="text-sm font-medium bg-[#2563EB] text-white px-4 py-2 rounded-lg hover:bg-[#1D4ED8] transition-colors"
          >
            Get Started
          </Link>
        </div>
      </div>
    </nav>
  );
}
