import { EmailVerificationResponse } from '@/types/verification';

export const MOCK_EMAIL_VERIFICATION: EmailVerificationResponse = {
  status: 'Pending',
  emailAddress: 'alex@example.com',
  message: 'Verification link was dispatched to your email address.',
};
