"""Client profiling data models for SEBI RIA compliance."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, computed_field, model_validator


class GoalType(str, Enum):
    """SEBI-recognized financial advisory goal categories."""
    EMERGENCY_FUND = "emergency_fund"
    LONG_TERM_WEALTH = "long_term_wealth"
    CHILD_EDUCATION = "child_education"
    RETIREMENT = "retirement"
    HEALTHCARE_BUFFER = "healthcare_buffer"
    MONTHLY_INCOME = "monthly_income"
    CAPITAL_PRESERVATION = "capital_preservation"
    AGGRESSIVE_GROWTH = "aggressive_growth"


class RiskTolerance(str, Enum):
    """Stated subjective risk appetite."""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    MODERATELY_AGGRESSIVE = "moderately_aggressive"
    AGGRESSIVE = "aggressive"


class CashFlowStability(str, Enum):
    """Cash flow predictability and employment stability."""
    STABLE_SALARIED = "stable_salaried"
    DUAL_INCOME_SALARIED = "dual_income_salaried"
    HIGH_PROFESSIONAL = "high_professional"
    IRREGULAR_BUSINESS = "irregular_business"
    PENSION_FIXED = "pension_fixed"


class ClientProfile(BaseModel):
    """Comprehensive client profile designed with reference to SEBI (Investment Advisers) Regulations, 2013, Regulation 16 (Risk Profiling).

    Captures financial capacity, obligations, liquidity buffers, and self-reported risk.
    """

    # Identification
    client_id: str = Field(..., description="Unique client identifier or persona key")
    name: str = Field(..., description="Client legal / display name")
    age: int = Field(..., ge=18, le=100, description="Client age (18-100)")

    # Cash Flow & Balance Sheet (all in INR)
    monthly_income: float = Field(..., ge=0.0, description="Net monthly take-home income")
    monthly_expenses: float = Field(..., ge=0.0, description="Essential monthly living expenses")
    monthly_debt_obligations: float = Field(
        default=0.0, ge=0.0, description="Monthly loan EMIs / servicing costs"
    )
    existing_savings: float = Field(
        ..., ge=0.0, description="Liquid cash and savings bank balance available immediately"
    )
    existing_investments: float = Field(
        default=0.0, ge=0.0, description="Current investment corpus (FD, MFs, Equity, etc.)"
    )
    total_liabilities: float = Field(
        default=0.0, ge=0.0, description="Total outstanding debt (Home loan, personal loan, etc.)"
    )

    # Investment Parameters
    investment_amount: float = Field(
        ..., gt=0.0, description="Proposed lump sum or monthly investment capacity in INR"
    )
    is_sip: bool = Field(
        default=True, description="True if investment_amount is monthly SIP, False if lump sum"
    )
    investment_horizon_years: float = Field(
        ..., gt=0.0, le=50.0, description="Investment time horizon in years"
    )

    # Goals & Attributes
    primary_goal: GoalType = Field(..., description="Primary stated financial goal")
    secondary_goals: List[GoalType] = Field(
        default_factory=list, description="Additional stated goals"
    )
    stated_risk_tolerance: RiskTolerance = Field(
        ..., description="Self-reported psychological risk tolerance"
    )
    cash_flow_stability: CashFlowStability = Field(
        default=CashFlowStability.STABLE_SALARIED,
        description="Predictability of income streams",
    )

    # Suitability & Risk Flags
    has_emergency_fund: bool = Field(
        default=False,
        description="Self-declared presence of adequate emergency reserves",
    )
    past_fo_drawdown: bool = Field(
        default=False,
        description="Flag indicating history of severe drawdowns in speculative F&O trading",
    )
    notes: Optional[str] = Field(
        default=None, description="RIA qualitative notes or contextual circumstances"
    )

    @computed_field
    def net_monthly_surplus(self) -> float:
        """Net monthly investable surplus after expenses and debt servicing."""
        return max(0.0, self.monthly_income - self.monthly_expenses - self.monthly_debt_obligations)

    @computed_field
    def computed_emergency_buffer_months(self) -> float:
        """Months of expenses covered by immediately liquid savings."""
        if self.monthly_expenses <= 0.0:
            return 99.0
        return round(self.existing_savings / self.monthly_expenses, 2)

    @computed_field
    def debt_to_income_ratio(self) -> float:
        """Debt service obligations as percentage of monthly income."""
        if self.monthly_income <= 0.0:
            return 1.0 if self.monthly_debt_obligations > 0 else 0.0
        return round(self.monthly_debt_obligations / self.monthly_income, 4)

    @computed_field
    def savings_rate(self) -> float:
        """Proportion of income saved after expenses and debt obligations."""
        if self.monthly_income <= 0.0:
            return 0.0
        return round(self.net_monthly_surplus / self.monthly_income, 4)

    @model_validator(mode="after")
    def validate_financial_sanity(self) -> "ClientProfile":
        """Validate consistency of financial inputs."""
        if self.monthly_expenses + self.monthly_debt_obligations > self.monthly_income:
            # Not an error (could live off savings/corpus like a retiree), but we ensure non-negative surplus
            pass
        return self

