'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, ChevronLeft, ChevronRight, Video, FileText, Award, CalendarDays, Clock, MapPin } from 'lucide-react';
import { CalendarEvent } from '@/types/calendar';

interface CalendarWidgetProps {
  events: CalendarEvent[];
}

export default function CalendarWidget({ events }: CalendarWidgetProps) {
  // Current calendar month view state
  const [currentDate, setCurrentDate] = useState(new Date(2026, 6, 27)); // Base inside Jul 2026 to fit mock events
  const [selectedDateStr, setSelectedDateStr] = useState<string | null>('2026-07-28'); // Google technical round day

  const currentYear = currentDate.getFullYear();
  const currentMonth = currentDate.getMonth();

  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const firstDayIndex = new Date(currentYear, currentMonth, 1).getDay();

  const monthNames = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ];

  const handlePrevMonth = () => {
    setCurrentDate(new Date(currentYear, currentMonth - 1, 1));
  };

  const handleNextMonth = () => {
    setCurrentDate(new Date(currentYear, currentMonth + 1, 1));
  };

  const getEventsForDay = (day: number) => {
    const paddedMonth = String(currentMonth + 1).padStart(2, '0');
    const paddedDay = String(day).padStart(2, '0');
    const dateStr = `${currentYear}-${paddedMonth}-${paddedDay}`;
    return events.filter((e) => e.date === dateStr);
  };

  const selectDate = (day: number) => {
    const paddedMonth = String(currentMonth + 1).padStart(2, '0');
    const paddedDay = String(day).padStart(2, '0');
    setSelectedDateStr(`${currentYear}-${paddedMonth}-${paddedDay}`);
  };

  const selectedEvents = events.filter((e) => e.date === selectedDateStr);

  const renderCells = () => {
    const cells = [];

    // Empty cells for prior days of week offsets
    for (let i = 0; i < firstDayIndex; i++) {
      cells.push(<div key={`empty-${i}`} className="h-8" />);
    }

    // Days grid
    for (let day = 1; day <= daysInMonth; day++) {
      const paddedMonth = String(currentMonth + 1).padStart(2, '0');
      const paddedDay = String(day).padStart(2, '0');
      const dateStr = `${currentYear}-${paddedMonth}-${paddedDay}`;
      const isSelected = selectedDateStr === dateStr;
      const dayEvents = getEventsForDay(day);

      cells.push(
        <button
          key={`day-${day}`}
          onClick={() => selectDate(day)}
          className={`relative h-8 w-full rounded-lg text-xs font-semibold flex items-center justify-center transition-all ${
            isSelected
              ? 'bg-blue-600 text-white shadow-md'
              : 'hover:bg-slate-100 text-slate-800'
          }`}
        >
          <span>{day}</span>
          {dayEvents.length > 0 && (
            <div className="absolute bottom-1 flex gap-0.5 justify-center w-full">
              {dayEvents.slice(0, 3).map((e) => {
                let dotColor = 'bg-blue-500';
                if (e.type === 'deadline') dotColor = 'bg-rose-500';
                if (e.type === 'assessment') dotColor = 'bg-amber-500';
                if (e.type === 'event') dotColor = 'bg-purple-500';
                return <span key={e.id} className={`w-1 h-1 rounded-full ${dotColor}`} />;
              })}
            </div>
          )}
        </button>
      );
    }

    return cells;
  };

  const getEventTagClass = (type: CalendarEvent['type']) => {
    switch (type) {
      case 'interview':
        return 'text-blue-600 bg-blue-50 border-blue-100';
      case 'deadline':
        return 'text-rose-600 bg-rose-50 border-rose-100';
      case 'assessment':
        return 'text-amber-600 bg-amber-50 border-amber-100';
      default:
        return 'text-purple-600 bg-purple-50 border-purple-100';
    }
  };

  return (
    <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left flex flex-col h-full">
      <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-3">
        <div className="flex items-center gap-2">
          <Calendar size={18} className="text-[#2563EB]" />
          <h3 className="font-bold text-[#0F172A] text-base sm:text-lg">Schedule Calendar</h3>
        </div>
        <div className="flex items-center gap-1.5">
          <button
            onClick={handlePrevMonth}
            className="p-1 border border-[#E2E8F0] hover:bg-slate-50 rounded-lg transition-colors"
          >
            <ChevronLeft size={16} className="text-[#64748B]" />
          </button>
          <span className="text-xs font-bold text-[#0F172A] min-w-[90px] text-center">
            {monthNames[currentMonth]} {currentYear}
          </span>
          <button
            onClick={handleNextMonth}
            className="p-1 border border-[#E2E8F0] hover:bg-slate-50 rounded-lg transition-colors"
          >
            <ChevronRight size={16} className="text-[#64748B]" />
          </button>
        </div>
      </div>

      {/* Days Names */}
      <div className="grid grid-cols-7 gap-1 text-center font-bold text-[10px] text-[#94A3B8] uppercase">
        <div>Su</div>
        <div>Mo</div>
        <div>Tu</div>
        <div>We</div>
        <div>Th</div>
        <div>Fr</div>
        <div>Sa</div>
      </div>

      {/* Grid Cells */}
      <div className="grid grid-cols-7 gap-1">{renderCells()}</div>

      {/* Selected day events log */}
      <div className="flex-1 mt-3 border-t border-[#F1F5F9] pt-4">
        <h4 className="text-xs font-bold text-[#64748B] uppercase tracking-wider mb-2">
          Agenda: {selectedDateStr ? new Date(selectedDateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'No Selection'}
        </h4>

        <div className="space-y-2 max-h-[160px] overflow-y-auto pr-1">
          <AnimatePresence mode="popLayout">
            {selectedEvents.length === 0 ? (
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-xs text-[#94A3B8] italic"
              >
                No scheduled activities for this day.
              </motion.p>
            ) : (
              selectedEvents.map((e) => (
                <motion.div
                  key={e.id}
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -5 }}
                  className="p-2.5 bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl text-xs space-y-1.5"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-bold text-[#0F172A] truncate">{e.title}</span>
                    <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wide flex-shrink-0 ${getEventTagClass(e.type)}`}>
                      {e.type}
                    </span>
                  </div>
                  {e.time && (
                    <div className="flex items-center gap-1 text-[10px] text-[#64748B]">
                      <Clock size={11} className="text-[#94A3B8]" />
                      <span>{e.time}</span>
                      {e.location && (
                        <>
                          <span className="text-[#CBD5E1]">•</span>
                          <MapPin size={11} className="text-[#94A3B8]" />
                          <span className="truncate">{e.location}</span>
                        </>
                      )}
                    </div>
                  )}
                </motion.div>
              ))
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
