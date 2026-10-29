import React from 'react';
import { 
  HeartPulse, 
  Wallet, 
  TrendingUp, 
  Target, 
  Sparkles, 
  ArrowRight, 
  ShieldCheck, 
  AlertCircle, 
  Plus, 
  Bot, 
  Layers,
  ArrowUpRight,
  Clock,
  Coins,
  ChevronRight
} from 'lucide-react';
import { 
  PieChart, 
  Pie, 
  Cell, 
  ResponsiveContainer, 
  Tooltip 
} from 'recharts';
import { useFinancial } from '../context/FinancialContext';

export const Dashboard: React.FC = () => {
  const { 
    profile, 
    goals, 
    analysis, 
    portfolioPlan, 
    setCurrentPage, 
    setIsChatOpen, 
    sendChatMessage 
  } = useFinancial();

  const healthScore = analysis?.financial_health_score || 78;
  const healthStatus = analysis?.health_status || 'Healthy';
  const breakdown = analysis?.health_score_breakdown || {
    savings: 82,
    expenses: 70,
    emergency: 62,
    debt: 90,
    goals: 80,
  };

  const monthlyIncome = analysis?.monthly_income || 50000;
  const monthlyExpenses = analysis?.monthly_expenses || 30000;
  const monthlySurplus = analysis?.monthly_surplus || 20000;

  // Assets & Liabilities
  const totalAssets = (profile.existing_savings || 100000) + 350000; // includes existing investments
  const totalLiabilities = profile.total_debt || 0;
  const netPosition = totalAssets - totalLiabilities;

  const allocationData = [
    { name: 'Growth', value: portfolioPlan?.growth_equity_pct || 50, color: '#092B49' },
    { name: 'Stable Debt', value: portfolioPlan?.stable_debt_pct || 25, color: '#28B89A' },
    { name: 'Government', value: portfolioPlan?.government_schemes_pct || 15, color: '#6366F1' },
    { name: 'Reserve', value: portfolioPlan?.emergency_reserve_pct || 10, color: '#F59E0B' },
  ];

  const quickPrompts = [
    'Can I afford a ₹70,000 laptop?',
    'How much should I save every month?',
    'How long will it take me to reach my goal?',
    'What happens if my expenses increase by ₹5,000?',
  ];

  const handlePromptClick = (prompt: string) => {
    setIsChatOpen(true);
    sendChatMessage(prompt);
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-[#F8FBFC] py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Welcome Banner */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs bg-[#DDF7F0] text-[#092B49] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider">
                Financial Dashboard
              </span>
              <span className="text-xs text-[#28B89A] font-semibold flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5" /> All Systems Nominal
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-[#092B49] tracking-tight">
              Welcome back, {profile.name}
            </h1>
            <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">
              Here is your holistic financial snapshot, health breakdown, and active goal trajectories.
            </p>
          </div>

          <div className="flex items-center gap-2.5">
            <button
              onClick={() => setCurrentPage('insights')}
              className="px-4 py-2 bg-white border border-[#DCE5EC] hover:bg-slate-50 text-[#102A43] text-xs font-semibold rounded-lg shadow-xs transition-colors flex items-center gap-1.5 cursor-pointer"
            >
              <TrendingUp className="w-3.5 h-3.5 text-[#28B89A]" />
              <span>What-If Simulator</span>
            </button>
            <button
              onClick={() => setIsChatOpen(true)}
              className="px-4 py-2 bg-[#092B49] hover:bg-[#102A43] text-white text-xs font-semibold rounded-lg shadow-xs transition-colors flex items-center gap-1.5 cursor-pointer"
            >
              <Bot className="w-3.5 h-3.5 text-[#28B89A]" />
              <span>Ask FinWise AI</span>
            </button>
          </div>
        </div>

        {/* 3 Main Stat Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Net Financial Position Card */}
          <div className="bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-[#64748B] uppercase tracking-wider">
                  Net Financial Position
                </span>
                <span className="text-xs bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded-md">
                  Positive Equity
                </span>
              </div>
              <div className="flex items-baseline gap-2 mb-4">
                <span className="text-3xl font-black text-[#092B49]">
                  ₹{netPosition.toLocaleString()}
                </span>
                <span className="text-xs text-[#28B89A] font-semibold">Net Worth</span>
              </div>

              <div className="grid grid-cols-2 gap-3 pt-3 border-t border-slate-100 text-xs">
                <div>
                  <span className="text-[#64748B] block text-[11px]">Total Assets</span>
                  <span className="font-bold text-[#102A43]">₹{totalAssets.toLocaleString()}</span>
                </div>
                <div>
                  <span className="text-[#64748B] block text-[11px]">Total Liabilities</span>
                  <span className="font-bold text-[#102A43]">₹{totalLiabilities.toLocaleString()}</span>
                </div>
              </div>
            </div>
            <button
              onClick={() => setCurrentPage('onboarding-profile')}
              className="mt-4 text-[11px] text-[#28B89A] hover:underline font-semibold text-left flex items-center gap-1"
            >
              <span>Update assets & liabilities</span>
              <ChevronRight className="w-3 h-3" />
            </button>
          </div>

          {/* Monthly Cash Flow Card */}
          <div className="bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-[#64748B] uppercase tracking-wider">
                  Monthly Cash Flow
                </span>
                <span className="text-xs bg-[#DDF7F0] text-[#092B49] font-bold px-2 py-0.5 rounded-md">
                  {analysis?.savings_rate_pct || 40}% Saved
                </span>
              </div>
              <div className="flex items-baseline gap-2 mb-4">
                <span className="text-3xl font-black text-[#28B89A]">
                  ₹{Math.round(monthlySurplus).toLocaleString()}
                </span>
                <span className="text-xs text-[#64748B] font-semibold">/ month surplus</span>
              </div>

              <div className="grid grid-cols-2 gap-3 pt-3 border-t border-slate-100 text-xs">
                <div>
                  <span className="text-[#64748B] block text-[11px]">Monthly Income</span>
                  <span className="font-bold text-[#102A43]">₹{Math.round(monthlyIncome).toLocaleString()}</span>
                </div>
                <div>
                  <span className="text-[#64748B] block text-[11px]">Monthly Expenses</span>
                  <span className="font-bold text-[#102A43]">₹{Math.round(monthlyExpenses).toLocaleString()}</span>
                </div>
              </div>
            </div>
            <button
              onClick={() => setCurrentPage('insights')}
              className="mt-4 text-[11px] text-[#28B89A] hover:underline font-semibold text-left flex items-center gap-1"
            >
              <span>Run cash flow scenario</span>
              <ChevronRight className="w-3 h-3" />
            </button>
          </div>

          {/* Emergency Fund Cushion Card */}
          <div className="bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-[#64748B] uppercase tracking-wider">
                  Emergency Liquidity
                </span>
                <span className="text-xs bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded-md">
                  Target: 6 mo
                </span>
              </div>
              <div className="flex items-baseline gap-2 mb-4">
                <span className="text-3xl font-black text-[#092B49]">
                  {analysis?.emergency_fund_months || 3.3}
                </span>
                <span className="text-xs text-[#64748B] font-semibold">months of living expenses</span>
              </div>

              <div className="space-y-1.5 pt-3 border-t border-slate-100 text-xs">
                <div className="flex justify-between text-[11px] text-[#64748B]">
                  <span>Current Liquid Buffer</span>
                  <span className="font-bold text-[#102A43]">₹{(profile.existing_savings || 100000).toLocaleString()}</span>
                </div>
                <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-[#28B89A] h-full rounded-full"
                    style={{ width: `${Math.min(100, ((analysis?.emergency_fund_months || 3.3) / 6) * 100)}%` }}
                  />
                </div>
              </div>
            </div>
            <p className="mt-4 text-[11px] text-[#64748B]">
              Top-up ₹5,000/mo to reach full 6-month buffer.
            </p>
          </div>
        </div>

        {/* Middle Section: Financial Health Score & Investment Allocation */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Financial Health Score (Section 15) */}
          <div className="lg:col-span-7 bg-white rounded-2xl border border-[#DCE5EC] p-6 sm:p-7 shadow-xs space-y-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-[#DDF7F0] text-[#28B89A] flex items-center justify-center font-bold">
                  <HeartPulse className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-[#102A43]">Financial Health Score</h3>
                  <p className="text-xs text-[#64748B]">5-Pillar Holistic Financial Resilience Index</p>
                </div>
              </div>

              <div className="text-right">
                <span className="text-2xl sm:text-3xl font-black text-[#092B49]">{healthScore}</span>
                <span className="text-xs text-slate-400 font-bold"> / 100</span>
                <p className="text-[11px] text-[#28B89A] font-bold">{healthStatus}</p>
              </div>
            </div>

            {/* 5-Bar Breakdown matching Section 15 */}
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between text-xs font-semibold text-[#102A43] mb-1">
                  <span>Savings Discipline (Surplus Rate)</span>
                  <span className="text-[#28B89A]">{breakdown.savings} / 100</span>
                </div>
                <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                  <div className="bg-[#28B89A] h-full rounded-full" style={{ width: `${breakdown.savings}%` }} />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between text-xs font-semibold text-[#102A43] mb-1">
                  <span>Expense Control (50/30/20 Ratio)</span>
                  <span className="text-[#092B49]">{breakdown.expenses} / 100</span>
                </div>
                <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                  <div className="bg-[#092B49] h-full rounded-full" style={{ width: `${breakdown.expenses}%` }} />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between text-xs font-semibold text-[#102A43] mb-1">
                  <span>Emergency Cushion (Liquid Reserve)</span>
                  <span className="text-amber-600">{breakdown.emergency} / 100</span>
                </div>
                <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                  <div className="bg-amber-500 h-full rounded-full" style={{ width: `${breakdown.emergency}%` }} />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between text-xs font-semibold text-[#102A43] mb-1">
                  <span>Debt Burden (Debt-to-Income DTI)</span>
                  <span className="text-emerald-600">{breakdown.debt} / 100</span>
                </div>
                <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                  <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${breakdown.debt}%` }} />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between text-xs font-semibold text-[#102A43] mb-1">
                  <span>Goal Feasibility (Surplus Coverage)</span>
                  <span className="text-[#28B89A]">{breakdown.goals} / 100</span>
                </div>
                <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                  <div className="bg-[#28B89A] h-full rounded-full" style={{ width: `${breakdown.goals}%` }} />
                </div>
              </div>
            </div>

            {/* AI Insights Observations */}
            <div className="bg-[#F8FBFC] p-3.5 rounded-xl border border-slate-100 text-xs text-[#64748B] space-y-1">
              <p className="font-bold text-[#102A43]">Key Copilot Observation:</p>
              <p>• Your savings discipline is in the top quartile with 40% surplus.</p>
              <p>• Emergency liquidity is at 3.3 months; reaching 6 months unlocks top-tier financial immunity.</p>
            </div>
          </div>

          {/* Allocation Donut Chart & Quick Scheme Shortcuts */}
          <div className="lg:col-span-5 bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs space-y-4 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <h3 className="text-base font-bold text-[#102A43]">Portfolio Allocation</h3>
                <button
                  onClick={() => setCurrentPage('recommendations')}
                  className="text-xs text-[#28B89A] hover:underline font-semibold"
                >
                  View Schemes →
                </button>
              </div>

              <div className="h-56 my-2">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={allocationData}
                      cx="50%"
                      cy="50%"
                      innerRadius={50}
                      outerRadius={80}
                      paddingAngle={3}
                      dataKey="value"
                    >
                      {allocationData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(val: any) => [`${val}%`, 'Weight']} />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
                {allocationData.map((item) => (
                  <div key={item.name} className="flex items-center gap-2 p-1.5 bg-[#F8FBFC] rounded-lg">
                    <div className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: item.color }} />
                    <span className="text-[#64748B] text-[11px] truncate">{item.name}</span>
                    <span className="font-bold text-[#102A43] ml-auto">{item.value}%</span>
                  </div>
                ))}
              </div>
            </div>

            <button
              onClick={() => setCurrentPage('plan')}
              className="w-full py-2.5 bg-[#EEF6FF] hover:bg-[#dbeafe] text-[#092B49] text-xs font-bold rounded-lg transition-colors flex items-center justify-center gap-1.5 cursor-pointer mt-4"
            >
              <span>View Personalized Investment Plan</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Goals Progress Grid (Section 16) */}
        <div className="bg-white rounded-2xl border border-[#DCE5EC] p-6 sm:p-7 shadow-xs space-y-6">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#EEF6FF] text-[#092B49] flex items-center justify-center font-bold">
                <Target className="w-5 h-5 text-[#28B89A]" />
              </div>
              <div>
                <h3 className="text-base font-bold text-[#102A43]">Financial Goal Progress</h3>
                <p className="text-xs text-[#64748B]">Active milestones and estimated required monthly SIPs</p>
              </div>
            </div>

            <button
              onClick={() => setCurrentPage('onboarding-goals')}
              className="text-xs font-semibold px-3 py-1.5 bg-[#DDF7F0] text-[#092B49] rounded-lg hover:bg-[#caefe4] transition-colors flex items-center gap-1 cursor-pointer"
            >
              <Plus className="w-3.5 h-3.5 text-[#28B89A]" />
              <span>Manage Goals</span>
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {goals.map((g) => {
              const remaining = Math.max(0, g.target_amount - g.current_amount);
              const months = Math.max(1, g.target_months);
              const monthlyReq = Math.round(remaining / months);
              const pct = Math.min(100, Math.round((g.current_amount / Math.max(1, g.target_amount)) * 100));

              return (
                <div key={g.id} className="p-4 rounded-xl border border-slate-200 bg-[#F8FBFC] space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-bold text-[#102A43]">{g.name}</span>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-200 text-slate-700">
                      {g.target_months} mo target
                    </span>
                  </div>

                  <div className="space-y-1.5">
                    <div className="flex justify-between text-xs">
                      <span className="font-semibold text-[#102A43]">
                        ₹{g.current_amount.toLocaleString()} / ₹{g.target_amount.toLocaleString()}
                      </span>
                      <span className="font-bold text-[#28B89A]">{pct}% complete</span>
                    </div>

                    <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                      <div className="bg-[#28B89A] h-full rounded-full" style={{ width: `${pct}%` }} />
                    </div>

                    <div className="flex justify-between text-[11px] text-[#64748B] pt-0.5">
                      <span>₹{remaining.toLocaleString()} remaining</span>
                      <span className="font-medium text-[#092B49]">Required: ₹{monthlyReq.toLocaleString()}/mo</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* AI Financial Copilot Prompts Banner (Section 17) */}
        <div className="bg-gradient-to-r from-[#092B49] to-[#102A43] rounded-2xl p-6 sm:p-8 text-white shadow-md relative overflow-hidden">
          <div className="relative z-10 space-y-4">
            <div className="flex items-center gap-2">
              <span className="bg-[#28B89A] text-white text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase tracking-wider">
                AI FINANCIAL COPILOT
              </span>
              <span className="text-xs text-slate-300">Profile-Grounded Financial Reasoning</span>
            </div>

            <div>
              <h3 className="text-xl sm:text-2xl font-bold">Ask FinWise AI</h3>
              <p className="text-xs sm:text-sm text-slate-300 max-w-xl mt-1">
                Your personal decision copilot. Inquire about purchase affordability, expense increases, timeline accelerations, or portfolio suitability.
              </p>
            </div>

            {/* Quick Prompt Chips */}
            <div className="flex flex-wrap gap-2 pt-2">
              {quickPrompts.map((p) => (
                <button
                  key={p}
                  onClick={() => handlePromptClick(p)}
                  className="text-xs bg-white/10 hover:bg-white/20 text-white px-3.5 py-2 rounded-full border border-white/20 transition-all cursor-pointer backdrop-blur-xs flex items-center gap-1.5"
                >
                  <Sparkles className="w-3 h-3 text-[#28B89A]" />
                  <span>{p}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

