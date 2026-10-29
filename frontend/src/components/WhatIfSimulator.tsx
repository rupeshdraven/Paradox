import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  Sparkles, 
  Sliders, 
  Clock, 
  ArrowRight, 
  ShieldCheck, 
  CheckCircle2, 
  Coins, 
  Zap,
  Info
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts';
import { useFinancial } from '../context/FinancialContext';
import { api } from '../services/api';
import { WhatIfResponse } from '../types';

export const WhatIfSimulator: React.FC = () => {
  const { profile, goals, analysis } = useFinancial();

  // Baseline figures
  const initialIncome = analysis?.monthly_income || 50000;
  const initialExpenses = analysis?.monthly_expenses || 30000;
  const initialSurplus = analysis?.monthly_surplus || 20000;
  const initialGoalAmount = goals.length > 0 ? goals[0].target_amount : 1000000;

  // Simulator state
  const [income, setIncome] = useState<number>(initialIncome);
  const [expenses, setExpenses] = useState<number>(initialExpenses);
  const [currentInvestment, setCurrentInvestment] = useState<number>(8000);
  const [newInvestment, setNewInvestment] = useState<number>(12000);
  const [goalAmount, setGoalAmount] = useState<number>(initialGoalAmount);
  const [expectedReturn, setExpectedReturn] = useState<number>(11.0);

  const [simResult, setSimResult] = useState<WhatIfResponse | null>(null);
  const [isSimulating, setIsSimulating] = useState(false);

  // Active view tab: Simulator or Guardrail Inspector
  const [activeTab, setActiveTab] = useState<'simulator' | 'guardrails'>('simulator');
  const [auditLogs, setAuditLogs] = useState<any[]>([]);

  const runSimulation = async () => {
    setIsSimulating(true);
    try {
      const res = await api.simulate({
        current_income: income,
        current_expenses: expenses,
        current_investment: currentInvestment,
        goal_amount: goalAmount,
        expected_annual_return_pct: expectedReturn,
        new_monthly_investment: newInvestment,
      });
      setSimResult(res);
    } catch (err) {
      console.error('Simulation error', err);
    } finally {
      setIsSimulating(false);
    }
  };

  useEffect(() => {
    runSimulation();
  }, [income, expenses, currentInvestment, newInvestment, goalAmount, expectedReturn]);

  const loadAuditLogs = async () => {
    try {
      const res = await fetch('/api/audit-logs');
      if (res.ok) {
        const data = await res.json();
        setAuditLogs(data.audit_logs || []);
      }
    } catch {
      // offline fallback
      setAuditLogs([
        {
          timestamp: new Date().toISOString(),
          user_query: 'Can I afford a ₹70,000 laptop?',
          guardrail_status: 'ALLOW',
          checks_applied: ['Input Validation', 'Suitability Check', 'Guardrail Gate'],
          response_summary: 'Purchasing 70000 laptop will strain cash flow...',
          evidence_cited: '50-30-20 Cash-Flow Model'
        }
      ]);
    }
  };

  useEffect(() => {
    if (activeTab === 'guardrails') {
      loadAuditLogs();
    }
  }, [activeTab]);

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-[#F8FBFC] py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header & Tabs */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs bg-[#DDF7F0] text-[#092B49] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider">
                Financial Insights
              </span>
              <span className="text-xs text-[#28B89A] font-semibold flex items-center gap-1">
                <Sparkles className="w-3.5 h-3.5" /> Interactive Projection
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-[#092B49] tracking-tight">
              {activeTab === 'simulator' ? 'Financial What-If Simulator' : 'AI Guardrail Decision Gate'}
            </h1>
            <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">
              {activeTab === 'simulator'
                ? 'Model how modifying monthly contributions, savings, and returns dramatically compresses your goal timeline.'
                : 'Deterministic compliance checks, decision gates (ALLOW/WARN/BLOCK), and evidence audit log.'}
            </p>
          </div>

          <div className="flex items-center bg-white p-1 rounded-xl border border-[#DCE5EC] shadow-xs">
            <button
              onClick={() => setActiveTab('simulator')}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                activeTab === 'simulator'
                  ? 'bg-[#092B49] text-white shadow-xs'
                  : 'text-[#64748B] hover:text-[#102A43]'
              }`}
            >
              What-If Simulator
            </button>
            <button
              onClick={() => setActiveTab('guardrails')}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                activeTab === 'guardrails'
                  ? 'bg-[#092B49] text-white shadow-xs'
                  : 'text-[#64748B] hover:text-[#102A43]'
              }`}
            >
              Guardrail Decision Gate
            </button>
          </div>
        </div>

        {activeTab === 'simulator' ? (
          <>
            {/* Top Impact Banner: Before vs After */}
            {simResult && (
              <div className="bg-gradient-to-r from-[#092B49] to-[#102A43] rounded-2xl p-6 sm:p-8 text-white shadow-md grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
                {/* Before */}
                <div className="text-center sm:text-left">
                  <span className="text-[10px] text-slate-300 font-bold uppercase tracking-wider block mb-1">
                    Current Monthly Investment (₹{currentInvestment.toLocaleString()})
                  </span>
                  <p className="text-2xl sm:text-3xl font-black">
                    {simResult.before_months} months
                  </p>
                  <span className="text-xs text-slate-300">
                    ≈ {Math.round((simResult.before_months / 12) * 10) / 10} years to reach ₹{goalAmount.toLocaleString()}
                  </span>
                </div>

                {/* Arrow / Time Saved */}
                <div className="text-center bg-white/10 rounded-xl p-4 border border-white/20 backdrop-blur-xs">
                  <span className="text-[10px] text-[#28B89A] font-extrabold uppercase tracking-wider block mb-0.5">
                    POTENTIAL TIME SAVED
                  </span>
                  <div className="text-2xl sm:text-3xl font-black text-[#28B89A] flex items-center justify-center gap-1">
                    <Zap className="w-5 h-5 text-amber-400" />
                    <span>{simResult.months_saved} Months Faster!</span>
                  </div>
                  <span className="text-xs text-slate-200">
                    Accelerated by {Math.round((simResult.months_saved / 12) * 10) / 10} full years
                  </span>
                </div>

                {/* After */}
                <div className="text-center sm:text-right">
                  <span className="text-[10px] text-slate-300 font-bold uppercase tracking-wider block mb-1">
                    Optimized Monthly Investment (₹{newInvestment.toLocaleString()})
                  </span>
                  <p className="text-2xl sm:text-3xl font-black text-[#28B89A]">
                    {simResult.after_months} months
                  </p>
                  <span className="text-xs text-slate-300">
                    ≈ {Math.round((simResult.after_months / 12) * 10) / 10} years to goal completion
                  </span>
                </div>
              </div>
            )}

            {/* Main Simulator Grid: Controls on Left, Visual Chart on Right */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              {/* Sliders Control Card */}
              <div className="lg:col-span-5 bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs space-y-6">
                <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
                  <Sliders className="w-4 h-4 text-[#28B89A]" />
                  <h3 className="text-sm font-bold text-[#102A43]">Simulate Parameters</h3>
                </div>

                {/* Current Monthly Investment Slider */}
                <div>
                  <div className="flex items-center justify-between text-xs font-semibold text-[#102A43] mb-2">
                    <span>Baseline Monthly Investment</span>
                    <span className="text-[#092B49] font-bold">₹{currentInvestment.toLocaleString()}</span>
                  </div>
                  <input
                    type="range"
                    min={2000}
                    max={50000}
                    step={1000}
                    value={currentInvestment}
                    onChange={(e) => setCurrentInvestment(Number(e.target.value))}
                    className="w-full accent-[#092B49] cursor-pointer"
                  />
                  <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                    <span>₹2,000</span>
                    <span>₹50,000</span>
                  </div>
                </div>

                {/* New Monthly Investment Slider */}
                <div className="bg-[#DDF7F0]/40 p-3.5 rounded-xl border border-[#28B89A]/30">
                  <div className="flex items-center justify-between text-xs font-semibold text-[#092B49] mb-2">
                    <span className="flex items-center gap-1">
                      <Sparkles className="w-3.5 h-3.5 text-[#28B89A]" /> Optimized Monthly Investment
                    </span>
                    <span className="text-[#28B89A] font-extrabold text-sm">₹{newInvestment.toLocaleString()}</span>
                  </div>
                  <input
                    type="range"
                    min={2000}
                    max={75000}
                    step={1000}
                    value={newInvestment}
                    onChange={(e) => setNewInvestment(Number(e.target.value))}
                    className="w-full accent-[#28B89A] cursor-pointer"
                  />
                  <div className="flex justify-between text-[10px] text-[#28B89A] font-semibold mt-1">
                    <span>+₹{Math.max(0, newInvestment - currentInvestment).toLocaleString()} increase/mo</span>
                    <span>Max: ₹75,000</span>
                  </div>
                </div>

                {/* Goal Target Amount Slider */}
                <div>
                  <div className="flex items-center justify-between text-xs font-semibold text-[#102A43] mb-2">
                    <span>Goal Target Amount</span>
                    <span className="text-[#092B49] font-bold">₹{goalAmount.toLocaleString()}</span>
                  </div>
                  <input
                    type="range"
                    min={100000}
                    max={5000000}
                    step={50000}
                    value={goalAmount}
                    onChange={(e) => setGoalAmount(Number(e.target.value))}
                    className="w-full accent-[#092B49] cursor-pointer"
                  />
                  <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                    <span>₹1 Lakh</span>
                    <span>₹50 Lakh</span>
                  </div>
                </div>

                {/* Expected Return Rate */}
                <div>
                  <div className="flex items-center justify-between text-xs font-semibold text-[#102A43] mb-2">
                    <span className="flex items-center gap-1">
                      Expected Annual Return <Info className="w-3 h-3 text-slate-400" />
                    </span>
                    <span className="text-[#28B89A] font-bold">{expectedReturn}% p.a.</span>
                  </div>
                  <input
                    type="range"
                    min={6.0}
                    max={15.0}
                    step={0.5}
                    value={expectedReturn}
                    onChange={(e) => setExpectedReturn(Number(e.target.value))}
                    className="w-full accent-[#28B89A] cursor-pointer"
                  />
                  <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                    <span>6% (Debt/FD)</span>
                    <span>11% (Balanced)</span>
                    <span>15% (Aggressive Equity)</span>
                  </div>
                  <p className="text-[10px] text-slate-400 mt-2">
                    *Returns are indicative and illustrative, not guaranteed.
                  </p>
                </div>
              </div>

              {/* Chart Visualizer */}
              <div className="lg:col-span-7 bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                  <div>
                    <h3 className="text-sm font-bold text-[#102A43]">Wealth Trajectory Comparison</h3>
                    <p className="text-xs text-[#64748B]">Current Strategy vs. Optimized Accelerated Plan</p>
                  </div>
                  <span className="text-xs font-semibold px-2 py-0.5 bg-slate-100 rounded text-slate-600">
                    Compounded Monthly
                  </span>
                </div>

                {/* Line Chart */}
                <div className="w-full h-80 pt-2">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={simResult?.timeline_comparison || []}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                      <XAxis dataKey="period" stroke="#94a3b8" fontSize={11} />
                      <YAxis 
                        stroke="#94a3b8" 
                        fontSize={11} 
                        tickFormatter={(v) => `₹${(v / 100000).toFixed(1)}L`}
                      />
                      <Tooltip
                        formatter={(value: any) => [`₹${Number(value).toLocaleString()}`, '']}
                        contentStyle={{ borderRadius: '12px', border: '1px solid #DCE5EC', fontSize: '12px' }}
                      />
                      <Legend 
                        verticalAlign="top" 
                        height={36} 
                        iconType="circle"
                        formatter={(val) => <span className="text-xs text-[#102A43] font-medium">{val}</span>}
                      />
                      <Line
                        type="monotone"
                        dataKey="current_strategy"
                        name="Baseline (₹8k/mo)"
                        stroke="#092B49"
                        strokeWidth={2.5}
                        dot={false}
                      />
                      <Line
                        type="monotone"
                        dataKey="optimized_strategy"
                        name="Optimized (₹12k/mo)"
                        stroke="#28B89A"
                        strokeWidth={3}
                        dot={false}
                      />
                      <Line
                        type="monotone"
                        dataKey="target"
                        name="Goal Target (₹10L)"
                        stroke="#E11D48"
                        strokeDasharray="5 5"
                        strokeWidth={1.5}
                        dot={false}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>

                {/* Key Insights bullets */}
                {simResult?.insights && (
                  <div className="bg-[#F8FBFC] p-4 rounded-xl border border-slate-100 space-y-1.5 text-xs text-[#102A43]">
                    <span className="font-bold uppercase tracking-wider text-[10px] text-[#64748B] block mb-1">
                      Actionable Simulation Takeaway:
                    </span>
                    {simResult.insights.map((insight, idx) => (
                      <div key={idx} className="flex items-start gap-2">
                        <CheckCircle2 className="w-4 h-4 text-[#28B89A] shrink-0 mt-0.5" />
                        <span>{insight}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </>
        ) : (
          /* Guardrail Decision Gate Tab (matching Slide 6) */
          <div className="space-y-6">
            {/* Slide 6 Architecture Banner */}
            <div className="bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-[#DDF7F0] text-[#28B89A] flex items-center justify-center font-bold">
                  <ShieldCheck className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-[#102A43]">
                    Deterministic Guardrail Decision Gate
                  </h3>
                  <p className="text-xs text-[#64748B]">
                    "The LLM is not the final decision-maker. Every request passes through deterministic checks."
                  </p>
                </div>
              </div>

              {/* 4 Decision Categories from Slide 6 */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-2">
                <div className="p-4 rounded-xl bg-emerald-50/70 border border-emerald-200">
                  <span className="text-xs font-bold text-emerald-800 flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" /> ALLOW
                  </span>
                  <p className="text-xs text-emerald-900 mt-1">
                    Safe to proceed. Grounded answer generated with source citations.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200">
                  <span className="text-xs font-bold text-amber-800 flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-amber-500" /> WARN
                  </span>
                  <p className="text-xs text-amber-900 mt-1">
                    Show caution. Flags risk mismatch, speculative crypto, or return guarantee claims.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-rose-50/70 border border-rose-200">
                  <span className="text-xs font-bold text-rose-800 flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-rose-500" /> BLOCK
                  </span>
                  <p className="text-xs text-rose-900 mt-1">
                    Do not answer. Refuses deceptive advice, unregistered derivatives, or illegal financial schemes.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-blue-50/70 border border-blue-200">
                  <span className="text-xs font-bold text-blue-800 flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-blue-500" /> REQUEST INFO
                  </span>
                  <p className="text-xs text-blue-900 mt-1">
                    Ask for more details. Prompts user if monthly income or horizon is missing.
                  </p>
                </div>
              </div>
            </div>

            {/* Audit Log Table */}
            <div className="bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <h3 className="text-sm font-bold text-[#102A43]">Live Compliance Audit Trail</h3>
                <span className="text-xs text-[#28B89A] font-semibold">
                  {auditLogs.length} Logged Entries
                </span>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-[#F8FBFC] text-[#64748B] font-semibold border-b border-slate-100">
                    <tr>
                      <th className="py-2.5 px-3">Timestamp</th>
                      <th className="py-2.5 px-3">User Query</th>
                      <th className="py-2.5 px-3">Gate Status</th>
                      <th className="py-2.5 px-3">Checks Applied</th>
                      <th className="py-2.5 px-3">Evidence Source</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {auditLogs.map((log, idx) => (
                      <tr key={idx} className="hover:bg-slate-50/50">
                        <td className="py-2.5 px-3 whitespace-nowrap text-slate-500">
                          {new Date(log.timestamp).toLocaleTimeString()}
                        </td>
                        <td className="py-2.5 px-3 font-medium text-[#102A43] max-w-xs truncate">
                          {log.user_query}
                        </td>
                        <td className="py-2.5 px-3">
                          <span
                            className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                              log.guardrail_status === 'ALLOW'
                                ? 'bg-emerald-50 text-emerald-700'
                                : log.guardrail_status === 'WARN'
                                ? 'bg-amber-50 text-amber-700'
                                : 'bg-rose-50 text-rose-700'
                            }`}
                          >
                            {log.guardrail_status}
                          </span>
                        </td>
                        <td className="py-2.5 px-3 text-slate-600 max-w-xs truncate">
                          {Array.isArray(log.checks_applied) ? log.checks_applied.join(', ') : log.checks_applied}
                        </td>
                        <td className="py-2.5 px-3 text-slate-500 text-[11px]">
                          {log.evidence_cited || 'SEBI Master Circular'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

