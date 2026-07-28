import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { ATSResult } from '@/types/ats';
import { MOCK_ATS_SCORE } from '@/mock/ats';
import {
  MOCK_SECTION_ANALYSIS,
  MOCK_FORMATTING_ANALYSIS,
  MOCK_GRAMMAR_ANALYSIS,
  MOCK_SKILL_ANALYSIS,
  MOCK_EDUCATION_ANALYSIS,
  MOCK_EXPERIENCE_ANALYSIS,
  MOCK_PROJECT_ANALYSIS
} from '@/mock/atsAnalysis';
import { MOCK_KEYWORDS } from '@/mock/atsKeywords';
import { MOCK_SUGGESTIONS } from '@/mock/atsSuggestions';
import { MOCK_TIMELINE } from '@/mock/atsTimeline';

export class ATSService {
  static async getATSAnalysis(): Promise<ATSResult> {
    if (DEV_MODE) {
      await mockDelay(600);
      return {
        score: MOCK_ATS_SCORE,
        keywords: MOCK_KEYWORDS,
        sections: MOCK_SECTION_ANALYSIS,
        suggestions: MOCK_SUGGESTIONS,
        timeline: MOCK_TIMELINE,
        formatting: MOCK_FORMATTING_ANALYSIS,
        grammar: MOCK_GRAMMAR_ANALYSIS,
        skills: MOCK_SKILL_ANALYSIS,
        education: MOCK_EDUCATION_ANALYSIS,
        experience: MOCK_EXPERIENCE_ANALYSIS,
        projects: MOCK_PROJECT_ANALYSIS,
      };
    }

    // Call FastAPI backend in the future
    const res = await fetch('/api/ats/analyze');
    if (!res.ok) {
      throw new Error('Failed to fetch ATS analysis');
    }
    return res.json();
  }
}
