import { OTPVerifyResponse } from '@/types/otp';
import { MOCK_OTP_CODE } from '@/mock/otp';

const DEV_MODE = true;

export const otpService = {
  async verifyOTP(code: string): Promise<OTPVerifyResponse> {
    if (DEV_MODE) {
      await new Promise((r) => setTimeout(r, 600));
      if (code === MOCK_OTP_CODE || code === '000000') {
        return { success: true, message: 'OTP Verified successfully', sessionToken: 'otp-verified-token-123' };
      }
      return { success: false, message: 'Incorrect OTP code. Please try again.', errorType: 'invalid' };
    }
    const res = await fetch('/api/auth/verify-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code }),
    });
    return res.json();
  },

  async resendOTP(targetEmailOrPhone?: string): Promise<{ success: boolean; message: string }> {
    if (DEV_MODE) {
      await new Promise((r) => setTimeout(r, 400));
      return { success: true, message: `New 6-digit OTP dispatched to ${targetEmailOrPhone || 'your registered contact'}` };
    }
    const res = await fetch('/api/auth/send-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target: targetEmailOrPhone }),
    });
    return res.json();
  },
};
