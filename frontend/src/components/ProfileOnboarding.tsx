import React, { useState } from 'react';
import { 
  User, 
  Calendar, 
  HelpCircle, 
  Lock, 
  Sparkles, 
  Lightbulb, 
  Target, 
  ShieldCheck, 
  TrendingUp,
  ArrowRight,
  Coins
} from 'lucide-react';
import { useFinancial } from '../context/FinancialContext';
import { ProgressStepper } from './ProgressStepper';
import { UserProfile } from '../types';

export const ProfileOnboarding: React.FC = () => {
  const { profile, saveUserProfile, setCurrentPage } = useFinancial();

  const [formData, setFormData] = useState<UserProfile>({ ...profile });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const incomeOptions = [
    'Below ₹3 Lakh',
    '₹3–5 Lakh',
    '₹5–10 Lakh',
    '₹10–20 Lakh',
    '₹20–50 Lakh',
    'Above ₹50 Lakh',
  ];

  const expenseOptions = [
    'Below ₹10,000',
    '₹10,000–₹25,000',
    '₹25,000–₹50,000',
    '₹50,000–₹1 Lakh',
    'Above ₹1 Lakh',
  ];

  const goalOptions = [
    'Wealth Creation',
    'Retirement',
    'Emergency Fund',
    'Buying a House',
    'Buying a Vehicle',
    'Education',
    "Child's Future",
    'Tax Saving',
    'Short-Term Savings',
    'Other',
  ];

  const horizonOptions = [
    'Less than 1 year',
    '1–3 years',
    '3–5 years',
    '5–10 years',
    '10+ years',
  ];

  const riskOptions = [
    'Very Conservative',
    'Conservative',
    'Moderate',
    'Aggressive',
    'Very Aggressive',
  ];

  const validate = (): boolean => {
    const errs: Record<string, string> = {};
    if (!formData.age || formData.age < 18 || formData.age > 100) {
      errs.age = 'Please enter a valid adult age between 18 and 100';
    }
    if (!formData.annual_income_range) {
      errs.annual_income_range = 'Please select your annual income range';
    }
    if (!formData.monthly_expenses_range) {
      errs.monthly_expenses_range = 'Please select your monthly expenses range';
    }
    if (!formData.investment_goal) {
      errs.investment_goal = 'Please select your primary investment goal';
    }
    if (!formData.investment_horizon) {
      errs.investment_horizon = 'Please select your target investment horizon';
    }
    if (!formData.risk_appetite) {
      errs.risk_appetite = 'Please select your initial risk appetite';
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    await saveUserProfile(formData);
    setCurrentPage('onboarding-goals');
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-gradient-to-br from-[#F8FBFC] via-[#EEF6FF]/40 to-[#DDF7F0]/30 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
        {/* Left Column: Heading, Stepper & Graphic Card */}
        <div className="lg:col-span-5 flex flex-col justify-between space-y-6">
          <div>
            <span className="inline-block bg-[#DDF7F0] text-[#092B49] text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-4 border border-[#28B89A]/30">
              STEP 1 OF 4
            </span>
            <h1 className="text-3xl sm:text-4xl lg:text-[42px] font-extrabold text-[#092B49] leading-tight tracking-tight">
              Let's understand your <br />
              <span className="text-[#092B49]">financial profile</span>
            </h1>
            <p className="mt-3 text-sm sm:text-base text-[#64748B] max-w-md leading-relaxed">
              Tell us a little about your finances so we can personalize your financial plan.
            </p>

            {/* Stepper */}
            <ProgressStepper currentStep={1} onStepClick={(s) => {
              if (s === 2) setCurrentPage('onboarding-goals');
              if (s === 3) setCurrentPage('onboarding-risk');
              if (s === 4) setCurrentPage('onboarding-review');
            }} />
          </div>

          {/* 3D-styled Graphic Card matching Screenshot 1 */}
          <div className="relative pt-4">
            <div className="bg-white/90 backdrop-blur-md rounded-2xl p-5 border border-[#DCE5EC] shadow-sm relative overflow-hidden">
              {/* Card top banner */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 rounded-md bg-[#EEF6FF] flex items-center justify-center text-[#28B89A]">
                    <TrendingUp className="w-3.5 h-3.5" />
                  </div>
                  <span className="text-xs font-bold text-[#102A43]">Smart Financial Planning</span>
                </div>
                <span className="text-[10px] bg-[#DDF7F0] text-[#092B49] font-medium px-2 py-0.5 rounded-full flex items-center gap-1">
                  <Sparkles className="w-2.5 h-2.5 text-[#28B89A]" /> Our AI Guidance
                </span>
              </div>

              {/* Mini visual chart graphic */}
              <div className="h-28 bg-gradient-to-t from-slate-50 to-white rounded-xl p-3 flex items-end justify-between gap-2 border border-slate-100 mb-4 relative">
                <div className="flex items-end gap-1.5 h-full w-2/3">
                  <div className="w-1/5 bg-[#DDF7F0] rounded-t-sm h-[40%]" />
                  <div className="w-1/5 bg-[#28B89A]/60 rounded-t-sm h-[65%]" />
                  <div className="w-1/5 bg-[#28B89A] rounded-t-sm h-[85%]" />
                  <div className="w-1/5 bg-[#092B49]/70 rounded-t-sm h-[55%]" />
                  <div className="w-1/5 bg-[#092B49] rounded-t-sm h-[95%]" />
                </div>
                {/* Gold coins stack illustration */}
                <div className="flex flex-col items-center justify-end">
                  <div className="w-10 h-10 rounded-full bg-amber-400 border-2 border-amber-300 shadow-md flex items-center justify-center text-amber-900 font-bold text-sm">
                    ₹
                  </div>
                  <span className="text-[9px] text-[#64748B] font-medium mt-1">₹10L Goal</span>
                </div>
              </div>

              {/* Floating Feature Pills */}
              <div className="space-y-2 pt-2 border-t border-slate-100">
                <div className="flex items-center gap-2 text-xs text-[#102A43] font-medium">
                  <div className="w-5 h-5 rounded-full bg-amber-50 flex items-center justify-center text-amber-600">
                    <Lightbulb className="w-3 h-3" />
                  </div>
                  <span>Personalized Insights</span>
                </div>
                <div className="flex items-center gap-2 text-xs text-[#102A43] font-medium">
                  <div className="w-5 h-5 rounded-full bg-teal-50 flex items-center justify-center text-[#28B89A]">
                    <Target className="w-3 h-3" />
                  </div>
                  <span>Smarter Goal Planning</span>
                </div>
                <div className="flex items-center gap-2 text-xs text-[#102A43] font-medium">
                  <div className="w-5 h-5 rounded-full bg-blue-50 flex items-center justify-center text-blue-600">
                    <ShieldCheck className="w-3 h-3" />
                  </div>
                  <span>A More Secure Future</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Investor Profile Form Card matching Screenshot 1 */}
        <div className="lg:col-span-7">
          <div className="bg-white rounded-2xl border border-[#DCE5EC] shadow-sm p-6 sm:p-8">
            {/* Form Header */}
            <div className="flex items-start gap-4 mb-6 pb-4 border-b border-slate-100">
              <div className="w-12 h-12 rounded-full bg-[#EEF6FF] text-[#092B49] flex items-center justify-center shrink-0">
                <User className="w-6 h-6 text-[#28B89A]" />
              </div>
              <div>
                <h2 className="text-xl sm:text-2xl font-bold text-[#102A43]">Investor Profile</h2>
                <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">
                  Enter your basic financial information to get started.
                </p>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-5">
                {/* Age */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-xs font-semibold text-[#102A43]">Age</label>
                  </div>
                  <div className="relative">
                    <input
                      type="number"
                      min={18}
                      max={100}
                      placeholder="e.g. 25"
                      value={formData.age || ''}
                      onChange={(e) => setFormData({ ...formData, age: parseInt(e.target.value) || 0 })}
                      className={`w-full px-3.5 py-2.5 rounded-lg border text-sm text-[#102A43] bg-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#28B89A] focus:border-transparent ${
                        errors.age ? 'border-red-400 bg-red-50/30' : 'border-[#DCE5EC]'
                      }`}
                    />
                    <Calendar className="w-4 h-4 text-slate-400 absolute right-3 top-3 pointer-events-none" />
                  </div>
                  {errors.age && <p className="text-red-500 text-[11px] mt-1">{errors.age}</p>}
                </div>

                {/* Annual Income */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-xs font-semibold text-[#102A43] flex items-center gap-1">
                      Annual Income <HelpCircle className="w-3 h-3 text-slate-400" />
                    </label>
                  </div>
                  <select
                    value={formData.annual_income_range}
                    onChange={(e) => setFormData({ ...formData, annual_income_range: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-lg border text-sm text-[#102A43] bg-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#28B89A] focus:border-transparent ${
                      errors.annual_income_range ? 'border-red-400' : 'border-[#DCE5EC]'
                    }`}
                  >
                    <option value="">Select range</option>
                    {incomeOptions.map((opt) => (
                      <option key={opt} value={opt}>{opt}</option>
                    ))}
                  </select>
                  {errors.annual_income_range && (
                    <p className="text-red-500 text-[11px] mt-1">{errors.annual_income_range}</p>
                  )}
                </div>

                {/* Monthly Expenses */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-xs font-semibold text-[#102A43] flex items-center gap-1">
                      Monthly Expenses <HelpCircle className="w-3 h-3 text-slate-400" />
                    </label>
                  </div>
                  <select
                    value={formData.monthly_expenses_range}
                    onChange={(e) => setFormData({ ...formData, monthly_expenses_range: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-lg border text-sm text-[#102A43] bg-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#28B89A] focus:border-transparent ${
                      errors.monthly_expenses_range ? 'border-red-400' : 'border-[#DCE5EC]'
                    }`}
                  >
                    <option value="">Select range</option>
                    {expenseOptions.map((opt) => (
                      <option key={opt} value={opt}>{opt}</option>
                    ))}
                  </select>
                  {errors.monthly_expenses_range && (
                    <p className="text-red-500 text-[11px] mt-1">{errors.monthly_expenses_range}</p>
                  )}
                </div>

                {/* Investment Goal */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-xs font-semibold text-[#102A43] flex items-center gap-1">
                      Investment Goal <HelpCircle className="w-3 h-3 text-slate-400" />
                    </label>
                  </div>
                  <select
                    value={formData.investment_goal}
                    onChange={(e) => setFormData({ ...formData, investment_goal: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-lg border text-sm text-[#102A43] bg-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#28B89A] focus:border-transparent ${
                      errors.investment_goal ? 'border-red-400' : 'border-[#DCE5EC]'
                    }`}
                  >
                    <option value="">Select goal</option>
                    {goalOptions.map((opt) => (
                      <option key={opt} value={opt}>{opt}</option>
                    ))}
                  </select>
                  {errors.investment_goal && (
                    <p className="text-red-500 text-[11px] mt-1">{errors.investment_goal}</p>
                  )}
                </div>

                {/* Investment Horizon */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-xs font-semibold text-[#102A43] flex items-center gap-1">
                      Investment Horizon <HelpCircle className="w-3 h-3 text-slate-400" />
                    </label>
                  </div>
                  <select
                    value={formData.investment_horizon}
                    onChange={(e) => setFormData({ ...formData, investment_horizon: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-lg border text-sm text-[#102A43] bg-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#28B89A] focus:border-transparent ${
                      errors.investment_horizon ? 'border-red-400' : 'border-[#DCE5EC]'
                    }`}
                  >
                    <option value="">Select horizon</option>
                    {horizonOptions.map((opt) => (
                      <option key={opt} value={opt}>{opt}</option>
                    ))}
                  </select>
                  {errors.investment_horizon && (
                    <p className="text-red-500 text-[11px] mt-1">{errors.investment_horizon}</p>
                  )}
                </div>

                {/* Risk Appetite */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-xs font-semibold text-[#102A43] flex items-center gap-1">
                      Risk Appetite <HelpCircle className="w-3 h-3 text-slate-400" />
                    </label>
                  </div>
                  <select
                    value={formData.risk_appetite}
                    onChange={(e) => setFormData({ ...formData, risk_appetite: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-lg border text-sm text-[#102A43] bg-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#28B89A] focus:border-transparent ${
                      errors.risk_appetite ? 'border-red-400' : 'border-[#DCE5EC]'
                    }`}
                  >
                    <option value="">Select initial preference</option>
                    {riskOptions.map((opt) => (
                      <option key={opt} value={opt}>{opt}</option>
                    ))}
                  </select>
                  {errors.risk_appetite && (
                    <p className="text-red-500 text-[11px] mt-1">{errors.risk_appetite}</p>
                  )}
                </div>
              </div>

              {/* Existing Investments / Liabilities */}
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="text-xs font-semibold text-[#102A43] flex items-center gap-1">
                    Existing Investments / Liabilities <HelpCircle className="w-3 h-3 text-slate-400" />
                  </label>
                </div>
                <textarea
                  rows={3}
                  placeholder="e.g. Mutual funds, stocks, EPF, loans, credit card dues, etc."
                  value={formData.existing_investments_liabilities}
                  onChange={(e) => setFormData({ ...formData, existing_investments_liabilities: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-lg border border-[#DCE5EC] text-sm text-[#102A43] bg-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#28B89A] focus:border-transparent"
                />
              </div>

              {/* Continue Button */}
              <button
                type="submit"
                className="w-full py-3.5 px-6 bg-[#092B49] hover:bg-[#102A43] text-white font-semibold rounded-lg shadow-sm transition-all duration-150 flex items-center justify-center gap-2 cursor-pointer group"
              >
                <span>Continue</span>
                <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
              </button>

              {/* Security Note Banner */}
              <div className="flex items-center justify-center gap-2 py-2.5 px-3 bg-[#DDF7F0]/60 rounded-lg text-xs text-[#092B49] font-medium border border-[#28B89A]/20">
                <Lock className="w-3.5 h-3.5 text-[#28B89A]" />
                <span>Your information is encrypted and used only to personalize your financial plan.</span>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

