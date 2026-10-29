import math
from typing import List, Dict, Any, Tuple
from ..models import UserProfile, Goal, FinancialAnalysis

INCOME_MAP = {
    "Below ₹3 Lakh": 250000.0,
    "₹3–5 Lakh": 400000.0,
    "₹5–10 Lakh": 600000.0,
    "₹6–10 Lakh": 600000.0,
    "₹10–20 Lakh": 1400000.0,
    "₹20–50 Lakh": 3000000.0,
    "Above ₹50 Lakh": 6000000.0
}

EXPENSE_MAP = {
    "Below ₹10,000": 8000.0,
    "₹10,000–₹25,000": 18000.0,
    "₹25,000–₹50,000": 30000.0,
    "₹50,000–₹1 Lakh": 65000.0,
    "Above ₹1 Lakh": 120000.0
}

def resolve_monthly_income(profile: UserProfile) -> float:
    if profile.annual_income > 0:
        return profile.annual_income / 12.0
    return INCOME_MAP.get(profile.annual_income_range, 50000.0) / 12.0

def resolve_monthly_expenses(profile: UserProfile) -> float:
    if profile.monthly_expenses > 0:
        return profile.monthly_expenses
    return EXPENSE_MAP.get(profile.monthly_expenses_range, 30000.0)

def calculate_goal_metrics(goal: Goal) -> Goal:
    remaining = max(0.0, goal.target_amount - goal.current_amount)
    months = max(1, goal.target_months)
    monthly_req = remaining / months
    pct = min(100.0, round((goal.current_amount / max(1.0, goal.target_amount)) * 100.0, 1))
    
    goal.amount_remaining = round(remaining, 2)
    goal.required_monthly_saving = round(monthly_req, 2)
    goal.progress_percentage = pct
    return goal

def analyze_finances(profile: UserProfile, goals: List[Goal]) -> FinancialAnalysis:
    monthly_inc = resolve_monthly_income(profile)
    monthly_exp = resolve_monthly_expenses(profile)
    monthly_surplus = max(0.0, monthly_inc - monthly_exp)
    savings_rate = (monthly_surplus / max(1.0, monthly_inc)) * 100.0
    
    # Existing savings & emergency coverage
    savings = profile.existing_savings
    if savings <= 0 and "₹" in profile.existing_investments_liabilities:
        # fallback default
        savings = 100000.0
    
    emergency_months = round(savings / max(1000.0, monthly_exp), 1)
    
    if emergency_months >= 6:
        emergency_status = "Optimal (6+ months)"
    elif emergency_months >= 3:
        emergency_status = "Moderate (3-6 months)"
    else:
        emergency_status = "Underfunded (<3 months)"
        
    debt_payments = profile.total_debt * 0.03 if profile.total_debt > 0 else 0.0
    dti = (debt_payments / max(1.0, monthly_inc)) * 100.0
    
    # Process goals
    total_target = sum(g.target_amount for g in goals)
    total_saved = sum(g.current_amount for g in goals)
    total_monthly_req = sum(calculate_goal_metrics(g).required_monthly_saving for g in goals)
    
    surplus_coverage = (monthly_surplus / max(1.0, total_monthly_req)) if total_monthly_req > 0 else 1.5
    
    # Calculate health score components (0-100 total)
    # 1. Savings Score (20 max)
    if savings_rate >= 40:
        score_savings = 20
    elif savings_rate >= 25:
        score_savings = 17
    elif savings_rate >= 15:
        score_savings = 13
    elif savings_rate > 0:
        score_savings = 8
    else:
        score_savings = 3
        
    # 2. Expenses Score (20 max)
    exp_ratio = (monthly_exp / max(1.0, monthly_inc)) * 100.0
    if exp_ratio <= 50:
        score_expenses = 20
    elif exp_ratio <= 65:
        score_expenses = 16
    elif exp_ratio <= 80:
        score_expenses = 11
    else:
        score_expenses = 5
        
    # 3. Emergency Cushion (20 max)
    if emergency_months >= 6:
        score_emergency = 20
    elif emergency_months >= 4:
        score_emergency = 16
    elif emergency_months >= 2:
        score_emergency = 12
    else:
        score_emergency = 6
        
    # 4. Debt Management (20 max)
    if dti == 0:
        score_debt = 20
    elif dti <= 15:
        score_debt = 16
    elif dti <= 35:
        score_debt = 11
    else:
        score_debt = 5
        
    # 5. Goal Feasibility (20 max)
    if surplus_coverage >= 1.2:
        score_goals = 20
    elif surplus_coverage >= 0.9:
        score_goals = 16
    elif surplus_coverage >= 0.6:
        score_goals = 12
    else:
        score_goals = 7
        
    total_score = score_savings + score_expenses + score_emergency + score_debt + score_goals
    # Scale to 0-100
    total_score = max(10, min(98, total_score))
    
    if total_score >= 80:
        health_status = "Excellent"
    elif total_score >= 68:
        health_status = "Healthy"
    elif total_score >= 50:
        health_status = "Fair"
    else:
        health_status = "Needs Attention"
        
    observations = []
    if savings_rate >= 30:
        observations.append(f"Strong savings discipline with a {round(savings_rate)}% monthly surplus rate.")
    else:
        observations.append(f"Current savings rate is {round(savings_rate)}%; target 30%+ for accelerated wealth creation.")
        
    if emergency_months >= 3:
        observations.append(f"Emergency cushion covers ~{emergency_months} months of mandatory living expenses.")
    else:
        observations.append(f"Emergency reserve is at {emergency_months} months; consider topping up to at least 3-6 months.")
        
    if surplus_coverage >= 1.0:
        observations.append(f"Your monthly surplus (₹{int(monthly_surplus):,}) adequately supports planned goal contributions.")
    else:
        observations.append(f"Goal funding targets (₹{int(total_monthly_req):,}/mo) exceed current surplus; recommend priority sequencing.")

    return FinancialAnalysis(
        monthly_income=round(monthly_inc, 2),
        monthly_expenses=round(monthly_exp, 2),
        monthly_surplus=round(monthly_surplus, 2),
        savings_rate_pct=round(savings_rate, 1),
        emergency_fund_months=emergency_months,
        emergency_fund_status=emergency_status,
        debt_to_income_pct=round(dti, 1),
        total_goals_target=round(total_target, 2),
        total_goals_saved=round(total_saved, 2),
        total_monthly_saving_required=round(total_monthly_req, 2),
        surplus_coverage_ratio=round(surplus_coverage, 2),
        financial_health_score=total_score,
        health_score_breakdown={
            "savings": score_savings * 5,     # out of 100
            "expenses": score_expenses * 5,
            "emergency": score_emergency * 5,
            "debt": score_debt * 5,
            "goals": score_goals * 5,
        },
        health_status=health_status,
        key_observations=observations
    )

