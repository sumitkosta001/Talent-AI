import { EmailVerificationResponse } from '@/types/verification';
import { MOCK_EMAIL_VERIFICATION } from '@/mock/emailVerification';

const DEV_MODE = true;

export const verificationService = {
  async getStatus(email?: string): Promise<EmailVerificationResponse> {
    if (DEV_MODE) {
      await new Promise((r) => setTimeout(r, 300));
      return {
        ...MOCK_EMAIL_VERIFICATION,
        emailAddress: email || MOCK_EMAIL_VERIFICATION.emailAddress,
      };
    }
    const res = await fetch(`/api/auth/verify-email?email=${encodeURIComponent(email || '')}`);
    return res.json();
  },

  async resendVerificationEmail(email: string): Promise<{ success: boolean; message: string }> {
    if (DEV_MODE) {
      await new Promise((r) => setTimeout(r, 500));
      return { success: true, message: `Verification link sent to ${email}` };
    }
    const res = await fetch('/api/auth/send-verification', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    return res.json();
  },
};
