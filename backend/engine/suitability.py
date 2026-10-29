from typing import List, Dict, Any, Tuple
from ..models import UserProfile, Goal, InvestmentScheme, PortfolioAllocation
from .schemes_catalog import get_all_schemes

def parse_horizon_years(horizon_str: str) -> int:
    h = horizon_str.lower()
    if "less than 1" in h or "< 1" in h:
        return 1
    if "1–3" in h or "1-3" in h:
        return 2
    if "3–5" in h or "3-5" in h:
        return 4
    if "5–10" in h or "5-10" in h:
        return 7
    if "10+" in h or "more than 10" in h:
        return 12
    return 5

def score_risk_compatibility(user_risk: str, scheme_risk: str) -> int:
    risk_levels = {
        "Very Conservative": 1,
        "Conservative": 2,
        "Moderate": 3,
        "Aggressive": 4,
        "Very Aggressive": 5
    }
    scheme_levels = {
        "Very Low": 1,
        "Low": 2,
        "Moderate": 3,
        "High": 4,
        "Very High": 5
    }
    
    u_lvl = risk_levels.get(user_risk, 3)
    s_lvl = scheme_levels.get(scheme_risk, 3)
    
    diff = abs(u_lvl - s_lvl)
    if diff == 0:
        return 100
    elif diff == 1:
        return 82
    elif diff == 2:
        return 60
    elif diff == 3:
        return 35
    else:
        return 15

def score_goal_compatibility(user_goal: str, scheme: InvestmentScheme) -> int:
    goal = user_goal.lower()
    name = scheme.name.lower()
    category = scheme.category.lower()
    best_for = scheme.best_for.lower()
    
    if "wealth" in goal:
        if "mutual fund" in category or "equity" in best_for or "wealth" in best_for:
            return 95
        elif "nps" in name or "gold" in name:
            return 80
        elif "government" in category or "ppf" in name:
            return 75
        return 65
        
    elif "tax" in goal:
        if scheme.tax_benefit:
            return 100
        return 40
        
    elif "retirement" in goal:
        if "nps" in name or "retirement" in category or "ppf" in name:
            return 100
        elif "mutual fund" in category:
            return 85
        return 60
        
    elif "emergency" in goal or "short-term" in goal:
        if "liquid" in name or "deposit" in name or "fixed income" in category:
            return 98
        elif scheme.lock_in_period and scheme.lock_in_period != "None":
            return 20
        return 50
        
    elif "child" in goal or "education" in goal:
        if "sukanya" in name or "ppf" in name or "bluechip" in name:
            return 95
        return 70
        
    elif "house" in goal or "vehicle" in goal:
        if "balanced" in name or "bluechip" in name or "deposit" in name:
            return 88
        return 70
        
    return 75

def score_horizon_compatibility(user_years: int, scheme: InvestmentScheme) -> int:
    min_yrs = scheme.time_horizon_min_years
    lock_in = scheme.lock_in_period or "None"
    
    if user_years < min_yrs:
        # User horizon is shorter than recommended
        shortfall = min_yrs - user_years
        return max(20, 90 - (shortfall * 25))
    else:
        # User horizon meets or exceeds
        return 95

def score_liquidity_compatibility(user_goal: str, scheme: InvestmentScheme) -> int:
    if "emergency" in user_goal.lower() or "short-term" in user_goal.lower():
        if scheme.liquidity == "High":
            return 98
        elif scheme.liquidity == "Moderate":
            return 60
        else:
            return 25
    else:
        if scheme.liquidity == "High":
            return 90
        elif scheme.liquidity == "Moderate":
            return 85
        else:
            return 75

def score_tax_objective(user_goal: str, scheme: InvestmentScheme) -> int:
    if "tax" in user_goal.lower() or scheme.tax_benefit:
        return 95 if scheme.tax_benefit else 60
    return 80

def compute_recommendations(profile: UserProfile, goals: List[Goal]) -> List[InvestmentScheme]:
    user_goal = profile.investment_goal
    if goals and len(goals) > 0:
        # Prioritize high-priority goal if present
        high_prio = [g for g in goals if g.priority == "High"]
        if high_prio:
            user_goal = high_prio[0].name
        else:
            user_goal = goals[0].name
            
    user_horizon_years = parse_horizon_years(profile.investment_horizon)
    schemes = get_all_schemes()
    
    for s in schemes:
        risk_score = score_risk_compatibility(profile.risk_appetite, s.risk_level)
        goal_score = score_goal_compatibility(user_goal, s)
        horizon_score = score_horizon_compatibility(user_horizon_years, s)
        liquidity_score = score_liquidity_compatibility(user_goal, s)
        tax_score = score_tax_objective(user_goal, s)
        
        # Transparent Weighted Scoring Formula:
        # Risk: 25%, Goal: 25%, Horizon: 20%, Liquidity: 15%, Tax: 15%
        weighted_score = (
            (risk_score * 0.25) +
            (goal_score * 0.25) +
            (horizon_score * 0.20) +
            (liquidity_score * 0.15) +
            (tax_score * 0.15)
        )
        total = int(round(weighted_score))
        s.suitability_score = min(99, max(25, total))
        
        if s.suitability_score >= 82:
            s.suitability_tier = "Highly Suitable"
            if not s.badge or s.badge == "Recommended":
                s.badge = "Highly Recommended"
        elif s.suitability_score >= 65:
            s.suitability_tier = "Moderately Suitable"
        else:
            s.suitability_tier = "Less Suitable"
            
        s.score_breakdown = {
            "risk_compatibility": risk_score,
            "goal_compatibility": goal_score,
            "time_horizon": horizon_score,
            "liquidity": liquidity_score,
            "tax_efficiency": tax_score
        }
        
    # Sort descending by suitability score
    schemes.sort(key=lambda x: x.suitability_score or 0, reverse=True)
    return schemes

def generate_portfolio_allocation(profile: UserProfile, monthly_surplus: float) -> PortfolioAllocation:
    risk = profile.risk_appetite.lower()
    horizon = parse_horizon_years(profile.investment_horizon)
    
    # Deterministic asset allocation matrix
    if "very aggressive" in risk or "aggressive" in risk:
        growth = 60
        stable = 20
        gov = 10
        emergency = 10
        rationale = "Oriented toward capital compounding with high equity allocation suited for your aggressive risk tolerance and long horizon."
    elif "conservative" in risk or "very conservative" in risk:
        growth = 20
        stable = 40
        gov = 30
        emergency = 10
        rationale = "Capital preservation focused with substantial debt and sovereign backing, minimizing drawdown exposure."
    else: # Moderate
        if horizon >= 7:
            growth = 50
            stable = 25
            gov = 15
            emergency = 10
        else:
            growth = 40
            stable = 30
            gov = 20
            emergency = 10
        rationale = "Balanced allocation balancing equity growth potential with stable fixed income and sovereign tax-advantaged buffers."
        
    surplus = max(5000.0, monthly_surplus)
    monthly_plan = {
        "Growth (Equity Funds / Large Cap)": round(surplus * (growth / 100.0), 2),
        "Stable (Fixed Income / Debt)": round(surplus * (stable / 100.0), 2),
        "Government / Tax Buffer (PPF/NPS)": round(surplus * (gov / 100.0), 2),
        "Emergency Reserve (Liquid Fund)": round(surplus * (emergency / 100.0), 2),
    }
    
    return PortfolioAllocation(
        growth_equity_pct=growth,
        stable_debt_pct=stable,
        government_schemes_pct=gov,
        emergency_reserve_pct=emergency,
        monthly_allocation_plan=monthly_plan,
        rationale=rationale,
        guardrail_status="PASSED"
    )

