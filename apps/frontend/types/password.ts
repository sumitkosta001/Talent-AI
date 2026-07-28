export interface PasswordRulesCheck {
  minLength: boolean;
  hasUppercase: boolean;
  hasLowercase: boolean;
  hasNumber: boolean;
  hasSpecial: boolean;
  passwordsMatch: boolean;
}

export type PasswordStrengthLevel = 'Very Weak' | 'Weak' | 'Medium' | 'Strong' | 'Very Strong';
