"""End-to-end integration tests for the full PS4 advisory pipeline across all 6 personas."""

import json
from pathlib import Path
from src.documents import BM25Retriever, DocumentParser
from src.guardrails import ComplianceGuardrails
from src.llm import AICopilot, AdvisoryAuditRecord, DocumentAnswer
from src.portfolio import PortfolioEngine
from src.profiling import (
    CashFlowStability,
    ClientProfile,
    GoalType,
    RiskTolerance,
    get_all_personas,
    get_persona,
)
from src.suitability import SuitabilityEngine


def test_full_pipeline_all_six_personas():
    """Verify that every target persona executes through the entire advisory pipeline seamlessly."""
    raw_dir = Path("data/raw")
    chunks = DocumentParser.parse_directory(raw_dir)
    retriever = BM25Retriever(chunks)
    personas = get_all_personas()

    assert len(personas) == 6

    for p_id, profile in personas.items():
        # 1. Suitability Assessment
        suitability = SuitabilityEngine.assess(profile)
        assert suitability.client_id == p_id
        assert suitability.final_category in list(RiskTolerance)

        # 2. Portfolio Construction
        portfolio = PortfolioEngine.construct_portfolio(profile, suitability)
        assert abs((portfolio.equity_pct + portfolio.debt_pct + portfolio.liquid_pct + portfolio.gold_pct) - 100.0) < 1e-4

        # 3. Compliance Guardrails
        guardrails = ComplianceGuardrails.evaluate_all(profile=profile, assessment=suitability)
        assert guardrails.is_compliant is True  # All standard personas must be compliant

        # 4. AI Copilot Rationale Generation
        explanation = AICopilot.generate_recommendation_explanation(
            profile=profile,
            assessment=suitability,
            portfolio=portfolio,
            guardrails=guardrails,
        )
        assert len(explanation) > 100
        assert profile.name in explanation

        # 5. Full Audit Record Generation & Serialization
        audit = AICopilot.create_audit_record(
            profile=profile,
            assessment=suitability,
            portfolio=portfolio,
            guardrails=guardrails,
            explanation_text=explanation,
        )
        assert isinstance(audit, AdvisoryAuditRecord)

        audit_json = audit.model_dump_json()
        deserialized = json.loads(audit_json)
        assert deserialized["client_input"]["client_id"] == p_id
        assert "client_input" in deserialized
        assert "calculated_suitability_score" in deserialized
        assert "portfolio_allocation" in deserialized
        assert "guardrail_decisions" in deserialized
        assert "llm_generated_explanation" in deserialized
        assert "trace_flow" in deserialized


def test_document_qa_pipeline_all_three_funds():
    """Verify that queries against all 3 indexed funds return accurate page citations."""
    raw_dir = Path("data/raw")
    chunks = DocumentParser.parse_directory(raw_dir)
    retriever = BM25Retriever(chunks)

    test_cases = [
        ("What is the exit load for HDFC Top 100 Fund?", "HDFC_Top_100_Fund_SID.pdf", 3, "1.00%"),
        ("What is the Macaulay duration for ICICI Prudential Corporate Bond Fund?", "ICICI_Pru_Corporate_Bond_Fund_SID.pdf", 2, "2 years and 4 years"),
        ("What is the Day 1 exit load for SBI Liquid Fund?", "SBI_Liquid_Fund_SID.pdf", 3, "0.0070%"),
    ]

    for q, expected_doc, expected_page, expected_keyword in test_cases:
        guardrail = ComplianceGuardrails.evaluate_all(query=q)
        assert guardrail.is_compliant is True

        retrieval = retriever.query(q)
        assert retrieval.has_sufficient_evidence is True

        answer = AICopilot.answer_document_query(q, retrieval, guardrail)
        assert isinstance(answer, DocumentAnswer)
        assert answer.document_name == expected_doc
        assert answer.page_number == expected_page
        assert expected_keyword in answer.retrieved_evidence
