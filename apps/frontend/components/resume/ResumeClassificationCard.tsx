'use client';

import React from 'react';
import { BrainCircuit, RefreshCw, AlertTriangle, Sparkles, Info } from 'lucide-react';
import { ResumeClassification } from '@/types/ml';

interface ResumeClassificationCardProps {
  classification: ResumeClassification | null;
  loading: boolean;
  error: string | null;
  onRetry?: () => void;
}

function getConfidencePct(val?: number): number {
  if (val === undefined || val === null) return 0;
  const pct = val <= 1 ? Math.round(val * 100) : Math.round(val);
  return Math.min(100, Math.max(0, pct));
}

function formatEnumLabel(val?: string | null): string {
  if (!val) return 'N/A';
  return val
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

export const ResumeClassificationCard: React.FC<ResumeClassificationCardProps> = ({
  classification,
  loading,
  error,
  onRetry,
}) => {
  if (loading) {
    return (
      <div className="bg-slate-900 rounded-2xl p-6 text-white shadow-md space-y-4 animate-pulse">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-slate-800 rounded-full" />
            <div className="h-5 w-48 bg-slate-800 rounded" />
          </div>
          <div className="h-5 w-20 bg-slate-800 rounded-full" />
        </div>
        <div className="grid sm:grid-cols-3 gap-4 pt-2">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-white/5 rounded-xl p-4 space-y-3 border border-white/10">
              <div className="h-3 w-24 bg-slate-800 rounded" />
              <div className="h-6 w-36 bg-slate-800 rounded" />
              <div className="h-2 w-full bg-slate-800 rounded-full" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-amber-50/90 border border-amber-200 rounded-2xl p-6 text-slate-800 space-y-3">
        <div className="flex items-center gap-2 text-amber-700 font-bold">
          <AlertTriangle size={20} />
          <h3>Resume Classification Error</h3>
        </div>
        <p className="text-sm text-slate-600">
          {error || 'Unable to load AI classification details for this resume.'}
        </p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="inline-flex items-center gap-2 bg-amber-600 text-white px-4 py-2 rounded-xl text-xs font-semibold hover:bg-amber-700 transition-colors cursor-pointer"
          >
            <RefreshCw size={14} />
            Retry Classification
          </button>
        )}
      </div>
    );
  }

  if (!classification) {
    return (
      <div className="bg-slate-900 rounded-2xl p-6 text-white shadow-md space-y-2 text-center">
        <BrainCircuit className="mx-auto text-indigo-400 opacity-60" size={32} />
        <h3 className="font-bold text-base">Classification Unavailable</h3>
        <p className="text-xs text-slate-400">
          Process your resume to view AI domain, role, and experience level classification.
        </p>
      </div>
    );
  }

  const domainPct = getConfidencePct(classification.domain_confidence);
  const rolePct = getConfidencePct(classification.role_confidence);
  const expPct = getConfidencePct(classification.experience_level_confidence);

  return (
    <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-2xl p-6 text-white shadow-md space-y-5 border border-indigo-900/50">
      {/* Card Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/10 pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-indigo-500/20 rounded-xl border border-indigo-400/30 text-indigo-300">
            <BrainCircuit size={22} />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="font-bold text-lg text-white">AI Domain & Role Classification</h2>
              <span className="bg-indigo-500/20 text-indigo-300 border border-indigo-400/30 text-[10px] font-semibold px-2 py-0.5 rounded-full flex items-center gap-1">
                <Sparkles size={10} />
                DAY 29 ML
              </span>
            </div>
            <p className="text-xs text-indigo-200/80 mt-0.5">
              Explainable classification based on skill patterns and career trajectory
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto">
          {classification.classification_method && (
            <span className="text-[11px] text-indigo-300 bg-white/5 border border-white/10 px-2.5 py-1 rounded-lg font-mono">
              {classification.classification_method}
            </span>
          )}
          <span className="text-xs text-indigo-300 bg-indigo-900/60 border border-indigo-700/50 px-3 py-1 rounded-full font-mono">
            {classification.classifier_version || 'day29-v1'}
          </span>
        </div>
      </div>

      {/* Grid of 3 Main Metrics */}
      <div className="grid sm:grid-cols-3 gap-4">
        {/* Primary Domain Card */}
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/10 space-y-3 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between text-xs text-indigo-200 font-semibold tracking-wider uppercase">
            <span>Primary Domain</span>
            <span className="text-emerald-400 font-bold font-mono">{domainPct}%</span>
          </div>
          <p className="font-bold text-lg text-white truncate" title={formatEnumLabel(classification.domain)}>
            {formatEnumLabel(classification.domain)}
          </p>

          {/* Accessible Confidence Progress Bar */}
          <div className="space-y-1">
            <div
              className="w-full bg-slate-800/80 rounded-full h-2 overflow-hidden border border-white/5"
              role="progressbar"
              aria-label="Domain Confidence"
              aria-valuenow={domainPct}
              aria-valuemin={0}
              aria-valuemax={100}
            >
              <div
                className="bg-gradient-to-r from-indigo-500 to-emerald-400 h-full rounded-full transition-all duration-500"
                style={{ width: `${domainPct}%` }}
              />
            </div>
            <div className="flex justify-between items-center text-[10px] text-indigo-300/70 pt-0.5">
              <span>Confidence Score</span>
              <span>{domainPct}/100</span>
            </div>
          </div>
        </div>

        {/* Predicted Role Card */}
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/10 space-y-3 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between text-xs text-indigo-200 font-semibold tracking-wider uppercase">
            <span>Predicted Role</span>
            <span className="text-emerald-400 font-bold font-mono">{rolePct}%</span>
          </div>
          <p className="font-bold text-lg text-white truncate" title={formatEnumLabel(classification.role)}>
            {formatEnumLabel(classification.role)}
          </p>

          {/* Accessible Confidence Progress Bar */}
          <div className="space-y-1">
            <div
              className="w-full bg-slate-800/80 rounded-full h-2 overflow-hidden border border-white/5"
              role="progressbar"
              aria-label="Role Confidence"
              aria-valuenow={rolePct}
              aria-valuemin={0}
              aria-valuemax={100}
            >
              <div
                className="bg-gradient-to-r from-indigo-500 to-emerald-400 h-full rounded-full transition-all duration-500"
                style={{ width: `${rolePct}%` }}
              />
            </div>
            <div className="flex justify-between items-center text-[10px] text-indigo-300/70 pt-0.5">
              <span>Confidence Score</span>
              <span>{rolePct}/100</span>
            </div>
          </div>
        </div>

        {/* Experience Level Card */}
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/10 space-y-3 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between text-xs text-indigo-200 font-semibold tracking-wider uppercase">
            <span>Experience Level</span>
            <span className="text-emerald-400 font-bold font-mono">{expPct}%</span>
          </div>
          <p className="font-bold text-lg text-white truncate" title={formatEnumLabel(classification.experience_level)}>
            {formatEnumLabel(classification.experience_level)}
          </p>

          {/* Accessible Confidence Progress Bar */}
          <div className="space-y-1">
            <div
              className="w-full bg-slate-800/80 rounded-full h-2 overflow-hidden border border-white/5"
              role="progressbar"
              aria-label="Experience Level Confidence"
              aria-valuenow={expPct}
              aria-valuemin={0}
              aria-valuemax={100}
            >
              <div
                className="bg-gradient-to-r from-indigo-500 to-emerald-400 h-full rounded-full transition-all duration-500"
                style={{ width: `${expPct}%` }}
              />
            </div>
            <div className="flex justify-between items-center text-[10px] text-indigo-300/70 pt-0.5">
              <span>Confidence Score</span>
              <span>{expPct}/100</span>
            </div>
          </div>
        </div>
      </div>

      {/* Optional Evidence Breakdown */}
      {classification.evidence && Object.keys(classification.evidence).length > 0 && (
        <div className="pt-2 border-t border-white/10 space-y-2">
          <div className="flex items-center gap-1.5 text-xs text-indigo-200 font-semibold">
            <Info size={14} className="text-indigo-400" />
            <span>Key Extraction Evidence</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {Object.entries(classification.evidence).map(([key, items]) => (
              <div key={key} className="bg-white/5 rounded-lg px-3 py-1.5 border border-white/10 text-xs">
                <span className="text-indigo-300 font-semibold uppercase text-[10px] mr-2">{formatEnumLabel(key)}:</span>
                <span className="text-slate-200">{Array.isArray(items) ? items.join(', ') : String(items)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
