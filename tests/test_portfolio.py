"""Unit tests for deterministic goal-based portfolio construction."""

import pytest
from src.portfolio import PortfolioEngine
from src.profiling import get_persona
from src.suitability import SuitabilityEngine


@pytest.mark.parametrize(
    "persona_id",
    [
        "fresh_graduate",
        "young_couple",
        "small_business",
        "doctor_patna",
        "retiree_chennai",
        "aggressive_trader",
    ],
)
def test_all_personas_portfolio_weights_sum_to_100(persona_id):
    """Every portfolio recommendation must strictly sum to 100.0% across broad asset classes."""
    p = get_persona(persona_id)
    assessment = SuitabilityEngine.assess(p)
    rec = PortfolioEngine.construct_portfolio(p, assessment)

    total_weight = rec.equity_pct + rec.debt_pct + rec.liquid_pct + rec.gold_pct
    assert abs(total_weight - 100.0) < 1e-4

    # Also verify category weights sum to 100.0%
    cat_sum = sum(c.target_weight_pct for c in rec.category_allocations)
    assert abs(cat_sum - 100.0) < 1e-2


def test_fresh_graduate_portfolio_carveout():
    """Fresh graduate must receive an emergency fund carve-out instruction."""
    p = get_persona("fresh_graduate")
    assessment = SuitabilityEngine.assess(p)
    rec = PortfolioEngine.construct_portfolio(p, assessment)

    assert rec.emergency_carveout_amount == 25_000.0
    assert rec.emergency_carveout_instruction is not None
    assert "₹25,000" in rec.emergency_carveout_instruction


def test_young_couple_portfolio_child_education():
    """Young couple monthly SIPs across SEBI categories must match total monthly investment."""
    p = get_persona("young_couple")
    assessment = SuitabilityEngine.assess(p)
    rec = PortfolioEngine.construct_portfolio(p, assessment)

    assert rec.is_sip is True
    assert rec.investment_amount == 40_000.0
    total_sip = sum(c.monthly_sip_amount for c in rec.category_allocations if c.monthly_sip_amount)
    assert abs(total_sip - 40_000.0) < 1.0
    assert rec.equity_pct == 65.0


def test_doctor_patna_healthcare_buffer_allocation():
    """Doctor Patna must have liquid allocation earmarked for parent healthcare."""
    p = get_persona("doctor_patna")
    assessment = SuitabilityEngine.assess(p)
    rec = PortfolioEngine.construct_portfolio(p, assessment)

    assert rec.liquid_pct == 20.0
    assert rec.equity_pct == 15.0
    assert rec.debt_pct == 60.0
    total_sip = sum(c.monthly_sip_amount for c in rec.category_allocations if c.monthly_sip_amount)
    assert abs(total_sip - 120_000.0) < 1.0


def test_retiree_chennai_lump_sum_swp():
    """Retiree Chennai must allocate ₹80L lump sum with SWP liquidity and capital preservation."""
    p = get_persona("retiree_chennai")
    assessment = SuitabilityEngine.assess(p)
    rec = PortfolioEngine.construct_portfolio(p, assessment)

    assert rec.is_sip is False
    assert rec.equity_pct == 15.0
    assert rec.debt_pct == 70.0
    assert rec.liquid_pct == 15.0
    total_lump_sum = sum(c.lump_sum_amount for c in rec.category_allocations if c.lump_sum_amount)
    assert abs(total_lump_sum - 8_000_000.0) < 1.0


def test_aggressive_trader_correction():
    """Aggressive trader short horizon must cap equity at 10% and allocate 90% in debt/liquid."""
    p = get_persona("aggressive_trader")
    assessment = SuitabilityEngine.assess(p)
    rec = PortfolioEngine.construct_portfolio(p, assessment)

    assert rec.equity_pct == 10.0
    assert rec.debt_pct == 60.0
    assert rec.liquid_pct == 30.0


@pytest.mark.parametrize(
    "persona_id",
    [
        "fresh_graduate",
        "young_couple",
        "small_business",
        "doctor_patna",
        "retiree_chennai",
        "aggressive_trader",
    ],
)
def test_no_negative_allocations_anywhere(persona_id):
    """Ensure no broad asset class or category weight is negative."""
    p = get_persona(persona_id)
    assessment = SuitabilityEngine.assess(p)
    rec = PortfolioEngine.construct_portfolio(p, assessment)

    assert rec.equity_pct >= 0.0
    assert rec.debt_pct >= 0.0
    assert rec.liquid_pct >= 0.0
    assert rec.gold_pct >= 0.0

    for cat in rec.category_allocations:
        assert cat.target_weight_pct >= 0.0
        if cat.monthly_sip_amount is not None:
            assert cat.monthly_sip_amount >= 0.0
        if cat.lump_sum_amount is not None:
            assert cat.lump_sum_amount >= 0.0


@pytest.mark.parametrize(
    "persona_id",
    [
        "fresh_graduate",
        "young_couple",
        "small_business",
        "doctor_patna",
    ],
)
def test_total_sip_matches_sum_of_category_allocations(persona_id):
    """Total SIP amount must strictly equal sum of category monthly SIP allocations."""
    p = get_persona(persona_id)
    assessment = SuitabilityEngine.assess(p)
    rec = PortfolioEngine.construct_portfolio(p, assessment)

    assert rec.is_sip is True
    total_allocated_sip = sum(c.monthly_sip_amount for c in rec.category_allocations if c.monthly_sip_amount is not None)
    assert abs(total_allocated_sip - rec.investment_amount) < 0.01


def test_deterministic_sensitivity_to_input_changes():
    """Modifying age, horizon, goal, or savings must deterministically alter calculations."""
    base_p = get_persona("young_couple")
    base_assessment = SuitabilityEngine.assess(base_p)
    base_rec = PortfolioEngine.construct_portfolio(base_p, base_assessment)

    # 1. Changing horizon from 15 to 2 years should reduce equity to <= 20%
    short_p = base_p.model_copy(update={"investment_horizon_years": 2.0})
    short_assessment = SuitabilityEngine.assess(short_p)
    short_rec = PortfolioEngine.construct_portfolio(short_p, short_assessment)
    assert short_rec.equity_pct < base_rec.equity_pct
    assert short_rec.equity_pct == 10.0  # short horizon constraint

    # 2. Changing savings from adequate to zero should trigger emergency shortfall
    zero_sav_p = base_p.model_copy(update={"existing_savings": 0.0})
    zero_sav_assessment = SuitabilityEngine.assess(zero_sav_p)
    zero_sav_rec = PortfolioEngine.construct_portfolio(zero_sav_p, zero_sav_assessment)
    assert zero_sav_assessment.requires_emergency_carveout is True
    assert zero_sav_rec.emergency_carveout_amount > 0.0
    assert base_rec.emergency_carveout_amount == 0.0

    # 3. Changing age from 31 to 68 with monthly income goal enforces conservative SWP allocation
    from src.profiling.models import GoalType
    retiree_p = base_p.model_copy(update={"age": 68, "primary_goal": GoalType.MONTHLY_INCOME})
    retiree_assessment = SuitabilityEngine.assess(retiree_p)
    retiree_rec = PortfolioEngine.construct_portfolio(retiree_p, retiree_assessment)
    assert retiree_rec.equity_pct == 15.0
    assert retiree_rec.debt_pct == 70.0
    assert retiree_rec.liquid_pct == 15.0


