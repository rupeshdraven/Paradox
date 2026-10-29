import React, { useState } from 'react';
import { 
  Target, 
  Plus, 
  Trash2, 
  ArrowRight, 
  ArrowLeft, 
  CheckCircle2, 
  Sparkles, 
  Calendar, 
  ShieldAlert,
  Coins
} from 'lucide-react';
import { useFinancial } from '../context/FinancialContext';
import { ProgressStepper } from './ProgressStepper';
import { Goal } from '../types';

export const GoalsManager: React.FC = () => {
  const { goals, addGoal, removeGoal, setCurrentPage } = useFinancial();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newGoal, setNewGoal] = useState<Partial<Goal>>({
    name: '',
    target_amount: 500000,
    current_amount: 50000,
    target_months: 36,
    priority: 'Medium',
    category: 'Wealth'
  });
  const [error, setError] = useState<string | null>(null);

  const predefinedGoalTemplates = [
    { name: 'Emergency Fund', target: 150000, current: 40000, months: 12, priority: 'High' as const },
    { name: 'Wealth Creation', target: 1000000, current: 100000, months: 60, priority: 'High' as const },
    { name: 'Buying a Car', target: 800000, current: 150000, months: 36, priority: 'Medium' as const },
    { name: 'House Downpayment', target: 2000000, current: 250000, months: 60, priority: 'High' as const },
    { name: 'Higher Education', target: 600000, current: 75000, months: 24, priority: 'Medium' as const },
  ];

  const handleCreateGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newGoal.name?.trim()) {
      setError('Please provide a goal name');
      return;
    }
    if (!newGoal.target_amount || newGoal.target_amount <= 0) {
      setError('Target amount must be greater than zero');
      return;
    }

    const g: Goal = {
      id: `goal-${Date.now()}`,
      name: newGoal.name,
      target_amount: Number(newGoal.target_amount),
      current_amount: Number(newGoal.current_amount || 0),
      target_months: Number(newGoal.target_months || 12),
      priority: (newGoal.priority as 'High' | 'Medium' | 'Low') || 'Medium',
      category: newGoal.category || 'General',
    };

    await addGoal(g);
    setIsModalOpen(false);
    setNewGoal({
      name: '',
      target_amount: 500000,
      current_amount: 50000,
      target_months: 36,
      priority: 'Medium',
      category: 'Wealth'
    });
    setError(null);
  };

  const handleApplyTemplate = (tmpl: typeof predefinedGoalTemplates[0]) => {
    setNewGoal({
      name: tmpl.name,
      target_amount: tmpl.target,
      current_amount: tmpl.current,
      target_months: tmpl.months,
      priority: tmpl.priority,
    });
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-[#F8FBFC] py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Header & Stepper */}
        <div>
          <span className="inline-block bg-[#DDF7F0] text-[#092B49] text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-2 border border-[#28B89A]/30">
            STEP 2 OF 4
          </span>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl sm:text-4xl font-extrabold text-[#092B49] tracking-tight">
                What are you planning for?
              </h1>
              <p className="mt-1 text-sm sm:text-base text-[#64748B]">
                Tell us what you want your money to achieve.
              </p>
            </div>

            <button
              onClick={() => setIsModalOpen(true)}
              className="inline-flex items-center gap-2 px-4 py-2.5 bg-[#28B89A] hover:bg-[#229c82] text-white rounded-lg text-sm font-semibold transition-all shadow-xs cursor-pointer self-start sm:self-auto"
            >
              <Plus className="w-4 h-4" />
              <span>Add Another Goal</span>
            </button>
          </div>

          <ProgressStepper currentStep={2} onStepClick={(s) => {
            if (s === 1) setCurrentPage('onboarding-profile');
            if (s === 3) setCurrentPage('onboarding-risk');
            if (s === 4) setCurrentPage('onboarding-review');
          }} />
        </div>

        {/* Goals Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {goals.map((goal) => {
            const remaining = Math.max(0, goal.target_amount - goal.current_amount);
            const months = Math.max(1, goal.target_months);
            const monthlyReq = Math.round(remaining / months);
            const pct = Math.min(100, Math.round((goal.current_amount / Math.max(1, goal.target_amount)) * 100));

            return (
              <div
                key={goal.id}
                className="bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs hover:shadow-md transition-all duration-200 relative group flex flex-col justify-between"
              >
                <div>
                  {/* Top row */}
                  <div className="flex items-start justify-between gap-2 mb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-[#EEF6FF] text-[#28B89A] flex items-center justify-center font-bold">
                        <Target className="w-5 h-5" />
                      </div>
                      <div>
                        <h3 className="text-base font-bold text-[#102A43]">{goal.name}</h3>
                        <div className="flex items-center gap-2 mt-0.5">
                          <span className="text-xs text-[#64748B] flex items-center gap-1">
                            <Calendar className="w-3 h-3" /> {goal.target_months} months ({roundYears(goal.target_months)} yrs)
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <span
                        className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider ${
                          goal.priority === 'High'
                            ? 'bg-rose-50 text-rose-600 border border-rose-200'
                            : goal.priority === 'Medium'
                            ? 'bg-amber-50 text-amber-600 border border-amber-200'
                            : 'bg-slate-100 text-slate-600'
                        }`}
                      >
                        {goal.priority} Priority
                      </span>
                      <button
                        onClick={() => removeGoal(goal.id)}
                        className="text-slate-300 hover:text-red-500 transition-colors p-1"
                        title="Delete goal"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  {/* Progress bar */}
                  <div className="space-y-2 mb-4">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-[#102A43]">
                        ₹{goal.current_amount.toLocaleString()} <span className="text-[#64748B] font-normal">saved</span>
                      </span>
                      <span className="font-bold text-[#28B89A]">{pct}%</span>
                      <span className="font-semibold text-[#102A43]">
                        ₹{goal.target_amount.toLocaleString()} <span className="text-[#64748B] font-normal">target</span>
                      </span>
                    </div>

                    <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                      <div
                        className="bg-[#28B89A] h-full rounded-full transition-all duration-500"
                        style={{ width: `${pct}%` }}
                      />
                    </div>

                    <div className="flex items-center justify-between text-[11px] text-[#64748B] pt-0.5">
                      <span>₹{remaining.toLocaleString()} remaining</span>
                      <span className="font-medium text-[#092B49]">
                        Target: {goal.target_months} mo
                      </span>
                    </div>
                  </div>
                </div>

                {/* Calculation Footer */}
                <div className="bg-[#F8FBFC] rounded-xl p-3 border border-slate-100 mt-2 flex items-center justify-between text-xs">
                  <div>
                    <p className="text-[10px] text-[#64748B] uppercase font-semibold">Required Monthly Saving</p>
                    <p className="text-sm font-bold text-[#092B49]">
                      ₹{monthlyReq.toLocaleString()}<span className="text-xs font-normal text-slate-500">/mo</span>
                    </p>
                  </div>
                  <span className="text-[10px] text-[#28B89A] bg-[#DDF7F0] px-2 py-1 rounded-md font-medium">
                    Linear Baseline
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Empty state if no goals */}
        {goals.length === 0 && (
          <div className="bg-white rounded-2xl border-2 border-dashed border-[#DCE5EC] p-12 text-center">
            <Target className="w-12 h-12 text-[#28B89A] mx-auto mb-3" />
            <h3 className="text-lg font-bold text-[#102A43]">No goals created yet</h3>
            <p className="text-sm text-[#64748B] max-w-sm mx-auto mt-1 mb-5">
              Add your wealth targets (e.g. Emergency Fund, Buying a Home, or Retirement) so we can calculate monthly contribution targets.
            </p>
            <button
              onClick={() => setIsModalOpen(true)}
              className="px-5 py-2.5 bg-[#092B49] text-white rounded-lg text-sm font-semibold hover:bg-[#102A43] transition-all"
            >
              + Create First Goal
            </button>
          </div>
        )}

        {/* Navigation bottom bar */}
        <div className="flex items-center justify-between pt-6 border-t border-[#DCE5EC]">
          <button
            onClick={() => setCurrentPage('onboarding-profile')}
            className="flex items-center gap-2 px-5 py-2.5 text-sm font-semibold text-[#64748B] hover:text-[#102A43] rounded-lg transition-colors cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Profile</span>
          </button>

          <button
            onClick={() => setCurrentPage('onboarding-risk')}
            className="flex items-center gap-2 px-6 py-3 bg-[#092B49] hover:bg-[#102A43] text-white text-sm font-semibold rounded-lg shadow-sm transition-all duration-150 cursor-pointer group"
          >
            <span>Continue to Risk Assessment</span>
            <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
          </button>
        </div>
      </div>

      {/* Add Goal Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-[#DCE5EC] animate-scaleUp">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-[#102A43] flex items-center gap-2">
                <Target className="w-5 h-5 text-[#28B89A]" /> Create Financial Goal
              </h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 text-lg font-bold"
              >
                ✕
              </button>
            </div>

            {/* Quick Templates */}
            <div className="mb-4">
              <p className="text-xs font-semibold text-[#64748B] mb-2">Popular Templates:</p>
              <div className="flex flex-wrap gap-1.5">
                {predefinedGoalTemplates.map((t) => (
                  <button
                    key={t.name}
                    type="button"
                    onClick={() => handleApplyTemplate(t)}
                    className="text-[11px] px-2.5 py-1 bg-slate-100 hover:bg-[#EEF6FF] hover:text-[#092B49] text-slate-700 rounded-md font-medium transition-colors"
                  >
                    + {t.name} (₹{(t.target / 100000).toFixed(1)}L)
                  </button>
                ))}
              </div>
            </div>

            {error && (
              <div className="mb-4 p-2.5 bg-red-50 text-red-600 text-xs rounded-lg border border-red-200">
                {error}
              </div>
            )}

            <form onSubmit={handleCreateGoal} className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-[#102A43] block mb-1">Goal Name</label>
                <input
                  type="text"
                  placeholder="e.g. Emergency Fund or Wealth Creation"
                  value={newGoal.name}
                  onChange={(e) => setNewGoal({ ...newGoal, name: e.target.value })}
                  className="w-full px-3.5 py-2.5 border border-[#DCE5EC] rounded-lg text-sm text-[#102A43] focus:outline-none focus:ring-2 focus:ring-[#28B89A]"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-[#102A43] block mb-1">Target Amount (₹)</label>
                  <input
                    type="number"
                    min={1000}
                    step={5000}
                    value={newGoal.target_amount}
                    onChange={(e) => setNewGoal({ ...newGoal, target_amount: parseFloat(e.target.value) || 0 })}
                    className="w-full px-3.5 py-2.5 border border-[#DCE5EC] rounded-lg text-sm text-[#102A43] focus:outline-none focus:ring-2 focus:ring-[#28B89A]"
                  />
                </div>

                <div>
                  <label className="text-xs font-semibold text-[#102A43] block mb-1">Current Saved (₹)</label>
                  <input
                    type="number"
                    min={0}
                    step={5000}
                    value={newGoal.current_amount}
                    onChange={(e) => setNewGoal({ ...newGoal, current_amount: parseFloat(e.target.value) || 0 })}
                    className="w-full px-3.5 py-2.5 border border-[#DCE5EC] rounded-lg text-sm text-[#102A43] focus:outline-none focus:ring-2 focus:ring-[#28B89A]"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-[#102A43] block mb-1">Horizon (Months)</label>
                  <input
                    type="number"
                    min={1}
                    max={360}
                    value={newGoal.target_months}
                    onChange={(e) => setNewGoal({ ...newGoal, target_months: parseInt(e.target.value) || 12 })}
                    className="w-full px-3.5 py-2.5 border border-[#DCE5EC] rounded-lg text-sm text-[#102A43] focus:outline-none focus:ring-2 focus:ring-[#28B89A]"
                  />
                </div>

                <div>
                  <label className="text-xs font-semibold text-[#102A43] block mb-1">Priority</label>
                  <select
                    value={newGoal.priority}
                    onChange={(e) => setNewGoal({ ...newGoal, priority: e.target.value as any })}
                    className="w-full px-3.5 py-2.5 border border-[#DCE5EC] rounded-lg text-sm text-[#102A43] focus:outline-none focus:ring-2 focus:ring-[#28B89A]"
                  >
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                  </select>
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 pt-3">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-xs font-semibold text-[#64748B] hover:text-[#102A43]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2.5 bg-[#092B49] hover:bg-[#102A43] text-white text-xs font-semibold rounded-lg shadow-xs"
                >
                  Save Goal
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

function roundYears(months: number): number {
  return Math.round((months / 12) * 10) / 10;
}

