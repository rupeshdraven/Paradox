"""Unit tests for AI Copilot, explainability, and audit logging."""

import json
from pathlib import Path
from src.documents import BM25Retriever, DocumentParser
from src.guardrails import ComplianceGuardrails
from src.llm import AICopilot, AdvisoryAuditRecord, DocumentAnswer
from src.portfolio import PortfolioEngine
from src.profiling import get_persona
from src.suitability import SuitabilityEngine


def test_copilot_explanation_generation():
    """Copilot must synthesize clear, compliant advisory rationale for Fresh Graduate."""
    p = get_persona("fresh_graduate")
    assessment = SuitabilityEngine.assess(p)
    portfolio = PortfolioEngine.construct_portfolio(p, assessment)
    guardrails = ComplianceGuardrails.evaluate_all(profile=p, assessment=assessment)

    explanation = AICopilot.generate_recommendation_explanation(
        profile=p,
        assessment=assessment,
        portfolio=portfolio,
        guardrails=guardrails,
    )

    assert "Advisory Rationale & Portfolio Construction" in explanation
    assert "Fresh Graduate" in explanation
    assert "₹25,000" in explanation  # Emergency carveout mentioned
    assert "Equity (65%)" in explanation
    assert "not SEBI-approved or certified" in explanation


def test_copilot_document_query_grounded():
    """Document Q&A must cite page number and source document when answering."""
    chunks = DocumentParser.parse_directory(Path("data/raw"))
    retriever = BM25Retriever(chunks)
    query = "What is the exit load for HDFC Top 100 Fund?"

    retrieval_res = retriever.query(query)
    guardrail_res = ComplianceGuardrails.evaluate_all(query=query)

    answer = AICopilot.answer_document_query(query, retrieval_res, guardrail_res)
    assert isinstance(answer, DocumentAnswer)
    assert answer.is_grounded is True
    assert answer.document_name == "HDFC_Top_100_Fund_SID.pdf"
    assert answer.page_number == 3
    assert "1.00%" in answer.answer


def test_copilot_document_query_ungrounded_refusal():
    """Document Q&A must return exact 'Evidence not found in the indexed documents.' when evidence is absent."""
    chunks = DocumentParser.parse_directory(Path("data/raw"))
    retriever = BM25Retriever(chunks)
    query = "What is the price-to-earnings ratio of Alphabet Inc stock in 2026?"

    retrieval_res = retriever.query(query)
    guardrail_res = ComplianceGuardrails.evaluate_all(query=query)

    answer = AICopilot.answer_document_query(query, retrieval_res, guardrail_res)
    assert isinstance(answer, DocumentAnswer)
    assert answer.is_grounded is False
    assert answer.answer == "Evidence not found in the indexed documents."
    assert answer.document_name is None


def test_copilot_audit_trail_serializable():
    """Audit record must capture all layers, trace flow, and serialize to valid JSON."""
    p = get_persona("young_couple")
    assessment = SuitabilityEngine.assess(p)
    portfolio = PortfolioEngine.construct_portfolio(p, assessment)
    guardrails = ComplianceGuardrails.evaluate_all(profile=p, assessment=assessment)
    explanation = AICopilot.generate_recommendation_explanation(p, assessment, portfolio, guardrails)

    audit = AICopilot.create_audit_record(
        profile=p,
        assessment=assessment,
        portfolio=portfolio,
        guardrails=guardrails,
        explanation_text=explanation,
    )

    assert isinstance(audit, AdvisoryAuditRecord)
    assert audit.client_input["client_id"] == "young_couple"
    assert audit.risk_category == "moderately_aggressive"
    assert audit.portfolio_allocation["equity_pct"] == 65.0
    assert "INPUT → CALCULATION → RISK PROFILE → SUITABILITY → GUARDRAIL → PORTFOLIO → AI EXPLANATION → SOURCE" in audit.trace_flow

    # Ensure JSON serializable
    json_str = audit.model_dump_json()
    parsed = json.loads(json_str)
    assert parsed["request_id"].startswith("REQ_young_couple_")
    assert "regulatory_disclaimer" in parsed
