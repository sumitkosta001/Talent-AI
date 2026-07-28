'use client';

import React from 'react';
import { AlertCircle, ArrowUpRight, HelpCircle } from 'lucide-react';
import Link from 'next/link';

interface RejectedFeedbackProps {
  reason?: string;
  feedback?: string;
  improvement?: string[];
}

export default function RejectedFeedback({
  reason = 'Skills alignment mismatch',
  feedback = 'We evaluated your graph algorithms experience and decided to seek profiles with more hands-on dynamic programming targets.',
  improvement = ['Complete 40+ tree/graph Leetcode challenges.', 'Structure computational complexity arguments.'],
}: RejectedFeedbackProps) {
  return (
    <div className="bg-red-50/50 border border-red-200 rounded-2xl p-5 text-left space-y-4">
      <div className="flex items-center gap-2 text-red-700">
        <AlertCircle size={18} />
        <h4 className="font-bold text-sm">Application Status: Rejected</h4>
      </div>

      <div className="space-y-3 text-xs">
        <div>
          <span className="font-semibold text-slate-700 block mb-0.5">Primary Reason:</span>
          <p className="font-bold text-red-950">{reason}</p>
        </div>

        <div>
          <span className="font-semibold text-slate-700 block mb-0.5">Recruiter Feedback:</span>
          <p className="text-slate-600 leading-relaxed">{feedback}</p>
        </div>

        {improvement.length > 0 && (
          <div className="space-y-1.5">
            <span className="font-semibold text-slate-700 block">Recommended Areas of Improvement:</span>
            <ul className="list-disc pl-5 space-y-1 text-slate-600">
              {improvement.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <div className="pt-2 flex flex-wrap gap-2 border-t border-red-200/50">
        <Link
          href="/candidate/resume/upload"
          className="inline-flex items-center gap-1 text-xs font-bold text-red-700 hover:text-red-950 transition-colors cursor-pointer"
        >
          Optimize Resume & Apply Again
          <ArrowUpRight size={13} />
        </Link>
      </div>
    </div>
  );
}
