'use client';

import React from 'react';
import { SystemHealthMetrics } from '@/types/systemHealth';
import { ShieldAlert, Cpu, Database, Server, Clock } from 'lucide-react';

interface SystemHealthCardProps {
  health: SystemHealthMetrics;
}

export default function SystemHealthCard({ health }: SystemHealthCardProps) {
  const getStatusColor = (s: string) => {
    if (s === 'Healthy') return 'text-emerald-600 bg-emerald-50 border-emerald-200';
    if (s === 'Degraded') return 'text-amber-600 bg-amber-50 border-amber-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  const formatUptime = (sec: number) => {
    const days = Math.floor(sec / (24 * 3600));
    const hours = Math.floor((sec % (24 * 3600)) / 3600);
    return `${days} days, ${hours} hours`;
  };

  return (
    <div className="space-y-6 text-[#0F172A] text-left">
      {/* Diagnostics grid */}
      <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'API Gateway Status', value: health.apiStatus, sub: 'Response latency: 42ms', color: getStatusColor(health.apiStatus), icon: Server },
          { label: 'Primary DB Status', value: health.dbStatus, sub: 'Database replica synchronized', color: getStatusColor(health.dbStatus), icon: Database },
          { label: 'Uptime Clock', value: formatUptime(health.uptimeSeconds), sub: 'Zero disruptions recorded', color: 'bg-slate-50 border-slate-200', icon: Clock },
          { label: 'Deploy Version', value: health.version, sub: health.environment, color: 'bg-slate-50 border-slate-200', icon: Cpu },
        ].map(({ label, value, sub, color, icon: Icon }) => (
          <div key={label} className="bg-white rounded-2xl border border-[#E2E8F0] p-4 shadow-sm flex flex-col justify-between min-h-[110px]">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-bold text-[#64748B] uppercase tracking-wide">{label}</span>
              <Icon size={15} className="text-slate-400" />
            </div>
            <div className="mt-3">
              <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${color}`}>{value}</span>
              <p className="text-[10px] text-slate-400 font-semibold mt-2">{sub}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Dials sliders indicators split */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
          <h4 className="font-bold text-xs uppercase tracking-wider text-[#64748B] border-b border-[#F1F5F9] pb-2">
            Resource Consumption
          </h4>

          <div className="space-y-3.5 text-xs font-semibold">
            {/* CPU */}
            <div className="space-y-1">
              <div className="flex justify-between">
                <span className="text-slate-700">CPU Usage</span>
                <span className="text-[#0F172A]">{health.cpuUsagePct}%</span>
              </div>
              <div className="h-1.5 bg-slate-50 border border-slate-100 rounded-full overflow-hidden">
                <div className="h-full bg-blue-600 rounded-full" style={{ width: `${health.cpuUsagePct}%` }} />
              </div>
            </div>

            {/* Memory */}
            <div className="space-y-1">
              <div className="flex justify-between">
                <span className="text-slate-700">Memory Usage</span>
                <span className="text-[#0F172A]">{health.memoryUsagePct}%</span>
              </div>
              <div className="h-1.5 bg-slate-50 border border-slate-100 rounded-full overflow-hidden">
                <div className="h-full bg-violet-600 rounded-full" style={{ width: `${health.memoryUsagePct}%` }} />
              </div>
            </div>

            {/* Storage */}
            <div className="space-y-1">
              <div className="flex justify-between">
                <span className="text-slate-700">Storage Capacity</span>
                <span className="text-[#0F172A]">{health.storageUsagePct}%</span>
              </div>
              <div className="h-1.5 bg-slate-50 border border-slate-100 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-600 rounded-full" style={{ width: `${health.storageUsagePct}%` }} />
              </div>
            </div>
          </div>
        </div>

        {/* Error queues logs */}
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
          <h4 className="font-bold text-xs uppercase tracking-wider text-[#64748B] border-b border-[#F1F5F9] pb-2 flex items-center gap-1.5">
            <ShieldAlert size={14} className="text-red-500" />
            Active Warning Logs
          </h4>

          <div className="space-y-3">
            {health.errorLogs.map((log, idx) => (
              <div key={idx} className="p-3 border border-slate-100 bg-[#F8FAFC]/50 rounded-xl space-y-1 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200 uppercase text-[8px]">
                    {log.level}
                  </span>
                  <span className="text-[10px] text-slate-400 font-bold">{log.timestamp}</span>
                </div>
                <p className="text-slate-600 leading-relaxed font-medium">{log.message}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
