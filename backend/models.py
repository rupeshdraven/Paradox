import os
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class UserProfile(BaseModel):
    id: str = "user_default"
    name: str = "Rupesh"
    age: int = 21
    annual_income_range: str = "₹5–10 Lakh"
    annual_income: float = 600000.0
    monthly_expenses_range: str = "₹25,000–₹50,000"
    monthly_expenses: float = 30000.0
    investment_goal: str = "Wealth Creation"
    investment_horizon: str = "5–10 years"
    risk_appetite: str = "Moderate"
    existing_investments_liabilities: str = "Mutual Funds: ₹60,000, Bank FD: ₹40,000, No active loans"
    existing_savings: float = 100000.0
    total_debt: float = 0.0
    risk_score: int = 67
    risk_category: str = "Moderate"

class Goal(BaseModel):
    id: str
    user_id: str = "user_default"
    name: str
    target_amount: float
    current_amount: float = 0.0
    target_months: int = 60
    priority: str = "Medium"  # High, Medium, Low
    category: Optional[str] = "General"
    amount_remaining: Optional[float] = 0.0
    required_monthly_saving: Optional[float] = 0.0
    progress_percentage: Optional[float] = 0.0

class RiskAnswer(BaseModel):
    question_id: int
    selected_option_index: int
    points: int

class RiskAssessmentSubmission(BaseModel):
    answers: List[RiskAnswer]

class FinancialAnalysis(BaseModel):
    monthly_income: float
    monthly_expenses: float
    monthly_surplus: float
    savings_rate_pct: float
    emergency_fund_months: float
    emergency_fund_status: str
    debt_to_income_pct: float
    total_goals_target: float
    total_goals_saved: float
    total_monthly_saving_required: float
    surplus_coverage_ratio: float
    financial_health_score: int
    health_score_breakdown: Dict[str, int]
    health_status: str
    key_observations: List[str]

class InvestmentScheme(BaseModel):
    id: str
    name: str
    provider: str
    category: str  # "Mutual Funds", "Government Schemes", "Fixed Income", "Tax Saving", "Retirement", "Others"
    risk_level: str  # "Very Low", "Low", "Moderate", "High", "Very High"
    indicative_return: str  # e.g., "10–12% p.a."
    indicative_rate_num: float  # e.g. 11.0
    min_investment: str  # e.g., "₹500"
    min_investment_num: float
    time_horizon_min_years: int
    time_horizon_ideal: str
    tax_benefit: bool
    tax_section: Optional[str] = None
    lock_in_period: Optional[str] = None
    liquidity: str  # "High", "Moderate", "Low"
    best_for: str
    description: str
    badge: Optional[str] = None  # "Highly Recommended", "Tax Benefits", "Stable Returns", etc.
    suitability_score: Optional[int] = None
    suitability_tier: Optional[str] = None  # "Highly Suitable", "Moderately Suitable", "Less Suitable"
    score_breakdown: Optional[Dict[str, int]] = None
    why_recommended: Optional[List[str]] = None
    things_to_consider: Optional[List[str]] = None
    source_evidence: Optional[Dict[str, str]] = None

class PortfolioAllocation(BaseModel):
    growth_equity_pct: int
    stable_debt_pct: int
    government_schemes_pct: int
    emergency_reserve_pct: int
    monthly_allocation_plan: Dict[str, float]
    rationale: str
    guardrail_status: str

class WhatIfRequest(BaseModel):
    current_income: float
    current_expenses: float
    current_investment: float
    goal_amount: float
    current_savings: float = 0.0
    expected_annual_return_pct: float = 10.0
    new_income: Optional[float] = None
    new_expenses: Optional[float] = None
    new_monthly_investment: Optional[float] = None

class WhatIfResponse(BaseModel):
    before_months: int
    after_months: int
    months_saved: int
    before_total_invested: float
    after_total_invested: float
    before_future_value: float
    after_future_value: float
    timeline_comparison: List[Dict[str, Any]]
    insights: List[str]

class AICopilotQuery(BaseModel):
    query: str
    profile: Optional[UserProfile] = None
    goals: Optional[List[Goal]] = None
    financial_analysis: Optional[FinancialAnalysis] = None

class AICopilotResponse(BaseModel):
    guardrail_status: str  # "ALLOW", "WARN", "BLOCK", "REQUEST_INFO"
    short_answer: str
    why: List[str]
    better_option: str
    impact: Dict[str, Any]
    checks_applied: List[str]
    evidence_citation: Optional[str] = None
    timestamp: str

