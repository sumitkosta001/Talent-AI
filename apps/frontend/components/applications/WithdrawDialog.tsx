'use client';

import React, { useState } from 'react';
import { X, AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface WithdrawDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (reason: string) => void;
}

export default function WithdrawDialog({ isOpen, onClose, onConfirm }: WithdrawDialogProps) {
  const [reason, setReason] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!reason.trim()) {
      alert('Please specify a reason for withdrawal');
      return;
    }
    onConfirm(reason);
    setReason('');
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
        {/* Overlay backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.4 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black"
          onClick={onClose}
        />

        {/* Modal body */}
        <motion.div
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.95, opacity: 0 }}
          className="bg-white rounded-3xl border border-[#E2E8F0] shadow-2xl p-6 max-w-md w-full relative z-[110] text-left space-y-4"
        >
          <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-3">
            <h3 className="font-bold text-[#0F172A] text-base flex items-center gap-1.5 text-red-600">
              <AlertCircle size={18} />
              Withdraw Application
            </h3>
            <button onClick={onClose} className="p-1 rounded-lg hover:bg-slate-50 cursor-pointer">
              <X size={16} className="text-slate-400" />
            </button>
          </div>

          <p className="text-xs text-[#64748B] leading-relaxed">
            Are you sure you want to withdraw your application? This action cannot be undone. Please specify your reason for withdrawal:
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <textarea
              required
              rows={3}
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              placeholder="Reason (e.g. accepted another offer, salary mismatch, change of interest)..."
              className="w-full border border-[#E2E8F0] rounded-xl p-3 text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-red-500 bg-white"
            />

            <div className="flex gap-2 justify-end pt-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 border border-[#E2E8F0] rounded-xl text-xs font-bold text-slate-600 hover:bg-[#F8FAFC] cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl text-xs font-bold cursor-pointer"
              >
                Confirm Withdrawal
              </button>
            </div>
          </form>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
