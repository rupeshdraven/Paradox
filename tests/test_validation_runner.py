"""Unit tests executing the 8 validation mode test cases."""

from src.validation import ValidationRunner


def test_validation_runner_all_pass():
    """Execute all 8 mandatory validation cases (A to H) and verify 100% pass rate."""
    results = ValidationRunner.run_all_cases()
    assert len(results) == 8

    failed_cases = [r for r in results if r.status != "PASS"]
    error_summary = "\n".join([f"{r.case_id} ({r.case_name}): {r.actual_behaviour}" for r in failed_cases])
    assert len(failed_cases) == 0, f"The following cases failed:\n{error_summary}"

    for r in results:
        assert r.status == "PASS"
        assert len(r.expected_behaviour) > 0
        assert len(r.actual_behaviour) > 0

