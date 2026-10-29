import React from 'react';
import { ShieldAlert, ExternalLink, CheckCircle2, Lock } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-auto border-t border-[#DCE5EC] bg-white text-[#64748B] text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Responsible Financial Advisory Disclaimer Box */}
        <div className="bg-[#F8FBFC] border border-[#DCE5EC] rounded-xl p-4 sm:p-5 mb-6">
          <div className="flex items-start gap-3">
            <ShieldAlert className="w-5 h-5 text-[#28B89A] shrink-0 mt-0.5" />
            <div className="space-y-1.5">
              <div className="flex items-center gap-2">
                <h4 className="text-xs font-bold text-[#102A43] uppercase tracking-wider">
                  Responsible Advisory Notice & Regulatory Guardrails
                </h4>
                <span className="bg-[#DDF7F0] text-[#092B49] text-[10px] font-semibold px-2 py-0.5 rounded-full">
                  Educational Decision Support
                </span>
              </div>
              <p className="text-[11px] leading-relaxed text-[#64748B]">
                FinWise AI provides educational and decision-support information for demonstration purposes. Investment values and returns are subject to market conditions and are not guaranteed. Projections, indicative return rates, and financial health scores are illustrative estimations derived from user inputs and publicly available fund documentation.
              </p>
              <p className="text-[11px] leading-relaxed text-[#64748B]">
                This platform is not a SEBI-registered Investment Adviser (RIA). Users should verify current product disclosures, Scheme Information Documents (SIDs), and consult a certified financial planner before executing any financial transaction.
              </p>
            </div>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-slate-500 pt-4 border-t border-slate-100">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-[#092B49]">FinWise AI</span>
            <span>•</span>
            <span>Two Engines, One Controlled Advisory Copilot</span>
          </div>

          <div className="flex items-center gap-6">
            <span className="flex items-center gap-1 text-slate-600">
              <Lock className="w-3 h-3 text-[#28B89A]" /> Client-Side Encryption
            </span>
            <span className="flex items-center gap-1 text-slate-600">
              <CheckCircle2 className="w-3 h-3 text-[#28B89A]" /> Guardrail Gate Active
            </span>
            <span>Prototype v2.0</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

