import { TwoFactorChallenge } from '@/types/twoFactor';

export const MOCK_2FA_CHALLENGE: TwoFactorChallenge = {
  method: 'authenticator',
};

export const MOCK_SMS_CHALLENGE: TwoFactorChallenge = {
  method: 'sms',
  maskedTarget: '+1 ••• ••• ••99',
};

export const MOCK_EMAIL_CHALLENGE: TwoFactorChallenge = {
  method: 'email',
  maskedTarget: 'al•••@ex•••.com',
};

export const MOCK_RECOVERY_CODES = [
  'ABCD-1234-EFGH',
  'IJKL-5678-MNOP',
  'QRST-9012-UVWX',
  'YZAB-3456-CDEF',
];
