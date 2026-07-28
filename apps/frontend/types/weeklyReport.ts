export interface ReportMetric {
  label: string;
  currentValue: number;
  previousValue: number;
  changePercentage: number;
  unit?: string;
  improved: boolean;
}

export interface WeeklyReportData {
  weekStartDate: string;
  weekEndDate: string;
  metrics: ReportMetric[];
  productivityScore: number;
  productivityScoreChange: number;
}
