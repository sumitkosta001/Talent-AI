import { Application } from '../types/application';
import { MOCK_APPLICATIONS } from './applications';

export const MOCK_APPLICATION_MAP = new Map<string, Application>(
  MOCK_APPLICATIONS.map(app => [app.id, app])
);

export function getMockApplicationById(id: string): Application | undefined {
  return MOCK_APPLICATION_MAP.get(id);
}
