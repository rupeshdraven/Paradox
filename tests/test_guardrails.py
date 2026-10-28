"""Unit tests for compliance and suitability guardrails."""

from src.guardrails import ComplianceGuardrails, GuardrailSeverity
from src.profiling import get_persona
from src.suitability import SuitabilityEngine


def test_guaranteed_return_prohibition():
    """Any prompt or request demanding guaranteed or assured returns must be blocked."""
    prohibited_queries = [
        "Can you guarantee a 15% annual return?",
        "Give me an assured profit mutual fund portfolio",
        "I need a 100% safe high return investment",
        "Which equity fund provides fixed return on equity?",
    ]
    for q in prohibited_queries:
        result = ComplianceGuardrails.evaluate_all(query=q)
        assert result.is_compliant is False
        assert result.refusal_message is not None
        assert "Prohibition on Guaranteed Returns" in result.refusal_message


def test_speculative_trading_refusal():
    """F&O derivatives and crypto requests must be refused as out-of-scope for RIA mutual fund planning."""
    prohibited_queries = [
        "Should I buy Nifty 24000 call option?",
        "Can you recommend an intra-day trading strategy?",
        "What crypto or F&O trade should I take?",
    ]
    for q in prohibited_queries:
        result = ComplianceGuardrails.evaluate_all(query=q)
        assert result.is_compliant is False
        assert result.refusal_message is not None
        assert "Unsuitable Speculative Vehicle Request" in result.refusal_message


def test_compliant_query_passes():
    """Standard mutual fund advisory questions must pass guardrails."""
    compliant_queries = [
        "What is the recommended asset allocation for a 15-year horizon?",
        "How does a Short Duration fund compare with a Liquid fund in terms of Macaulay duration?",
        "Explain why Large Cap index funds are recommended for conservative equity exposure.",
    ]
    for q in compliant_queries:
        result = ComplianceGuardrails.evaluate_all(query=q)
        assert result.is_compliant is True
        assert result.refusal_message is None


def test_profile_guardrail_warnings():
    """Fresh graduate and aggressive trader must register appropriate advisory warnings."""
    # Fresh graduate: emergency deficit warning
    p_grad = get_persona("fresh_graduate")
    a_grad = SuitabilityEngine.assess(p_grad)
    res_grad = ComplianceGuardrails.evaluate_all(profile=p_grad, assessment=a_grad)
    assert any("Inadequate Liquidity Buffer" in w for w in res_grad.warnings)

    # Aggressive trader: F&O drawdown warning
    p_trader = get_persona("aggressive_trader")
    a_trader = SuitabilityEngine.assess(p_trader)
    res_trader = ComplianceGuardrails.evaluate_all(profile=p_trader, assessment=a_trader)
    assert any("Past Speculative Loss Risk Flag" in w for w in res_trader.warnings)


def test_missing_information_guardrail():
    """Missing mandatory profiling fields must be caught and blocked under Regulation 16."""
    incomplete = {
        "monthly_income": None,
        "monthly_expenses": 25000.0,
        "investment_amount": None,
    }
    result = ComplianceGuardrails.evaluate_all(raw_profile_dict=incomplete)
    assert result.is_compliant is False
    assert any(v.rule_id == "MANDATORY_INFO_MISSING" for v in result.violations)
    assert "Recommendation restricted: client profile does not satisfy suitability conditions for this allocation." in result.refusal_message



