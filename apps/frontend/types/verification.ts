export type VerificationStatus = 'Pending' | 'Verified' | 'Expired' | 'Failed' | 'AlreadyVerified';

export interface EmailVerificationResponse {
  status: VerificationStatus;
  emailAddress: string;
  message: string;
}
