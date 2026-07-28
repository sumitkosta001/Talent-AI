import React from 'react';
import Link from 'next/link';
import { ExternalLink } from 'lucide-react';
import Logo from '@/components/common/Logo';

export default function Footer() {
  return (
    <footer className="bg-[#0F172A] text-white py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="grid md:grid-cols-4 gap-10 mb-12">
          <div>
            <div className="mb-4">
              <Logo lightText={true} />
            </div>
            <p className="text-sm text-slate-400 leading-relaxed">
              AI-powered recruitment platform for the modern world of work.
            </p>
            <div className="flex gap-3 mt-4">
              {[ExternalLink, ExternalLink, ExternalLink].map((Icon, i) => (
                <a
                  key={i}
                  href="#"
                  className="w-8 h-8 bg-slate-800 rounded-lg flex items-center justify-center hover:bg-slate-700 transition-colors"
                >
                  <Icon size={14} className="text-slate-400" />
                </a>
              ))}
            </div>
          </div>
          {[
            { title: 'Product', links: ['Features', 'Pricing', 'Changelog', 'Roadmap'] },
            { title: 'Company', links: ['About', 'Blog', 'Careers', 'Press'] },
            {
              title: 'Legal',
              links: ['Privacy Policy', 'Terms of Service', 'Cookie Policy', 'GDPR'],
            },
          ].map(({ title, links }) => (
            <div key={title}>
              <h4 className="font-semibold text-sm mb-4">{title}</h4>
              <ul className="space-y-2">
                {links.map((l) => (
                  <li key={l}>
                    <a href="#" className="text-sm text-slate-400 hover:text-white transition-colors">
                      {l}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="border-t border-slate-800 pt-6 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-xs text-slate-500">© 2025 TalentAI Inc. All rights reserved.</p>
          <p className="text-xs text-slate-500">Made with ♥ for better hiring</p>
        </div>
      </div>
    </footer>
  );
}
