export interface UserProfile {
  id: string;
  name: string;
  age: number;
  annual_income_range: string;
  annual_income: number;
  monthly_expenses_range: string;
  monthly_expenses: number;
  investment_goal: string;
  investment_horizon: string;
  risk_appetite: string;
  existing_investments_liabilities: string;
  existing_savings: number;
  total_debt: number;
  risk_score: number;
  risk_category: string;
}

export interface Goal {
  id: string;
  user_id?: string;
  name: string;
  target_amount: number;
  current_amount: number;
  target_months: number;
  priority: 'High' | 'Medium' | 'Low';
  category?: string;
  amount_remaining?: number;
  required_monthly_saving?: number;
  progress_percentage?: number;
}

export interface FinancialAnalysis {
  monthly_income: number;
  monthly_expenses: number;
  monthly_surplus: number;
  savings_rate_pct: number;
  emergency_fund_months: number;
  emergency_fund_status: string;
  debt_to_income_pct: number;
  total_goals_target: number;
  total_goals_saved: number;
  total_monthly_saving_required: number;
  surplus_coverage_ratio: number;
  financial_health_score: number;
  health_score_breakdown: {
    savings: number;
    expenses: number;
    emergency: number;
    debt: number;
    goals: number;
  };
  health_status: string;
  key_observations: string[];
}

export interface InvestmentScheme {
  id: string;
  name: string;
  provider: string;
  category: string;
  risk_level: string;
  indicative_return: string;
  indicative_rate_num: number;
  min_investment: string;
  min_investment_num: number;
  time_horizon_min_years: number;
  time_horizon_ideal: string;
  tax_benefit: boolean;
  tax_section?: string;
  lock_in_period?: string;
  liquidity: string;
  best_for: string;
  description: string;
  badge?: string;
  suitability_score?: number;
  suitability_tier?: string;
  score_breakdown?: {
    risk_compatibility: number;
    goal_compatibility: number;
    time_horizon: number;
    liquidity: number;
    tax_efficiency: number;
  };
  why_recommended?: string[];
  things_to_consider?: string[];
  source_evidence?: Record<string, string>;
}

export interface PortfolioAllocation {
  growth_equity_pct: number;
  stable_debt_pct: number;
  government_schemes_pct: number;
  emergency_reserve_pct: number;
  monthly_allocation_plan: Record<string, number>;
  rationale: string;
  guardrail_status: string;
}

export interface WhatIfRequest {
  current_income: number;
  current_expenses: number;
  current_investment: number;
  goal_amount: number;
  current_savings?: number;
  expected_annual_return_pct?: number;
  new_income?: number;
  new_expenses?: number;
  new_monthly_investment?: number;
}

export interface WhatIfResponse {
  before_months: number;
  after_months: number;
  months_saved: number;
  before_total_invested: number;
  after_total_invested: number;
  before_future_value: number;
  after_future_value: number;
  timeline_comparison: Array<{
    month: number;
    period: string;
    current_strategy: number;
    optimized_strategy: number;
    target: number;
  }>;
  insights: string[];
}

export interface AICopilotResponse {
  guardrail_status: 'ALLOW' | 'WARN' | 'BLOCK' | 'REQUEST_INFO';
  short_answer: string;
  why: string[];
  better_option: string;
  impact: Record<string, any>;
  checks_applied: string[];
  evidence_citation?: string;
  timestamp: string;
}

