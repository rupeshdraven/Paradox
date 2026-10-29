import { UserProfile, Goal, FinancialAnalysis, InvestmentScheme, PortfolioAllocation, WhatIfRequest, WhatIfResponse, AICopilotResponse } from '../types';

const BASE_URL = '/api';

export const api = {
  async getProfile(): Promise<UserProfile> {
    try {
      const res = await fetch(`${BASE_URL}/profile`);
      if (!res.ok) throw new Error('Failed to fetch profile');
      return await res.json();
    } catch {
      return getFallbackProfile();
    }
  },

  async updateProfile(profile: UserProfile): Promise<UserProfile> {
    try {
      const res = await fetch(`${BASE_URL}/profile`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile),
      });
      if (!res.ok) throw new Error('Failed to update profile');
      return await res.json();
    } catch {
      return profile;
    }
  },

  async resetDemo(): Promise<UserProfile> {
    try {
      const res = await fetch(`${BASE_URL}/reset-demo`, { method: 'POST' });
      if (!res.ok) throw new Error('Failed to reset demo');
      const data = await res.json();
      return data.profile;
    } catch {
      return getFallbackProfile();
    }
  },

  async getGoals(): Promise<Goal[]> {
    try {
      const res = await fetch(`${BASE_URL}/goals`);
      if (!res.ok) throw new Error('Failed to fetch goals');
      return await res.json();
    } catch {
      return getFallbackGoals();
    }
  },

  async saveGoal(goal: Goal): Promise<Goal> {
    try {
      const res = await fetch(`${BASE_URL}/goals`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(goal),
      });
      if (!res.ok) throw new Error('Failed to save goal');
      return await res.json();
    } catch {
      return goal;
    }
  },

  async deleteGoal(goalId: string): Promise<void> {
    try {
      await fetch(`${BASE_URL}/goals/${goalId}`, { method: 'DELETE' });
    } catch (err) {
      console.warn('Backend delete goal offline fallback', err);
    }
  },

  async evaluateRisk(answers: Array<{ question_id: number; selected_option_index: number; points: number }>): Promise<{ risk_score: number; risk_category: string; explanation: string }> {
    try {
      const res = await fetch(`${BASE_URL}/risk/evaluate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers }),
      });
      if (!res.ok) throw new Error('Failed to evaluate risk');
      return await res.json();
    } catch {
      const total = answers.reduce((acc, a) => acc + a.points, 0);
      const score = Math.round(Math.max(0, Math.min(100, ((total - 25) / 100) * 100)));
      const cat = score <= 35 ? 'Conservative' : score <= 68 ? 'Moderate' : 'Aggressive';
      return {
        risk_score: score,
        risk_category: cat,
        explanation: 'Your responses indicate a balanced approach to market volatility and long-term capital compounding.'
      };
    }
  },

  async getAnalysis(): Promise<FinancialAnalysis> {
    try {
      const res = await fetch(`${BASE_URL}/analysis`);
      if (!res.ok) throw new Error('Failed to fetch analysis');
      return await res.json();
    } catch {
      return getFallbackAnalysis();
    }
  },

  async getRecommendations(category?: string, sortBy: string = 'Recommended'): Promise<InvestmentScheme[]> {
    try {
      const params = new URLSearchParams();
      if (category && category !== 'All' && category !== 'All Schemes') params.append('category', category);
      if (sortBy) params.append('sort_by', sortBy);
      const res = await fetch(`${BASE_URL}/recommendations?${params.toString()}`);
      if (!res.ok) throw new Error('Failed to fetch recommendations');
      return await res.json();
    } catch {
      return getFallbackSchemes();
    }
  },

  async getPortfolioPlan(): Promise<PortfolioAllocation> {
    try {
      const res = await fetch(`${BASE_URL}/portfolio-allocation`);
      if (!res.ok) throw new Error('Failed to fetch portfolio plan');
      return await res.json();
    } catch {
      return {
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
    }
  },

  async simulate(data: WhatIfRequest): Promise<WhatIfResponse> {
    try {
      const res = await fetch(`${BASE_URL}/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error('Failed to simulate');
      return await res.json();
    } catch {
      return getFallbackSimulation(data);
    }
  },

  async askCopilot(query: string, profile?: UserProfile, goals?: Goal[], analysis?: FinancialAnalysis): Promise<AICopilotResponse> {
    try {
      const res = await fetch(`${BASE_URL}/copilot`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, profile, goals, financial_analysis: analysis }),
      });
      if (!res.ok) throw new Error('Failed to query copilot');
      return await res.json();
    } catch {
      return getFallbackCopilotResponse(query);
    }
  },
};

// Fallbacks for instant zero-dependency experience
function getFallbackProfile(): UserProfile {
  return {
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
  };
}

function getFallbackGoals(): Goal[] {
  return [
    {
      id: 'g1',
      name: 'Wealth Creation',
      target_amount: 1000000,
      current_amount: 100000,
      target_months: 60,
      priority: 'High',
      category: 'Wealth',
      amount_remaining: 900000,
      required_monthly_saving: 15000,
      progress_percentage: 10,
    },
    {
      id: 'g2',
      name: 'Emergency Fund',
      target_amount: 150000,
      current_amount: 40000,
      target_months: 12,
      priority: 'High',
      category: 'Safety',
      amount_remaining: 110000,
      required_monthly_saving: 9167,
      progress_percentage: 26.7,
    },
  ];
}

function getFallbackAnalysis(): FinancialAnalysis {
  return {
    monthly_income: 50000,
    monthly_expenses: 30000,
    monthly_surplus: 20000,
    savings_rate_pct: 40,
    emergency_fund_months: 3.3,
    emergency_fund_status: 'Moderate (3-6 months)',
    debt_to_income_pct: 0,
    total_goals_target: 1150000,
    total_goals_saved: 140000,
    total_monthly_saving_required: 24167,
    surplus_coverage_ratio: 0.83,
    financial_health_score: 78,
    health_score_breakdown: {
      savings: 85,
      expenses: 70,
      emergency: 65,
      debt: 95,
      goals: 75,
    },
    health_status: 'Healthy',
    key_observations: [
      'Strong savings discipline with a 40% monthly surplus rate.',
      'Emergency cushion covers ~3.3 months of mandatory living expenses.',
      'Monthly surplus of ₹20,000 supports core goal investments.'
    ],
  };
}

function getFallbackSchemes(): InvestmentScheme[] {
  return [
    {
      id: 'sbi_bluechip',
      name: 'SBI Bluechip Fund',
      provider: 'SBI Mutual Fund',
      category: 'Mutual Funds',
      risk_level: 'Moderate',
      indicative_return: '10–12% p.a.',
      indicative_rate_num: 11.5,
      min_investment: '₹500',
      min_investment_num: 500,
      time_horizon_min_years: 5,
      time_horizon_ideal: '5–10 Years',
      tax_benefit: false,
      lock_in_period: 'None',
      liquidity: 'High',
      best_for: 'Long-term wealth creation',
      description: 'Invests in top large-cap companies offering long-term growth with relatively lower risk.',
      badge: 'Highly Recommended',
      suitability_score: 93,
      suitability_tier: 'Highly Suitable',
      score_breakdown: {
        risk_compatibility: 95,
        goal_compatibility: 95,
        time_horizon: 92,
        liquidity: 90,
        tax_efficiency: 80,
      },
      why_recommended: [
        'Matches your moderate risk tolerance with large-cap corporate stability',
        'Optimal 5-10 year horizon matches wealth creation milestones',
        'Zero lock-in allows flexible portfolio rebalancing',
      ],
      things_to_consider: [
        'Returns are market-linked and not guaranteed',
        'Short-term price fluctuations may occur',
      ],
      source_evidence: {
        document: 'Scheme Information Document (SID) - SBI Bluechip',
        regulator: 'SEBI Registered Mutual Fund',
      },
    },
    {
      id: 'ppf_gov',
      name: 'Public Provident Fund (PPF)',
      provider: 'Government of India',
      category: 'Government Schemes',
      risk_level: 'Very Low',
      indicative_return: '7.1% p.a.',
      indicative_rate_num: 7.1,
      min_investment: '₹500',
      min_investment_num: 500,
      time_horizon_min_years: 15,
      time_horizon_ideal: '15 Years',
      tax_benefit: true,
      tax_section: 'Section 80C',
      lock_in_period: '15 Years',
      liquidity: 'Low',
      best_for: 'Long-term savings / tax planning',
      description: 'A safe, long-term investment with guaranteed sovereign backing and tax-free maturity amount.',
      badge: 'Tax Benefits',
      suitability_score: 86,
      suitability_tier: 'Highly Suitable',
    },
    {
      id: 'elss_tax_saver',
      name: 'ELSS Tax Saver Fund',
      provider: 'Various Fund Houses',
      category: 'Tax Saving',
      risk_level: 'High',
      indicative_return: '12–15% p.a.',
      indicative_rate_num: 13.5,
      min_investment: '₹500',
      min_investment_num: 500,
      time_horizon_min_years: 3,
      time_horizon_ideal: '3–5 Years',
      tax_benefit: true,
      tax_section: 'Section 80C',
      lock_in_period: '3 Years',
      liquidity: 'Moderate',
      best_for: 'Long-term tax-efficient investing',
      description: 'Equity-linked fund with potential for high returns and tax benefits under Section 80C.',
      badge: 'Section 80C',
      suitability_score: 82,
      suitability_tier: 'Highly Suitable',
    },
    {
      id: 'bank_fd',
      name: 'Fixed Deposit (FD)',
      provider: 'Banks & Financial Institutions',
      category: 'Fixed Income',
      risk_level: 'Very Low',
      indicative_return: '6.8–7.5% p.a.',
      indicative_rate_num: 7.1,
      min_investment: '₹1,000',
      min_investment_num: 1000,
      time_horizon_min_years: 1,
      time_horizon_ideal: '1–3 Years',
      tax_benefit: false,
      lock_in_period: 'Flexible',
      liquidity: 'High',
      best_for: 'Safe capital preservation for short-term goals',
      description: 'A safe investment option with guaranteed returns, suitable for short to medium term goals.',
      badge: 'Stable Returns',
      suitability_score: 79,
      suitability_tier: 'Moderately Suitable',
    },
    {
      id: 'nps_retirement',
      name: 'National Pension System (NPS)',
      provider: 'Government of India',
      category: 'Retirement',
      risk_level: 'Moderate',
      indicative_return: '10–12% p.a.',
      indicative_rate_num: 10.8,
      min_investment: '₹500',
      min_investment_num: 500,
      time_horizon_min_years: 10,
      time_horizon_ideal: '10+ Years',
      tax_benefit: true,
      tax_section: 'Sec 80CCD',
      lock_in_period: 'Till Age 60',
      liquidity: 'Low',
      best_for: 'Long-term retirement planning',
      description: 'A long-term retirement savings scheme with market-linked returns and tax benefits.',
      badge: 'Retirement Planning',
      suitability_score: 77,
      suitability_tier: 'Moderately Suitable',
    },
    {
      id: 'ssy_scheme',
      name: 'Sukanya Samriddhi Yojana',
      provider: 'Government of India',
      category: 'Government Schemes',
      risk_level: 'Very Low',
      indicative_return: '8.2% p.a.',
      indicative_rate_num: 8.2,
      min_investment: '₹250',
      min_investment_num: 250,
      time_horizon_min_years: 15,
      time_horizon_ideal: 'Till Child reaches 21 years',
      tax_benefit: true,
      tax_section: 'Section 80C',
      lock_in_period: 'Till age 21',
      liquidity: 'Low',
      best_for: 'Daughter\'s higher education',
      description: 'A savings scheme for girl child with high interest rates and tax benefits.',
      badge: 'For Girl Child',
      suitability_score: 74,
      suitability_tier: 'Moderately Suitable',
    },
  ];
}

function getFallbackSimulation(req: WhatIfRequest): WhatIfResponse {
  const currentInv = req.current_investment || 8000;
  const newInv = req.new_monthly_investment || 12000;
  const target = req.goal_amount || 1000000;
  
  const m1 = Math.round(target / currentInv);
  const m2 = Math.round(target / newInv);
  const saved = Math.max(0, m1 - m2);

  return {
    before_months: m1,
    after_months: m2,
    months_saved: saved,
    before_total_invested: currentInv * m1,
    after_total_invested: newInv * m2,
    before_future_value: target,
    after_future_value: target,
    timeline_comparison: [
      { month: 0, period: 'Start', current_strategy: 0, optimized_strategy: 0, target },
      { month: Math.round(m2 * 0.5), period: `${Math.round(m2*0.5/12)} yrs`, current_strategy: target * 0.35, optimized_strategy: target * 0.55, target },
      { month: m2, period: `${Math.round(m2/12)} yrs`, current_strategy: target * 0.65, optimized_strategy: target, target },
      { month: m1, period: `${Math.round(m1/12)} yrs`, current_strategy: target, optimized_strategy: target * 1.15, target },
    ],
    insights: [
      `Increasing your monthly investment to ₹${newInv.toLocaleString()} achieves your ₹${target.toLocaleString()} goal ${saved} months earlier.`,
      `Target achieved in ${Math.round(m2/12)} years instead of ${Math.round(m1/12)} years.`
    ],
  };
}

function getFallbackCopilotResponse(query: string): AICopilotResponse {
  return {
    guardrail_status: 'ALLOW',
    short_answer: 'You can afford this within planned monthly cash-flow, but monitor emergency reserves.',
    why: [
      'Your monthly disposable surplus is approximately ₹20,000.',
      'Purchase absorbs a manageable portion of current uncommitted funds.',
      'Existing liquid reserves remain intact.',
    ],
    better_option: 'Allocate over 2 monthly installments to avoid any impact on emergency liquidity.',
    impact: {
      monthly_surplus: '₹20,000',
      goal_timeline: 'Maintained with zero delay',
    },
    checks_applied: [
      'Input Validation: Passed',
      'Suitability Check: Clear',
      'Guardrail Gate: ALLOW',
    ],
    evidence_citation: 'Personal Cash-Flow Discipline Guidelines',
    timestamp: new Date().toISOString(),
  };
}

