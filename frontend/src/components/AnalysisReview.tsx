import React, { useState } from 'react';
import { 
  User, 
  Target, 
  ShieldCheck, 
  TrendingUp, 
  Check, 
  ArrowRight, 
  ArrowLeft, 
  Loader2,
  Wallet,
  Coins,
  Sparkles
} from 'lucide-react';
import { useFinancial } from '../context/FinancialContext';
import { ProgressStepper } from './ProgressStepper';

export const AnalysisReview: React.FC = () => {
  const { profile, goals, analysis, activeRiskScore, riskCategory, refreshAnalysisAndRecs, setCurrentPage } = useFinancial();
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [completedCheckpoints, setCompletedCheckpoints] = useState<number[]>([]);

  const checkpoints = [
    'Understanding income & expenses telemetry',
    'Evaluating financial milestones & target dates',
    'Assessing psychological & capacity risk tolerance',
    'Matching suitable investment categories & schemes',
    'Preparing your personalized financial roadmap',
  ];

  const handleStartAnalysis = async () => {
    setIsAnalyzing(true);
    setCompletedCheckpoints([]);

    // Animate the 5 checkpoints sequentially for realistic fintech feel
    for (let i = 0; i < checkpoints.length; i++) {
      await new Promise((resolve) => setTimeout(resolve, 600));
      setCompletedCheckpoints((prev) => [...prev, i]);
    }

    await refreshAnalysisAndRecs();
    await new Promise((resolve) => setTimeout(resolve, 500));
    setIsAnalyzing(false);
    setCurrentPage('recommendations');
  };

  const monthlyIncome = analysis?.monthly_income || (profile.annual_income > 0 ? profile.annual_income / 12 : 50000);
  const monthlyExpenses = analysis?.monthly_expenses || profile.monthly_expenses || 30000;
  const monthlySurplus = analysis?.monthly_surplus || Math.max(0, monthlyIncome - monthlyExpenses);
  const savingsRate = analysis?.savings_rate_pct || Math.round((monthlySurplus / monthlyIncome) * 100);
  const emergencyCoverage = analysis?.emergency_fund_months || 3.3;

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-[#F8FBFC] py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header & Stepper */}
        <div>
          <span className="inline-block bg-[#DDF7F0] text-[#092B49] text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-2 border border-[#28B89A]/30">
            STEP 4 OF 4
          </span>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-[#092B49] tracking-tight">
            Review & Analyze Your Profile
          </h1>
          <p className="mt-1 text-sm sm:text-base text-[#64748B]">
            Confirm your financial profile before running our recommendation and allocation engines.
          </p>

          <ProgressStepper currentStep={4} onStepClick={(s) => {
            if (s === 1) setCurrentPage('onboarding-profile');
            if (s === 2) setCurrentPage('onboarding-goals');
            if (s === 3) setCurrentPage('onboarding-risk');
          }} />
        </div>

        {/* Loading Overlay State */}
        {isAnalyzing ? (
          <div className="bg-white rounded-2xl border border-[#DCE5EC] p-8 sm:p-12 text-center shadow-lg animate-fadeIn">
            <div className="relative w-16 h-16 mx-auto mb-6 flex items-center justify-center">
              <div className="w-16 h-16 rounded-full border-4 border-[#EEF6FF] border-t-[#28B89A] animate-spin" />
              <Sparkles className="w-6 h-6 text-[#28B89A] absolute" />
            </div>

            <h3 className="text-xl font-bold text-[#102A43] mb-2">
              Analyzing your financial profile...
            </h3>
            <p className="text-sm text-[#64748B] mb-8 max-w-md mx-auto">
              Our deterministic financial rules engine is calibrating optimal asset allocation and suitability matches.
            </p>

            <div className="max-w-md mx-auto space-y-3 text-left">
              {checkpoints.map((cp, idx) => {
                const isDone = completedCheckpoints.includes(idx);
                return (
                  <div
                    key={idx}
                    className={`flex items-center gap-3 p-3 rounded-xl transition-all duration-300 ${
                      isDone ? 'bg-[#DDF7F0]/60 text-[#092B49]' : 'bg-slate-50 text-slate-400'
                    }`}
                  >
                    <div
                      className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                        isDone ? 'bg-[#28B89A] text-white' : 'bg-slate-200 text-slate-500'
                      }`}
                    >
                      {isDone ? <Check className="w-3 h-3" /> : idx + 1}
                    </div>
                    <span className="text-xs font-semibold">{cp}</span>
                  </div>
                );
              })}
            </div>
          </div>
        ) : (
          <>
            {/* Grid of Profile Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              {/* Profile Card */}
              <div className="bg-white rounded-2xl border border-[#DCE5EC] p-5 shadow-xs flex flex-col justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-3 text-[#28B89A]">
                    <User className="w-4 h-4" />
                    <h3 className="text-xs font-bold uppercase tracking-wider text-[#64748B]">Your Profile</h3>
                  </div>
                  <p className="text-lg font-bold text-[#102A43]">{profile.name}, {profile.age}</p>
                  <div className="mt-3 space-y-1.5 text-xs text-[#64748B]">
                    <p>Income: <strong className="text-[#102A43]">{profile.annual_income_range}</strong></p>
                    <p>Expenses: <strong className="text-[#102A43]">{profile.monthly_expenses_range}</strong></p>
                    <p>Horizon: <strong className="text-[#102A43]">{profile.investment_horizon}</strong></p>
                  </div>
                </div>
                <button
                  onClick={() => setCurrentPage('onboarding-profile')}
                  className="mt-4 text-[11px] text-[#28B89A] hover:underline font-semibold text-left"
                >
                  Edit Profile →
                </button>
              </div>

              {/* Goals Card */}
              <div className="bg-white rounded-2xl border border-[#DCE5EC] p-5 shadow-xs flex flex-col justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-3 text-[#28B89A]">
                    <Target className="w-4 h-4" />
                    <h3 className="text-xs font-bold uppercase tracking-wider text-[#64748B]">Active Goals</h3>
                  </div>
                  <p className="text-lg font-bold text-[#102A43]">
                    {goals.length} Defined Goal{goals.length === 1 ? '' : 's'}
                  </p>
                  <div className="mt-3 space-y-1.5 text-xs text-[#64748B]">
                    {goals.slice(0, 2).map((g) => (
                      <p key={g.id}>
                        {g.name}: <strong className="text-[#102A43]">₹{(g.target_amount / 100000).toFixed(1)}L</strong> ({g.target_months} mo)
                      </p>
                    ))}
                    {goals.length === 0 && <p className="text-slate-400">No goals added yet</p>}
                  </div>
                </div>
                <button
                  onClick={() => setCurrentPage('onboarding-goals')}
                  className="mt-4 text-[11px] text-[#28B89A] hover:underline font-semibold text-left"
                >
                  Manage Goals →
                </button>
              </div>

              {/* Risk Profile Card */}
              <div className="bg-white rounded-2xl border border-[#DCE5EC] p-5 shadow-xs flex flex-col justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-3 text-[#28B89A]">
                    <ShieldCheck className="w-4 h-4" />
                    <h3 className="text-xs font-bold uppercase tracking-wider text-[#64748B]">Risk Profile</h3>
                  </div>
                  <p className="text-lg font-bold text-[#102A43]">{riskCategory}</p>
                  <div className="mt-3 space-y-1.5 text-xs text-[#64748B]">
                    <p>Risk Score: <strong className="text-[#102A43]">{activeRiskScore} / 100</strong></p>
                    <p>Orientation: <strong className="text-[#102A43]">Balanced Growth</strong></p>
                    <p>Loss Resilience: <strong className="text-[#102A43]">Moderate Dip Tolerance</strong></p>
                  </div>
                </div>
                <button
                  onClick={() => setCurrentPage('onboarding-risk')}
                  className="mt-4 text-[11px] text-[#28B89A] hover:underline font-semibold text-left"
                >
                  Retake Quiz →
                </button>
              </div>
            </div>

            {/* Financial Snapshot Card */}
            <div className="bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs">
              <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
                <div className="flex items-center gap-2">
                  <Wallet className="w-5 h-5 text-[#28B89A]" />
                  <h3 className="text-base font-bold text-[#102A43]">Financial Snapshot & Cash Flow</h3>
                </div>
                <span className="text-xs text-[#28B89A] bg-[#DDF7F0] px-2.5 py-0.5 rounded-full font-semibold">
                  Estimated Metrics
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 text-center">
                <div className="bg-[#F8FBFC] p-3 rounded-xl border border-slate-100">
                  <p className="text-[10px] text-[#64748B] font-semibold uppercase">Monthly Income</p>
                  <p className="text-base font-bold text-[#092B49] mt-1">₹{Math.round(monthlyIncome).toLocaleString()}</p>
                </div>
                <div className="bg-[#F8FBFC] p-3 rounded-xl border border-slate-100">
                  <p className="text-[10px] text-[#64748B] font-semibold uppercase">Monthly Expenses</p>
                  <p className="text-base font-bold text-[#092B49] mt-1">₹{Math.round(monthlyExpenses).toLocaleString()}</p>
                </div>
                <div className="bg-[#DDF7F0]/50 p-3 rounded-xl border border-[#28B89A]/30">
                  <p className="text-[10px] text-[#092B49] font-semibold uppercase">Monthly Surplus</p>
                  <p className="text-base font-bold text-[#28B89A] mt-1">₹{Math.round(monthlySurplus).toLocaleString()}</p>
                </div>
                <div className="bg-[#F8FBFC] p-3 rounded-xl border border-slate-100">
                  <p className="text-[10px] text-[#64748B] font-semibold uppercase">Savings Rate</p>
                  <p className="text-base font-bold text-[#092B49] mt-1">{savingsRate}%</p>
                </div>
                <div className="bg-[#F8FBFC] p-3 rounded-xl border border-slate-100">
                  <p className="text-[10px] text-[#64748B] font-semibold uppercase">Emergency Cushion</p>
                  <p className="text-base font-bold text-[#092B49] mt-1">{emergencyCoverage} mo</p>
                </div>
                <div className="bg-[#F8FBFC] p-3 rounded-xl border border-slate-100">
                  <p className="text-[10px] text-[#64748B] font-semibold uppercase">Debt Burden</p>
                  <p className="text-base font-bold text-emerald-600 mt-1">0% (Low)</p>
                </div>
              </div>
            </div>

            {/* Big Action Button */}
            <div className="bg-gradient-to-r from-[#092B49] to-[#102A43] rounded-2xl p-6 sm:p-8 text-white shadow-md flex flex-col sm:flex-row items-center justify-between gap-6">
              <div className="space-y-1 text-center sm:text-left">
                <h3 className="text-xl sm:text-2xl font-extrabold tracking-tight">
                  Ready to Generate Your Personalized Plan?
                </h3>
                <p className="text-xs sm:text-sm text-slate-300 max-w-lg leading-relaxed">
                  Our recommendation engine applies deterministic suitability constraints against verified mutual funds and government schemes.
                </p>
              </div>

              <button
                onClick={handleStartAnalysis}
                className="w-full sm:w-auto px-8 py-4 bg-[#28B89A] hover:bg-[#209f84] text-white font-bold rounded-xl shadow-lg transition-all duration-150 flex items-center justify-center gap-2 cursor-pointer shrink-0 text-base"
              >
                <Sparkles className="w-5 h-5" />
                <span>Analyze My Financial Profile</span>
                <ArrowRight className="w-5 h-5 ml-1" />
              </button>
            </div>

            {/* Bottom Nav */}
            <div className="flex items-center justify-between pt-4">
              <button
                onClick={() => setCurrentPage('onboarding-risk')}
                className="flex items-center gap-2 px-5 py-2.5 text-sm font-semibold text-[#64748B] hover:text-[#102A43] rounded-lg transition-colors cursor-pointer"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Back to Risk Assessment</span>
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

