"""Unit tests for client profiling and target personas."""

import pytest
from pydantic import ValidationError

from src.profiling import (
    CashFlowStability,
    ClientProfile,
    GoalType,
    RiskTolerance,
    TARGET_PERSONAS,
    get_all_personas,
    get_persona,
)


def test_all_target_personas_exist():
    """Verify that all 6 rulebook personas are defined and valid."""
    expected_keys = {
        "fresh_graduate",
        "young_couple",
        "small_business",
        "doctor_patna",
        "retiree_chennai",
        "aggressive_trader",
    }
    personas = get_all_personas()
    assert set(personas.keys()) == expected_keys
    for key in expected_keys:
        p = get_persona(key)
        assert isinstance(p, ClientProfile)
        assert p.client_id == key


def test_fresh_graduate_persona():
    """Verify Fresh Graduate specific metrics."""
    p = get_persona("fresh_graduate")
    assert p.age == 23
    assert p.monthly_income == 55_000.0
    assert p.monthly_expenses == 25_000.0
    assert p.computed_emergency_buffer_months == 2.0  # ₹50k / ₹25k = 2.0 months (< 3-6 months)
    assert p.net_monthly_surplus == 30_000.0
    assert p.savings_rate == round(30_000.0 / 55_000.0, 4)
    assert p.primary_goal == GoalType.EMERGENCY_FUND


def test_young_couple_persona():
    """Verify Young Couple dual-income and debt-servicing ratio."""
    p = get_persona("young_couple")
    assert p.age == 31
    assert p.cash_flow_stability == CashFlowStability.DUAL_INCOME_SALARIED
    assert p.debt_to_income_ratio == 0.25  # 45k / 180k
    assert p.computed_emergency_buffer_months >= 5.0
    assert p.investment_horizon_years == 15.0


def test_small_business_persona():
    """Verify Small Business Owner profile parameters."""
    p = get_persona("small_business")
    assert p.age == 44
    assert p.cash_flow_stability == CashFlowStability.IRREGULAR_BUSINESS
    assert p.investment_horizon_years == 14.0  # Retiring at age 58
    assert p.computed_emergency_buffer_months >= 7.0  # Adequate buffer for irregular income


def test_doctor_patna_persona():
    """Verify Doctor Patna profile (high earner, risk-averse)."""
    p = get_persona("doctor_patna")
    assert p.age == 38
    assert p.stated_risk_tolerance == RiskTolerance.CONSERVATIVE
    assert p.monthly_income == 320_000.0
    assert p.investment_amount == 120_000.0
    assert GoalType.HEALTHCARE_BUFFER in p.secondary_goals


def test_retiree_chennai_persona():
    """Verify Retiree Chennai corpus and systematic monthly cash flow requirement."""
    p = get_persona("retiree_chennai")
    assert p.age == 68
    assert p.is_sip is False
    assert p.investment_amount == 8_000_000.0  # ₹80L corpus
    assert p.stated_risk_tolerance == RiskTolerance.CONSERVATIVE
    assert p.primary_goal == GoalType.MONTHLY_INCOME


def test_aggressive_trader_persona():
    """Verify Aggressive Trader profile has past F&O drawdown flag set."""
    p = get_persona("aggressive_trader")
    assert p.past_fo_drawdown is True
    assert p.stated_risk_tolerance == RiskTolerance.AGGRESSIVE
    assert p.investment_horizon_years == 3.0
    assert p.computed_emergency_buffer_months < 2.0  # Under-buffered


def test_client_profile_validation():
    """Verify Pydantic validation rejects illegal values."""
    # Negative income
    with pytest.raises(ValidationError):
        ClientProfile(
            client_id="test_invalid",
            name="Invalid",
            age=30,
            monthly_income=-5000.0,
            monthly_expenses=2000.0,
            existing_savings=10000.0,
            investment_amount=5000.0,
            investment_horizon_years=5.0,
            primary_goal=GoalType.LONG_TERM_WEALTH,
            stated_risk_tolerance=RiskTolerance.MODERATE,
        )

    # Invalid age (under 18)
    with pytest.raises(ValidationError):
        ClientProfile(
            client_id="test_underage",
            name="Underage",
            age=16,
            monthly_income=20000.0,
            monthly_expenses=10000.0,
            existing_savings=5000.0,
            investment_amount=2000.0,
            investment_horizon_years=5.0,
            primary_goal=GoalType.LONG_TERM_WEALTH,
            stated_risk_tolerance=RiskTolerance.MODERATE,
        )

    # Zero or negative horizon
    with pytest.raises(ValidationError):
        ClientProfile(
            client_id="test_zero_horizon",
            name="Zero Horizon",
            age=30,
            monthly_income=50000.0,
            monthly_expenses=20000.0,
            existing_savings=10000.0,
            investment_amount=5000.0,
            investment_horizon_years=0.0,
            primary_goal=GoalType.LONG_TERM_WEALTH,
            stated_risk_tolerance=RiskTolerance.MODERATE,
        )

