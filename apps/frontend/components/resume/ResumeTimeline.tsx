import React from 'react';

interface TimelineItem {
  id: string;
  title: string;
  subtitle: string;
  date: string;
  description?: string;
  extra?: React.ReactNode;
}

interface ResumeTimelineProps {
  items: TimelineItem[];
}

export default function ResumeTimeline({ items }: ResumeTimelineProps) {
  return (
    <div className="relative pl-6 border-l-2 border-[#E2E8F0] space-y-6">
      {items.map((item, index) => (
        <div key={item.id} className="relative group">
          {/* Timeline Dot */}
          <div className="absolute -left-[31px] top-1.5 w-4 h-4 rounded-full border-2 border-white bg-[#2563EB] group-hover:scale-125 transition-transform duration-200" />
          
          <div>
            <div className="flex flex-col sm:flex-row sm:items-baseline justify-between mb-1">
              <h3 className="font-bold text-[#0F172A] text-sm sm:text-base">{item.title}</h3>
              <span className="text-xs text-[#94A3B8] font-medium">{item.date}</span>
            </div>
            <p className="text-xs sm:text-sm text-[#2563EB] font-semibold mb-1">{item.subtitle}</p>
            {item.description && (
              <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed mb-2">{item.description}</p>
            )}
            {item.extra && <div className="mt-2">{item.extra}</div>}
          </div>
        </div>
      ))}
    </div>
  );
}
