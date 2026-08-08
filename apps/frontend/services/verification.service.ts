import { EmailVerificationResponse } from '@/types/verification';

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export const verificationService = {
  /**
   * Get the verification status for the current email.
   *
   * The backend does not currently expose a dedicated
   * "verification status by email" endpoint, so the frontend
   * uses the email passed from the registration flow and
   * displays Pending until verification is completed.
   */
  async getStatus(email: string): Promise<EmailVerificationResponse> {
    return {
      status: 'Pending',
      emailAddress: email,
      message: `Verification link was dispatched to ${email}`,
    };
  },

  /**
   * Resend verification email.
   */
  async resendVerificationEmail(
    email: string
  ): Promise<{ success: boolean; message: string }> {
    const res = await fetch(
      `${API_URL}/api/v1/auth/resend-verification`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({
          email,
        }),
      }
    );

    const data = await res.json();

    if (!res.ok) {
      throw new Error(
        data?.error?.message ||
          data?.detail ||
          'Failed to resend verification email.'
      );
    }

    return {
      success: true,
      message:
        data?.message ||
        `Verification link sent to ${email}`,
    };
  },

  /**
   * Verify email using the JWT verification token.
   */
  async verifyEmail(
    token: string
  ): Promise<{ success: boolean; message: string; email?: string }> {
    const res = await fetch(
      `${API_URL}/api/v1/auth/verify-email?token=${encodeURIComponent(token)}`,
      {
        method: 'GET',
        headers: {
          Accept: 'application/json',
        },
      }
    );

    const data = await res.json();

    if (!res.ok) {
      throw new Error(
        data?.error?.message ||
          data?.detail ||
          'Email verification failed.'
      );
    }

    return {
      success: true,
      message:
        data?.message ||
        'Email verified successfully.',
      email: data?.email,
    };
  },
};