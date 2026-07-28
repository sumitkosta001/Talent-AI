import React from 'react';
import { Certificate } from '../../types/resume';
import { Award, Calendar } from 'lucide-react';

interface CertificateCardProps {
  certificate: Certificate;
}

export default function CertificateCard({ certificate }: CertificateCardProps) {
  const { certificate: certName, issuer, issueDate, credentialId } = certificate;

  return (
    <div className="bg-white rounded-xl border border-[#E2E8F0] p-4 flex gap-3.5 items-start hover:shadow-sm transition-all duration-200">
      <div className="w-10 h-10 rounded-lg bg-blue-50 text-[#2563EB] flex items-center justify-center flex-shrink-0">
        <Award size={20} />
      </div>
      <div className="min-w-0 flex-1">
        <h3 className="font-bold text-[#0F172A] text-sm sm:text-base truncate">{certName}</h3>
        <p className="text-xs sm:text-sm text-[#64748B] font-semibold mt-0.5">{issuer}</p>
        <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 mt-2 text-xs text-[#94A3B8]">
          <span className="flex items-center gap-1">
            <Calendar size={12} />
            {issueDate}
          </span>
          {credentialId && (
            <span className="truncate">
              ID: <span className="font-mono text-[#64748B]">{credentialId}</span>
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
