'use client';

import React, { useState } from 'react';
import { Award, Check, X, Download } from 'lucide-react';
import { Offer } from '@/types/application';

interface OfferLetterProps {
  offer?: Offer;
  onAccept?: () => void;
  onDecline?: () => void;
}

export default function OfferLetter({ offer, onAccept, onDecline }: OfferLetterProps) {
  const [status, setStatus] = useState<'Pending' | 'Accepted' | 'Declined'>(offer?.status || 'Pending');

  if (!offer) {
    return (
      <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-6 rounded-2xl text-center text-xs text-[#64748B] font-semibold">
        No active job offers are currently listed.
      </div>
    );
  }

  const handleAccept = () => {
    setStatus('Accepted');
    if (onAccept) onAccept();
    alert('Offer Accepted! Congratulations on your new journey!');
  };

  const handleDecline = () => {
    setStatus('Declined');
    if (onDecline) onDecline();
    alert('Offer declined.');
  };

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left relative overflow-hidden">
      {status === 'Accepted' && (
        <div className="absolute top-0 right-0 bg-green-500 text-white font-bold text-[9px] px-3 py-1 uppercase tracking-wider rounded-bl-xl">
          Accepted
        </div>
      )}
      {status === 'Declined' && (
        <div className="absolute top-0 right-0 bg-red-500 text-white font-bold text-[9px] px-3 py-1 uppercase tracking-wider rounded-bl-xl">
          Declined
        </div>
      )}

      <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-3">
        <h4 className="font-bold text-sm text-[#0F172A] flex items-center gap-1.5">
          <Award size={18} className="text-[#22C55E]" />
          Job Offer Details
        </h4>
        <span className="text-[10px] text-[#64748B] font-semibold">
          Deadline: {offer.deadline}
        </span>
      </div>

      <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-3 text-xs leading-relaxed">
        <div className="grid grid-cols-2 gap-3.5">
          <div>
            <p className="text-[#64748B] font-semibold">Compensation</p>
            <p className="font-bold text-[#0F172A] text-sm mt-0.5">{offer.salary}</p>
          </div>
          <div>
            <p className="text-[#64748B] font-semibold">Joining Date</p>
            <p className="font-bold text-[#0F172A] text-sm mt-0.5">{offer.joiningDate}</p>
          </div>
          <div>
            <p className="text-[#64748B] font-semibold">Location</p>
            <p className="font-bold text-[#0F172A] text-sm mt-0.5">{offer.location}</p>
          </div>
          <div>
            <p className="text-[#64748B] font-semibold">Employment Type</p>
            <p className="font-bold text-[#0F172A] text-sm mt-0.5">{offer.employmentType}</p>
          </div>
        </div>
      </div>

      {status === 'Pending' ? (
        <div className="flex gap-2 justify-end pt-2">
          <button
            onClick={() => alert('Downloading offer letter PDF...')}
            className="px-3.5 py-2 border border-[#E2E8F0] rounded-xl text-xs font-bold text-[#64748B] hover:bg-[#F8FAFC] flex items-center gap-1 cursor-pointer"
          >
            <Download size={13} />
            PDF
          </button>
          <button
            onClick={handleDecline}
            className="px-4 py-2 border border-red-200 text-red-600 rounded-xl text-xs font-bold hover:bg-red-50 flex items-center gap-1 cursor-pointer"
          >
            <X size={13} />
            Decline
          </button>
          <button
            onClick={handleAccept}
            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-xl text-xs font-bold flex items-center gap-1 cursor-pointer"
          >
            <Check size={13} />
            Accept Offer
          </button>
        </div>
      ) : (
        <div className="flex gap-2 justify-end pt-2">
          <button
            onClick={() => alert('Downloading signed offer copy...')}
            className="px-4 py-2 border border-[#E2E8F0] rounded-xl text-xs font-bold text-[#64748B] hover:bg-[#F8FAFC] flex items-center gap-1.5 cursor-pointer"
          >
            <Download size={13} />
            Download Signed Copy
          </button>
        </div>
      )}
    </div>
  );
}
