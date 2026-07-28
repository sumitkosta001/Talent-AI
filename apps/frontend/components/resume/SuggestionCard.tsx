import React from 'react';

interface Suggestion {
  priority: 'high' | 'medium' | 'low';
  text: string;
}

interface SuggestionCardProps {
  suggestions: Suggestion[];
}

export default function SuggestionCard({ suggestions }: SuggestionCardProps) {
  const getPriorityStyles = (priority: 'high' | 'medium' | 'low') => {
    switch (priority) {
      case 'high':
        return {
          wrapper: 'border-red-200 bg-red-50/50',
          badge: 'bg-red-100 text-red-700',
        };
      case 'medium':
        return {
          wrapper: 'border-amber-200 bg-amber-50/50',
          badge: 'bg-amber-100 text-amber-700',
        };
      case 'low':
        return {
          wrapper: 'border-blue-200 bg-blue-50/50',
          badge: 'bg-blue-100 text-blue-700',
        };
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5">
      <h3 className="font-semibold text-[#0F172A] mb-4">Improvement Suggestions</h3>
      <div className="space-y-3">
        {suggestions.map(({ priority, text }, idx) => {
          const styles = getPriorityStyles(priority);
          return (
            <div
              key={idx}
              className={`flex items-start gap-3 p-3 rounded-xl border ${styles.wrapper}`}
            >
              <span
                className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider flex-shrink-0 mt-0.5 ${styles.badge}`}
              >
                {priority}
              </span>
              <p className="text-xs sm:text-sm text-[#475569] leading-relaxed">{text}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
