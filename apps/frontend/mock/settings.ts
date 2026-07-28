import { CandidateSettings } from '../types/settings';
import { MOCK_PROFILE } from './profile';
import { MOCK_SOCIALS } from './socialLinks';
import { MOCK_RESUME_VISIBILITY } from './resumeVisibility';
import { MOCK_PRIVACY } from './privacySettings';
import { MOCK_NOTIFICATIONS_SETTINGS } from './notificationSettings';

export const MOCK_SETTINGS: CandidateSettings = {
  profile: MOCK_PROFILE,
  socials: MOCK_SOCIALS,
  resume: MOCK_RESUME_VISIBILITY,
  privacy: MOCK_PRIVACY,
  notifications: MOCK_NOTIFICATIONS_SETTINGS,
  theme: 'Light',
  language: 'en',
};
