'use client';

import React from 'react';
import Link from 'next/link';
import { MapPin, DollarSign, Clock, Users, ArrowRight, Eye, Trash2, RotateCcw } from 'lucide-react';
import { Application } from '@/types/application';

interface ApplicationCardProps {
  application: Application;
  onArchive?: (id: string) => void;
  onRestore?: (id: string) => void;
}

export default function ApplicationCard({
  application,
  onArchive,
  onRestore,
}: ApplicationCardProps) {
  const { id, company, jobTitle, location, salary, appliedDate, status, matchPercentage, logo, logoColor } = application;

  const getStatusStyle = (s: string) => {
    switch (s) {
      case 'Offer Received':
      case 'Offer Accepted':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'Technical Interview':
      case 'HR Interview':
      case 'Final Interview':
        return 'bg-violet-50 text-violet-700 border-violet-200';
      case 'Rejected':
        return 'bg-red-50 text-red-700 border-red-200';
      case 'Withdrawn':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'Archived':
        return 'bg-slate-100 text-slate-700 border-slate-300';
      default:
        return 'bg-blue-50 text-blue-700 border-blue-200';
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 hover:shadow-md hover:border-[#CBD5E1] transition-all relative text-left">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        {/* Company & Role details */}
        <div className="flex gap-4">
          <div className={`w-12 h-12 rounded-xl ${logoColor} flex items-center justify-center text-white font-bold text-lg flex-shrink-0`}>
            {logo}
          </div>
          <div>
            <Link href={`/candidate/applications/${id}`}>
              <h3 className="font-bold text-[#0F172A] text-sm sm:text-base hover:text-blue-600 transition-colors line-clamp-1">
                {jobTitle}
              </h3>
            </Link>
            <p className="text-xs text-[#64748B] mt-0.5">{company} · {location}</p>
            <div className="flex flex-wrap items-center gap-3 mt-2 text-[10px] sm:text-xs text-[#64748B] font-semibold">
              <span className="flex items-center gap-0.5"><DollarSign size={12} /> {salary}</span>
              <span>·</span>
              <span className="flex items-center gap-0.5"><Clock size={12} /> Applied {appliedDate}</span>
            </div>
          </div>
        </div>

        {/* Status flags & Actions */}
        <div className="flex sm:flex-col items-start sm:items-end justify-between sm:justify-center gap-3 flex-shrink-0 border-t sm:border-t-0 border-[#F1F5F9] pt-3 sm:pt-0">
          <div className="flex items-center gap-2">
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${getStatusStyle(status)}`}>
              {status}
            </span>
            <span className="text-[10px] font-bold bg-green-50 text-green-700 border border-green-200 px-2 py-0.5 rounded-full uppercase tracking-wider">
              {matchPercentage}% AI Match
            </span>
          </div>

          <div className="flex items-center gap-2">
            <Link
              href={`/candidate/applications/${id}`}
              className="inline-flex items-center gap-1 bg-[#2563EB] text-white px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-[#1D4ED8] transition-colors cursor-pointer"
            >
              <Eye size={12} />
              Track Status
            </Link>
            
            {/* Archive / Restore actions */}
            {application.archived ? (
              onRestore && (
                <button
                  onClick={() => onRestore(id)}
                  className="p-1.5 text-slate-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg cursor-pointer transition-colors"
                  title="Restore application"
                >
                  <RotateCcw size={14} />
                </button>
              )
            ) : (
              onArchive && (
                <button
                  onClick={() => onArchive(id)}
                  className="p-1.5 text-slate-500 hover:text-red-600 hover:bg-red-50 rounded-lg cursor-pointer transition-colors"
                  title="Archive application"
                >
                  <Trash2 size={14} />
                </button>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
