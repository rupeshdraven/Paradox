"""Deterministic, inspectable Suitability Engine for SEBI-Registered Investment Advisers.

Implements inspectable suitability scoring aligned with SEBI (Investment Advisers) Regulations, 2013:
- Fully mathematical and rule-based
- Explicit scoring weights and transparent arithmetic
- System Suitability Guardrails & Model-Imposed Constraints
- Prohibits non-deterministic LLM scoring
"""

from typing import Dict, List, Tuple
from pydantic import BaseModel, Field

from src.profiling.models import (
    CashFlowStability,
    ClientProfile,
    GoalType,
    RiskTolerance,
)


class SuitabilityAssessment(BaseModel):
    """Result of deterministic suitability assessment with complete calculation transparency."""

    client_id: str
    client_name: str

    # Dimension scores (0.0 to 100.0)
    capacity_score: float = Field(..., ge=0.0, le=100.0, description="Financial loss-absorption ability")
    tolerance_score: float = Field(..., ge=0.0, le=100.0, description="Psychological risk appetite")
    horizon_score: float = Field(..., ge=0.0, le=100.0, description="Goal time-horizon runway")
    liquidity_score: float = Field(..., ge=0.0, le=100.0, description="Emergency buffer adequacy")
    composite_score: float = Field(..., ge=0.0, le=100.0, description="Weighted composite suitability score")

    # Transparent calculation formula & weights
    weights: Dict[str, float] = Field(default_factory=dict, description="Dimension weights summing to 1.0")
    score_formula: str = Field(..., description="Verifiable mathematical calculation string")

    # Risk categorization
    raw_category: RiskTolerance = Field(..., description="Unconstrained score-derived category")
    final_category: RiskTolerance = Field(..., description="Guardrail-adjusted approved category")
    guardrail_adjusted_category: RiskTolerance = Field(..., description="Alias for final approved category")

    # Model-Imposed Asset Class Exposure Limits (Not statutory SEBI mandates)
    max_equity_pct: float = Field(..., ge=0.0, le=100.0, description="Model-imposed equity ceiling")
    min_debt_pct: float = Field(..., ge=0.0, le=100.0, description="Model-imposed debt/liquid floor")

    # Emergency carve-out requirements
    requires_emergency_carveout: bool = False
    emergency_shortfall_amount: float = 0.0

    # Compliance flags and audit trail
    active_overrides: List[str] = Field(default_factory=list)
    risk_flags: List[str] = Field(default_factory=list)
    scoring_breakdown: List[str] = Field(default_factory=list)


class SuitabilityEngine:
    """Rules-based engine calculating verifiable client risk suitability."""

    # Dimension Weights (Total = 1.0)
    WEIGHT_CAPACITY: float = 0.30
    WEIGHT_TOLERANCE: float = 0.25
    WEIGHT_HORIZON: float = 0.25
    WEIGHT_LIQUIDITY: float = 0.20

    @classmethod
    def score_capacity(cls, profile: ClientProfile) -> Tuple[float, List[str]]:
        """Compute financial capacity to absorb losses (0-100)."""
        reasons = []

        # Age component (max 30 pts)
        if profile.age < 30:
            age_pts = 30.0
            reasons.append("Age < 30: High recovery runway (+30 pts)")
        elif profile.age <= 45:
            age_pts = 22.0
            reasons.append("Age 30-45: Moderate career runway (+22 pts)")
        elif profile.age <= 60:
            age_pts = 14.0
            reasons.append("Age 46-60: Approaching retirement runway (+14 pts)")
        else:
            age_pts = 6.0
            reasons.append("Age > 60: Post-retirement preservation runway (+6 pts)")

        # Savings rate component (max 30 pts)
        rate = profile.savings_rate
        if rate >= 0.40:
            save_pts = 30.0
            reasons.append(f"Savings rate {rate:.1%}: Excellent surplus (+30 pts)")
        elif rate >= 0.25:
            save_pts = 22.0
            reasons.append(f"Savings rate {rate:.1%}: Solid surplus (+22 pts)")
        elif rate >= 0.10:
            save_pts = 14.0
            reasons.append(f"Savings rate {rate:.1%}: Modest surplus (+14 pts)")
        else:
            save_pts = 6.0
            reasons.append(f"Savings rate {rate:.1%}: Low surplus (+6 pts)")

        # Debt obligation component (max 20 pts)
        dti = profile.debt_to_income_ratio
        if dti == 0.0:
            debt_pts = 20.0
            reasons.append("Zero debt obligations (+20 pts)")
        elif dti <= 0.20:
            debt_pts = 15.0
            reasons.append(f"Low DTI {dti:.1%}: Controlled leverage (+15 pts)")
        elif dti <= 0.40:
            debt_pts = 10.0
            reasons.append(f"Moderate DTI {dti:.1%}: Significant debt servicing (+10 pts)")
        else:
            debt_pts = 3.0
            reasons.append(f"High DTI {dti:.1%}: High debt servicing vulnerability (+3 pts)")

        # Income stability component (max 20 pts)
        stability_map = {
            CashFlowStability.DUAL_INCOME_SALARIED: (20.0, "Dual salaried income: Maximum stability (+20 pts)"),
            CashFlowStability.HIGH_PROFESSIONAL: (18.0, "High earning professional: High stability (+18 pts)"),
            CashFlowStability.PENSION_FIXED: (16.0, "Guaranteed fixed pension: High predictability (+16 pts)"),
            CashFlowStability.STABLE_SALARIED: (15.0, "Stable salaried income: Good stability (+15 pts)"),
            CashFlowStability.IRREGULAR_BUSINESS: (8.0, "Irregular business cash flows: High variance (+8 pts)"),
        }
        stab_pts, stab_msg = stability_map.get(
            profile.cash_flow_stability, (12.0, "Standard stability (+12 pts)")
        )
        reasons.append(stab_msg)

        total_capacity = age_pts + save_pts + debt_pts + stab_pts
        return round(total_capacity, 2), reasons

    @classmethod
    def score_tolerance(cls, profile: ClientProfile) -> Tuple[float, List[str]]:
        """Score psychological willingness to accept volatility (0-100)."""
        reasons = []
        tolerance_map = {
            RiskTolerance.CONSERVATIVE: (20.0, "Stated appetite: Conservative / Risk-averse (20 pts)"),
            RiskTolerance.MODERATE: (50.0, "Stated appetite: Moderate (50 pts)"),
            RiskTolerance.MODERATELY_AGGRESSIVE: (75.0, "Stated appetite: Moderately Aggressive (75 pts)"),
            RiskTolerance.AGGRESSIVE: (95.0, "Stated appetite: Aggressive (95 pts)"),
        }
        score, msg = tolerance_map.get(profile.stated_risk_tolerance, (50.0, "Default moderate"))
        reasons.append(msg)
        return score, reasons

    @classmethod
    def score_horizon(cls, profile: ClientProfile) -> Tuple[float, List[str]]:
        """Score horizon capacity (0-100)."""
        h = profile.investment_horizon_years
        reasons = []
        if h < 1.0:
            score = 10.0
            reasons.append("Horizon < 1 year: Ultra-short, capital preservation vital (10 pts)")
        elif h < 3.0:
            score = 25.0
            reasons.append("Horizon 1-3 years: Short-term, vulnerable to equity drawdowns (25 pts)")
        elif h < 7.0:
            score = 55.0
            reasons.append("Horizon 3-7 years: Medium-term, balanced growth permitted (55 pts)")
        elif h < 12.0:
            score = 80.0
            reasons.append("Horizon 7-12 years: Long-term, full market cycle runway (80 pts)")
        else:
            score = 95.0
            reasons.append("Horizon 12+ years: Multi-cycle long-term compounding (95 pts)")
        return score, reasons

    @classmethod
    def score_liquidity(cls, profile: ClientProfile) -> Tuple[float, List[str]]:
        """Score emergency fund adequacy (0-100)."""
        months = profile.computed_emergency_buffer_months
        reasons = []
        if months < 2.0:
            score = 15.0
            reasons.append(f"Emergency buffer {months:.1f} mo: Severely under-reserved (15 pts)")
        elif months < 3.0:
            score = 40.0
            reasons.append(f"Emergency buffer {months:.1f} mo: Below standard 3-6 mo reserve threshold (40 pts)")
        elif months <= 6.0:
            score = 80.0
            reasons.append(f"Emergency buffer {months:.1f} mo: Well-buffered 3-6 mo reserve (80 pts)")
        else:
            score = 95.0
            reasons.append(f"Emergency buffer {months:.1f} mo: Surplus liquidity buffer (95 pts)")
        return score, reasons

    @classmethod
    def assess(cls, profile: ClientProfile) -> SuitabilityAssessment:
        """Execute full deterministic suitability evaluation with system guardrails."""
        cap_score, cap_reasons = cls.score_capacity(profile)
        tol_score, tol_reasons = cls.score_tolerance(profile)
        hor_score, hor_reasons = cls.score_horizon(profile)
        liq_score, liq_reasons = cls.score_liquidity(profile)

        composite = round(
            cls.WEIGHT_CAPACITY * cap_score
            + cls.WEIGHT_TOLERANCE * tol_score
            + cls.WEIGHT_HORIZON * hor_score
            + cls.WEIGHT_LIQUIDITY * liq_score,
            2,
        )

        formula_str = (
            f"Composite ({composite:.2f}) = 0.30 * {cap_score:.1f} (Capacity) + "
            f"0.25 * {tol_score:.1f} (Tolerance) + "
            f"0.25 * {hor_score:.1f} (Horizon) + "
            f"0.20 * {liq_score:.1f} (Liquidity)"
        )

        # Base category mapping
        if composite < 35.0:
            raw_cat = RiskTolerance.CONSERVATIVE
        elif composite < 55.0:
            raw_cat = RiskTolerance.MODERATE
        elif composite < 75.0:
            raw_cat = RiskTolerance.MODERATELY_AGGRESSIVE
        else:
            raw_cat = RiskTolerance.AGGRESSIVE

        final_cat = raw_cat
        active_overrides = []
        risk_flags = []
        requires_emergency_carveout = False
        emergency_shortfall = 0.0

        # Risk hierarchy for comparison
        risk_rank = {
            RiskTolerance.CONSERVATIVE: 1,
            RiskTolerance.MODERATE: 2,
            RiskTolerance.MODERATELY_AGGRESSIVE: 3,
            RiskTolerance.AGGRESSIVE: 4,
        }

        # GUARDRAIL 1: Model-Imposed Liquidity Buffer Shortfall (< target months)
        target_buffer_months = 6.0 if profile.cash_flow_stability == CashFlowStability.IRREGULAR_BUSINESS else 3.0
        if profile.computed_emergency_buffer_months < target_buffer_months:
            requires_emergency_carveout = True
            shortfall_months = target_buffer_months - profile.computed_emergency_buffer_months
            emergency_shortfall = round(shortfall_months * profile.monthly_expenses, 2)
            active_overrides.append(
                f"System Suitability Guardrail (Liquidity): Liquid reserves ({profile.computed_emergency_buffer_months:.1f} mo) "
                f"below model-recommended buffer ({target_buffer_months:.0f} mo). ₹{emergency_shortfall:,.0f} "
                "must be allocated to liquid/overnight funds before equity exposure."
            )
            risk_flags.append("LIQUIDITY_BUFFER_DEFICIT")

        # GUARDRAIL 2: Model-Imposed Senior Citizen Capital Preservation Rule
        if profile.age >= 60 and profile.primary_goal in (
            GoalType.MONTHLY_INCOME,
            GoalType.CAPITAL_PRESERVATION,
            GoalType.RETIREMENT,
        ):
            if risk_rank[final_cat] > risk_rank[RiskTolerance.MODERATE]:
                final_cat = RiskTolerance.MODERATE
                active_overrides.append(
                    f"Model-Imposed Constraint (Age {profile.age}): Senior citizen wealth preservation mandate "
                    "caps equity exposure at Moderate."
                )
            if profile.primary_goal == GoalType.MONTHLY_INCOME:
                final_cat = RiskTolerance.CONSERVATIVE
                active_overrides.append(
                    "Model-Imposed Constraint: Client requires 25-year regular monthly income; "
                    "suitability restricted to Conservative."
                )
            risk_flags.append("RETIREE_CAPITAL_PRESERVATION")

        # GUARDRAIL 3: Model-Imposed Horizon-Risk Alignment (<= 3.0 years)
        if profile.investment_horizon_years <= 3.0:
            if risk_rank[final_cat] > risk_rank[RiskTolerance.CONSERVATIVE]:
                final_cat = RiskTolerance.CONSERVATIVE
                active_overrides.append(
                    f"Model-Imposed Constraint: Investment horizon ({profile.investment_horizon_years:.1f} yrs) "
                    "is short-term and cannot absorb equity market cycles. Restricted to Conservative."
                )
            risk_flags.append("SHORT_HORIZON_EQUITY_RESTRICTION")

        # GUARDRAIL 4: Speculative Risk Mitigation (Past F&O Drawdowns)
        if profile.past_fo_drawdown:
            risk_flags.append("PAST_FO_DRAWDOWN_FLAG")
            risk_flags.append("SPECULATIVE_TRADING_MISMATCH")
            if risk_rank[final_cat] > risk_rank[RiskTolerance.MODERATE]:
                final_cat = RiskTolerance.MODERATE
                active_overrides.append(
                    "System Suitability Guardrail: Past F&O trading losses indicate vulnerability to speculative drawdowns. "
                    "Core portfolio restricted to Moderate; high-risk speculative exposure barred."
                )

        # GUARDRAIL 5: Fiduciary Stated Risk Ceiling Principle
        if risk_rank[final_cat] > risk_rank[profile.stated_risk_tolerance]:
            final_cat = profile.stated_risk_tolerance
            active_overrides.append(
                f"Fiduciary Conservatism Guardrail: Suitability capped at client's self-declared risk appetite "
                f"({profile.stated_risk_tolerance.value.replace('_', ' ').title()})."
            )
            risk_flags.append("STATED_RISK_CAP_ENFORCED")

        # Model-Imposed Asset Class Exposure Limits (Quantitative Risk Budgeting)
        equity_caps = {
            RiskTolerance.CONSERVATIVE: (20.0, 75.0),  # Max 20% equity, Min 75% debt/liquid
            RiskTolerance.MODERATE: (45.0, 50.0),      # Max 45% equity, Min 50% debt/hybrid
            RiskTolerance.MODERATELY_AGGRESSIVE: (70.0, 25.0), # Max 70% equity, Min 25% debt/fixed
            RiskTolerance.AGGRESSIVE: (85.0, 15.0),    # Max 85% equity, Min 15% debt/liquid
        }
        max_eq, min_dt = equity_caps[final_cat]

        scoring_breakdown = [
            f"Capacity Score: {cap_score:.1f}/100 (Weight: {cls.WEIGHT_CAPACITY:.0%})",
            f"Tolerance Score: {tol_score:.1f}/100 (Weight: {cls.WEIGHT_TOLERANCE:.0%})",
            f"Horizon Score: {hor_score:.1f}/100 (Weight: {cls.WEIGHT_HORIZON:.0%})",
            f"Liquidity Score: {liq_score:.1f}/100 (Weight: {cls.WEIGHT_LIQUIDITY:.0%})",
            f"Arithmetic: {formula_str}",
            f"Raw Category: {raw_cat.value.replace('_', ' ').title()}",
            f"Guardrail-Adjusted Category: {final_cat.value.replace('_', ' ').title()}",
        ]

        return SuitabilityAssessment(
            client_id=profile.client_id,
            client_name=profile.name,
            capacity_score=cap_score,
            tolerance_score=tol_score,
            horizon_score=hor_score,
            liquidity_score=liq_score,
            composite_score=composite,
            weights={
                "capacity": cls.WEIGHT_CAPACITY,
                "tolerance": cls.WEIGHT_TOLERANCE,
                "horizon": cls.WEIGHT_HORIZON,
                "liquidity": cls.WEIGHT_LIQUIDITY,
            },
            score_formula=formula_str,
            raw_category=raw_cat,
            final_category=final_cat,
            guardrail_adjusted_category=final_cat,
            max_equity_pct=max_eq,
            min_debt_pct=min_dt,
            requires_emergency_carveout=requires_emergency_carveout,
            emergency_shortfall_amount=emergency_shortfall,
            active_overrides=active_overrides,
            risk_flags=risk_flags,
            scoring_breakdown=scoring_breakdown,
        )
