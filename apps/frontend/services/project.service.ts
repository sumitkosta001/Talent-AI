import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { CandidateProject } from '@/types/project';
import { MOCK_PROJECTS } from '@/mock/projects';

export class CandidateProjectService {
  static getLocalProjects(): CandidateProject[] {
    if (typeof window === 'undefined') return MOCK_PROJECTS;
    const stored = localStorage.getItem('talentai_candidate_projects');
    if (!stored) {
      localStorage.setItem('talentai_candidate_projects', JSON.stringify(MOCK_PROJECTS));
      return MOCK_PROJECTS;
    }
    return JSON.parse(stored);
  }

  static saveLocalProjects(list: CandidateProject[]) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_candidate_projects', JSON.stringify(list));
  }

  static async getProjects(): Promise<CandidateProject[]> {
    if (DEV_MODE) {
      await mockDelay(200);
      return this.getLocalProjects();
    }

    const res = await fetch('/api/profile/projects');
    if (!res.ok) throw new Error('Failed to retrieve projects list');
    return res.json();
  }

  static async addProject(proj: Partial<CandidateProject>): Promise<CandidateProject> {
    if (DEV_MODE) {
      await mockDelay(300);
      const list = this.getLocalProjects();
      const newProj: CandidateProject = {
        id: `proj-${Date.now()}`,
        projectName: proj.projectName || 'New Project',
        description: proj.description || '',
        technologies: proj.technologies || [],
        role: proj.role || 'Developer',
        duration: proj.duration || '',
        githubUrl: proj.githubUrl || '',
        liveUrl: proj.liveUrl || '',
        achievements: proj.achievements || [],
      };
      list.unshift(newProj);
      this.saveLocalProjects(list);
      return newProj;
    }

    const res = await fetch('/api/profile/projects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(proj),
    });
    if (!res.ok) throw new Error('Failed to create project block');
    return res.json();
  }

  static async deleteProject(id: string): Promise<boolean> {
    if (DEV_MODE) {
      await mockDelay(200);
      const list = this.getLocalProjects();
      const filtered = list.filter((p) => p.id !== id);
      this.saveLocalProjects(filtered);
      return true;
    }

    const res = await fetch(`/api/profile/projects/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete project block');
    return true;
  }
}
