"""PDF document parser extracting verifiable page-level chunks for SID/factsheets."""

import json
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field
import pypdf


class DocumentChunk(BaseModel):
    """An inspectable text segment tied to an exact PDF and page number."""

    chunk_id: str = Field(..., description="Unique chunk identifier: <doc_name>_p<page>_c<idx>")
    document_name: str = Field(..., description="Filename of the source SID / Factsheet")
    page_number: int = Field(..., ge=1, description="1-indexed physical page number in source PDF")
    chunk_index: int = Field(..., ge=0, description="Sequential index of chunk on this page")
    text: str = Field(..., description="Authentic extracted verbatim text segment")
    char_count: int = Field(..., ge=0)


class DocumentParser:
    """Extracts text page-by-page from official mutual fund Scheme Information Documents."""

    @classmethod
    def parse_pdf(
        cls,
        pdf_path: Path,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
    ) -> List[DocumentChunk]:
        """Extract text page-by-page and partition into cited chunks."""
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"Document not found: {pdf_path}")

        reader = pypdf.PdfReader(str(pdf_path))
        chunks: List[DocumentChunk] = []

        for page_idx, page in enumerate(reader.pages):
            page_num = page_idx + 1
            raw_text = page.extract_text() or ""
            cleaned_text = " ".join(raw_text.split())

            if not cleaned_text:
                continue

            # Clean scheme title from filename for context enrichment
            clean_scheme = pdf_path.stem.replace("_", " ")
            enriched_text = f"[{clean_scheme} - Page {page_num}] {cleaned_text}"

            # Split into chunks if page text exceeds chunk_size
            if len(enriched_text) <= chunk_size:
                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{pdf_path.stem}_p{page_num}_c0",
                        document_name=pdf_path.name,
                        page_number=page_num,
                        chunk_index=0,
                        text=enriched_text,
                        char_count=len(enriched_text),
                    )
                )
            else:
                start = 0
                c_idx = 0
                while start < len(enriched_text):
                    end = min(start + chunk_size, len(enriched_text))
                    segment = enriched_text[start:end]
                    chunks.append(
                        DocumentChunk(
                            chunk_id=f"{pdf_path.stem}_p{page_num}_c{c_idx}",
                            document_name=pdf_path.name,
                            page_number=page_num,
                            chunk_index=c_idx,
                            text=segment,
                            char_count=len(segment),
                        )
                    )
                    c_idx += 1
                    start += chunk_size - chunk_overlap
                    if end == len(enriched_text):
                        break

        return chunks

    @classmethod
    def parse_directory(cls, dir_path: Path) -> List[DocumentChunk]:
        """Parse all PDF files in the specified directory."""
        dir_path = Path(dir_path)
        all_chunks: List[DocumentChunk] = []
        for pdf_file in sorted(dir_path.glob("*.pdf")):
            all_chunks.extend(cls.parse_pdf(pdf_file))
        return all_chunks

    @classmethod
    def save_processed_chunks(cls, chunks: List[DocumentChunk], output_file: Path) -> None:
        """Persist extracted chunks to JSON for caching and audit inspection."""
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        data = [c.model_dump() for c in chunks]
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_processed_chunks(cls, input_file: Path) -> List[DocumentChunk]:
        """Load cached document chunks."""
        input_file = Path(input_file)
        if not input_file.exists():
            return []
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [DocumentChunk.model_validate(item) for item in data]
