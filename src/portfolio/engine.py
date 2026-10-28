"""Deterministic Goal-Based Mutual Fund Portfolio Construction Engine.

Implements SEBI Categorization (SEBI/HO/IMD/DF3/CIR/P/2017/114) and transparent,
mathematical asset allocation. The LLM never invents percentages; allocations are
derived strictly from suitability assessment, horizon, and goal mechanics.

Portfolio Construction Methodology:
Risk Profile + Goal + Horizon + Liquidity + Constraints -> Deterministic Allocation Engine -> Final Portfolio
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from src.profiling.models import (
    ClientProfile,
    GoalType,
    RiskTolerance,
)
from src.suitability.engine import SuitabilityAssessment


class CategoryAllocation(BaseModel):
    """SEBI-defined mutual fund category allocation item with full audit factors."""

    asset_class: str = Field(..., description="Equity, Debt, Hybrid, Liquid, or Commodities")
    sebi_category: str = Field(..., description="Standard SEBI Scheme Category name (SEBI Circular 2017/114)")
    target_weight_pct: float = Field(..., ge=0.0, le=100.0, description="Target allocation percentage")
    monthly_sip_amount: Optional[float] = Field(default=None, description="Allocated monthly SIP in INR")
    lump_sum_amount: Optional[float] = Field(default=None, description="Allocated lump sum in INR")
    rationale: str = Field(..., description="Goal and asset-class rationale for this category")
    input_factors: List[str] = Field(default_factory=list, description="Client inputs driving this allocation")
    applicable_constraints: List[str] = Field(default_factory=list, description="Model constraints applied")


class PortfolioRecommendation(BaseModel):
    """Complete deterministic portfolio recommendation with audit trail."""

    client_id: str
    client_name: str
    investment_amount: float
    is_sip: bool

    # Broad Asset Class Weights (Must sum to 100.0%)
    equity_pct: float = Field(..., ge=0.0, le=100.0)
    debt_pct: float = Field(..., ge=0.0, le=100.0)
    liquid_pct: float = Field(..., ge=0.0, le=100.0)
    gold_pct: float = Field(..., ge=0.0, le=100.0)

    # Detailed SEBI Categories
    category_allocations: List[CategoryAllocation] = Field(default_factory=list)

    # Methodology and Provenance
    methodology_summary: str = Field(
        default="Risk Profile + Goal + Horizon + Liquidity + Constraints -> Deterministic Allocation Engine -> Final Portfolio",
        description="Core formula pipeline"
    )
    input_factors: List[str] = Field(default_factory=list)
    applicable_constraints: List[str] = Field(default_factory=list)

    # Emergency carveout & Glidepath
    emergency_carveout_amount: float = 0.0
    emergency_carveout_instruction: Optional[str] = None
    glidepath_strategy: str = Field(..., description="De-risking schedule as goal horizon nears")
    calculation_trail: List[str] = Field(default_factory=list)


class PortfolioEngine:
    """Calculates deterministic goal-based asset allocation."""

    METHODOLOGY = (
        "Risk Profile + Goal + Horizon + Liquidity + Constraints "
        "→ Deterministic Allocation Engine → Final Portfolio"
    )

    @classmethod
    def construct_portfolio(
        cls,
        profile: ClientProfile,
        suitability: SuitabilityAssessment,
    ) -> PortfolioRecommendation:
        """Construct deterministic portfolio based on suitability and goal specifications."""
        calc_trail = []
        calc_trail.append(f"Methodology: {cls.METHODOLOGY}")
        calc_trail.append(f"Input Suitability Category: {suitability.final_category.value.title()}")
        calc_trail.append(f"Primary Goal: {profile.primary_goal.value} | Horizon: {profile.investment_horizon_years:.1f} yrs")

        # Capture input factors for auditability
        input_factors = [
            f"Risk Category: {suitability.final_category.value.replace('_', ' ').title()} (Score: {suitability.composite_score:.1f}/100)",
            f"Stated Goal: {profile.primary_goal.value.replace('_', ' ').title()}",
            f"Investment Horizon: {profile.investment_horizon_years:.1f} years",
            f"Liquidity Buffer: {profile.computed_emergency_buffer_months:.1f} months expenses",
            f"Investment Mode: {'Monthly SIP (₹' + f'{profile.investment_amount:,.0f}' + ')' if profile.is_sip else 'Lump Sum (₹' + f'{profile.investment_amount:,.0f}' + ')'}",
        ]

        # Capture applicable constraints
        applicable_constraints = [
            f"Model Equity Cap for {suitability.final_category.value.title()}: Max {suitability.max_equity_pct:.0f}%",
            f"Model Debt/Liquid Floor for {suitability.final_category.value.title()}: Min {suitability.min_debt_pct:.0f}%",
        ]
        if suitability.active_overrides:
            applicable_constraints.extend(suitability.active_overrides)

        # 1. Base Allocation by Suitability Category
        base_allocations = {
            RiskTolerance.CONSERVATIVE: {"equity": 15.0, "debt": 65.0, "liquid": 20.0, "gold": 0.0},
            RiskTolerance.MODERATE: {"equity": 40.0, "debt": 45.0, "liquid": 10.0, "gold": 5.0},
            RiskTolerance.MODERATELY_AGGRESSIVE: {"equity": 65.0, "debt": 25.0, "liquid": 5.0, "gold": 5.0},
            RiskTolerance.AGGRESSIVE: {"equity": 80.0, "debt": 15.0, "liquid": 5.0, "gold": 0.0},
        }

        weights = dict(base_allocations[suitability.final_category])
        calc_trail.append(
            f"Base weights for {suitability.final_category.value}: "
            f"Eq {weights['equity']}%, Debt {weights['debt']}%, Liq {weights['liquid']}%, Gold {weights['gold']}%"
        )

        # 2. Goal-Specific Structural Adjustments
        # Case A: Senior Citizen Monthly Income / Systematic Withdrawal (Retiree Chennai)
        if profile.primary_goal == GoalType.MONTHLY_INCOME and profile.age >= 60:
            weights = {"equity": 15.0, "debt": 70.0, "liquid": 15.0, "gold": 0.0}
            applicable_constraints.append("Retiree Monthly Income Constraint: 15% Liquid SWP buffer, 70% Debt yield, 15% Large Cap hedge.")
            calc_trail.append(
                "Goal Adjustment (Senior Monthly Income): 15% Liquid for SWP liquidity, "
                "70% Short/Corporate Debt for monthly yield, 15% Large Cap Equity for inflation buffer."
            )

        # Case B: Dual Goal with Dedicated Parent Healthcare Buffer (Doctor Patna)
        elif GoalType.HEALTHCARE_BUFFER in profile.secondary_goals:
            weights = {"equity": 15.0, "debt": 60.0, "liquid": 20.0, "gold": 5.0}
            applicable_constraints.append("Healthcare Corpus Carveout: 20% liquid debt earmarked for parent medical liquidity.")
            calc_trail.append(
                "Goal Adjustment (Healthcare Corpus): Earmarked 20% in Liquid/Overnight Funds "
                "for parent healthcare buffer; 60% high-quality debt for capital preservation."
            )

        # Case C: Short Horizon (<= 3 years) Capital Preservation (e.g. Aggressive Trader correction)
        elif profile.investment_horizon_years <= 3.0:
            weights = {"equity": 10.0, "debt": 60.0, "liquid": 30.0, "gold": 0.0}
            applicable_constraints.append("Short Horizon Volatility Constraint: Horizon <= 3 yrs caps equity at 10%.")
            calc_trail.append(
                "Horizon Adjustment (<= 3 years): Volatility mitigation requires 90% in Debt/Liquid, "
                "maximum 10% in large cap equity."
            )

        # Verify weights sum to 100%
        total_w = sum(weights.values())
        assert abs(total_w - 100.0) < 1e-4, f"Weights must sum to 100%, got {total_w}"

        # 3. Handle Emergency Fund Carve-out
        carveout_amount = 0.0
        carveout_instruction = None
        if suitability.requires_emergency_carveout:
            carveout_amount = suitability.emergency_shortfall_amount
            if profile.is_sip:
                carveout_instruction = (
                    f"Priority Routing: Redirect 50% of monthly SIP (₹{profile.investment_amount * 0.5:,.0f}/mo) "
                    f"to Liquid Fund until emergency shortfall of ₹{carveout_amount:,.0f} is fully achieved."
                )
            else:
                carveout_instruction = (
                    f"Immediate Carve-out: Segregate ₹{carveout_amount:,.0f} from the lump sum directly into "
                    "Overnight/Liquid Fund prior to deploying remaining capital."
                )
            calc_trail.append(f"Emergency Carve-out Enforced: ₹{carveout_amount:,.0f}")

        # 4. Map Asset Weights into SEBI Mutual Fund Scheme Categories
        cat_allocations: List[CategoryAllocation] = []
        inv_amt = profile.investment_amount

        # Equity Categories
        eq_wt = weights["equity"]
        if eq_wt > 0:
            if eq_wt <= 20.0:
                cat_allocations.append(
                    CategoryAllocation(
                        asset_class="Equity",
                        sebi_category="Large Cap Fund / Nifty 50 Index",
                        target_weight_pct=eq_wt,
                        monthly_sip_amount=round(inv_amt * (eq_wt / 100.0), 2) if profile.is_sip else None,
                        lump_sum_amount=round(inv_amt * (eq_wt / 100.0), 2) if not profile.is_sip else None,
                        rationale="Low tracking error, blue-chip stability for conservative equity participation.",
                        input_factors=input_factors,
                        applicable_constraints=applicable_constraints,
                    )
                )
            elif eq_wt <= 45.0:
                lc_wt = round(eq_wt * 0.65, 2)
                fc_wt = round(eq_wt - lc_wt, 2)
                cat_allocations.append(
                    CategoryAllocation(
                        asset_class="Equity",
                        sebi_category="Large Cap Fund",
                        target_weight_pct=lc_wt,
                        monthly_sip_amount=round(inv_amt * (lc_wt / 100.0), 2) if profile.is_sip else None,
                        lump_sum_amount=round(inv_amt * (lc_wt / 100.0), 2) if not profile.is_sip else None,
                        rationale="Core large-cap stability with regulated 80%+ top-100 stock allocation.",
                        input_factors=input_factors,
                        applicable_constraints=applicable_constraints,
                    )
                )
                cat_allocations.append(
                    CategoryAllocation(
                        asset_class="Equity",
                        sebi_category="Flexi Cap Fund",
                        target_weight_pct=fc_wt,
                        monthly_sip_amount=round(inv_amt * (fc_wt / 100.0), 2) if profile.is_sip else None,
                        lump_sum_amount=round(inv_amt * (fc_wt / 100.0), 2) if not profile.is_sip else None,
                        rationale="Dynamic multi-cap capitalization flexibility across market cycles.",
                        input_factors=input_factors,
                        applicable_constraints=applicable_constraints,
                    )
                )
            else:
                lc_wt = round(eq_wt * 0.55, 2)
                fc_wt = round(eq_wt * 0.25, 2)
                mc_wt = round(eq_wt - lc_wt - fc_wt, 2)
                cat_allocations.append(
                    CategoryAllocation(
                        asset_class="Equity",
                        sebi_category="Large Cap / Nifty 50 Index Fund",
                        target_weight_pct=lc_wt,
                        monthly_sip_amount=round(inv_amt * (lc_wt / 100.0), 2) if profile.is_sip else None,
                        lump_sum_amount=round(inv_amt * (lc_wt / 100.0), 2) if not profile.is_sip else None,
                        rationale="Core anchor holding providing market index returns with high liquidity.",
                        input_factors=input_factors,
                        applicable_constraints=applicable_constraints,
                    )
                )
                cat_allocations.append(
                    CategoryAllocation(
                        asset_class="Equity",
                        sebi_category="Flexi Cap Fund",
                        target_weight_pct=fc_wt,
                        monthly_sip_amount=round(inv_amt * (fc_wt / 100.0), 2) if profile.is_sip else None,
                        lump_sum_amount=round(inv_amt * (fc_wt / 100.0), 2) if not profile.is_sip else None,
                        rationale="Unconstrained capitalization allocation across large, mid, and small caps.",
                        input_factors=input_factors,
                        applicable_constraints=applicable_constraints,
                    )
                )
                cat_allocations.append(
                    CategoryAllocation(
                        asset_class="Equity",
                        sebi_category="Mid Cap Fund",
                        target_weight_pct=mc_wt,
                        monthly_sip_amount=round(inv_amt * (mc_wt / 100.0), 2) if profile.is_sip else None,
                        lump_sum_amount=round(inv_amt * (mc_wt / 100.0), 2) if not profile.is_sip else None,
                        rationale="Growth alpha generation over long horizon (101st-250th companies).",
                        input_factors=input_factors,
                        applicable_constraints=applicable_constraints,
                    )
                )

        # Debt Categories
        dt_wt = weights["debt"]
        if dt_wt > 0:
            if dt_wt <= 30.0:
                cat_allocations.append(
                    CategoryAllocation(
                        asset_class="Debt",
                        sebi_category="Corporate Bond Fund",
                        target_weight_pct=dt_wt,
                        monthly_sip_amount=round(inv_amt * (dt_wt / 100.0), 2) if profile.is_sip else None,
                        lump_sum_amount=round(inv_amt * (dt_wt / 100.0), 2) if not profile.is_sip else None,
                        rationale="High credit quality (min 80% in AA+ and above rated debt) for portfolio stability.",
                        input_factors=input_factors,
                        applicable_constraints=applicable_constraints,
                    )
                )
            else:
                sd_wt = round(dt_wt * 0.60, 2)
                cb_wt = round(dt_wt - sd_wt, 2)
                cat_allocations.append(
                    CategoryAllocation(
                        asset_class="Debt",
                        sebi_category="Short Duration Fund",
                        target_weight_pct=sd_wt,
                        monthly_sip_amount=round(inv_amt * (sd_wt / 100.0), 2) if profile.is_sip else None,
                        lump_sum_amount=round(inv_amt * (sd_wt / 100.0), 2) if not profile.is_sip else None,
                        rationale="Macaulay duration 1-3 years: mitigates interest rate risk while beating cash yield.",
                        input_factors=input_factors,
                        applicable_constraints=applicable_constraints,
                    )
                )
                cat_allocations.append(
                    CategoryAllocation(
                        asset_class="Debt",
                        sebi_category="Banking & PSU Debt Fund",
                        target_weight_pct=cb_wt,
                        monthly_sip_amount=round(inv_amt * (cb_wt / 100.0), 2) if profile.is_sip else None,
                        lump_sum_amount=round(inv_amt * (cb_wt / 100.0), 2) if not profile.is_sip else None,
                        rationale="Sovereign / PSU backed paper with near-zero credit default risk.",
                        input_factors=input_factors,
                        applicable_constraints=applicable_constraints,
                    )
                )

        # Liquid / Cash Equivalent Categories
        lq_wt = weights["liquid"]
        if lq_wt > 0:
            cat_allocations.append(
                CategoryAllocation(
                    asset_class="Liquid",
                    sebi_category="Liquid Fund",
                    target_weight_pct=lq_wt,
                    monthly_sip_amount=round(inv_amt * (lq_wt / 100.0), 2) if profile.is_sip else None,
                    lump_sum_amount=round(inv_amt * (lq_wt / 100.0), 2) if not profile.is_sip else None,
                    rationale="Macaulay duration up to 91 days: immediate liquidity and capital preservation.",
                    input_factors=input_factors,
                    applicable_constraints=applicable_constraints,
                )
            )

        # Gold / Commodities
        gd_wt = weights["gold"]
        if gd_wt > 0:
            cat_allocations.append(
                CategoryAllocation(
                    asset_class="Commodities",
                    sebi_category="Gold ETF / Fund of Fund",
                    target_weight_pct=gd_wt,
                    monthly_sip_amount=round(inv_amt * (gd_wt / 100.0), 2) if profile.is_sip else None,
                    lump_sum_amount=round(inv_amt * (gd_wt / 100.0), 2) if not profile.is_sip else None,
                    rationale="Hedge against currency depreciation and geopolitical tail risks (non-correlated asset).",
                    input_factors=input_factors,
                    applicable_constraints=applicable_constraints,
                )
            )

        # Ensure category weights and amounts balance exactly to total targets
        if cat_allocations:
            cat_sum = sum(c.target_weight_pct for c in cat_allocations)
            diff_wt = round(100.0 - cat_sum, 2)
            if abs(diff_wt) > 0:
                cat_allocations[-1].target_weight_pct = round(cat_allocations[-1].target_weight_pct + diff_wt, 2)

            if profile.is_sip:
                sip_sum = sum(c.monthly_sip_amount for c in cat_allocations if c.monthly_sip_amount is not None)
                diff_sip = round(inv_amt - sip_sum, 2)
                if abs(diff_sip) > 0 and cat_allocations[-1].monthly_sip_amount is not None:
                    cat_allocations[-1].monthly_sip_amount = round(cat_allocations[-1].monthly_sip_amount + diff_sip, 2)
            else:
                lump_sum = sum(c.lump_sum_amount for c in cat_allocations if c.lump_sum_amount is not None)
                diff_lump = round(inv_amt - lump_sum, 2)
                if abs(diff_lump) > 0 and cat_allocations[-1].lump_sum_amount is not None:
                    cat_allocations[-1].lump_sum_amount = round(cat_allocations[-1].lump_sum_amount + diff_lump, 2)

        # 5. Formulate Glidepath Strategy
        h = profile.investment_horizon_years
        if h > 10:
            glidepath = (
                f"Horizon is {h:.0f} years. Maintain growth allocation for initial {h - 4:.0f} years. "
                "At T-3 years to goal, systematically shift 20% equity annually into Short Duration / Liquid funds "
                "to immunize the target corpus against market down-cycles."
            )
        elif h > 5:
            glidepath = (
                f"Horizon is {h:.0f} years. Maintain allocation for {h - 2:.0f} years. "
                "Shift 25% equity per year to liquid/debt over the final 2 years before goal maturity."
            )
        else:
            glidepath = (
                f"Short horizon of {h:.1f} years. Strictly retain debt and liquid majority; "
                "do not increase equity exposure."
            )

        return PortfolioRecommendation(
            client_id=profile.client_id,
            client_name=profile.name,
            investment_amount=profile.investment_amount,
            is_sip=profile.is_sip,
            equity_pct=weights["equity"],
            debt_pct=weights["debt"],
            liquid_pct=weights["liquid"],
            gold_pct=weights["gold"],
            category_allocations=cat_allocations,
            methodology_summary=cls.METHODOLOGY,
            input_factors=input_factors,
            applicable_constraints=applicable_constraints,
            emergency_carveout_amount=carveout_amount,
            emergency_carveout_instruction=carveout_instruction,
            glidepath_strategy=glidepath,
            calculation_trail=calc_trail,
        )
