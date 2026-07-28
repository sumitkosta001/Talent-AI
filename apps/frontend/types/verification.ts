export type VerificationStatus = 'Pending' | 'Verified' | 'Expired' | 'Failed';

export interface EmailVerificationResponse {
  status: VerificationStatus;
  emailAddress: string;
  message: string;
}
