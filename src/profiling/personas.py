"""Official hackathon target personas from the PS4 rulebook."""

from typing import Dict
from src.profiling.models import (
    CashFlowStability,
    ClientProfile,
    GoalType,
    RiskTolerance,
)

TARGET_PERSONAS: Dict[str, ClientProfile] = {
    "fresh_graduate": ClientProfile(
        client_id="fresh_graduate",
        name="Aarav Sharma (Fresh Graduate)",
        age=23,
        monthly_income=55_000.0,
        monthly_expenses=25_000.0,
        monthly_debt_obligations=0.0,
        existing_savings=50_000.0,  # ~2.0 months: needs emergency fund top-up to 3-6 months
        existing_investments=10_000.0,
        total_liabilities=0.0,
        investment_amount=15_000.0,
        is_sip=True,
        investment_horizon_years=10.0,
        primary_goal=GoalType.EMERGENCY_FUND,
        secondary_goals=[GoalType.LONG_TERM_WEALTH],
        stated_risk_tolerance=RiskTolerance.MODERATELY_AGGRESSIVE,
        cash_flow_stability=CashFlowStability.STABLE_SALARIED,
        has_emergency_fund=False,
        past_fo_drawdown=False,
        notes="Early career. Must build ₹75k-₹1.5L emergency buffer before heavy equity deployment.",
    ),
    "young_couple": ClientProfile(
        client_id="young_couple",
        name="Vikram & Neha (Young Couple)",
        age=31,
        monthly_income=180_000.0,
        monthly_expenses=65_000.0,
        monthly_debt_obligations=45_000.0,  # Home loan EMI
        existing_savings=350_000.0,  # ~5.3 months: adequate emergency fund
        existing_investments=600_000.0,
        total_liabilities=4_500_000.0,  # Outstanding home loan
        investment_amount=40_000.0,
        is_sip=True,
        investment_horizon_years=15.0,
        primary_goal=GoalType.CHILD_EDUCATION,
        secondary_goals=[GoalType.LONG_TERM_WEALTH],
        stated_risk_tolerance=RiskTolerance.MODERATELY_AGGRESSIVE,
        cash_flow_stability=CashFlowStability.DUAL_INCOME_SALARIED,
        has_emergency_fund=True,
        past_fo_drawdown=False,
        notes="Dual income with long 15-year horizon for child education. Significant debt service obligations.",
    ),
    "small_business": ClientProfile(
        client_id="small_business",
        name="Rajesh Patel (Small Business Owner)",
        age=44,
        monthly_income=160_000.0,  # Average monthly draw
        monthly_expenses=70_000.0,
        monthly_debt_obligations=15_000.0,  # Equipment loan
        existing_savings=500_000.0,  # ~7.1 months buffer required due to irregular cash flows
        existing_investments=1_200_000.0,
        total_liabilities=1_000_000.0,
        investment_amount=35_000.0,
        is_sip=True,
        investment_horizon_years=14.0,  # Planning retirement at age 58
        primary_goal=GoalType.RETIREMENT,
        secondary_goals=[GoalType.CAPITAL_PRESERVATION],
        stated_risk_tolerance=RiskTolerance.MODERATE,
        cash_flow_stability=CashFlowStability.IRREGULAR_BUSINESS,
        has_emergency_fund=True,
        past_fo_drawdown=False,
        notes="Irregular cash flows necessitate higher liquidity buffer. 14 years remaining until age 58 retirement.",
    ),
    "doctor_patna": ClientProfile(
        client_id="doctor_patna",
        name="Dr. Alok Verma (Doctor, Patna)",
        age=38,
        monthly_income=320_000.0,
        monthly_expenses=85_000.0,
        monthly_debt_obligations=0.0,
        existing_savings=2_000_000.0,
        existing_investments=4_500_000.0,
        total_liabilities=0.0,
        investment_amount=120_000.0,
        is_sip=True,
        investment_horizon_years=12.0,
        primary_goal=GoalType.RETIREMENT,
        secondary_goals=[GoalType.HEALTHCARE_BUFFER],
        stated_risk_tolerance=RiskTolerance.CONSERVATIVE,  # High income but strictly risk-averse
        cash_flow_stability=CashFlowStability.HIGH_PROFESSIONAL,
        has_emergency_fund=True,
        past_fo_drawdown=False,
        notes="High earning professional with strong savings capacity, but inherently risk-averse. Priority on parent healthcare corpus & capital safety.",
    ),
    "retiree_chennai": ClientProfile(
        client_id="retiree_chennai",
        name="S. Sundaram (Retiree, Chennai)",
        age=68,
        monthly_income=28_000.0,  # Monthly pension
        monthly_expenses=55_000.0,  # Net monthly cash deficit of ₹27,000 needing systematic withdrawal
        monthly_debt_obligations=0.0,
        existing_savings=500_000.0,
        existing_investments=8_000_000.0,  # ₹80L retirement corpus
        total_liabilities=0.0,
        investment_amount=8_000_000.0,  # Allocating ₹80L corpus for 25 years systematic monthly income
        is_sip=False,  # Lump sum allocation
        investment_horizon_years=25.0,
        primary_goal=GoalType.MONTHLY_INCOME,
        secondary_goals=[GoalType.CAPITAL_PRESERVATION],
        stated_risk_tolerance=RiskTolerance.CONSERVATIVE,
        cash_flow_stability=CashFlowStability.PENSION_FIXED,
        has_emergency_fund=True,
        past_fo_drawdown=False,
        notes="Senior citizen requiring guaranteed monthly income for 25 years from ₹80L corpus + pension. Strict preservation mandate.",
    ),
    "aggressive_trader": ClientProfile(
        client_id="aggressive_trader",
        name="Karan Malhotra (Aggressive Trader)",
        age=29,
        monthly_income=120_000.0,
        monthly_expenses=55_000.0,
        monthly_debt_obligations=15_000.0,  # Personal loan
        existing_savings=100_000.0,  # Only 1.8 months buffer!
        existing_investments=400_000.0,
        total_liabilities=300_000.0,
        investment_amount=40_000.0,
        is_sip=True,
        investment_horizon_years=3.0,  # Short horizon + aggressive stated appetite = high risk mismatch
        primary_goal=GoalType.AGGRESSIVE_GROWTH,
        secondary_goals=[],
        stated_risk_tolerance=RiskTolerance.AGGRESSIVE,
        cash_flow_stability=CashFlowStability.STABLE_SALARIED,
        has_emergency_fund=False,
        past_fo_drawdown=True,  # F&O losses history
        notes="Past F&O drawdown history with high stated risk and short horizon. Must enforce suitability cap and risk mismatch warnings.",
    ),
}


def get_persona(client_id: str) -> ClientProfile:
    """Retrieve a copy of a pre-configured target persona."""
    if client_id not in TARGET_PERSONAS:
        raise KeyError(
            f"Persona '{client_id}' not found. Available personas: {list(TARGET_PERSONAS.keys())}"
        )
    return TARGET_PERSONAS[client_id].model_copy(deep=True)


def get_all_personas() -> Dict[str, ClientProfile]:
    """Retrieve all target personas."""
    return {k: v.model_copy(deep=True) for k, v in TARGET_PERSONAS.items()}

