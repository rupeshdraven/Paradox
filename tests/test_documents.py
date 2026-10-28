"""Unit tests for document parsing, page-level citation, and BM25 retrieval."""

from pathlib import Path
from src.documents import BM25Retriever, DocumentParser


def test_parse_sids_from_directory():
    """All 3 authentic SID PDFs must be parsed into page-indexed chunks."""
    raw_dir = Path("data/raw")
    chunks = DocumentParser.parse_directory(raw_dir)

    assert len(chunks) >= 12  # At least 3 documents * 4 pages
    doc_names = {c.document_name for c in chunks}
    assert "HDFC_Top_100_Fund_SID.pdf" in doc_names
    assert "ICICI_Pru_Corporate_Bond_Fund_SID.pdf" in doc_names
    assert "SBI_Liquid_Fund_SID.pdf" in doc_names

    # Check page numbers are properly 1-indexed (1 to 4)
    for c in chunks:
        assert 1 <= c.page_number <= 4
        assert len(c.text) > 0


def test_bm25_retrieval_hdfc_exit_load():
    """Querying HDFC Top 100 exit load must return Page 3 with 1.00% load."""
    chunks = DocumentParser.parse_directory(Path("data/raw"))
    retriever = BM25Retriever(chunks)

    res = retriever.query("What is the exit load for HDFC Top 100 Fund?")
    assert res.has_sufficient_evidence is True
    assert len(res.top_citations) > 0

    top_cit = res.top_citations[0]
    assert top_cit.document_name == "HDFC_Top_100_Fund_SID.pdf"
    assert top_cit.page_number == 3
    assert "1.00%" in top_cit.excerpt
    assert "365 days" in top_cit.excerpt


def test_bm25_retrieval_sbi_liquid_graded_load():
    """Querying SBI Liquid Fund graded exit load must return Page 3 with exact percentage."""
    chunks = DocumentParser.parse_directory(Path("data/raw"))
    retriever = BM25Retriever(chunks)

    res = retriever.query("What is the Day 1 exit load for SBI Liquid Fund?")
    assert res.has_sufficient_evidence is True
    assert len(res.top_citations) > 0

    top_cit = res.top_citations[0]
    assert top_cit.document_name == "SBI_Liquid_Fund_SID.pdf"
    assert top_cit.page_number == 3
    assert "0.0070%" in top_cit.excerpt


def test_bm25_retrieval_icici_corporate_duration():
    """Querying ICICI Corporate Bond duration must cite Page 2 (2 to 4 years)."""
    chunks = DocumentParser.parse_directory(Path("data/raw"))
    retriever = BM25Retriever(chunks)

    res = retriever.query("What is the Macaulay duration for ICICI Prudential Corporate Bond Fund?")
    assert res.has_sufficient_evidence is True
    assert len(res.top_citations) > 0

    top_cit = res.top_citations[0]
    assert top_cit.document_name == "ICICI_Pru_Corporate_Bond_Fund_SID.pdf"
    assert top_cit.page_number == 2
    assert "2 years and 4 years" in top_cit.excerpt


def test_bm25_unrelated_query_insufficient_evidence():
    """Unrelated queries outside the SID evidence corpus must be flagged as insufficient."""
    chunks = DocumentParser.parse_directory(Path("data/raw"))
    retriever = BM25Retriever(chunks)

    res = retriever.query("What is the quarterly revenue of Tesla electric vehicle sales?")
    assert res.has_sufficient_evidence is False
    assert res.evidence_status_message == "Evidence not found in the indexed documents."

