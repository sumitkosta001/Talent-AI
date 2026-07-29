import { TwoFactorChallenge, TwoFactorMethod } from '@/types/twoFactor';
import { MOCK_2FA_CHALLENGE, MOCK_SMS_CHALLENGE, MOCK_EMAIL_CHALLENGE, MOCK_RECOVERY_CODES } from '@/mock/twoFactor';

const DEV_MODE = true;

export const twoFactorService = {
  async getChallenge(method: TwoFactorMethod = 'authenticator'): Promise<TwoFactorChallenge> {
    if (DEV_MODE) {
      if (method === 'sms') return MOCK_SMS_CHALLENGE;
      if (method === 'email') return MOCK_EMAIL_CHALLENGE;
      return MOCK_2FA_CHALLENGE;
    }
    const res = await fetch(`/api/auth/2fa/setup?method=${method}`);
    return res.json();
  },

  async verifyTwoFactor(code: string, method: TwoFactorMethod = 'authenticator', rememberDevice: boolean = false): Promise<{ success: boolean; message: string }> {
    if (DEV_MODE) {
      await new Promise((r) => setTimeout(r, 600));
      if (method === 'recovery') {
        if (MOCK_RECOVERY_CODES.includes(code.toUpperCase())) {
          return { success: true, message: 'Recovery code accepted' };
        }
        return { success: false, message: 'Invalid recovery code' };
      }
      if (code === '123456' || code === '000000') {
        return { success: true, message: 'Two-factor authentication successful' };
      }
      return { success: false, message: 'Invalid two-factor code' };
    }
    const res = await fetch('/api/auth/2fa/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, method, rememberDevice }),
    });
    return res.json();
  },
};
