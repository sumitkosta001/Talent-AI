export interface MockCommand {
  id: string;
  title: string;
  category: 'pages' | 'actions' | 'tools' | 'settings';
  shortcut?: string;
  route?: string;
  actionId?: string;
}

export const MOCK_COMMANDS: MockCommand[] = [
  // Navigation
  { id: 'cmd-nav-dash', title: 'Go to Dashboard', category: 'pages', shortcut: '⌥ H', route: '/candidate' },
  { id: 'cmd-nav-jobs', title: 'Browse Job Openings', category: 'pages', shortcut: '⌥ J', route: '/candidate/jobs' },
  { id: 'cmd-nav-apps', title: 'View Job Applications', category: 'pages', shortcut: '⌥ A', route: '/candidate/applications' },
  { id: 'cmd-nav-notif', title: 'Open Alerts & Notifications', category: 'pages', shortcut: '⌥ N', route: '/candidate/notifications' },
  { id: 'cmd-nav-prof', title: 'Edit Candidate Profile', category: 'pages', shortcut: '⌥ P', route: '/candidate/profile' },
  { id: 'cmd-nav-settings', title: 'Adjust System Settings', category: 'pages', shortcut: '⌥ S', route: '/candidate/settings' },
  { id: 'cmd-nav-resume', title: 'Review Uploaded Resumes', category: 'pages', shortcut: '⌥ R', route: '/candidate/resume' },
  
  // AI Tools
  { id: 'cmd-tool-builder', title: 'Launch AI Resume Builder', category: 'tools', shortcut: '⌥ I', route: '/candidate/ai/resume-builder' },
  { id: 'cmd-tool-cover', title: 'Generate AI Cover Letter', category: 'tools', route: '/candidate/ai/cover-letter' },
  { id: 'cmd-tool-interview', title: 'Practice AI Mock Interview', category: 'tools', route: '/candidate/ai/mock-interview' },
  { id: 'cmd-tool-roadmap', title: 'Generate AI Career Roadmap', category: 'tools', route: '/candidate/ai/roadmap' },

  // Actions
  { id: 'cmd-act-theme-light', title: 'Switch to Light Theme', category: 'settings', actionId: 'set-theme-light' },
  { id: 'cmd-act-theme-dark', title: 'Switch to Dark Theme', category: 'settings', actionId: 'set-theme-dark' },
  { id: 'cmd-act-theme-system', title: 'Sync with System Theme', category: 'settings', actionId: 'set-theme-system' },
  { id: 'cmd-act-shortcuts', title: 'Show Keyboard Shortcuts List', category: 'actions', shortcut: 'Ctrl + /', actionId: 'show-shortcuts' },
  { id: 'cmd-act-logout', title: 'Log Out of Platform', category: 'actions', actionId: 'logout' },
];
