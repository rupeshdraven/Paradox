import React from 'react';
import { FinancialProvider, useFinancial } from './context/FinancialContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { ProfileOnboarding } from './components/ProfileOnboarding';
import { GoalsManager } from './components/GoalsManager';
import { RiskAssessment } from './components/RiskAssessment';
import { AnalysisReview } from './components/AnalysisReview';
import { RecommendedSchemes } from './components/RecommendedSchemes';
import { InvestmentPlan } from './components/InvestmentPlan';
import { Dashboard } from './components/Dashboard';
import { WhatIfSimulator } from './components/WhatIfSimulator';
import { LearnSection } from './components/LearnSection';
import { AICopilotModal } from './components/AICopilotModal';

const AppContent: React.FC = () => {
  const { currentPage } = useFinancial();

  const renderCurrentView = () => {
    switch (currentPage) {
      case 'onboarding-profile':
        return <ProfileOnboarding />;
      case 'onboarding-goals':
        return <GoalsManager />;
      case 'onboarding-risk':
        return <RiskAssessment />;
      case 'onboarding-review':
        return <AnalysisReview />;
      case 'recommendations':
        return <RecommendedSchemes />;
      case 'plan':
        return <InvestmentPlan />;
      case 'insights':
        return <WhatIfSimulator />;
      case 'learn':
        return <LearnSection />;
      case 'dashboard':
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#F8FBFC] text-[#102A43]">
      <Navbar />
      <main className="flex-1">
        {renderCurrentView()}
      </main>
      <Footer />
      {/* AI Financial Copilot Dialog */}
      <AICopilotModal />
    </div>
  );
};

export default function App() {
  return (
    <FinancialProvider>
      <AppContent />
    </FinancialProvider>
  );
}
