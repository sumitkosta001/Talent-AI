export interface PlatformReport {
  id: string;
  title: string;
  type: 'Daily' | 'Weekly' | 'Monthly';
  generatedDate: string;
  downloadUrl: string;
  fileSize: string;
}
