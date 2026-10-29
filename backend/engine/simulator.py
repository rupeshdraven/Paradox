import math
from typing import List, Dict, Any
from ..models import WhatIfRequest, WhatIfResponse

def simulate_future_value(monthly_inv: float, annual_return_pct: float, target_amount: float, initial_corpus: float = 0.0) -> Tuple[int, List[Dict[str, Any]]]:
    r = (annual_return_pct / 100.0) / 12.0
    current_val = initial_corpus
    months = 0
    max_months = 360 # 30 years limit
    trajectory = []
    
    # Store starting point
    trajectory.append({
        "month": 0,
        "year": 0,
        "invested": round(initial_corpus, 2),
        "corpus": round(current_val, 2)
    })
    
    total_invested = initial_corpus
    
    if monthly_inv <= 0:
        return (max_months, trajectory)
        
    while current_val < target_amount and months < max_months:
        months += 1
        total_invested += monthly_inv
        current_val = (current_val + monthly_inv) * (1.0 + r)
        
        # Record milestones (every 6 months or when target is reached)
        if months % 6 == 0 or current_val >= target_amount:
            trajectory.append({
                "month": months,
                "year": round(months / 12.0, 1),
                "invested": round(total_invested, 2),
                "corpus": round(current_val, 2)
            })
            
    return (months, trajectory)

def run_what_if_simulation(req: WhatIfRequest) -> WhatIfResponse:
    # Baseline
    baseline_income = req.current_income
    baseline_expenses = req.current_expenses
    baseline_inv = req.current_investment
    if baseline_inv <= 0:
        baseline_inv = max(2000.0, baseline_income - baseline_expenses)
        
    target = max(10000.0, req.goal_amount)
    r = req.expected_annual_return_pct
    initial = req.current_savings
    
    # After scenario
    new_inc = req.new_income if req.new_income is not None else baseline_income
    new_exp = req.new_expenses if req.new_expenses is not None else baseline_expenses
    
    if req.new_monthly_investment is not None:
        after_inv = req.new_monthly_investment
    else:
        # Default scenario: increase investment by ₹4,000 or (new_inc - new_exp)
        after_inv = max(baseline_inv + 4000.0, (new_inc - new_exp))
        
    before_months, before_traj = simulate_future_value(baseline_inv, r, target, initial)
    after_months, after_traj = simulate_future_value(after_inv, r, target, initial)
    
    months_saved = max(0, before_months - after_months)
    
    # Build unified timeline comparison for charting
    # Sample up to 24 time intervals
    max_m = max(before_months, after_months)
    step = max(1, int(max_m / 10))
    timeline = []
    
    # Build chart data points
    curr_b = initial
    curr_a = initial
    invested_b = initial
    invested_a = initial
    monthly_r = (r / 100.0) / 12.0
    
    for m in range(0, max_m + 1, step):
        # Calculate compound values at month m
        if m == 0:
            val_b = initial
            val_a = initial
        else:
            val_b = initial * ((1 + monthly_r) ** m) + (baseline_inv * (((1 + monthly_r) ** m - 1) / monthly_r))
            val_a = initial * ((1 + monthly_r) ** m) + (after_inv * (((1 + monthly_r) ** m - 1) / monthly_r))
            
        timeline.append({
            "month": m,
            "period": f"{round(m/12.0, 1)} yrs" if m >= 12 else f"{m} mo",
            "current_strategy": round(min(val_b, target * 1.2), 0),
            "optimized_strategy": round(min(val_a, target * 1.2), 0),
            "target": target
        })
        
    insights = []
    if months_saved > 0:
        insights.append(f"By contributing ₹{int(after_inv):,} monthly instead of ₹{int(baseline_inv):,}, you reach your ₹{int(target):,} target {months_saved} months faster.")
        insights.append(f"Target completion accelerates from {round(before_months/12.0, 1)} years to {round(after_months/12.0, 1)} years.")
    else:
        insights.append("Increasing your monthly investment surplus directly shortens your goal horizon.")
        
    if new_exp < baseline_expenses:
        saved_from_exp = baseline_expenses - new_exp
        insights.append(f"Reducing discretionary expenses by ₹{int(saved_from_exp):,}/mo frees up substantial cash flow for compounding.")

    return WhatIfResponse(
        before_months=before_months,
        after_months=after_months,
        months_saved=months_saved,
        before_total_invested=round(baseline_inv * before_months + initial, 2),
        after_total_invested=round(after_inv * after_months + initial, 2),
        before_future_value=target,
        after_future_value=target,
        timeline_comparison=timeline,
        insights=insights
    )

