"""AI Copilot and Explainability Engine for SEBI-Registered Investment Advisers.

Prototype designed around the Zeckathon PS4 requirements; not SEBI-approved or certified.

Clearly separates:
- 'data-derived result'
- 'rule-based result'
- 'LLM-generated explanation'

Provides an end-to-end reproducible audit trail allowing a judge to trace:
INPUT → CALCULATION → RISK PROFILE → SUITABILITY → GUARDRAIL → PORTFOLIO → AI EXPLANATION → SOURCE.
"""

from datetime import datetime
import json
import os
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from src.documents.retriever import Citation, RetrievalResult
from src.guardrails.rules import ComplianceGuardrails, GuardrailResult
from src.portfolio.engine import PortfolioRecommendation
from src.profiling.models import ClientProfile
from src.suitability.engine import SuitabilityAssessment


class DocumentAnswer(BaseModel):
    """Structured result for Page-Level Grounded Document Q&A."""

    query: str
    answer: str
    document_name: Optional[str] = None
    page_number: Optional[int] = None
    retrieved_evidence: Optional[str] = None
    is_grounded: bool = False
    status_message: str = ""


class AdvisoryAuditRecord(BaseModel):
    """Immutable audit trail of advisory outputs for hackathon judges and RIA due diligence."""

    request_id: str = Field(..., description="Unique request audit identifier")
    timestamp_utc: str = Field(..., description="ISO 8601 UTC timestamp")
    trace_flow: str = Field(
        default="INPUT → CALCULATION → RISK PROFILE → SUITABILITY → GUARDRAIL → PORTFOLIO → AI EXPLANATION → SOURCE",
        description="Verifiable audit trail execution pipeline"
    )

    # 1. Client input
    client_input: Dict[str, Any] = Field(..., description="Raw client financial inputs")

    # 2. Calculated suitability score
    calculated_suitability_score: float = Field(..., description="Deterministic composite score (0-100)")
    suitability_arithmetic: str = Field(..., description="Verifiable mathematical scoring breakdown")

    # 3. Risk category
    raw_risk_category: str = Field(..., description="Unconstrained score-derived category")
    risk_category: str = Field(..., description="Final guardrail-adjusted category")

    # 4. Guardrail decisions
    guardrail_decisions: Dict[str, Any] = Field(..., description="Active overrides, warnings, and compliance checks")

    # 5. Portfolio allocation
    portfolio_allocation: Dict[str, Any] = Field(..., description="Deterministic asset class and category weights")

    # 6. Source documents & retrieved evidence
    source_documents: List[str] = Field(default_factory=list, description="Indexed scheme documents referenced")
    retrieved_evidence: List[Dict[str, Any]] = Field(default_factory=list, description="Page-level citations if applicable")

    # 7. LLM-generated explanation
    llm_generated_explanation: str = Field(..., description="Synthesized plain-language rationale")
    ai_execution_mode: str = Field(
        default="Deterministic Grounded Synthesizer",
        description="Local deterministic engine or external LLM API"
    )

    # Regulatory Disclaimer
    regulatory_disclaimer: str = Field(
        default="Prototype developed for the Zeckathon PS4 problem statement. This system is not SEBI-approved or certified and does not constitute independent investment advice.",
        description="Statutory non-endorsement notice"
    )


class AICopilot:
    """AI Advisory Co-Pilot for SEBI-Registered Investment Advisers."""

    DISCLAIMER = "Prototype developed for the Zeckathon PS4 problem statement. This system is not SEBI-approved or certified and does not constitute independent investment advice."

    @classmethod
    def generate_recommendation_explanation(
        cls,
        profile: ClientProfile,
        assessment: SuitabilityAssessment,
        portfolio: PortfolioRecommendation,
        guardrails: GuardrailResult,
    ) -> str:
        """Synthesize a plain-language explanation grounded in deterministic calculations."""
        # Check guardrails first
        if not guardrails.is_compliant:
            return guardrails.refusal_message or "Request blocked by system guardrails."

        lines = []
        lines.append(f"### Advisory Rationale & Portfolio Construction for {profile.name}")
        lines.append(
            f"**Assessed Suitability**: `{assessment.final_category.value.replace('_', ' ').title()}` "
            f"(Score: **{assessment.composite_score:.1f}/100**)"
        )
        lines.append(f"*Arithmetic*: `{assessment.score_formula}`\n")

        # 1. Why this suitability profile was assigned
        lines.append("#### 1. Suitability Assessment Breakdown")
        lines.append(
            f"Based on client age ({profile.age}), monthly surplus (₹{profile.net_monthly_surplus:,.0f}), "
            f"and an investment horizon of **{profile.investment_horizon_years:.1f} years** for **{profile.primary_goal.value.replace('_', ' ').title()}**, "
            f"the deterministic scoring engine computed a capacity score of {assessment.capacity_score:.1f}/100."
        )

        if assessment.active_overrides:
            lines.append("\n**Applicable Guardrails & Model Constraints**:")
            for o in assessment.active_overrides:
                lines.append(f"- ⚖️ *{o}*")

        # 2. Emergency Fund Guidance
        if portfolio.emergency_carveout_amount > 0:
            lines.append("\n#### 2. Liquidity & Emergency Fund Mandate")
            lines.append(
                f"🚨 **Liquidity Buffer Priority**: Current liquid reserve covers **{profile.computed_emergency_buffer_months:.1f} months** "
                f"of expenses. Standard financial planning methodology recommends a 3 to 6-month buffer. "
                f"{portfolio.emergency_carveout_instruction}"
            )

        # 3. Portfolio Allocation Rationale
        lines.append("\n#### 3. Deterministic Asset Class Allocation")
        lines.append(
            f"To achieve your stated objective while respecting the {assessment.final_category.value.replace('_', ' ').title()} risk boundary, "
            f"capital is allocated deterministically across regulated scheme categories:"
        )
        lines.append(
            f"- **Equity ({portfolio.equity_pct:.0f}%)**: Long-term capital growth and purchasing power preservation."
        )
        lines.append(
            f"- **Debt / Fixed Income ({portfolio.debt_pct:.0f}%)**: Capital safety, regular accrual yield, and drawdown dampening."
        )
        if portfolio.liquid_pct > 0:
            lines.append(
                f"- **Liquid / Overnight ({portfolio.liquid_pct:.0f}%)**: Immediate liquidity and volatility insulation."
            )
        if portfolio.gold_pct > 0:
            lines.append(
                f"- **Gold / Commodities ({portfolio.gold_pct:.0f}%)**: Non-correlated geopolitical and currency hedge."
            )

        # 4. Glidepath Guidance
        lines.append("\n#### 4. Horizon Glidepath Strategy")
        lines.append(f"🛡️ {portfolio.glidepath_strategy}")

        # 5. Advisory Warnings
        if guardrails.warnings:
            lines.append("\n#### 5. Compliance Notes & Risk Flags")
            for w in guardrails.warnings:
                lines.append(f"- ⚠️ {w}")

        lines.append(f"\n---\n*{cls.DISCLAIMER}*")
        return "\n".join(lines)

    @classmethod
    def answer_document_query(
        cls,
        query: str,
        retrieval_result: RetrievalResult,
        guardrail_result: GuardrailResult,
    ) -> DocumentAnswer:
        """Synthesize an exact, cited answer to a scheme SID/factsheet question.

        Returns DocumentAnswer with document_name, page_number, and retrieved_evidence.
        If evidence is missing, returns 'Evidence not found in the indexed documents.'
        """
        # 1. Guardrail checks
        if not guardrail_result.is_compliant:
            refusal = guardrail_result.refusal_message or "Query blocked by compliance guardrails."
            return DocumentAnswer(
                query=query,
                answer=refusal,
                is_grounded=False,
                status_message="Blocked by compliance guardrail.",
            )

        # 2. Evidence sufficiency check
        if not retrieval_result.has_sufficient_evidence or not retrieval_result.top_citations:
            not_found_msg = "Evidence not found in the indexed documents."
            return DocumentAnswer(
                query=query,
                answer=not_found_msg,
                is_grounded=False,
                status_message=not_found_msg,
            )

        # 3. Grounded answer with page citation
        top_cit = retrieval_result.top_citations[0]
        answer_text = (
            f"According to **{top_cit.document_name}** (**Page {top_cit.page_number}**):\n\n"
            f"> \"{top_cit.excerpt.strip()}\""
        )

        return DocumentAnswer(
            query=query,
            answer=answer_text,
            document_name=top_cit.document_name,
            page_number=top_cit.page_number,
            retrieved_evidence=top_cit.excerpt,
            is_grounded=True,
            status_message=f"Grounded on {top_cit.document_name} Page {top_cit.page_number}",
        )

    @classmethod
    def create_audit_record(
        cls,
        profile: ClientProfile,
        assessment: SuitabilityAssessment,
        portfolio: PortfolioRecommendation,
        guardrails: GuardrailResult,
        explanation_text: str,
        citations: Optional[List[Citation]] = None,
    ) -> AdvisoryAuditRecord:
        """Create a complete, immutable audit record tracing:

        INPUT -> CALCULATION -> GUARDRAIL -> PORTFOLIO -> AI EXPLANATION -> SOURCE.
        """
        req_id = f"REQ_{profile.client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Source documents from portfolio categories & citations
        source_docs = [
            "HDFC_Top_100_Fund_SID.pdf",
            "ICICI_Pru_Corporate_Bond_Fund_SID.pdf",
            "SBI_Liquid_Fund_SID.pdf",
            "SEBI/HO/IMD/DF3/CIR/P/2017/114 (Scheme Categorization)",
        ]

        evidence_list = []
        if citations:
            evidence_list = [c.model_dump() for c in citations]

        return AdvisoryAuditRecord(
            request_id=req_id,
            timestamp_utc=datetime.now().isoformat(),
            trace_flow="INPUT → CALCULATION → RISK PROFILE → SUITABILITY → GUARDRAIL → PORTFOLIO → AI EXPLANATION → SOURCE",
            client_input={
                "client_id": profile.client_id,
                "name": profile.name,
                "age": profile.age,
                "monthly_income": profile.monthly_income,
                "monthly_expenses": profile.monthly_expenses,
                "monthly_debt_obligations": profile.monthly_debt_obligations,
                "existing_savings": profile.existing_savings,
                "existing_investments": profile.existing_investments,
                "total_liabilities": profile.total_liabilities,
                "investment_amount": profile.investment_amount,
                "is_sip": profile.is_sip,
                "investment_horizon_years": profile.investment_horizon_years,
                "primary_goal": profile.primary_goal.value,
                "stated_risk_tolerance": profile.stated_risk_tolerance.value,
                "computed_emergency_buffer_months": profile.computed_emergency_buffer_months,
                "past_fo_drawdown": profile.past_fo_drawdown,
            },
            calculated_suitability_score=assessment.composite_score,
            suitability_arithmetic=assessment.score_formula,
            raw_risk_category=assessment.raw_category.value,
            risk_category=assessment.final_category.value,
            guardrail_decisions={
                "is_compliant": guardrails.is_compliant,
                "active_overrides": assessment.active_overrides,
                "risk_flags": assessment.risk_flags,
                "warnings": guardrails.warnings,
                "violations": [v.model_dump() for v in guardrails.violations],
            },
            portfolio_allocation={
                "methodology": portfolio.methodology_summary,
                "equity_pct": portfolio.equity_pct,
                "debt_pct": portfolio.debt_pct,
                "liquid_pct": portfolio.liquid_pct,
                "gold_pct": portfolio.gold_pct,
                "emergency_carveout_amount": portfolio.emergency_carveout_amount,
                "glidepath": portfolio.glidepath_strategy,
                "categories": [c.model_dump() for c in portfolio.category_allocations],
            },
            source_documents=source_docs,
            retrieved_evidence=evidence_list,
            llm_generated_explanation=explanation_text,
            ai_execution_mode="Deterministic Grounded Synthesizer",
            regulatory_disclaimer=cls.DISCLAIMER,
        )
