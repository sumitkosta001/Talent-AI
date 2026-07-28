'use client';

import React, { useState } from 'react';
import { usePortfolio } from '@/hooks/usePortfolio';
import { Award, Plus, Trash2, Link as LinkIcon, FileText } from 'lucide-react';

export default function PortfolioSection() {
  const { portfolio, addPortfolioItem, deletePortfolioItem } = usePortfolio();

  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [type, setType] = useState<'Certificate' | 'Award' | 'Hackathon' | 'Research Paper' | 'Blog' | 'Video'>('Certificate');
  const [url, setUrl] = useState('');

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title) return;
    const res = await addPortfolioItem({
      title,
      description: desc,
      type,
      url,
    });
    if (res) {
      setTitle('');
      setDesc('');
      setUrl('');
    }
  };

  return (
    <div className="space-y-6 text-[#0F172A] text-left">
      {/* Add portfolio form */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4">
        <h3 className="font-bold text-sm sm:text-base">Add Portfolio Item</h3>

        <form onSubmit={handleAdd} className="space-y-3.5 text-xs font-semibold">
          <div className="grid sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Item Title</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. hackathon First Place Winner"
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Category Type</label>
              <select
                value={type}
                onChange={(e) => setType(e.target.value as any)}
                className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
              >
                <option value="Certificate">Certificate</option>
                <option value="Award">Award</option>
                <option value="Hackathon">Hackathon</option>
                <option value="Research Paper">Research Paper</option>
                <option value="Blog">Blog</option>
                <option value="Video">Video</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Resource URL link</label>
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="e.g. https://certificates.dev/..."
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Brief Description</label>
            <input
              type="text"
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              placeholder="Short detail summary..."
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs px-4 py-2.5 rounded-xl transition-all cursor-pointer inline-flex items-center gap-1.5"
          >
            <Plus size={15} /> Add Item
          </button>
        </form>
      </div>

      {/* Portfolio Items list */}
      <div className="grid sm:grid-cols-2 gap-4">
        {portfolio.map((item) => (
          <div key={item.id} className="bg-white border border-[#E2E8F0] rounded-2xl p-4.5 shadow-sm space-y-2 hover:shadow-md transition-all flex justify-between items-start gap-4">
            <div className="space-y-1 text-xs">
              <span className="text-[9px] font-bold text-blue-600 bg-blue-50 border border-blue-200 px-1.5 py-0.5 rounded uppercase tracking-wide">
                {item.type}
              </span>
              <h4 className="font-bold text-sm text-[#0F172A] leading-normal pt-1.5">{item.title}</h4>
              <p className="text-[#64748B] font-semibold">{item.description}</p>
              {item.url && (
                <a href={item.url} className="text-blue-600 hover:underline inline-flex items-center gap-0.5 text-[10px] font-bold pt-1">
                  <LinkIcon size={12} /> View Certificate
                </a>
              )}
            </div>

            <button
              onClick={() => deletePortfolioItem(item.id)}
              className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
              title="Delete portfolio item"
            >
              <Trash2 size={13} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
