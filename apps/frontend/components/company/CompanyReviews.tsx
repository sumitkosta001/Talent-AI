'use client';

import React from 'react';
import { CompanyReview } from '@/types/companyReview';
import { CompanyRating } from '@/types/companyRating';
import { Star, MessageSquare } from 'lucide-react';

interface CompanyReviewsProps {
  reviews: CompanyReview[];
  ratings: CompanyRating | null;
}

export default function CompanyReviews({ reviews, ratings }: CompanyReviewsProps) {
  return (
    <div className="space-y-6 text-[#0F172A] text-left">
      {/* Overall breakdown metrics if available */}
      {ratings && (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 sm:p-6 shadow-sm space-y-4">
          <div className="flex flex-col sm:flex-row gap-5 items-center">
            <div className="text-center bg-[#F8FAFC] border border-[#E2E8F0] p-5 rounded-2xl flex-shrink-0 w-32">
              <span className="text-3xl font-black text-[#0F172A]">{ratings.overall}</span>
              <div className="flex items-center justify-center gap-0.5 text-amber-500 mt-1.5">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} size={13} fill={i < Math.round(ratings.overall) ? 'currentColor' : 'none'} />
                ))}
              </div>
              <p className="text-[9px] text-[#64748B] font-bold mt-2 uppercase tracking-wide">Overall Rating</p>
            </div>

            {/* Progress breakdown indicators */}
            <div className="flex-1 grid sm:grid-cols-2 gap-3 text-xs w-full">
              {[
                { label: 'Work-Life Balance', val: ratings.workLifeBalance },
                { label: 'Salary & Perks', val: ratings.salaryBenefits },
                { label: 'Career Growth', val: ratings.careerGrowth },
                { label: 'Management', val: ratings.management },
              ].map(({ label, val }) => (
                <div key={label} className="space-y-1 font-semibold">
                  <div className="flex justify-between text-slate-700">
                    <span>{label}</span>
                    <span className="font-bold text-[#0F172A]">{val} / 5</span>
                  </div>
                  <div className="h-1.5 bg-[#F1F5F9] rounded-full overflow-hidden">
                    <div className="h-full bg-blue-600 rounded-full" style={{ width: `${(val / 5) * 100}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Reviews list */}
      <div className="space-y-4">
        <div className="flex items-center gap-1.5 border-b border-[#F1F5F9] pb-3">
          <MessageSquare size={16} className="text-[#2563EB]" />
          <h3 className="font-bold text-[#0F172A] text-sm">Employee Reviews ({reviews.length})</h3>
        </div>

        {reviews.length === 0 ? (
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-8 text-center text-xs text-slate-500 font-semibold shadow-sm">
            No employee reviews written yet for this company.
          </div>
        ) : (
          reviews.map((rev) => (
            <div key={rev.id} className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-3.5">
              {/* Header */}
              <div className="flex items-start justify-between gap-3 text-xs sm:text-sm">
                <div>
                  <h4 className="font-bold text-[#0F172A] leading-normal">{rev.title}</h4>
                  <p className="text-[10px] text-[#64748B] font-semibold mt-1">
                    {rev.authorName} · {rev.isCurrentEmployee ? 'Current Employee' : 'Former Employee'} · {rev.department}
                  </p>
                </div>
                <div className="flex items-center gap-1 bg-amber-50 text-amber-700 px-2 py-0.5 rounded border border-amber-200 font-black text-[10px]">
                  <Star size={11} fill="currentColor" />
                  {rev.rating}.0
                </div>
              </div>

              {/* Body */}
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed font-semibold">
                {rev.description}
              </p>

              {/* Pros & Cons */}
              <div className="grid sm:grid-cols-2 gap-3 text-xs pt-2 border-t border-[#F8FAFC]">
                <div className="space-y-0.5">
                  <span className="font-bold text-emerald-700 block">Pros</span>
                  <p className="text-slate-500 leading-relaxed font-medium">{rev.pros}</p>
                </div>
                <div className="space-y-0.5">
                  <span className="font-bold text-amber-700 block">Cons</span>
                  <p className="text-slate-500 leading-relaxed font-medium">{rev.cons}</p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
