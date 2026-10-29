import React, { useState } from 'react';
import { 
  Check, 
  Target, 
  BarChart3, 
  Clock, 
  Wallet, 
  ChevronDown, 
  ArrowRight, 
  Sparkles, 
  Sprout, 
  Building2, 
  FileText, 
  Coins, 
  User, 
  Heart,
  TrendingUp,
  ShieldCheck,
  CheckCircle2
} from 'lucide-react';
import { useFinancial } from '../context/FinancialContext';
import { InvestmentDetailModal } from './InvestmentDetailModal';
import { InvestmentScheme } from '../types';

export const RecommendedSchemes: React.FC = () => {
  const { 
    recommendations, 
    profile, 
    goals, 
    selectedScheme, 
    setSelectedScheme, 
    setCurrentPage 
  } = useFinancial();

  const [activeCategory, setActiveCategory] = useState<string>('All Schemes');
  const [sortBy, setSortBy] = useState<string>('Recommended');

  const categories = [
    'All Schemes',
    'Mutual Funds',
    'Government Schemes',
    'Fixed Income',
    'Tax Saving',
    'Others',
  ];

  // Primary goal
  const primaryGoal = goals.length > 0 ? goals[0].name : profile.investment_goal || 'Wealth Creation';

  // Filter schemes
  const filteredSchemes = recommendations
    .filter((s) => {
      if (activeCategory === 'All Schemes') return true;
      return s.category.toLowerCase() === activeCategory.toLowerCase();
    })
    .sort((a, b) => {
      if (sortBy === 'Risk') {
        const order: Record<string, number> = { 'Very Low': 1, 'Low': 2, 'Moderate': 3, 'High': 4, 'Very High': 5 };
        return (order[a.risk_level] || 3) - (order[b.risk_level] || 3);
      }
      if (sortBy === 'Potential Return') {
        return (b.indicative_rate_num || 0) - (a.indicative_rate_num || 0);
      }
      if (sortBy === 'Minimum Investment') {
        return (a.min_investment_num || 0) - (b.min_investment_num || 0);
      }
      return (b.suitability_score || 0) - (a.suitability_score || 0);
    });

  // Category Icon helper matching Screenshot 2
  const getSchemeIcon = (scheme: InvestmentScheme) => {
    const name = scheme.name.toLowerCase();
    if (name.includes('bluechip') || name.includes('index')) {
      return (
        <div className="w-10 h-10 rounded-xl bg-[#DDF7F0] text-[#28B89A] flex items-center justify-center">
          <Sprout className="w-5 h-5" />
        </div>
      );
    }
    if (name.includes('ppf') || name.includes('provident')) {
      return (
        <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-500 flex items-center justify-center">
          <Building2 className="w-5 h-5" />
        </div>
      );
    }
    if (name.includes('elss') || name.includes('tax')) {
      return (
        <div className="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
          <FileText className="w-5 h-5" />
        </div>
      );
    }
    if (name.includes('deposit') || name.includes('fd') || name.includes('gold')) {
      return (
        <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
          <Coins className="w-5 h-5" />
        </div>
      );
    }
    if (name.includes('nps') || name.includes('pension')) {
      return (
        <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
          <User className="w-5 h-5" />
        </div>
      );
    }
    if (name.includes('sukanya')) {
      return (
        <div className="w-10 h-10 rounded-xl bg-pink-50 text-pink-500 flex items-center justify-center">
          <Heart className="w-5 h-5" />
        </div>
      );
    }
    return (
      <div className="w-10 h-10 rounded-xl bg-slate-100 text-slate-600 flex items-center justify-center">
        <TrendingUp className="w-5 h-5" />
      </div>
    );
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-[#F8FBFC] py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Sidebar Navigation Stepper matching Screenshot 2 */}
        <div className="lg:col-span-3 space-y-6">
          <div className="bg-white rounded-2xl border border-[#DCE5EC] p-5 shadow-xs space-y-4">
            {/* Step 1 */}
            <div 
              onClick={() => setCurrentPage('onboarding-profile')}
              className="flex items-start gap-3 p-2.5 rounded-xl hover:bg-slate-50 transition-colors cursor-pointer"
            >
              <div className="w-6 h-6 rounded-full bg-[#28B89A] text-white flex items-center justify-center text-xs shrink-0 mt-0.5">
                <Check className="w-3.5 h-3.5" />
              </div>
              <div>
                <p className="text-xs font-bold text-[#102A43]">01 Investor Profile</p>
                <p className="text-[11px] text-[#28B89A] font-medium">Completed</p>
              </div>
            </div>

            {/* Step 2 (Active) */}
            <div className="flex items-start gap-3 p-2.5 rounded-xl bg-[#DDF7F0]/70 border border-[#28B89A]/40">
              <div className="w-6 h-6 rounded-full bg-[#28B89A] text-white flex items-center justify-center text-xs shrink-0 mt-0.5">
                <Check className="w-3.5 h-3.5" />
              </div>
              <div>
                <p className="text-xs font-bold text-[#092B49]">02 Recommended Schemes</p>
                <p className="text-[11px] text-[#092B49] font-medium">Based on your profile</p>
              </div>
            </div>

            {/* Step 3 */}
            <div 
              onClick={() => setCurrentPage('plan')}
              className="flex items-start gap-3 p-2.5 rounded-xl hover:bg-slate-50 transition-colors cursor-pointer"
            >
              <div className="w-6 h-6 rounded-full bg-slate-100 text-slate-500 flex items-center justify-center text-xs shrink-0 mt-0.5 font-bold">
                03
              </div>
              <div>
                <p className="text-xs font-semibold text-[#64748B]">Investment Plan</p>
                <p className="text-[11px] text-slate-400">Create your roadmap</p>
              </div>
            </div>

            {/* Step 4 */}
            <div 
              onClick={() => setCurrentPage('dashboard')}
              className="flex items-start gap-3 p-2.5 rounded-xl hover:bg-slate-50 transition-colors cursor-pointer"
            >
              <div className="w-6 h-6 rounded-full bg-slate-100 text-slate-500 flex items-center justify-center text-xs shrink-0 mt-0.5 font-bold">
                04
              </div>
              <div>
                <p className="text-xs font-semibold text-[#64748B]">Review & Confirm</p>
                <p className="text-[11px] text-slate-400">Finalize your plan</p>
              </div>
            </div>
          </div>

          {/* Left Bottom Floating Illustration Card matching Screenshot 2 */}
          <div className="bg-gradient-to-b from-[#EEF6FF]/70 to-[#DDF7F0]/60 rounded-2xl p-5 border border-[#DCE5EC] text-center shadow-xs">
            <div className="w-16 h-16 mx-auto mb-3 flex items-center justify-center text-[#28B89A]">
              <Sprout className="w-10 h-10" />
            </div>
            <p className="text-xs font-bold text-[#092B49] leading-snug">
              Personalized investment recommendations for a smarter future.
            </p>
            <p className="text-[10px] text-[#64748B] mt-1">
              Transparent, explainable & evidence-backed
            </p>
          </div>
        </div>

        {/* Right Main Content */}
        <div className="lg:col-span-9 space-y-6">
          {/* Header */}
          <div>
            <span className="inline-block bg-[#DDF7F0] text-[#092B49] text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-2 border border-[#28B89A]/30">
              STEP 2 OF 4
            </span>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h1 className="text-2xl sm:text-3xl font-extrabold text-[#092B49] tracking-tight">
                  Recommended Investment Schemes
                </h1>
                <p className="text-xs sm:text-sm text-[#64748B] mt-1">
                  Based on your profile, goals and risk appetite, here are the most suitable investment options for you.
                </p>
              </div>

              <button
                onClick={() => setCurrentPage('plan')}
                className="flex items-center gap-2 px-5 py-2.5 bg-[#092B49] hover:bg-[#102A43] text-white text-xs font-bold rounded-lg shadow-sm transition-all self-start sm:self-auto cursor-pointer shrink-0"
              >
                <span>View Portfolio Plan</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Top Summary Bar matching Screenshot 2 */}
          <div className="bg-white rounded-2xl border border-[#DCE5EC] p-4 sm:p-5 shadow-xs grid grid-cols-2 md:grid-cols-4 gap-4">
            {/* Goal */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#DDF7F0] text-[#28B89A] flex items-center justify-center shrink-0">
                <Target className="w-5 h-5" />
              </div>
              <div>
                <p className="text-[10px] text-[#64748B] font-semibold uppercase">Goal</p>
                <p className="text-xs sm:text-sm font-bold text-[#102A43]">{primaryGoal}</p>
              </div>
            </div>

            {/* Risk Profile */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#EEF6FF] text-blue-600 flex items-center justify-center shrink-0">
                <BarChart3 className="w-5 h-5" />
              </div>
              <div>
                <p className="text-[10px] text-[#64748B] font-semibold uppercase">Risk Profile</p>
                <p className="text-xs sm:text-sm font-bold text-[#102A43]">{profile.risk_appetite || 'Moderate'}</p>
              </div>
            </div>

            {/* Horizon */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center shrink-0">
                <Clock className="w-5 h-5" />
              </div>
              <div>
                <p className="text-[10px] text-[#64748B] font-semibold uppercase">Investment Horizon</p>
                <p className="text-xs sm:text-sm font-bold text-[#102A43]">{profile.investment_horizon || '5–10 Years'}</p>
              </div>
            </div>

            {/* Suggested Monthly Investment */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center shrink-0">
                <Wallet className="w-5 h-5" />
              </div>
              <div>
                <p className="text-[10px] text-[#64748B] font-semibold uppercase">Suggested Monthly</p>
                <p className="text-xs sm:text-sm font-bold text-[#102A43]">₹5,000 – ₹10,000</p>
              </div>
            </div>
          </div>

          {/* Filter Pills & Sort Bar matching Screenshot 2 */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            {/* Filter Pills */}
            <div className="flex flex-wrap items-center gap-2">
              {categories.map((cat) => {
                const isActive = activeCategory === cat;
                return (
                  <button
                    key={cat}
                    onClick={() => setActiveCategory(cat)}
                    className={`px-3.5 py-1.5 rounded-full text-xs font-semibold transition-all duration-150 cursor-pointer ${
                      isActive
                        ? 'bg-[#092B49] text-white shadow-xs'
                        : 'bg-white border border-[#DCE5EC] text-[#64748B] hover:bg-slate-50'
                    }`}
                  >
                    {cat}
                  </button>
                );
              })}
            </div>

            {/* Sort Dropdown */}
            <div className="flex items-center gap-2 text-xs text-[#64748B] self-end sm:self-auto">
              <span>Sort by</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-2.5 py-1.5 bg-white border border-[#DCE5EC] rounded-lg text-xs font-semibold text-[#102A43] focus:outline-none focus:ring-1 focus:ring-[#28B89A]"
              >
                <option value="Recommended">Recommended</option>
                <option value="Risk">Risk</option>
                <option value="Potential Return">Potential Return</option>
                <option value="Minimum Investment">Minimum Investment</option>
              </select>
            </div>
          </div>

          {/* Scheme Cards Grid matching Screenshot 2 */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
            {filteredSchemes.map((scheme) => (
              <div
                key={scheme.id}
                className="bg-white rounded-2xl border border-[#DCE5EC] p-5 shadow-xs hover:shadow-md transition-all duration-200 flex flex-col justify-between"
              >
                <div>
                  {/* Top Header */}
                  <div className="flex items-start gap-3 mb-3">
                    {getSchemeIcon(scheme)}
                    <div>
                      <h3 className="text-sm font-bold text-[#102A43] leading-snug">{scheme.name}</h3>
                      <p className="text-[11px] text-[#64748B]">{scheme.provider}</p>
                    </div>
                  </div>

                  {/* Badges Row */}
                  <div className="flex flex-wrap items-center gap-1.5 mb-3">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-[#DDF7F0] text-[#092B49]">
                      {scheme.category}
                    </span>
                    {scheme.badge && (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 border border-amber-200">
                        {scheme.badge}
                      </span>
                    )}
                    {scheme.suitability_score && (
                      <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-md bg-blue-50 text-blue-700">
                        {scheme.suitability_score}% Match
                      </span>
                    )}
                  </div>

                  {/* Description */}
                  <p className="text-xs text-[#64748B] line-clamp-2 leading-relaxed mb-4">
                    {scheme.description}
                  </p>

                  {/* 3 Metric Columns matching Screenshot 2 */}
                  <div className="grid grid-cols-3 gap-2 py-3 border-t border-b border-slate-100 text-center mb-4">
                    <div>
                      <p className="text-[10px] text-[#64748B]">Expected Return</p>
                      <p className="text-xs font-bold text-[#28B89A] mt-0.5">{scheme.indicative_return}</p>
                    </div>
                    <div>
                      <p className="text-[10px] text-[#64748B]">Risk Level</p>
                      <p className={`text-xs font-bold mt-0.5 ${
                        scheme.risk_level.includes('Very Low') || scheme.risk_level.includes('Low')
                          ? 'text-emerald-600'
                          : scheme.risk_level.includes('Moderate')
                          ? 'text-amber-600'
                          : 'text-rose-600'
                      }`}>
                        {scheme.risk_level}
                      </p>
                    </div>
                    <div>
                      <p className="text-[10px] text-[#64748B]">Min. Investment</p>
                      <p className="text-xs font-bold text-[#092B49] mt-0.5">{scheme.min_investment}</p>
                    </div>
                  </div>
                </div>

                {/* View Details Button matching Screenshot 2 */}
                <button
                  onClick={() => setSelectedScheme(scheme)}
                  className="w-full py-2.5 px-4 bg-[#092B49] hover:bg-[#102A43] text-white rounded-lg text-xs font-semibold transition-colors duration-150 flex items-center justify-center gap-1.5 cursor-pointer"
                >
                  <span>View Details</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}
          </div>

          {/* Bottom Action Card */}
          <div className="bg-[#EEF6FF]/60 rounded-2xl p-5 border border-blue-200/60 flex flex-col sm:flex-row items-center justify-between gap-4 mt-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-white text-[#28B89A] flex items-center justify-center shadow-xs">
                <CheckCircle2 className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-[#102A43]">Ready to implement this portfolio?</h4>
                <p className="text-xs text-[#64748B]">
                  See your personalized monthly allocation roadmap based on your selected schemes.
                </p>
              </div>
            </div>

            <button
              onClick={() => setCurrentPage('plan')}
              className="px-6 py-2.5 bg-[#28B89A] hover:bg-[#209f84] text-white text-xs font-bold rounded-lg shadow-sm transition-all cursor-pointer shrink-0 flex items-center gap-1.5"
            >
              <span>View Investment Plan</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Why This Recommendation Modal */}
      <InvestmentDetailModal
        scheme={selectedScheme}
        onClose={() => setSelectedScheme(null)}
      />
    </div>
  );
};

