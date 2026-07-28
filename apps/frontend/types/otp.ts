export interface OTPVerifyResponse {
  success: boolean;
  message: string;
  sessionToken?: string;
  errorType?: 'expired' | 'invalid' | 'attempts_exceeded';
}
