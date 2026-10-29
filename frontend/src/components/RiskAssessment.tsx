import React, { useState } from 'react';
import { 
  ShieldCheck, 
  HelpCircle, 
  ArrowRight, 
  ArrowLeft, 
  AlertTriangle, 
  Info,
  CheckCircle2,
  Gauge
} from 'lucide-react';
import { useFinancial } from '../context/FinancialContext';
import { ProgressStepper } from './ProgressStepper';

interface QuestionDef {
  id: number;
  question: string;
  options: Array<{ text: string; points: number }>;
}

export const RiskAssessment: React.FC = () => {
  const { submitRiskQuiz, activeRiskScore, riskCategory, setCurrentPage } = useFinancial();

  const questions: QuestionDef[] = [
    {
      id: 1,
      question: 'If your investment temporarily falls by 20%, what would you most likely do?',
      options: [
        { text: 'Sell immediately to stop further losses', points: 5 },
        { text: 'Wait until the market recovers', points: 15 },
        { text: 'Invest more at the lower valuation', points: 25 },
        { text: 'Not sure / Seek professional guidance', points: 10 },
      ],
    },
    {
      id: 2,
      question: 'When do you expect to need this invested money?',
      options: [
        { text: 'Within 1 year (Urgent liquidity)', points: 5 },
        { text: '1–3 years (Short term)', points: 10 },
        { text: '3–5 years (Medium term)', points: 15 },
        { text: '5–10 years (Long term)', points: 20 },
        { text: 'More than 10 years (Ultra long term)', points: 25 },
      ],
    },
    {
      id: 3,
      question: 'How important is protecting your original investment capital?',
      options: [
        { text: 'Extremely important (Cannot afford capital loss)', points: 5 },
        { text: 'Important (Prefer minimal drawdown)', points: 10 },
        { text: 'Neutral (Tolerate calculated market swings)', points: 15 },
        { text: 'Less important (Growth is more critical than safety)', points: 20 },
        { text: 'Not important (Seeking maximum compounding regardless of volatility)', points: 25 },
      ],
    },
    {
      id: 4,
      question: 'How comfortable are you with regular stock market fluctuations?',
      options: [
        { text: 'Not comfortable (Causes anxiety)', points: 5 },
        { text: 'Slightly comfortable (Prefer mostly fixed returns)', points: 10 },
        { text: 'Moderately comfortable (Accept seasonal dips)', points: 15 },
        { text: 'Comfortable (Understand equity volatility cycles)', points: 20 },
        { text: 'Very comfortable (Thrive in market corrections)', points: 25 },
      ],
    },
    {
      id: 5,
      question: 'What is your primary investment priority?',
      options: [
        { text: 'Capital preservation (Safety first)', points: 5 },
        { text: 'Stable regular income (Dividends & coupons)', points: 10 },
        { text: 'Balanced growth (Inflation hedge + stability)', points: 15 },
        { text: 'Long-term capital growth (Index & Bluechip)', points: 20 },
        { text: 'Maximum aggressive growth (Mid & Small cap equity)', points: 25 },
      ],
    },
  ];

  // Default selection matching Rupesh (Moderate profile: ~67/100)
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, { optIndex: number; points: number }>>({
    1: { optIndex: 1, points: 15 }, // Wait
    2: { optIndex: 3, points: 20 }, // 5-10 yrs
    3: { optIndex: 2, points: 15 }, // Neutral
    4: { optIndex: 2, points: 15 }, // Moderately
    5: { optIndex: 3, points: 20 }, // Long-term growth
  });

  const handleSelect = (qId: number, optIndex: number, pts: number) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [qId]: { optIndex, points: pts },
    }));
  };

  // Calculate live score
  const totalPts = Object.values(selectedAnswers).reduce((acc, curr) => acc + curr.points, 0);
  const calculatedScore = Math.round(Math.max(0, Math.min(100, ((totalPts - 25) / 100) * 100)));
  const calculatedCategory = calculatedScore <= 35 ? 'Conservative' : calculatedScore <= 68 ? 'Moderate' : 'Aggressive';

  const handleContinue = async () => {
    const formatted = Object.entries(selectedAnswers).map(([qId, val]) => ({
      question_id: parseInt(qId),
      selected_option_index: val.optIndex,
      points: val.points,
    }));
    await submitRiskQuiz(formatted);
    setCurrentPage('onboarding-review');
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-[#F8FBFC] py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header & Stepper */}
        <div>
          <span className="inline-block bg-[#DDF7F0] text-[#092B49] text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-2 border border-[#28B89A]/30">
            STEP 3 OF 4
          </span>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-[#092B49] tracking-tight">
            Assess Your Risk Profile
          </h1>
          <p className="mt-1 text-sm sm:text-base text-[#64748B]">
            We evaluate your psychological risk tolerance, investment horizon, and loss resilience objectively.
          </p>

          <ProgressStepper currentStep={3} onStepClick={(s) => {
            if (s === 1) setCurrentPage('onboarding-profile');
            if (s === 2) setCurrentPage('onboarding-goals');
            if (s === 4) setCurrentPage('onboarding-review');
          }} />
        </div>

        {/* Live Risk Meter Card */}
        <div className="bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-6">
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 rounded-2xl bg-[#EEF6FF] flex items-center justify-center text-[#28B89A] shrink-0 font-bold">
              <Gauge className="w-7 h-7" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold text-[#64748B] uppercase">Calculated Risk Score</span>
                <span className="text-[10px] bg-[#DDF7F0] text-[#092B49] px-2 py-0.5 rounded-full font-bold">
                  {calculatedCategory} Profile
                </span>
              </div>
              <div className="flex items-baseline gap-2 mt-0.5">
                <span className="text-2xl sm:text-3xl font-extrabold text-[#092B49]">
                  {calculatedScore}
                </span>
                <span className="text-sm text-slate-400 font-medium">/ 100</span>
              </div>
            </div>
          </div>

          <div className="flex-1 max-w-sm">
            <div className="flex items-center justify-between text-xs text-[#64748B] mb-1.5 font-medium">
              <span>Conservative</span>
              <span>Moderate</span>
              <span>Aggressive</span>
            </div>
            <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden flex">
              <div
                className={`h-full transition-all duration-300 rounded-full ${
                  calculatedScore <= 35
                    ? 'bg-blue-500'
                    : calculatedScore <= 68
                    ? 'bg-[#28B89A]'
                    : 'bg-amber-500'
                }`}
                style={{ width: `${calculatedScore}%` }}
              />
            </div>
          </div>
        </div>

        {/* Questionnaire List */}
        <div className="space-y-6">
          {questions.map((q, idx) => {
            const currentSelection = selectedAnswers[q.id]?.optIndex;

            return (
              <div
                key={q.id}
                className="bg-white rounded-2xl border border-[#DCE5EC] p-6 shadow-xs"
              >
                <div className="flex items-start gap-3 mb-4">
                  <span className="w-6 h-6 rounded-full bg-[#092B49] text-white flex items-center justify-center text-xs font-bold shrink-0">
                    {idx + 1}
                  </span>
                  <h3 className="text-base font-bold text-[#102A43] pt-0.5">
                    {q.question}
                  </h3>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pl-9">
                  {q.options.map((opt, oIdx) => {
                    const isSelected = currentSelection === oIdx;

                    return (
                      <button
                        key={oIdx}
                        type="button"
                        onClick={() => handleSelect(q.id, oIdx, opt.points)}
                        className={`text-left p-3.5 rounded-xl border text-xs sm:text-sm font-medium transition-all duration-150 flex items-center justify-between ${
                          isSelected
                            ? 'bg-[#EEF6FF] border-[#28B89A] text-[#092B49] font-semibold ring-1 ring-[#28B89A]'
                            : 'bg-white border-[#DCE5EC] text-[#64748B] hover:bg-slate-50 hover:border-slate-300'
                        }`}
                      >
                        <span>{opt.text}</span>
                        {isSelected && (
                          <CheckCircle2 className="w-4 h-4 text-[#28B89A] shrink-0 ml-2" />
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>

        {/* Explanation & Disclaimer Note */}
        <div className="bg-[#DDF7F0]/40 rounded-xl p-4 border border-[#28B89A]/30 flex items-start gap-3 text-xs text-[#092B49]">
          <Info className="w-4 h-4 text-[#28B89A] shrink-0 mt-0.5" />
          <p>
            Your responses indicate that you can tolerate <strong>{calculatedCategory.toLowerCase()} fluctuations</strong> while maintaining a steady multi-year investment horizon. This scoring model is an illustrative decision-support prototype and does not constitute certified statutory financial advisory.
          </p>
        </div>

        {/* Bottom Navigation */}
        <div className="flex items-center justify-between pt-6 border-t border-[#DCE5EC]">
          <button
            onClick={() => setCurrentPage('onboarding-goals')}
            className="flex items-center gap-2 px-5 py-2.5 text-sm font-semibold text-[#64748B] hover:text-[#102A43] rounded-lg transition-colors cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Goals</span>
          </button>

          <button
            onClick={handleContinue}
            className="flex items-center gap-2 px-6 py-3 bg-[#092B49] hover:bg-[#102A43] text-white text-sm font-semibold rounded-lg shadow-sm transition-all duration-150 cursor-pointer group"
          >
            <span>Continue to Review & Plan</span>
            <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
          </button>
        </div>
      </div>
    </div>
  );
};

