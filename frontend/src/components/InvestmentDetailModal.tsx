import React from 'react';
import { 
  X, 
  CheckCircle2, 
  AlertTriangle, 
  FileText, 
  ShieldCheck, 
  Gauge, 
  TrendingUp, 
  Clock, 
  Wallet,
  Sparkles
} from 'lucide-react';
import { InvestmentScheme } from '../types';

interface DetailModalProps {
  scheme: InvestmentScheme | null;
  onClose: () => void;
}

export const InvestmentDetailModal: React.FC<DetailModalProps> = ({ scheme, onClose }) => {
  if (!scheme) return null;

  const score = scheme.suitability_score || 88;
  const breakdown = scheme.score_breakdown || {
    risk_compatibility: 90,
    goal_compatibility: 88,
    time_horizon: 95,
    liquidity: 80,
    tax_efficiency: 85,
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-[#DCE5EC] my-8 animate-scaleUp">
        {/* Header */}
        <div className="flex items-start justify-between pb-4 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs bg-[#DDF7F0] text-[#092B49] font-bold px-2.5 py-0.5 rounded-full">
                {scheme.category}
              </span>
              {scheme.badge && (
                <span className="text-xs bg-amber-50 text-amber-700 font-bold px-2.5 py-0.5 rounded-full border border-amber-200">
                  {scheme.badge}
                </span>
              )}
            </div>
            <h2 className="text-2xl font-bold text-[#102A43] mt-1.5">{scheme.name}</h2>
            <p className="text-xs text-[#64748B]">{scheme.provider}</p>
          </div>

          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Suitability Score Banner */}
        <div className="my-5 p-4 rounded-xl bg-gradient-to-r from-[#EEF6FF] to-[#DDF7F0]/40 border border-[#28B89A]/30 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-[#28B89A] text-white flex items-center justify-center font-black text-xl shadow-xs">
              {score}%
            </div>
            <div>
              <p className="text-xs font-semibold text-[#092B49] uppercase">Profile Match Score</p>
              <p className="text-sm font-bold text-[#102A43]">
                {scheme.suitability_tier || (score >= 80 ? 'Highly Suitable for your profile' : 'Moderately Suitable')}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4 text-xs">
            <div>
              <span className="text-[#64748B] block text-[10px]">Indicative Return</span>
              <span className="font-bold text-[#28B89A]">{scheme.indicative_return}</span>
            </div>
            <div className="h-6 w-px bg-slate-200" />
            <div>
              <span className="text-[#64748B] block text-[10px]">Risk Rating</span>
              <span className="font-bold text-[#092B49]">{scheme.risk_level}</span>
            </div>
            <div className="h-6 w-px bg-slate-200" />
            <div>
              <span className="text-[#64748B] block text-[10px]">Min Investment</span>
              <span className="font-bold text-[#092B49]">{scheme.min_investment}</span>
            </div>
          </div>
        </div>

        {/* Explainability Scoring Breakdown */}
        <div className="space-y-4 mb-6">
          <h4 className="text-xs font-bold uppercase tracking-wider text-[#64748B]">
            Transparent Compatibility Breakdown
          </h4>

          <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-center text-xs">
            <div className="bg-[#F8FBFC] p-2.5 rounded-lg border border-slate-100">
              <span className="text-[10px] text-slate-500 block">Risk Match</span>
              <span className="font-bold text-[#092B49]">{breakdown.risk_compatibility}%</span>
            </div>
            <div className="bg-[#F8FBFC] p-2.5 rounded-lg border border-slate-100">
              <span className="text-[10px] text-slate-500 block">Goal Fit</span>
              <span className="font-bold text-[#092B49]">{breakdown.goal_compatibility}%</span>
            </div>
            <div className="bg-[#F8FBFC] p-2.5 rounded-lg border border-slate-100">
              <span className="text-[10px] text-slate-500 block">Time Horizon</span>
              <span className="font-bold text-[#092B49]">{breakdown.time_horizon}%</span>
            </div>
            <div className="bg-[#F8FBFC] p-2.5 rounded-lg border border-slate-100">
              <span className="text-[10px] text-slate-500 block">Liquidity</span>
              <span className="font-bold text-[#092B49]">{breakdown.liquidity}%</span>
            </div>
            <div className="bg-[#F8FBFC] p-2.5 rounded-lg border border-slate-100">
              <span className="text-[10px] text-slate-500 block">Tax Advantage</span>
              <span className="font-bold text-[#092B49]">{breakdown.tax_efficiency}%</span>
            </div>
          </div>
        </div>

        {/* Why this recommendation? */}
        <div className="space-y-4 mb-6">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-[#28B89A]" />
            <h4 className="text-sm font-bold text-[#102A43]">Why We Recommended This</h4>
          </div>
          <div className="space-y-2 bg-[#F8FBFC] p-4 rounded-xl border border-slate-100 text-xs text-[#102A43]">
            {(scheme.why_recommended || [
              `Matches your ${scheme.risk_level.toLowerCase()} risk tolerance profile.`,
              `Ideal for ${scheme.time_horizon_ideal} compounding.`,
              `Supports your wealth creation objective.`,
              `Minimum SIP of ${scheme.min_investment} fits within your surplus.`
            ]).map((point, idx) => (
              <div key={idx} className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-[#28B89A] shrink-0 mt-0.5" />
                <span>{point}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Things to Consider */}
        <div className="space-y-4 mb-6">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-500" />
            <h4 className="text-sm font-bold text-[#102A43]">Things to Consider Before Investing</h4>
          </div>
          <div className="space-y-2 bg-amber-50/50 p-4 rounded-xl border border-amber-200/60 text-xs text-amber-900">
            {(scheme.things_to_consider || [
              'Returns are market-linked and not guaranteed.',
              'Market volatility may cause short-term fluctuations in fund NAV.',
              'Ensure tax implications (LTCG / STCG) match your overall annual income slab.',
              'Maintain an emergency liquid buffer before committing capital.'
            ]).map((item, idx) => (
              <div key={idx} className="flex items-start gap-2">
                <span className="text-amber-600 font-bold">•</span>
                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Document Evidence Citation (Slide 6 / Factsheet) */}
        {scheme.source_evidence && (
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-[11px] text-[#64748B] flex items-center gap-2.5">
            <FileText className="w-4 h-4 text-slate-500 shrink-0" />
            <div>
              <span className="font-semibold text-[#102A43]">Document Evidence:</span>{' '}
              {scheme.source_evidence.document || 'Scheme Information Document (SID)'} (
              {scheme.source_evidence.regulator || 'SEBI Registered'})
            </div>
          </div>
        )}

        {/* Action Button */}
        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2.5 bg-[#092B49] hover:bg-[#102A43] text-white text-xs font-semibold rounded-lg transition-colors cursor-pointer"
          >
            Close Details
          </button>
        </div>
      </div>
    </div>
  );
};

