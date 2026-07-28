export interface CalendarEvent {
  id: string;
  title: string;
  type: 'interview' | 'assessment' | 'deadline' | 'event';
  date: string; // YYYY-MM-DD
  time?: string;
  description?: string;
  company?: string;
  location?: string;
}
