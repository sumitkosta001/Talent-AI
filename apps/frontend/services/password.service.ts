import { PasswordRulesCheck, PasswordStrengthLevel } from '@/types/password';

const DEV_MODE = true;

export const passwordService = {
  evaluateStrength(password: string): { level: PasswordStrengthLevel; score: number; rules: PasswordRulesCheck; suggestions: string[] } {
    const rules: PasswordRulesCheck = {
      minLength: password.length >= 8,
      hasUppercase: /[A-Z]/.test(password),
      hasLowercase: /[a-z]/.test(password),
      hasNumber: /[0-9]/.test(password),
      hasSpecial: /[^A-Za-z0-9]/.test(password),
      passwordsMatch: true,
    };

    let score = 0;
    if (rules.minLength) score += 1;
    if (rules.hasUppercase) score += 1;
    if (rules.hasLowercase) score += 1;
    if (rules.hasNumber) score += 1;
    if (rules.hasSpecial) score += 1;

    let level: PasswordStrengthLevel = 'Very Weak';
    if (score === 2) level = 'Weak';
    else if (score === 3) level = 'Medium';
    else if (score === 4) level = 'Strong';
    else if (score === 5) level = 'Very Strong';

    const suggestions: string[] = [];
    if (!rules.minLength) suggestions.push('Use at least 8 characters');
    if (!rules.hasUppercase) suggestions.push('Add uppercase letters');
    if (!rules.hasNumber) suggestions.push('Add numbers');
    if (!rules.hasSpecial) suggestions.push('Add special symbols (!@#$)');

    return { level, score, rules, suggestions };
  },

  async requestReset(email: string): Promise<{ success: boolean; message: string }> {
    if (DEV_MODE) {
      await new Promise((r) => setTimeout(r, 500));
      return { success: true, message: `Password reset instructions sent to ${email}` };
    }
    const res = await fetch('/api/auth/forgot-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    return res.json();
  },

  async resetPassword(token: string, newPass: string): Promise<{ success: boolean; message: string }> {
    if (DEV_MODE) {
      await new Promise((r) => setTimeout(r, 600));
      return { success: true, message: 'Password has been reset successfully. You can now login.' };
    }
    const res = await fetch('/api/auth/reset-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, password: newPass }),
    });
    return res.json();
  },
};
