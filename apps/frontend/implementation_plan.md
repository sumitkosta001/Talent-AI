# Implementation Plan - AI Career Tools Module

Implement the flagship AI Career Tools module inside the Candidate dashboard.

## Proposed Changes

### Types Definition

Create custom type definitions for all sub-tools under `/types/`:

#### [NEW] [ai.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/types/ai.ts)
- Main dashboard state types.

#### [NEW] [coverLetter.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/types/coverLetter.ts)
- Inputs, options, and historic cover letter items.

#### [NEW] [interview.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/types/interview.ts)
- Mock interview configurations, transcripts, questions, and scores.

#### [NEW] [salary.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/types/salary.ts)
- Salary prediction parameters and chart points.

#### [NEW] [careerRoadmap.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/types/careerRoadmap.ts)
- Path items and milestone structures.

#### [NEW] [skillGap.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/types/skillGap.ts)
- Matches metrics and radar point definitions.

#### [NEW] [learning.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/types/learning.ts)
- Course details, books, and articles bookmarks tracking.

#### [NEW] [careerScore.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/types/careerScore.ts)
- Metrics breakdowns.

---

### Mock Data Files

Create comprehensive datasets under `mock/`:

#### [NEW] [careerDashboard.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/mock/careerDashboard.ts)
#### [NEW] [resumeBuilder.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/mock/resumeBuilder.ts)
#### [NEW] [coverLetters.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/mock/coverLetters.ts)
#### [NEW] [interviewQuestions.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/mock/interviewQuestions.ts)
#### [NEW] [mockInterview.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/mock/mockInterview.ts)
#### [NEW] [salaryPrediction.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/mock/salaryPrediction.ts)
#### [NEW] [careerRoadmap.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/mock/careerRoadmap.ts)
#### [NEW] [skillGap.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/mock/skillGap.ts)
#### [NEW] [learning.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/mock/learning.ts)
#### [NEW] [careerScore.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/mock/careerScore.ts)
#### [NEW] [aiHistory.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/mock/aiHistory.ts)
#### [NEW] [aiInsights.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/mock/aiInsights.ts)

---

### Services

Implement mock API integrations under `services/` (preconfigured for FastAPI endpoints):

#### [NEW] [ai.service.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/services/ai.service.ts)
#### [NEW] [resumeBuilder.service.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/services/resumeBuilder.service.ts)
#### [NEW] [coverLetter.service.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/services/coverLetter.service.ts)
#### [NEW] [interview.service.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/services/interview.service.ts)
#### [NEW] [mockInterview.service.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/services/mockInterview.service.ts)
#### [NEW] [salary.service.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/services/salary.service.ts)
#### [NEW] [roadmap.service.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/services/roadmap.service.ts)
#### [NEW] [skillGap.service.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/services/skillGap.service.ts)
#### [NEW] [learning.service.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/services/learning.service.ts)
#### [NEW] [careerScore.service.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/services/careerScore.service.ts)

---

### React Hooks

Implement hooks under `hooks/` to bind services to page views:

#### [NEW] [useAI.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/hooks/useAI.ts)
#### [NEW] [useResumeBuilder.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/hooks/useResumeBuilder.ts)
#### [NEW] [useCoverLetter.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/hooks/useCoverLetter.ts)
#### [NEW] [useInterview.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/hooks/useInterview.ts)
#### [NEW] [useMockInterview.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/hooks/useMockInterview.ts)
#### [NEW] [useSalaryPrediction.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/hooks/useSalaryPrediction.ts)
#### [NEW] [useCareerRoadmap.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/hooks/useCareerRoadmap.ts)
#### [NEW] [useSkillGap.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/hooks/useSkillGap.ts)
#### [NEW] [useLearning.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/hooks/useLearning.ts)
#### [NEW] [useCareerScore.ts](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/hooks/useCareerScore.ts)

---

### Reusable Components

Create specific presentation and input elements under `components/ai/`:

#### [NEW] [AIToolCard.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/components/ai/AIToolCard.tsx)
- Reusable tool link widget card.

#### [NEW] [AIInsightCard.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/components/ai/AIInsightCard.tsx)
- Coaching cards presenting custom text.

#### [NEW] [SalaryChart.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/components/ai/SalaryChart.tsx)
- Recharts salary growth rendering.

#### [NEW] [SkillGapChart.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/components/ai/SkillGapChart.tsx)
- Recharts radar or bar display for skill matching percentages.

---

### Dashboard & Tool Routes

Create layout routing views under `app/(dashboard)/candidate/ai/`:

#### [NEW] [page.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/app/%28dashboard%29/candidate/ai/page.tsx)
- Aggregated AI dashboard view.

#### [NEW] [resume-builder/page.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/app/%28dashboard%29/candidate/ai/resume-builder/page.tsx)
- Fully functional custom section builder with template options and export simulations.

#### [NEW] [cover-letter/page.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/app/%28dashboard%29/candidate/ai/cover-letter/page.tsx)
- Generates letters using customized parameters.

#### [NEW] [interview/page.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/app/%28dashboard%29/candidate/ai/interview/page.tsx)
- Tailored question items based on difficulty and focus areas.

#### [NEW] [mock-interview/page.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/app/%28dashboard%29/candidate/ai/mock-interview/page.tsx)
- Audio/video status simulation feeds with timer checks and technical reviews.

#### [NEW] [salary/page.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/app/%28dashboard%29/candidate/ai/salary/page.tsx)
- Predictor outputs and salary progression curves.

#### [NEW] [roadmap/page.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/app/%28dashboard%29/candidate/ai/roadmap/page.tsx)
- Goal milestones progress tracks.

#### [NEW] [skill-gap/page.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/app/%28dashboard%29/candidate/ai/skill-gap/page.tsx)
- Radar gap diagrams comparing current skills.

#### [NEW] [learning/page.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/app/%28dashboard%29/candidate/ai/learning/page.tsx)
- Structured courses cards path details.

#### [NEW] [career-score/page.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/app/%28dashboard%29/candidate/ai/career-score/page.tsx)
- Detailed score breakdown.

---

### Navigation Layout Update

#### [MODIFY] [DashboardLayout.tsx](file:///c:/Users/sumit/OneDrive%20-%20National%20Institute%20of%20Technology,%20Rourkela/Desktop/TalentAI/apps/frontend/components/layouts/DashboardLayout.tsx)
- Integrate "AI Career Mentor" option to sidebar list.

## Verification Plan

### Automated Tests
- Run `npm run build` to confirm compilation.

### Manual Verification
- Access `/candidate/ai` on localhost web browser.
- Walk through each sub-tool flow generating letters, answering interview questions, checking salary curves, and roadmap targets.
