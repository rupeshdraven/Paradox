"""Deterministic BM25 Document Retriever with page-level citations for SID factsheets."""

import math
import re
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from src.documents.parser import DocumentChunk


class Citation(BaseModel):
    """Verifiable citation linking an answer directly to an exact PDF and page."""

    document_name: str = Field(..., description="Name of source document")
    page_number: int = Field(..., ge=1, description="Page number where evidence is located")
    relevance_score: float = Field(..., description="BM25 relevance score")
    excerpt: str = Field(..., description="Verbatim text excerpt demonstrating proof")


class RetrievalResult(BaseModel):
    """Result of document knowledge retrieval."""

    query: str
    has_sufficient_evidence: bool
    top_citations: List[Citation] = Field(default_factory=list)
    combined_context: str = ""
    evidence_status_message: str = ""


class BM25Retriever:
    """Inspectable, transparent BM25 information retrieval engine."""

    def __init__(
        self,
        chunks: Optional[List[DocumentChunk]] = None,
        k1: float = 1.5,
        b: float = 0.75,
        min_relevance_threshold: float = 1.5,
    ):
        self.k1 = k1
        self.b = b
        self.min_relevance_threshold = min_relevance_threshold
        self.chunks: List[DocumentChunk] = []
        self.doc_len: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_freqs: Dict[str, int] = {}
        self.term_freqs: List[Dict[str, int]] = []
        self.corpus_size: int = 0

        if chunks:
            self.index_chunks(chunks)

    STOPWORDS = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
        "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
        "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down",
        "during", "each", "few", "for", "from", "further", "had", "has", "have",
        "having", "he", "her", "here", "hers", "herself", "him", "himself", "his",
        "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me",
        "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on",
        "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own",
        "same", "she", "should", "so", "some", "such", "than", "that", "the", "their",
        "theirs", "them", "themselves", "then", "there", "these", "they", "this",
        "those", "through", "to", "too", "under", "until", "up", "very", "was", "we",
        "were", "what", "when", "where", "which", "while", "who", "whom", "why", "with",
        "would", "you", "your", "yours", "yourself", "yourselves",
    }

    @classmethod
    def tokenize(cls, text: str) -> List[str]:
        """Normalize, tokenize, and remove standard stopwords."""
        clean = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = [t for t in clean.split() if len(t) > 1 and t not in cls.STOPWORDS]
        return tokens

    def index_chunks(self, chunks: List[DocumentChunk]) -> None:
        """Build BM25 index over the provided document chunks."""
        self.chunks = list(chunks)
        self.corpus_size = len(chunks)
        self.doc_len = []
        self.term_freqs = []
        self.doc_freqs = {}

        if self.corpus_size == 0:
            self.avg_doc_len = 0.0
            return

        total_length = 0
        for chunk in self.chunks:
            tokens = self.tokenize(chunk.text)
            length = len(tokens)
            self.doc_len.append(length)
            total_length += length

            tf: Dict[str, int] = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            self.term_freqs.append(tf)

            for unique_token in tf.keys():
                self.doc_freqs[unique_token] = self.doc_freqs.get(unique_token, 0) + 1

        self.avg_doc_len = total_length / self.corpus_size if self.corpus_size > 0 else 0.0

    def query(self, query_text: str, top_k: int = 3) -> RetrievalResult:
        """Search indexed SID/factsheet chunks and return top page-level citations."""
        query_tokens = self.tokenize(query_text)
        if not query_tokens or self.corpus_size == 0:
            return RetrievalResult(
                query=query_text,
                has_sufficient_evidence=False,
                top_citations=[],
                combined_context="",
                evidence_status_message="No documents indexed or empty query.",
            )

        scores: List[float] = [0.0] * self.corpus_size

        for token in query_tokens:
            if token not in self.doc_freqs:
                continue

            # Robertson-Spärck Jones IDF
            df = self.doc_freqs[token]
            idf = math.log((self.corpus_size - df + 0.5) / (df + 0.5) + 1.0)

            for idx, tf_dict in enumerate(self.term_freqs):
                if token in tf_dict:
                    freq = tf_dict[token]
                    numerator = freq * (self.k1 + 1.0)
                    denominator = freq + self.k1 * (
                        1.0 - self.b + self.b * (self.doc_len[idx] / self.avg_doc_len)
                    )
                    scores[idx] += idf * (numerator / denominator)

        # Rank matches
        ranked_indices = sorted(
            range(self.corpus_size), key=lambda i: scores[i], reverse=True
        )

        top_citations: List[Citation] = []
        context_blocks: List[str] = []
        best_overlap_ratio = 0.0

        for idx in ranked_indices[:top_k]:
            score = scores[idx]
            if score <= 0.0:
                continue

            chunk = self.chunks[idx]
            chunk_tokens = set(self.tokenize(chunk.text))
            matched_terms = [t for t in set(query_tokens) if t in chunk_tokens]
            overlap_ratio = len(matched_terms) / len(set(query_tokens)) if query_tokens else 0.0
            best_overlap_ratio = max(best_overlap_ratio, overlap_ratio)

            # Format excerpt up to 600 chars to avoid clipping key table lines
            excerpt_text = chunk.text[:600] + ("..." if len(chunk.text) > 600 else "")

            top_citations.append(
                Citation(
                    document_name=chunk.document_name,
                    page_number=chunk.page_number,
                    relevance_score=round(score, 3),
                    excerpt=excerpt_text,
                )
            )
            context_blocks.append(
                f"[Source: {chunk.document_name} | Page {chunk.page_number} | Relevance: {score:.2f} | Overlap: {overlap_ratio:.0%}]\n{chunk.text}"
            )

        # Grounding condition: Sufficient relevance score AND term overlap ratio >= 30%
        has_sufficient = (
            len(top_citations) > 0
            and top_citations[0].relevance_score >= self.min_relevance_threshold
            and (best_overlap_ratio >= 0.30 or len(set(query_tokens)) <= 2)
        )

        status_msg = (
            f"Found {len(top_citations)} citations with sufficient documented evidence."
            if has_sufficient
            else "Evidence not found in the indexed documents."
        )

        return RetrievalResult(
            query=query_text,
            has_sufficient_evidence=has_sufficient,
            top_citations=top_citations,
            combined_context="\n\n---\n\n".join(context_blocks),
            evidence_status_message=status_msg,
        )
