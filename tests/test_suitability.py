"""Unit tests for deterministic SEBI RIA Suitability Engine."""

from src.profiling import RiskTolerance, get_persona
from src.suitability import SuitabilityEngine


def test_fresh_graduate_suitability():
    """Fresh graduate must trigger emergency carve-out before long-term wealth deployment."""
    p = get_persona("fresh_graduate")
    assessment = SuitabilityEngine.assess(p)

    assert assessment.requires_emergency_carveout is True
    assert assessment.emergency_shortfall_amount == 25_000.0  # (3 - 2) * 25k
    assert "LIQUIDITY_BUFFER_DEFICIT" in assessment.risk_flags
    assert len(assessment.active_overrides) >= 1


def test_young_couple_suitability():
    """Young couple with 15-year horizon and adequate buffer should be Moderately Aggressive."""
    p = get_persona("young_couple")
    assessment = SuitabilityEngine.assess(p)

    assert assessment.requires_emergency_carveout is False
    assert assessment.final_category == RiskTolerance.MODERATELY_AGGRESSIVE
    assert assessment.max_equity_pct == 70.0
    assert assessment.min_debt_pct == 25.0


def test_small_business_suitability():
    """Small business with irregular cash flows is assessed with appropriate liquidity buffer."""
    p = get_persona("small_business")
    assessment = SuitabilityEngine.assess(p)

    assert assessment.requires_emergency_carveout is False
    assert assessment.final_category == RiskTolerance.MODERATE
    assert assessment.max_equity_pct == 45.0


def test_doctor_patna_suitability_conservatism():
    """Doctor with high capacity but conservative appetite must NOT be pushed into aggressive products."""
    p = get_persona("doctor_patna")
    assessment = SuitabilityEngine.assess(p)

    # Stated risk cap must be enforced
    assert assessment.final_category == RiskTolerance.CONSERVATIVE
    assert assessment.max_equity_pct == 20.0
    assert "STATED_RISK_CAP_ENFORCED" in assessment.risk_flags


def test_retiree_chennai_preservation_override():
    """Senior citizen needing regular monthly income must have capital preservation override."""
    p = get_persona("retiree_chennai")
    assessment = SuitabilityEngine.assess(p)

    assert assessment.final_category == RiskTolerance.CONSERVATIVE
    assert "RETIREE_CAPITAL_PRESERVATION" in assessment.risk_flags
    assert assessment.max_equity_pct == 20.0
    assert assessment.min_debt_pct >= 75.0


def test_aggressive_trader_suitability_enforcement():
    """Aggressive trader with past F&O losses and short horizon must have overrides and warnings."""
    p = get_persona("aggressive_trader")
    assessment = SuitabilityEngine.assess(p)

    assert "PAST_FO_DRAWDOWN_FLAG" in assessment.risk_flags
    assert "SHORT_HORIZON_EQUITY_RESTRICTION" in assessment.risk_flags
    # Under-buffered
    assert assessment.requires_emergency_carveout is True
    # Final category is strictly prevented from being Aggressive
    assert assessment.final_category != RiskTolerance.AGGRESSIVE
    assert assessment.max_equity_pct <= 45.0


def test_score_ranges_and_determinism():
    """All dimension scores must lie strictly between 0 and 100 and produce repeatable outputs."""
    p = get_persona("fresh_graduate")
    a1 = SuitabilityEngine.assess(p)
    a2 = SuitabilityEngine.assess(p)

    assert a1.composite_score == a2.composite_score
    assert 0.0 <= a1.capacity_score <= 100.0
    assert 0.0 <= a1.tolerance_score <= 100.0
    assert 0.0 <= a1.horizon_score <= 100.0
    assert 0.0 <= a1.liquidity_score <= 100.0
    assert 0.0 <= a1.composite_score <= 100.0

