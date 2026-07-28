'use client';

import React, { use, useState, useEffect } from 'react';
import { ApplicationService } from '@/services/application.service';
import { Application } from '@/types/application';
import ApplicationDetailsComponent from '@/components/applications/ApplicationDetails';
import WithdrawDialog from '@/components/applications/WithdrawDialog';
import { Loader2, AlertCircle } from 'lucide-react';
import Link from 'next/link';

interface ApplicationDetailPageProps {
  params: Promise<{ id: string }>;
}

export default function ApplicationDetailPage({ params }: ApplicationDetailPageProps) {
  const { id } = use(params);

  const [application, setApplication] = useState<Application | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isWithdrawOpen, setIsWithdrawOpen] = useState(false);

  async function loadData() {
    setLoading(true);
    setError(null);
    try {
      const match = await ApplicationService.getApplicationById(id);
      if (match) {
        setApplication(match);
      } else {
        setError('Application details not found');
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to retrieve application details');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, [id]);

  const handleWithdrawConfirm = async (reason: string) => {
    if (!application) return;
    setLoading(true);
    try {
      const updated = await ApplicationService.withdrawApplication(application.id, reason);
      setApplication(updated);
      setIsWithdrawOpen(false);
      alert('Application successfully withdrawn');
    } catch (err: any) {
      alert(`Withdrawal failed: ${err?.message || 'Please try again.'}`);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !application) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Retrieving application stages details...</p>
      </div>
    );
  }

  if (error || !application) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <div className="text-red-500 font-bold text-lg">Error Loading Details</div>
        <p className="text-sm text-[#64748B]">{error || 'Application not found'}</p>
        <Link
          href="/candidate/applications"
          className="bg-blue-600 text-white px-4 py-2 rounded-xl text-sm font-semibold cursor-pointer inline-block"
        >
          Return to Applications List
        </Link>
      </div>
    );
  }

  const showWithdraw = application.status !== 'Withdrawn' && application.status !== 'Rejected' && application.status !== 'Offer Accepted';

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto text-[#0F172A]">
      {/* Top Withdraw option banner */}
      {showWithdraw && (
        <div className="bg-amber-50 border border-amber-200 p-4 rounded-2xl flex items-center justify-between gap-4 text-left">
          <div className="flex items-center gap-2 text-amber-800 text-xs sm:text-sm">
            <AlertCircle size={18} className="flex-shrink-0" />
            <p>Would you like to withdraw your application? This will cancel any interviews scheduled.</p>
          </div>
          <button
            onClick={() => setIsWithdrawOpen(true)}
            className="bg-red-600 hover:bg-red-700 text-white font-bold text-xs px-3.5 py-2 rounded-xl cursor-pointer transition-colors"
          >
            Withdraw Application
          </button>
        </div>
      )}

      {/* Main Details compositor */}
      <ApplicationDetailsComponent
        application={application}
        onBack={() => window.history.back()}
      />

      {/* Withdraw Modal popup */}
      <WithdrawDialog
        isOpen={isWithdrawOpen}
        onClose={() => setIsWithdrawOpen(false)}
        onConfirm={handleWithdrawConfirm}
      />
    </div>
  );
}
