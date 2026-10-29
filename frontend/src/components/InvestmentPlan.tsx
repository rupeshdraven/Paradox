import React from 'react';
import { 
  PieChart, 
  Pie, 
  Cell, 
  ResponsiveContainer, 
  Tooltip, 
  Legend 
} from 'recharts';
import { 
  ShieldCheck, 
  ArrowRight, 
  ArrowLeft, 
  CheckCircle2, 
  Sparkles, 
  TrendingUp, 
  Wallet,
  Clock,
  Layers
} from 'lucide-react';
import { useFinancial } from '../context/FinancialContext';

export const InvestmentPlan: React.FC = () => {
  const { portfolioPlan, profile, analysis, setCurrentPage } = useFinancial();

  const plan = portfolioPlan || {
    growth_equity_pct: 50,
    stable_debt_pct: 25,
    government_schemes_pct: 15,
    emergency_reserve_pct: 10,
    monthly_allocation_plan: {
      'Growth (Equity Funds / Large Cap)': 10000,
      'Stable (Fixed Income / Debt)': 5000,
      'Government / Tax Buffer (PPF/NPS)': 3000,
      'Emergency Reserve (Liquid Fund)': 2000,
    },
    rationale: 'Balanced allocation balancing equity growth potential with stable fixed income and sovereign tax-advantaged buffers.',
    guardrail_status: 'PASSED'
  };

  const chartData = [
    { name: 'Growth (Equity)', value: plan.growth_equity_pct, color: '#092B49' },
    { name: 'Stable (Fixed Income)', value: plan.stable_debt_pct, color: '#28B89A' },
    { name: 'Government Schemes', value: plan.government_schemes_pct, color: '#6366F1' },
    { name: 'Emergency Reserve', value: plan.emergency_reserve_pct, color: '#F59E0B' },
  ];

  const totalMonthlySurplus = analysis?.monthly_surplus || 20000;

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-[#F8FBFC] py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="bg-[#DDF7F0] text-[#092B49] text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider border border-[#28B89A]/30">
                PERSONALIZED ROADMAP
              </span>
              <span className="bg-emerald-50 text-emerald-700 text-xs font-bold px-2.5 py-0.5 rounded-full flex items-center gap-1 border border-emerald-200">
                <ShieldCheck className="w-3 h-3 text-emerald-600" /> Guardrail Verified
              </span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-[#092B49] tracking-tight">
              Your Personalized Financial Plan
            </h1>
            <p className="mt-1 text-sm sm:text-base text-[#64748B]">
              Goal-aware asset allocation and monthly contribution roadmap calibrated to your risk profile.
            </p>
          </div>

          <button
            onClick={() => setCurrentPage('dashboard')}
            className="flex items-center gap-2 px-6 py-3 bg-[#092B49] hover:bg-[#102A43] text-white text-sm font-semibold rounded-lg shadow-sm transition-all self-start sm:self-auto cursor-pointer group"
          >
            <span>Proceed to Dashboard</span>
            <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
          </button>
        </div>

        {/* Allocation Visual Card */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center bg-white rounded-2xl border border-[#DCE5EC] p-6 sm:p-8 shadow-xs">
          {/* Donut Chart */}
          <div className="lg:col-span-6 flex flex-col items-center justify-center">
            <h3 className="text-base font-bold text-[#102A43] mb-2">Suggested Asset Allocation</h3>
            <p className="text-xs text-[#64748B] mb-4 text-center">
              Calibrated for {profile.risk_appetite} risk with a {profile.investment_horizon} horizon
            </p>

            <div className="w-full h-64 sm:h-72">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={chartData}
                    cx="50%"
                    cy="50%"
                    innerRadius={70}
                    outerRadius={105}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(val: any) => [`${val}%`, 'Allocation']}
                    contentStyle={{ borderRadius: '12px', border: '1px solid #DCE5EC', fontSize: '12px' }}
                  />
                  <Legend 
                    verticalAlign="bottom" 
                    height={36} 
                    iconType="circle"
                    formatter={(value) => <span className="text-xs text-[#102A43] font-medium">{value}</span>}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Allocation Percentages & Monthly Breakdown */}
          <div className="lg:col-span-6 space-y-4">
            <h3 className="text-base font-bold text-[#102A43] flex items-center gap-2">
              <Layers className="w-4 h-4 text-[#28B89A]" /> Monthly Contribution Plan
            </h3>
            <p className="text-xs text-[#64748B]">
              Recommended distribution of your ₹{Math.round(totalMonthlySurplus).toLocaleString()} monthly disposable surplus:
            </p>

            <div className="space-y-3">
              {Object.entries(plan.monthly_allocation_plan).map(([bucket, amount], idx) => {
                const color = chartData[idx]?.color || '#092B49';
                const pct = chartData[idx]?.value || 25;

                return (
                  <div
                    key={bucket}
                    className="p-3.5 rounded-xl border border-slate-100 bg-[#F8FBFC] flex items-center justify-between"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: color }} />
                      <div>
                        <p className="text-xs font-bold text-[#102A43]">{bucket}</p>
                        <p className="text-[11px] text-[#64748B]">{pct}% Target Weight</p>
                      </div>
                    </div>

                    <div className="text-right">
                      <p className="text-sm font-extrabold text-[#092B49]">
                        ₹{Math.round(amount).toLocaleString()}
                        <span className="text-[10px] font-normal text-[#64748B]">/mo</span>
                      </p>
                      <span className="text-[10px] text-[#28B89A] font-semibold">SIP Automated</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Strategy Rationale Card */}
        <div className="bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs space-y-3">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-[#28B89A]" />
            <h3 className="text-sm font-bold text-[#102A43]">Allocation Rationale</h3>
          </div>
          <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed">
            {plan.rationale}
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 text-xs text-[#102A43]">
            <div className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-[#28B89A] shrink-0 mt-0.5" />
              <span>Protects downside risk via guaranteed sovereign baseline</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-[#28B89A] shrink-0 mt-0.5" />
              <span>Optimizes tax liability under Sections 80C & 80CCD</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-[#28B89A] shrink-0 mt-0.5" />
              <span>Maintains liquid emergency reserve for unexpected expenses</span>
            </div>
          </div>
        </div>

        {/* Navigation bottom */}
        <div className="flex items-center justify-between pt-4">
          <button
            onClick={() => setCurrentPage('recommendations')}
            className="flex items-center gap-2 px-5 py-2.5 text-sm font-semibold text-[#64748B] hover:text-[#102A43] rounded-lg transition-colors cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Schemes</span>
          </button>

          <button
            onClick={() => setCurrentPage('dashboard')}
            className="flex items-center gap-2 px-6 py-3 bg-[#28B89A] hover:bg-[#209f84] text-white text-sm font-semibold rounded-lg shadow-sm transition-all cursor-pointer group"
          >
            <span>Open Financial Dashboard</span>
            <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
          </button>
        </div>
      </div>
    </div>
  );
};

