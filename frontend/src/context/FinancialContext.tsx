import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserProfile, Goal, FinancialAnalysis, InvestmentScheme, PortfolioAllocation, AICopilotResponse } from '../types';
import { api } from '../services/api';

export type AppPage = 
  | 'onboarding-profile' 
  | 'onboarding-goals' 
  | 'onboarding-risk' 
  | 'onboarding-review' 
  | 'recommendations' 
  | 'plan' 
  | 'dashboard' 
  | 'insights' 
  | 'learn';

interface ChatMessage {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  response?: AICopilotResponse;
  timestamp: string;
}

interface FinancialContextType {
  currentPage: AppPage;
  setCurrentPage: (page: AppPage) => void;
  profile: UserProfile;
  setProfile: (profile: UserProfile) => void;
  goals: Goal[];
  setGoals: (goals: Goal[]) => void;
  analysis: FinancialAnalysis | null;
  recommendations: InvestmentScheme[];
  selectedScheme: InvestmentScheme | null;
  setSelectedScheme: (scheme: InvestmentScheme | null) => void;
  portfolioPlan: PortfolioAllocation | null;
  chatMessages: ChatMessage[];
  isChatOpen: boolean;
  setIsChatOpen: (open: boolean) => void;
  isAiLoading: boolean;
  activeRiskScore: number;
  setActiveRiskScore: (score: number) => void;
  riskCategory: string;
  setRiskCategory: (cat: string) => void;
  saveUserProfile: (p: UserProfile) => Promise<void>;
  addGoal: (g: Goal) => Promise<void>;
  removeGoal: (id: string) => Promise<void>;
  submitRiskQuiz: (answers: Array<{ question_id: number; selected_option_index: number; points: number }>) => Promise<{ risk_score: number; risk_category: string; explanation: string }>;
  refreshAnalysisAndRecs: () => Promise<void>;
  resetToDemo: () => Promise<void>;
  sendChatMessage: (msg: string) => Promise<void>;
  notification: string | null;
  showNotification: (msg: string) => void;
}

const FinancialContext = createContext<FinancialContextType | undefined>(undefined);

export const FinancialProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentPage, setCurrentPage] = useState<AppPage>('dashboard');
  const [profile, setProfile] = useState<UserProfile>({
    id: 'user_default',
    name: 'Rupesh',
    age: 21,
    annual_income_range: '₹5–10 Lakh',
    annual_income: 600000,
    monthly_expenses_range: '₹25,000–₹50,000',
    monthly_expenses: 30000,
    investment_goal: 'Wealth Creation',
    investment_horizon: '5–10 years',
    risk_appetite: 'Moderate',
    existing_investments_liabilities: 'Mutual Funds: ₹60,000, Bank FD: ₹40,000',
    existing_savings: 100000,
    total_debt: 0,
    risk_score: 67,
    risk_category: 'Moderate',
  });

  const [goals, setGoals] = useState<Goal[]>([]);
  const [analysis, setAnalysis] = useState<FinancialAnalysis | null>(null);
  const [recommendations, setRecommendations] = useState<InvestmentScheme[]>([]);
  const [selectedScheme, setSelectedScheme] = useState<InvestmentScheme | null>(null);
  const [portfolioPlan, setPortfolioPlan] = useState<PortfolioAllocation | null>(null);
  const [activeRiskScore, setActiveRiskScore] = useState<number>(67);
  const [riskCategory, setRiskCategory] = useState<string>('Moderate');
  const [isChatOpen, setIsChatOpen] = useState<boolean>(false);
  const [isAiLoading, setIsAiLoading] = useState<boolean>(false);
  const [notification, setNotification] = useState<string | null>(null);

  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'ai',
      text: 'Hello Rupesh! I am your FinWise AI financial copilot. Ask me questions about your affordability, investments, goal timelines, or health score.',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);

  const showNotification = (msg: string) => {
    setNotification(msg);
    setTimeout(() => setNotification(null), 4000);
  };

  const refreshAnalysisAndRecs = async () => {
    try {
      const [p, g, a, r, plan] = await Promise.all([
        api.getProfile(),
        api.getGoals(),
        api.getAnalysis(),
        api.getRecommendations(),
        api.getPortfolioPlan(),
      ]);
      setProfile(p);
      setGoals(g);
      setAnalysis(a);
      setRecommendations(r);
      setPortfolioPlan(plan);
      setActiveRiskScore(p.risk_score || 67);
      setRiskCategory(p.risk_category || 'Moderate');
    } catch (err) {
      console.error('Error refreshing financial telemetry', err);
    }
  };

  useEffect(() => {
    refreshAnalysisAndRecs();
  }, []);

  const saveUserProfile = async (updated: UserProfile) => {
    setProfile(updated);
    await api.updateProfile(updated);
    await refreshAnalysisAndRecs();
    showNotification('Investor profile updated successfully');
  };

  const addGoal = async (g: Goal) => {
    const saved = await api.saveGoal(g);
    setGoals((prev) => [...prev.filter((item) => item.id !== g.id), saved]);
    await refreshAnalysisAndRecs();
    showNotification(`Goal '${g.name}' saved!`);
  };

  const removeGoal = async (id: string) => {
    await api.deleteGoal(id);
    setGoals((prev) => prev.filter((item) => item.id !== id));
    await refreshAnalysisAndRecs();
    showNotification('Goal removed');
  };

  const submitRiskQuiz = async (answers: Array<{ question_id: number; selected_option_index: number; points: number }>) => {
    const result = await api.evaluateRisk(answers);
    setActiveRiskScore(result.risk_score);
    setRiskCategory(result.risk_category);
    await refreshAnalysisAndRecs();
    showNotification(`Risk profile assessed: ${result.risk_category} (${result.risk_score}/100)`);
    return result;
  };

  const resetToDemo = async () => {
    const demoProf = await api.resetDemo();
    setProfile(demoProf);
    await refreshAnalysisAndRecs();
    setCurrentPage('dashboard');
    showNotification('Demo loaded: Rupesh (21 yrs, ₹6L income, Moderate risk)');
  };

  const sendChatMessage = async (msg: string) => {
    if (!msg.trim()) return;
    const userMsg: ChatMessage = {
      id: `msg-${Date.now()}`,
      sender: 'user',
      text: msg,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    setChatMessages((prev) => [...prev, userMsg]);
    setIsAiLoading(true);

    try {
      const resp = await api.askCopilot(msg, profile, goals, analysis || undefined);
      const aiMsg: ChatMessage = {
        id: `ai-${Date.now()}`,
        sender: 'ai',
        text: resp.short_answer,
        response: resp,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setChatMessages((prev) => [...prev, aiMsg]);
    } catch {
      showNotification('AI response temporarily unavailable');
    } finally {
      setIsAiLoading(false);
    }
  };

  return (
    <FinancialContext.Provider
      value={{
        currentPage,
        setCurrentPage,
        profile,
        setProfile,
        goals,
        setGoals,
        analysis,
        recommendations,
        selectedScheme,
        setSelectedScheme,
        portfolioPlan,
        chatMessages,
        isChatOpen,
        setIsChatOpen,
        isAiLoading,
        activeRiskScore,
        setActiveRiskScore,
        riskCategory,
        setRiskCategory,
        saveUserProfile,
        addGoal,
        removeGoal,
        submitRiskQuiz,
        refreshAnalysisAndRecs,
        resetToDemo,
        sendChatMessage,
        notification,
        showNotification,
      }}
    >
      {children}
    </FinancialContext.Provider>
  );
};

export const useFinancial = () => {
  const context = useContext(FinancialContext);
  if (!context) throw new Error('useFinancial must be used within FinancialProvider');
  return context;
};

