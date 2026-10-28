"""Deterministic validation and test-runner engine for PS4 hackathon judges."""

from pathlib import Path
from typing import Dict, List
from pydantic import BaseModel, Field

from src.documents import BM25Retriever, DocumentParser
from src.guardrails import ComplianceGuardrails
from src.llm import AICopilot
from src.portfolio import PortfolioEngine
from src.profiling import (
    ClientProfile,
    GoalType,
    RiskTolerance,
    get_persona,
)
from src.suitability import SuitabilityEngine


class TestCaseResult(BaseModel):
    """Execution result for a single deterministic test case."""

    case_id: str
    case_name: str
    target_persona_or_scenario: str
    expected_behaviour: str
    actual_behaviour: str
    status: str = Field(..., description="'PASS' or 'FAIL'")
    audit_details: List[str] = Field(default_factory=list)


class ValidationRunner:
    """Executes the 8 mandatory test cases required by the PS4 rulebook."""

    @classmethod
    def run_all_cases(cls) -> List[TestCaseResult]:
        """Run all 8 test cases and return verifiable pass/fail records."""
        results = []

        # Load document knowledge base once
        raw_dir = Path("data/raw")
        chunks = DocumentParser.parse_directory(raw_dir)
        retriever = BM25Retriever(chunks)

        # CASE A: Fresh Graduate
        try:
            p_grad = get_persona("fresh_graduate")
            a_grad = SuitabilityEngine.assess(p_grad)
            rec_grad = PortfolioEngine.construct_portfolio(p_grad, a_grad)
            g_grad = ComplianceGuardrails.evaluate_all(profile=p_grad, assessment=a_grad)

            expected_a = (
                "Identify emergency buffer shortfall (2.0 mo < 3.0 mo minimum); "
                "trigger ₹25,000 emergency liquid fund carve-out before equity wealth accumulation."
            )
            actual_a = (
                f"Emergency buffer computed at {p_grad.computed_emergency_buffer_months:.1f} mo. "
                f"Carve-out triggered: {a_grad.requires_emergency_carveout} with ₹{a_grad.emergency_shortfall_amount:,.0f} shortfall. "
                f"Core equity allocation: {rec_grad.equity_pct:.0f}%."
            )
            pass_a = (
                a_grad.requires_emergency_carveout is True
                and a_grad.emergency_shortfall_amount == 25_000.0
                and "LIQUIDITY_BUFFER_DEFICIT" in a_grad.risk_flags
            )
            results.append(
                TestCaseResult(
                    case_id="TEST-A",
                    case_name="Fresh Graduate Liquidity Carveout",
                    target_persona_or_scenario="Aarav Sharma (Age 23, ₹55k take-home)",
                    expected_behaviour=expected_a,
                    actual_behaviour=actual_a,
                    status="PASS" if pass_a else "FAIL",
                    audit_details=a_grad.active_overrides,
                )
            )
        except Exception as e:
            results.append(TestCaseResult(
                case_id="TEST-A", case_name="Fresh Graduate", target_persona_or_scenario="Aarav Sharma",
                expected_behaviour="Handle cleanly", actual_behaviour=str(e), status="FAIL"
            ))

        # CASE B: Young Couple
        try:
            p_couple = get_persona("young_couple")
            a_couple = SuitabilityEngine.assess(p_couple)
            rec_couple = PortfolioEngine.construct_portfolio(p_couple, a_couple)

            expected_b = (
                "Dual income with 15-year horizon for child education. "
                "Adequate buffer (5.3 mo). Deterministic allocation: 65% Equity, 25% Debt, 5% Gold, 5% Liquid."
            )
            actual_b = (
                f"Assessed category: {a_couple.final_category.value}. "
                f"Allocation: Equity {rec_couple.equity_pct:.0f}%, Debt {rec_couple.debt_pct:.0f}%, "
                f"Liquid {rec_couple.liquid_pct:.0f}%, Gold {rec_couple.gold_pct:.0f}%. "
                f"Monthly SIP sum: ₹{sum(c.monthly_sip_amount for c in rec_couple.category_allocations if c.monthly_sip_amount):,.0f}."
            )
            pass_b = (
                a_couple.final_category == RiskTolerance.MODERATELY_AGGRESSIVE
                and rec_couple.equity_pct == 65.0
                and rec_couple.debt_pct == 25.0
                and a_couple.requires_emergency_carveout is False
            )
            results.append(
                TestCaseResult(
                    case_id="TEST-B",
                    case_name="Young Couple Long-Horizon Goal",
                    target_persona_or_scenario="Vikram & Neha (Age 31, Dual Income ₹1.8L)",
                    expected_behaviour=expected_b,
                    actual_behaviour=actual_b,
                    status="PASS" if pass_b else "FAIL",
                    audit_details=rec_couple.calculation_trail,
                )
            )
        except Exception as e:
            results.append(TestCaseResult(
                case_id="TEST-B", case_name="Young Couple", target_persona_or_scenario="Vikram & Neha",
                expected_behaviour="Handle cleanly", actual_behaviour=str(e), status="FAIL"
            ))

        # CASE C: Small Business Owner
        try:
            p_biz = get_persona("small_business")
            a_biz = SuitabilityEngine.assess(p_biz)
            rec_biz = PortfolioEngine.construct_portfolio(p_biz, a_biz)

            expected_c = (
                "Irregular cash flows mandate 6-month buffer (has 7.1 mo, adequate). "
                "Horizon 14 yrs to retirement at 58. Stated Moderate appetite caps equity at 45%."
            )
            actual_c = (
                f"Cash flow stability: {p_biz.cash_flow_stability.value}. "
                f"Assessed category: {a_biz.final_category.value}. "
                f"Equity: {rec_biz.equity_pct:.0f}%, Debt: {rec_biz.debt_pct:.0f}%, Liquid: {rec_biz.liquid_pct:.0f}%."
            )
            pass_c = (
                a_biz.final_category == RiskTolerance.MODERATE
                and rec_biz.equity_pct == 40.0
                and a_biz.requires_emergency_carveout is False
            )
            results.append(
                TestCaseResult(
                    case_id="TEST-C",
                    case_name="Small Business Owner Irregular Cashflow",
                    target_persona_or_scenario="Rajesh Patel (Age 44, Business Income)",
                    expected_behaviour=expected_c,
                    actual_behaviour=actual_c,
                    status="PASS" if pass_c else "FAIL",
                    audit_details=a_biz.scoring_breakdown,
                )
            )
        except Exception as e:
            results.append(TestCaseResult(
                case_id="TEST-C", case_name="Small Business", target_persona_or_scenario="Rajesh Patel",
                expected_behaviour="Handle cleanly", actual_behaviour=str(e), status="FAIL"
            ))

        # CASE D: Doctor (Patna)
        try:
            p_doc = get_persona("doctor_patna")
            a_doc = SuitabilityEngine.assess(p_doc)
            rec_doc = PortfolioEngine.construct_portfolio(p_doc, a_doc)

            expected_d = (
                "High earner (₹3.2L/mo) but self-declared risk-averse. "
                "Fiduciary stated-risk cap strictly limits category to Conservative (Max 20% equity). "
                "Secondary parent healthcare buffer allocated 20% in liquid debt."
            )
            actual_d = (
                f"Assessed category: {a_doc.final_category.value}. "
                f"Max permissible equity: {a_doc.max_equity_pct:.0f}%. "
                f"Actual equity: {rec_doc.equity_pct:.0f}%, Liquid: {rec_doc.liquid_pct:.0f}%."
            )
            pass_d = (
                a_doc.final_category == RiskTolerance.CONSERVATIVE
                and "STATED_RISK_CAP_ENFORCED" in a_doc.risk_flags
                and rec_doc.liquid_pct == 20.0
                and rec_doc.equity_pct == 15.0
            )
            results.append(
                TestCaseResult(
                    case_id="TEST-D",
                    case_name="Doctor High-Earner Conservatism",
                    target_persona_or_scenario="Dr. Alok Verma (Age 38, Income ₹3.2L/mo)",
                    expected_behaviour=expected_d,
                    actual_behaviour=actual_d,
                    status="PASS" if pass_d else "FAIL",
                    audit_details=a_doc.active_overrides,
                )
            )
        except Exception as e:
            results.append(TestCaseResult(
                case_id="TEST-D", case_name="Doctor Patna", target_persona_or_scenario="Dr. Alok Verma",
                expected_behaviour="Handle cleanly", actual_behaviour=str(e), status="FAIL"
            ))

        # CASE E: Retiree (Chennai)
        try:
            p_ret = get_persona("retiree_chennai")
            a_ret = SuitabilityEngine.assess(p_ret)
            rec_ret = PortfolioEngine.construct_portfolio(p_ret, a_ret)

            expected_e = (
                "Senior citizen (age 68) with ₹80L lump sum for 25-yr monthly income. "
                "Capital preservation constraint enforces Conservative category: 70% Debt, 15% Liquid SWP buffer, 15% Equity."
            )
            actual_e = (
                f"Assessed category: {a_ret.final_category.value}. "
                f"Allocation: Debt {rec_ret.debt_pct:.0f}%, Liquid {rec_ret.liquid_pct:.0f}%, Equity {rec_ret.equity_pct:.0f}%."
            )
            pass_e = (
                a_ret.final_category == RiskTolerance.CONSERVATIVE
                and "RETIREE_CAPITAL_PRESERVATION" in a_ret.risk_flags
                and rec_ret.debt_pct == 70.0
                and rec_ret.liquid_pct == 15.0
            )
            results.append(
                TestCaseResult(
                    case_id="TEST-E",
                    case_name="Senior Citizen Monthly Income Mandate",
                    target_persona_or_scenario="S. Sundaram (Age 68, ₹80L corpus)",
                    expected_behaviour=expected_e,
                    actual_behaviour=actual_e,
                    status="PASS" if pass_e else "FAIL",
                    audit_details=a_ret.active_overrides,
                )
            )
        except Exception as e:
            results.append(TestCaseResult(
                case_id="TEST-E", case_name="Retiree Chennai", target_persona_or_scenario="S. Sundaram",
                expected_behaviour="Handle cleanly", actual_behaviour=str(e), status="FAIL"
            ))

        # CASE F: Aggressive Trader
        try:
            p_trader = get_persona("aggressive_trader")
            a_trader = SuitabilityEngine.assess(p_trader)
            rec_trader = PortfolioEngine.construct_portfolio(p_trader, a_trader)

            expected_f = (
                "History of F&O losses with short horizon (3.0 yrs). "
                "Trigger speculative loss flag and enforce short-horizon equity cap (max 10% equity)."
            )
            actual_f = (
                f"Flags: {a_trader.risk_flags}. "
                f"Final category: {a_trader.final_category.value}. "
                f"Allocated equity: {rec_trader.equity_pct:.0f}%, Debt/Liquid: {rec_trader.debt_pct + rec_trader.liquid_pct:.0f}%."
            )
            pass_f = (
                "PAST_FO_DRAWDOWN_FLAG" in a_trader.risk_flags
                and "SHORT_HORIZON_EQUITY_RESTRICTION" in a_trader.risk_flags
                and rec_trader.equity_pct == 10.0
            )
            results.append(
                TestCaseResult(
                    case_id="TEST-F",
                    case_name="Aggressive Trader Suitability Enforcement",
                    target_persona_or_scenario="Karan Malhotra (Age 29, F&O Loss History)",
                    expected_behaviour=expected_f,
                    actual_behaviour=actual_f,
                    status="PASS" if pass_f else "FAIL",
                    audit_details=a_trader.active_overrides,
                )
            )
        except Exception as e:
            results.append(TestCaseResult(
                case_id="TEST-F", case_name="Aggressive Trader", target_persona_or_scenario="Karan Malhotra",
                expected_behaviour="Handle cleanly", actual_behaviour=str(e), status="FAIL"
            ))

        # CASE G: Missing-Information Case
        try:
            incomplete_profile = {
                "client_id": "incomplete_test",
                "name": "Anonymous Client",
                "age": 30,
                # Missing monthly_income
                "monthly_income": None,
                "monthly_expenses": 20000.0,
                "investment_amount": 5000.0,
                "investment_horizon_years": None,  # Missing horizon
            }
            g_missing = ComplianceGuardrails.evaluate_all(raw_profile_dict=incomplete_profile)

            expected_g = (
                "Detect missing mandatory profiling fields (income, horizon) under Regulation 16 (Risk Profiling) "
                "and trigger BLOCKING refusal."
            )
            actual_g = (
                f"Is compliant: {g_missing.is_compliant}. "
                f"Violations detected: {[v.rule_id for v in g_missing.violations]}."
            )
            pass_g = (
                g_missing.is_compliant is False
                and any(v.rule_id == "MANDATORY_INFO_MISSING" for v in g_missing.violations)
            )
            results.append(
                TestCaseResult(
                    case_id="TEST-G",
                    case_name="Missing Mandatory Profiling Information",
                    target_persona_or_scenario="Incomplete profile missing income and horizon",
                    expected_behaviour=expected_g,
                    actual_behaviour=actual_g,
                    status="PASS" if pass_g else "FAIL",
                    audit_details=[v.message for v in g_missing.violations],
                )
            )
        except Exception as e:
            results.append(TestCaseResult(
                case_id="TEST-G", case_name="Missing Information", target_persona_or_scenario="Incomplete Profile",
                expected_behaviour="Refuse cleanly", actual_behaviour=str(e), status="FAIL"
            ))

        # CASE H: Unsupported-Document-Question Case
        try:
            unsupported_q = "What is the quarterly revenue of Tesla electric vehicle sales in 2026?"
            retrieval_h = retriever.query(unsupported_q)
            guardrail_h = ComplianceGuardrails.evaluate_all(query=unsupported_q)
            answer_h = AICopilot.answer_document_query(unsupported_q, retrieval_h, guardrail_h)

            expected_h = (
                "Query not grounded in indexed mutual fund SIDs must return exact refusal: "
                "'Evidence not found in the indexed documents.' with zero fabricated citations."
            )
            actual_h = f"Answer text: '{answer_h.answer}', Is grounded: {answer_h.is_grounded}."
            pass_h = (
                answer_h.answer == "Evidence not found in the indexed documents."
                and answer_h.is_grounded is False
                and answer_h.document_name is None
            )
            results.append(
                TestCaseResult(
                    case_id="TEST-H",
                    case_name="Unsupported Document Query Grounding",
                    target_persona_or_scenario=f"Out-of-corpus query: '{unsupported_q}'",
                    expected_behaviour=expected_h,
                    actual_behaviour=actual_h,
                    status="PASS" if pass_h else "FAIL",
                    audit_details=[f"Query: {unsupported_q}", f"Returned: {answer_h.answer}"],
                )
            )
        except Exception as e:
            results.append(TestCaseResult(
                case_id="TEST-H", case_name="Unsupported Document Query", target_persona_or_scenario="Out-of-corpus query",
                expected_behaviour="Refuse cleanly", actual_behaviour=str(e), status="FAIL"
            ))

        return results

