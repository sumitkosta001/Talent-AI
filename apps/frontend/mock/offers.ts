import { Offer } from '../types/application';
import { MOCK_APPLICATIONS } from './applications';

export const MOCK_OFFERS: Offer[] = MOCK_APPLICATIONS
  .map(app => app.offer)
  .filter((off): off is Offer => !!off);
