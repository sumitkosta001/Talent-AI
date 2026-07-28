import { MockCommand, MOCK_COMMANDS } from '@/mock/commandPalette';
import { mockDelay } from '@/lib/mockDelay';

export class CommandPaletteService {
  static async getCommands(query: string = ''): Promise<MockCommand[]> {
    await mockDelay(50);
    const cleaned = query.trim().toLowerCase();
    if (!cleaned) return MOCK_COMMANDS;

    return MOCK_COMMANDS.filter((cmd) => cmd.title.toLowerCase().includes(cleaned));
  }
}
