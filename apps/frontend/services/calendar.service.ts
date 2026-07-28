import { MOCK_CALENDAR_EVENTS } from '@/mock/calendar';
import { mockDelay } from '@/lib/mockDelay';

export class CalendarService {
  static async getEvents() {
    await mockDelay(100);
    return MOCK_CALENDAR_EVENTS;
  }
}
