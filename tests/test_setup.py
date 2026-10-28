"""Smoke test to verify project modules import properly."""

def test_imports():
    import src.profiling
    import src.suitability
    import src.portfolio
    import src.documents
    import src.llm
    import src.guardrails

    assert src.profiling is not None
    assert src.suitability is not None
    assert src.portfolio is not None
    assert src.documents is not None
    assert src.llm is not None
    assert src.guardrails is not None

