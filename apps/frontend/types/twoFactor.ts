export type TwoFactorMethod = 'authenticator' | 'sms' | 'email' | 'recovery';

export interface TwoFactorChallenge {
  method: TwoFactorMethod;
  maskedTarget?: string;
}
