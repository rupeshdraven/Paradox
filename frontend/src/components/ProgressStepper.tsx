import React from 'react';
import { Check } from 'lucide-react';
import { AppPage } from '../context/FinancialContext';

interface ProgressStepperProps {
  currentStep: number; // 1, 2, 3, 4
  onStepClick?: (step: number) => void;
}

export const ProgressStepper: React.FC<ProgressStepperProps> = ({ currentStep, onStepClick }) => {
  const steps = [
    { num: 1, id: '01', label: 'Profile' },
    { num: 2, id: '02', label: 'Goals' },
    { num: 3, id: '03', label: 'Risk' },
    { num: 4, id: '04', label: 'Review' },
  ];

  return (
    <div className="flex items-center gap-2 sm:gap-4 my-6">
      {steps.map((step, idx) => {
        const isCompleted = currentStep > step.num;
        const isActive = currentStep === step.num;

        return (
          <React.Fragment key={step.id}>
            <div 
              onClick={() => onStepClick && onStepClick(step.num)}
              className={`flex items-center gap-2 cursor-pointer transition-all ${
                isActive ? 'opacity-100 scale-105' : isCompleted ? 'opacity-90' : 'opacity-40'
              }`}
            >
              <div
                className={`w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all shadow-xs ${
                  isActive
                    ? 'bg-[#28B89A] text-white ring-4 ring-[#DDF7F0]'
                    : isCompleted
                    ? 'bg-[#092B49] text-white'
                    : 'bg-slate-200 text-slate-600'
                }`}
              >
                {isCompleted ? <Check className="w-3.5 h-3.5" /> : step.id}
              </div>
              <span
                className={`text-xs sm:text-sm font-medium ${
                  isActive ? 'text-[#092B49] font-semibold' : 'text-[#64748B]'
                }`}
              >
                {step.label}
              </span>
            </div>

            {idx < steps.length - 1 && (
              <div
                className={`flex-1 h-0.5 min-w-[20px] max-w-[50px] transition-colors ${
                  currentStep > step.num ? 'bg-[#28B89A]' : 'bg-slate-200'
                }`}
              />
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};

