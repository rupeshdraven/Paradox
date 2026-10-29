import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from .models import (
    UserProfile, Goal, RiskAssessmentSubmission, FinancialAnalysis,
    InvestmentScheme, PortfolioAllocation, WhatIfRequest, WhatIfResponse,
    AICopilotQuery, AICopilotResponse
)
from .database import init_db, load_profile, save_profile, get_goals, save_goal, delete_goal, reset_demo
from .engine.financial_math import analyze_finances, calculate_goal_metrics
from .engine.suitability import compute_recommendations, generate_portfolio_allocation
from .engine.simulator import run_what_if_simulation
from .engine.ai_copilot import answer_financial_copilot
from .engine.guardrails import AUDIT_LOGS

app = FastAPI(
    title="FinWise AI - Financial Advisory API",
    description="Deterministic financial logic and AI copilot for personalized, suitability-aware financial planning.",
    version="1.0.0"
)

# Enable CORS for local Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FinWise AI Advisory Backend",
        "engine_version": "2.0.0",
        "guardrail_engine": "active"
    }

@app.get("/api/profile", response_model=UserProfile)
def get_user_profile():
    return load_profile()

@app.post("/api/profile", response_model=UserProfile)
def update_user_profile(profile: UserProfile):
    save_profile(profile)
    return profile

@app.post("/api/reset-demo")
def reset_to_demo():
    reset_demo()
    return {"message": "Demo profile successfully reset to Rupesh default profile", "profile": load_profile()}

@app.get("/api/goals", response_model=List[Goal])
def list_goals():
    goals = get_goals()
    return [calculate_goal_metrics(g) for g in goals]

@app.post("/api/goals", response_model=Goal)
def add_or_update_goal(goal: Goal):
    calc_goal = calculate_goal_metrics(goal)
    save_goal(calc_goal)
    return calc_goal

@app.delete("/api/goals/{goal_id}")
def remove_goal(goal_id: str):
    delete_goal(goal_id)
    return {"status": "deleted", "goal_id": goal_id}

@app.post("/api/risk/evaluate")
def evaluate_risk(submission: RiskAssessmentSubmission):
    # Sum points from questionnaire
    total_pts = sum(a.points for a in submission.answers)
    # Range is 25 to 125, normalize to 0 - 100
    norm_score = int(round(max(0, min(100, ((total_pts - 25) / 100.0) * 100.0))))
    
    if norm_score <= 35:
        cat = "Conservative"
        desc = "Your responses prioritize capital safety, with preference for minimal drawdown and predictable, sovereign-backed instruments."
    elif norm_score <= 68:
        cat = "Moderate"
        desc = "Your responses indicate tolerance for moderate market fluctuations in pursuit of healthy inflation-beating growth over a multi-year horizon."
    else:
        cat = "Aggressive"
        desc = "Your profile shows high risk resilience, comfortably weathering market corrections for maximum long-term compounding."
        
    # Update current profile with the newly evaluated risk score
    prof = load_profile()
    prof.risk_score = norm_score
    prof.risk_category = cat
    prof.risk_appetite = cat
    save_profile(prof)
    
    return {
        "risk_score": norm_score,
        "risk_category": cat,
        "explanation": desc
    }

@app.get("/api/analysis", response_model=FinancialAnalysis)
def get_financial_analysis():
    profile = load_profile()
    goals = get_goals()
    return analyze_finances(profile, goals)

@app.get("/api/recommendations", response_model=List[InvestmentScheme])
def get_recommendations(category: Optional[str] = None, sort_by: Optional[str] = "Recommended"):
    profile = load_profile()
    goals = get_goals()
    recs = compute_recommendations(profile, goals)
    
    # Filter by category if specified and not "All"
    if category and category.lower() not in ["all", "all schemes"]:
        recs = [r for r in recs if r.category.lower() == category.lower()]
        
    # Sort options
    if sort_by == "Risk":
        risk_order = {"Very Low": 1, "Low": 2, "Moderate": 3, "High": 4, "Very High": 5}
        recs.sort(key=lambda x: risk_order.get(x.risk_level, 3))
    elif sort_by == "Potential Return":
        recs.sort(key=lambda x: x.indicative_rate_num, reverse=True)
    elif sort_by == "Minimum Investment":
        recs.sort(key=lambda x: x.min_investment_num)
    else:
        # Recommended (by suitability score descending)
        recs.sort(key=lambda x: x.suitability_score or 0, reverse=True)
        
    return recs

@app.get("/api/portfolio-allocation", response_model=PortfolioAllocation)
def get_portfolio_plan():
    profile = load_profile()
    goals = get_goals()
    analysis = analyze_finances(profile, goals)
    return generate_portfolio_allocation(profile, analysis.monthly_surplus)

@app.post("/api/simulate", response_model=WhatIfResponse)
def simulate(req: WhatIfRequest):
    return run_what_if_simulation(req)

@app.post("/api/copilot", response_model=AICopilotResponse)
def copilot_chat(query_data: AICopilotQuery):
    if not query_data.profile:
        query_data.profile = load_profile()
    if not query_data.goals:
        query_data.goals = get_goals()
    if not query_data.financial_analysis:
        query_data.financial_analysis = analyze_finances(query_data.profile, query_data.goals)
        
    return answer_financial_copilot(query_data)

@app.get("/api/audit-logs")
def get_audit_trail():
    return {"audit_logs": AUDIT_LOGS}

