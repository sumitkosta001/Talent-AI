'use client';

import React, { useState } from 'react';
import { ShieldAlert, Trash2, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';

interface DeleteAccountSectionProps {
  onConfirmDelete: () => Promise<boolean>;
}

export default function DeleteAccountSection({ onConfirmDelete }: DeleteAccountSectionProps) {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [confirmInput, setConfirmInput] = useState('');
  const [deleting, setDeleting] = useState(false);

  const handleDelete = async (e: React.FormEvent) => {
    e.preventDefault();
    if (confirmInput !== 'DELETE') {
      alert('Confirmation word mismatch. Please type exactly "DELETE".');
      return;
    }

    setDeleting(true);
    const success = await onConfirmDelete();
    setDeleting(false);

    if (success) {
      alert('Account deleted successfully. We are sorry to see you go!');
      router.push('/login');
    }
  };

  return (
    <div className="space-y-4 text-left">
      <div className="bg-red-50/50 border border-red-200 rounded-2xl p-5 space-y-3.5">
        <div className="flex items-center gap-2 text-red-700">
          <ShieldAlert size={18} />
          <h4 className="font-bold text-sm">Danger Zone</h4>
        </div>
        <p className="text-xs text-[#64748B] leading-relaxed">
          Deleting your profile is permanent. Any parsed resume history, ATS scoring trends, active applications, and interview invitations will be deleted.
        </p>
        <button
          type="button"
          onClick={() => setIsOpen(true)}
          className="inline-flex items-center gap-1.5 bg-red-600 hover:bg-red-700 text-white font-bold text-xs px-4 py-2 rounded-xl transition-colors cursor-pointer"
        >
          <Trash2 size={13} />
          Delete Account
        </button>
      </div>

      <AnimatePresence>
        {isOpen && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.4 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black"
              onClick={() => setIsOpen(false)}
            />

            {/* Modal */}
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="bg-white border border-[#E2E8F0] shadow-2xl p-6 rounded-3xl max-w-sm w-full relative z-[110] space-y-4"
            >
              <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-3 text-red-600">
                <h4 className="font-bold text-sm flex items-center gap-1">
                  <ShieldAlert size={16} />
                  Delete My Account
                </h4>
                <button onClick={() => setIsOpen(false)} className="p-1 hover:bg-slate-50 rounded-lg cursor-pointer">
                  <X size={15} className="text-slate-400" />
                </button>
              </div>

              <p className="text-xs text-[#64748B] leading-relaxed">
                Type <strong className="font-bold text-[#0F172A]">DELETE</strong> in the box below to verify deletion:
              </p>

              <form onSubmit={handleDelete} className="space-y-4">
                <input
                  required
                  type="text"
                  value={confirmInput}
                  onChange={(e) => setConfirmInput(e.target.value)}
                  placeholder="Type DELETE..."
                  className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-red-500 bg-white"
                />

                <div className="flex gap-2 justify-end pt-2">
                  <button
                    type="button"
                    onClick={() => setIsOpen(false)}
                    className="px-3.5 py-2 border border-[#E2E8F0] rounded-xl text-xs font-bold text-[#64748B] hover:bg-[#F8FAFC] cursor-pointer"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={deleting}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl text-xs font-bold disabled:opacity-50 cursor-pointer"
                  >
                    {deleting ? 'Deleting...' : 'Delete Profile'}
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
