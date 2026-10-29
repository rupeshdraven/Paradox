import os
import re
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..models import UserProfile, Goal, FinancialAnalysis, AICopilotQuery, AICopilotResponse
from .guardrails import GuardrailEngine, record_audit

def extract_amount_from_query(text: str) -> Optional[float]:
    # Look for patterns like ₹70,000, 70000, 70k, 1.5 Lakh, 2L
    text = text.replace(",", "").lower()
    
    # 70k
    m_k = re.search(r"(\d+(\.\d+)?)\s*k\b", text)
    if m_k:
        return float(m_k.group(1)) * 1000.0
        
    # 1.5 lakh / 2 lakh
    m_l = re.search(r"(\d+(\.\d+)?)\s*(lakh|lac|l)\b", text)
    if m_l:
        return float(m_l.group(1)) * 100000.0
        
    # ₹70000 or Rs 70000 or 70000
    m_num = re.search(r"(?:₹|rs\.?|inr)?\s*(\d{3,8})", text)
    if m_num:
        return float(m_num.group(1))
        
    return None

def answer_financial_copilot(query_data: AICopilotQuery) -> AICopilotResponse:
    query = query_data.query.strip()
    profile = query_data.profile or UserProfile()
    analysis = query_data.financial_analysis
    
    # 1. Run deterministic Guardrail Check
    status, checks, message_override = GuardrailEngine.inspect_query(query, profile)
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if status == "BLOCK":
        record_audit(query, status, checks, message_override or "Blocked by safety guardrail")
        return AICopilotResponse(
            guardrail_status=status,
            short_answer="This request cannot be fulfilled under our responsible financial advisory rules.",
            why=[
                message_override or "Blocked due to regulatory compliance and risk management guardrails.",
                "FinWise AI adheres strictly to transparent, verified Indian financial guidelines."
            ],
            better_option="Explore diversified equity mutual funds, index funds, or sovereign savings schemes aligned to your horizon.",
            impact={"status": "Action Blocked", "risk_mitigation": "100% Capital Protection from Speculation"},
            checks_applied=checks,
            evidence_citation="SEBI Master Circular on Prohibited & High-Risk Unregulated Instruments",
            timestamp=now_str
        )
        
    if status == "WARN" and message_override and "guarantee" in message_override.lower():
        record_audit(query, status, checks, message_override)
        return AICopilotResponse(
            guardrail_status="WARN",
            short_answer="Market-linked investments cannot provide guaranteed returns.",
            why=[
                message_override,
                "Equity and hybrid mutual funds are subject to macroeconomic and corporate market cycles.",
                "Fixed interest returns are exclusively available via sovereign instruments like PPF (7.1%) or bank FDs (up to 7.5%)."
            ],
            better_option="If capital guarantee is your mandatory priority, utilize Public Provident Fund (PPF) or Bank Fixed Deposits. If seeking 11-14% growth, adopt an SIP in large-cap index funds with a 5+ year horizon.",
            impact={"variance": "Historical equity returns range between -15% in bear years to +35% in bull years", "safe_benchmark": "7.1% p.a. sovereign fixed"},
            checks_applied=checks,
            evidence_citation="SEBI (Mutual Funds) Regulations, 1996 - Regulation 24 & RBI Depository Safeguards",
            timestamp=now_str
        )

    # Resolve core metrics
    monthly_income = profile.annual_income / 12.0 if profile.annual_income > 0 else 50000.0
    monthly_expenses = profile.monthly_expenses if profile.monthly_expenses > 0 else 30000.0
    monthly_surplus = max(1000.0, monthly_income - monthly_expenses)
    savings_rate = (monthly_surplus / monthly_income) * 100.0
    emergency_fund = profile.existing_savings
    
    q_lower = query.lower()
    
    # 2. Check for "Can I afford [Amount / Item]?"
    if "afford" in q_lower or "buy" in q_lower or "purchase" in q_lower:
        amount = extract_amount_from_query(query) or 70000.0
        item_match = re.search(r"(?:afford|buy|purchase)\s+(?:a|an|the)?\s*([a-zA-Z0-9\s]+?)(?:\?|$|\s+for|\s+worth)", query, re.IGNORECASE)
        item_name = item_match.group(1).strip() if item_match else "this purchase"
        if len(item_name) > 30 or not item_name:
            item_name = "this purchase"
            
        months_of_surplus = round(amount / monthly_surplus, 1)
        can_afford_cash = emergency_fund >= amount * 1.5
        
        if months_of_surplus <= 1.0:
            short_ans = f"Yes, you can comfortably afford {item_name} (₹{int(amount):,}) within your regular monthly surplus."
            better_opt = "Allocate funds from your current month surplus without touching your emergency reserves."
        elif months_of_surplus <= 3.0:
            short_ans = f"You can afford {item_name} (₹{int(amount):,}), but it requires planning across {months_of_surplus} months of surplus."
            better_opt = f"Set up a dedicated sinking fund saving ₹{int(monthly_surplus * 0.5):,}/month for {int(months_of_surplus * 2)} months rather than paying in a single lump sum."
        else:
            short_ans = f"Purchasing {item_name} (₹{int(amount):,}) right now will significantly strain your monthly cash flow and delay financial goals."
            better_opt = f"Postpone this discretionary expense until your emergency fund covers at least 6 months of expenses, or budget ₹{int(monthly_surplus * 0.3):,}/month over {int(amount / (monthly_surplus * 0.3))} months."
            
        why_points = [
            f"Your current monthly disposable surplus is ₹{int(monthly_surplus):,}.",
            f"The ₹{int(amount):,} cost represents approximately {months_of_surplus} months of your entire unallocated savings.",
            f"Existing emergency savings stand at ₹{int(emergency_fund):,} (covers {round(emergency_fund/max(1.0, monthly_expenses), 1)} months of expenses)."
        ]
        
        goal_target = 500000.0
        if query_data.goals and len(query_data.goals) > 0:
            goal_target = query_data.goals[0].target_amount
            
        m_without = round(goal_target / monthly_surplus)
        m_with = round((goal_target + amount) / monthly_surplus)
        
        impact_data = {
            "purchase_amount": f"₹{int(amount):,}",
            "surplus_absorbed": f"{round((amount / monthly_surplus) * 100)}%",
            "without_purchase_goal_completion": f"{m_without} months",
            "with_purchase_goal_completion": f"{m_with} months",
            "delay_penalty": f"{m_with - m_without} months delay"
        }
        
        resp = AICopilotResponse(
            guardrail_status="ALLOW",
            short_answer=short_ans,
            why=why_points,
            better_option=better_opt,
            impact=impact_data,
            checks_applied=checks,
            evidence_citation="Budgeting Cash-Flow Model: 50-30-20 Discretionary Spending Ratio",
            timestamp=now_str
        )
        record_audit(query, "ALLOW", checks, short_ans, "Cash-Flow Affordability Ratio")
        return resp
        
    # 3. "How much should I save every month?"
    elif "how much should i save" in q_lower or "savings target" in q_lower or "how much to save" in q_lower:
        rec_savings = monthly_income * 0.30
        why_points = [
            f"Based on the standard 50/30/20 financial rule, 20%–30% of income should be directed into savings and wealth creation.",
            f"With an income of ₹{int(monthly_income):,}/month, your recommended saving baseline is ₹{int(rec_savings):,} (30%).",
            f"Your current reported expenses are ₹{int(monthly_expenses):,}, leaving an actual surplus of ₹{int(monthly_surplus):,} ({round(savings_rate)}%)."
        ]
        resp = AICopilotResponse(
            guardrail_status="ALLOW",
            short_answer=f"You should target saving at least ₹{int(rec_savings):,} every month (30% of your ₹{int(monthly_income):,} income).",
            why=why_points,
            better_option="Automate an SIP of ₹15,000 into a Large Cap Index Fund and ₹5,000 into PPF on the 5th of every month immediately following salary credit.",
            impact={
                "target_monthly_savings": f"₹{int(rec_savings):,}",
                "5_year_corpus_at_11pct": f"₹{int(rec_savings * 12 * 5 * 1.3):,}",
                "emergency_reserve_buffer": "Fully funded within 4 months"
            },
            checks_applied=checks,
            evidence_citation="Prudent Personal Finance Benchmark - Elizabeth Warren 50/30/20 Guidelines",
            timestamp=now_str
        )
        record_audit(query, "ALLOW", checks, resp.short_answer)
        return resp

    # 4. "How long will it take me to reach my goal?"
    elif "how long" in q_lower and "goal" in q_lower or "reach my goal" in q_lower:
        target = 500000.0
        g_name = "Primary Goal"
        if query_data.goals and len(query_data.goals) > 0:
            target = query_data.goals[0].target_amount
            g_name = query_data.goals[0].name
            
        months_linear = round(target / monthly_surplus)
        # With 11% compound interest
        r = 0.11 / 12.0
        months_compound = round(math.log(1 + (target * r / monthly_surplus)) / math.log(1 + r)) if (1 + (target * r / monthly_surplus)) > 0 else months_linear
        
        resp = AICopilotResponse(
            guardrail_status="ALLOW",
            short_answer=f"At your current monthly investment rate of ₹{int(monthly_surplus):,}, you will reach your '{g_name}' goal of ₹{int(target):,} in approximately {months_compound} months (~{round(months_compound/12.0, 1)} years).",
            why=[
                f"Your monthly contribution capacity is ₹{int(monthly_surplus):,}.",
                f"Assuming an illustrative 11% p.a. long-term market compound return, compounding shaves off {months_linear - months_compound} months compared to idle cash.",
                f"Total principal invested over the period will be approximately ₹{int(monthly_surplus * months_compound):,}."
            ],
            better_option=f"Stepping up your monthly SIP by just 10% each year (SIP Top-up) will reduce your timeline by an additional {round(months_compound * 0.2)} months.",
            impact={
                "projected_months": f"{months_compound} months",
                "idle_cash_duration": f"{months_linear} months",
                "compound_benefit": f"Saved {months_linear - months_compound} months via compounding"
            },
            checks_applied=checks,
            evidence_citation="Annuity Future Value Calculation Formula: FV = P * [((1 + r)^n - 1) / r]",
            timestamp=now_str
        )
        record_audit(query, "ALLOW", checks, resp.short_answer)
        return resp

    # 5. "What happens if my expenses increase by ₹5,000?"
    elif "expenses increase" in q_lower or "expense increase" in q_lower:
        delta = extract_amount_from_query(query) or 5000.0
        new_surplus = max(0.0, monthly_surplus - delta)
        target = 500000.0
        if query_data.goals and len(query_data.goals) > 0:
            target = query_data.goals[0].target_amount
            
        m_before = round(target / monthly_surplus) if monthly_surplus > 0 else 999
        m_after = round(target / new_surplus) if new_surplus > 0 else 999
        delay = m_after - m_before
        
        resp = AICopilotResponse(
            guardrail_status="ALLOW",
            short_answer=f"An expense increase of ₹{int(delta):,}/month drops your surplus from ₹{int(monthly_surplus):,} to ₹{int(new_surplus):,}, delaying your financial goals by ~{delay} months.",
            why=[
                f"Your savings rate reduces from {round(savings_rate)}% down to {round((new_surplus/monthly_income)*100)}%.",
                f"Annual wealth creation capacity drops by ₹{int(delta * 12):,} per year.",
                f"Over 5 years, the cumulative opportunity cost (including missed 11% compound growth) equals ~₹{int(delta * 12 * 5 * 1.3):,}."
            ],
            better_option="Audit your recurring subscriptions, dining, and utility bills to find offsetting savings of ₹2,000–₹3,000 so your investment momentum is unaffected.",
            impact={
                "original_completion": f"{m_before} months",
                "revised_completion": f"{m_after} months",
                "delay_incurred": f"{delay} months delay"
            },
            checks_applied=checks,
            evidence_citation="Cash Flow Sensitivity Analysis",
            timestamp=now_str
        )
        record_audit(query, "ALLOW", checks, resp.short_answer)
        return resp

    # 6. "Explain my financial health score"
    elif "health score" in q_lower or "explain my score" in q_lower:
        score = analysis.financial_health_score if analysis else 78
        status_txt = analysis.health_status if analysis else "Healthy"
        breakdown = analysis.health_score_breakdown if analysis else {"savings": 82, "expenses": 70, "emergency": 62, "debt": 90, "goals": 80}
        
        resp = AICopilotResponse(
            guardrail_status="ALLOW",
            short_answer=f"Your Financial Health Score is {score}/100 ('{status_txt}'), reflecting strong debt control and surplus generation with room to strengthen your emergency cushion.",
            why=[
                f"Debt Management ({breakdown.get('debt', 90)}/100): Excellent low debt-to-income ratio protects your net worth.",
                f"Savings Rate ({breakdown.get('savings', 82)}/100): Generating a healthy {round(savings_rate)}% monthly surplus rate.",
                f"Emergency Reserve ({breakdown.get('emergency', 62)}/100): Current liquidity covers ~{round(emergency_fund/max(1.0, monthly_expenses), 1)} months; target is 6 full months.",
                f"Expense Discipline ({breakdown.get('expenses', 70)}/100): Controlled living overheads."
            ],
            better_option="Channel ₹5,000 of your monthly surplus to an instant liquid fund until your emergency reserve reaches ₹1,80,000 (6 months of expenses). This will lift your health score above 88.",
            impact={
                "current_score": f"{score}/100",
                "potential_score": f"{min(98, score + 12)}/100",
                "primary_action": "Boost emergency liquidity"
            },
            checks_applied=checks,
            evidence_citation="FinWise Comprehensive 5-Pillar Health Score Matrix",
            timestamp=now_str
        )
        record_audit(query, "ALLOW", checks, resp.short_answer)
        return resp

    # 7. "Why did you recommend this investment?" / "Why SBI Bluechip / PPF?"
    elif "why did you recommend" in q_lower or "why this recommendation" in q_lower or "why recommend" in q_lower:
        resp = AICopilotResponse(
            guardrail_status="ALLOW",
            short_answer=f"Recommendations are matched deterministically based on your {profile.risk_appetite} risk profile, {profile.investment_horizon} horizon, and wealth creation goal.",
            why=[
                "Risk Suitability (Weight 25%): Matched against historical drawdown volatility appropriate for your comfort level.",
                "Horizon Alignment (Weight 20%): Funds with equity exposure require 5+ years to smooth market cycles.",
                "Liquidity Architecture (Weight 15%): Zero lock-in allows portfolio rebalancing, while sovereign debt provides capital security.",
                "Cost Efficiency: Selected schemes maintain top quartile tracking efficiency and competitive expense ratios."
            ],
            better_option="Review your allocation semi-annually. As you approach within 2 years of your target goal, systematically shift gains into fixed income to lock in returns.",
            impact={
                "risk_profile": profile.risk_appetite,
                "target_horizon": profile.investment_horizon,
                "portfolio_balance": "60% Equity / 30% Debt & Gov / 10% Cash"
            },
            checks_applied=checks,
            evidence_citation="Suitability Scoring Algorithm & SEBI Categorization Guidelines",
            timestamp=now_str
        )
        record_audit(query, "ALLOW", checks, resp.short_answer)
        return resp

    # 8. General / Fallback question
    else:
        resp = AICopilotResponse(
            guardrail_status="ALLOW",
            short_answer=f"Based on your profile (Income ₹{int(monthly_income):,}/mo, Surplus ₹{int(monthly_surplus):,}/mo, {profile.risk_appetite} risk), maintaining disciplined monthly SIPs and a 6-month safety buffer is your highest-leverage strategy.",
            why=[
                f"You have ₹{int(monthly_surplus):,} uncommitted monthly cash flow ready to compound.",
                f"Your risk profile ({profile.risk_appetite}) indicates readiness for balanced equity and fixed income allocations.",
                "Diversifying across Large Cap Index Funds, PPF, and Liquid funds protects capital while beating inflation."
            ],
            better_option="Focus on consistent monthly execution rather than attempting to time market fluctuations.",
            impact={
                "monthly_surplus": f"₹{int(monthly_surplus):,}",
                "annual_savings_capacity": f"₹{int(monthly_surplus * 12):,}",
                "guidance": "Educational decision-support model"
            },
            checks_applied=checks,
            evidence_citation="General Advisory Principles (SEBI RIA Code of Conduct Aligned)",
            timestamp=now_str
        )
        record_audit(query, "ALLOW", checks, resp.short_answer)
        return resp

