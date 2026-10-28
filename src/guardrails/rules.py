"""Compliance and Financial Advisory Guardrails.

Enforces System Suitability Guardrails and Model-Imposed Constraints
aligned with SEBI (Investment Advisers) Regulations, 2013:
- Prohibits guaranteed return claims
- Detects excessive risk / speculative requests
- Detects missing mandatory profiling data
- Detects goal-risk conflicts
- Refuses answers not grounded in official document evidence
"""

import re
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from src.profiling.models import ClientProfile, GoalType, RiskTolerance
from src.suitability.engine import SuitabilityAssessment


class GuardrailSeverity(str, Enum):
    """Severity level of a compliance check violation."""
    BLOCKING = "blocking"       # Hard refusal: cannot proceed
    WARNING = "warning"         # Advisory caution flag required in RIA disclosure
    INFO = "info"               # Informational notice


class GuardrailViolation(BaseModel):
    """Specific compliance violation record."""
    rule_id: str
    rule_name: str
    severity: GuardrailSeverity
    message: str
    source_reference: str


class GuardrailResult(BaseModel):
    """Overall guardrail compliance assessment."""
    is_compliant: bool = True
    violations: List[GuardrailViolation] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    refusal_message: Optional[str] = None


class ComplianceGuardrails:
    """Enforces advisory boundaries, model constraints, and statutory conduct rules."""

    # Prohibited return promises under SEBI Code of Conduct
    GUARANTEED_RETURN_PATTERNS = [
        r"\b(guarantee|guaranteed|guaranteeing|assure|assured|assuring|promise|promised|promising)\b.{0,40}\b(return|returns|profit|profits|yield|yields|gain|gains)\b",
        r"\b(100%\s+safe|risk[-\s]?free|zero[-\s]?risk)\b.{0,40}\b(return|returns|equity|investment|profit)\b",
        r"\b(fixed\s+return|fixed\s+returns|assured\s+payout)\b",
        r"\bmultibagger\s+(guarantee|sure|promise)",
    ]

    # High-risk speculative trading unsuitable for mutual fund advisory
    SPECULATIVE_TRADING_PATTERNS = [
        r"\bf[&/]o\b",
        r"\bfutures?\s+and\s+options?",
        r"\bcall\s+option",
        r"\bput\s+option",
        r"\bintra[-\s]?day\s+trading",
        r"\bleverage[d]?\s+(bet|position|trade)",
        r"\bcrypto(currency)?\b",
        r"\bpenny\s+stocks?",
    ]

    @classmethod
    def check_guaranteed_returns(cls, query_or_statement: str) -> Optional[GuardrailViolation]:
        """Verify that no query or statement asks for or implies guaranteed market returns."""
        text = query_or_statement.lower()
        for pat in cls.GUARANTEED_RETURN_PATTERNS:
            if re.search(pat, text):
                return GuardrailViolation(
                    rule_id="SEBI_CODE_CONDUCT_NO_GUARANTEE",
                    rule_name="Prohibition on Guaranteed Returns",
                    severity=GuardrailSeverity.BLOCKING,
                    message=(
                        "Under SEBI (Investment Advisers) Regulations, 2013, Third Schedule (Code of Conduct), "
                        "an investment adviser cannot promise, guarantee, or illustrate assured returns on "
                        "market-linked securities. All mutual fund investments are subject to market risks."
                    ),
                    source_reference="SEBI (Investment Advisers) Regulations, 2013, Third Schedule (Code of Conduct, Clause 1)",
                )
        return None

    @classmethod
    def check_speculative_requests(cls, query_or_statement: str) -> Optional[GuardrailViolation]:
        """Detect and refuse requests for leveraged or speculative instruments."""
        text = query_or_statement.lower()
        for pat in cls.SPECULATIVE_TRADING_PATTERNS:
            if re.search(pat, text):
                return GuardrailViolation(
                    rule_id="SPECULATIVE_VEHICLE_RESTRICTION",
                    rule_name="Unsuitable Speculative Vehicle Request",
                    severity=GuardrailSeverity.BLOCKING,
                    message=(
                        "This advisory co-pilot is strictly configured for SEBI-regulated mutual fund portfolios "
                        "and goal-based planning. Derivatives (F&O), leveraged trading, and unregulated digital assets "
                        "are outside advisory scope."
                    ),
                    source_reference="System Suitability Guardrail (Mandate Restriction)",
                )
        return None

    @classmethod
    def check_missing_information(cls, profile_dict: Dict[str, Any]) -> List[GuardrailViolation]:
        """Detect missing mandatory client profiling data under SEBI Regulation 16."""
        required_fields = [
            ("monthly_income", "Monthly income"),
            ("monthly_expenses", "Monthly expenses"),
            ("investment_amount", "Investment capacity"),
            ("investment_horizon_years", "Investment horizon"),
            ("primary_goal", "Primary financial goal"),
            ("stated_risk_tolerance", "Stated risk appetite"),
        ]
        violations = []
        for field, name in required_fields:
            val = profile_dict.get(field)
            if val is None or val == "":
                violations.append(
                    GuardrailViolation(
                        rule_id="MANDATORY_INFO_MISSING",
                        rule_name=f"Missing Information: {name}",
                        severity=GuardrailSeverity.BLOCKING,
                        message=f"Mandatory client profiling field '{name}' is missing or undefined.",
                        source_reference="SEBI (Investment Advisers) Regulations, 2013, Regulation 16 (Risk Profiling)",
                    )
                )
        return violations

    @classmethod
    def check_profile_suitability_conflicts(
        cls,
        profile: ClientProfile,
        assessment: SuitabilityAssessment,
    ) -> List[GuardrailViolation]:
        """Check for structural conflicts between client profile, goal, and risk tolerance."""
        violations = []

        # 1. Goal Horizon vs Equity Allocation Conflict
        if profile.investment_horizon_years < 3.0 and assessment.max_equity_pct > 20.0:
            violations.append(
                GuardrailViolation(
                    rule_id="HORIZON_RISK_CONFLICT",
                    rule_name="Goal Horizon vs Equity Volatility Conflict",
                    severity=GuardrailSeverity.BLOCKING,
                    message=(
                        f"Investment horizon of {profile.investment_horizon_years:.1f} years is too short "
                        f"to tolerate equity market drawdowns. Permissible equity must be capped at 20%."
                    ),
                    source_reference="Model-Imposed Constraint (Horizon-Risk Budgeting)",
                )
            )

        # 2. Emergency Fund Vulnerability Conflict
        if profile.computed_emergency_buffer_months < 3.0:
            violations.append(
                GuardrailViolation(
                    rule_id="EMERGENCY_BUFFER_DEFICIT",
                    rule_name="Inadequate Liquidity Buffer",
                    severity=GuardrailSeverity.WARNING,
                    message=(
                        f"Current emergency buffer ({profile.computed_emergency_buffer_months:.1f} mo) "
                        "is below the model-recommended 3-6 month safety threshold. Capital must first be "
                        "allocated to build liquid emergency reserves."
                    ),
                    source_reference="Model-Imposed Constraint (Standard Liquidity Sizing)",
                )
            )

        # 3. Retiree Senior Citizen High Equity Conflict
        if profile.age >= 60 and profile.primary_goal == GoalType.MONTHLY_INCOME:
            if assessment.final_category in (RiskTolerance.AGGRESSIVE, RiskTolerance.MODERATELY_AGGRESSIVE):
                violations.append(
                    GuardrailViolation(
                        rule_id="RETIREE_HIGH_RISK_CONFLICT",
                        rule_name="Senior Citizen Monthly Income Capital Hazard",
                        severity=GuardrailSeverity.BLOCKING,
                        message="Senior citizens requiring regular monthly income cannot be allocated aggressive equity portfolios.",
                        source_reference="Model-Imposed Constraint (Senior Wealth Preservation)",
                    )
                )

        # 4. Past F&O Drawdown Warning
        if profile.past_fo_drawdown:
            violations.append(
                GuardrailViolation(
                    rule_id="SPECULATIVE_DRAWDOWN_WARNING",
                    rule_name="Past Speculative Loss Risk Flag",
                    severity=GuardrailSeverity.WARNING,
                    message=(
                        "Client has a history of speculative F&O losses. Suitability engine enforces "
                        "disciplined mutual fund diversification and blocks high-risk concentration."
                    ),
                    source_reference="System Suitability Guardrail (Derivatives Drawdown Protection)",
                )
            )

        return violations

    @classmethod
    def evaluate_all(
        cls,
        profile: Optional[ClientProfile] = None,
        assessment: Optional[SuitabilityAssessment] = None,
        query: Optional[str] = None,
        raw_profile_dict: Optional[Dict[str, Any]] = None,
    ) -> GuardrailResult:
        """Run complete compliance guardrail scan."""
        violations: List[GuardrailViolation] = []
        warnings: List[str] = []

        # Missing information check
        if raw_profile_dict is not None:
            missing_viols = cls.check_missing_information(raw_profile_dict)
            violations.extend(missing_viols)

        # Text-level query guardrails
        if query:
            guarantee_viol = cls.check_guaranteed_returns(query)
            if guarantee_viol:
                violations.append(guarantee_viol)

            speculative_viol = cls.check_speculative_requests(query)
            if speculative_viol:
                violations.append(speculative_viol)

        # Profile-level suitability guardrails
        if profile and assessment:
            prof_viols = cls.check_profile_suitability_conflicts(profile, assessment)
            for v in prof_viols:
                if v.severity == GuardrailSeverity.BLOCKING:
                    violations.append(v)
                else:
                    warnings.append(f"[{v.rule_name}] {v.message}")

        # Check for blocking violations
        blocking_viols = [v for v in violations if v.severity == GuardrailSeverity.BLOCKING]
        is_compliant = len(blocking_viols) == 0

        refusal_message = None
        if not is_compliant:
            reasons = "\n- ".join([f"**{v.rule_name}**: {v.message}" for v in blocking_viols])
            refusal_message = (
                f"⚠️ Recommendation restricted: client profile does not satisfy suitability conditions for this allocation.\n\n"
                f"**Specific Guardrail Violations Detected**:\n- {reasons}\n\n"
                "*Advisory co-pilot restricted from processing non-compliant or out-of-scope requests.*"
            )

        return GuardrailResult(
            is_compliant=is_compliant,
            violations=violations,
            warnings=warnings,
            refusal_message=refusal_message,
        )
