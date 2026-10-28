"""Central Source Registry for AI Co-Pilot for SEBI-Registered Investment Advisers.

Maintains verifiable provenance and authoritative citations for:
1. Regulatory References (SEBI Regulations 16, 17, 19, Circulars, and Code of Conduct)
2. Scheme Information Documents (SIDs)
3. Model-Imposed Constraints & Methodologies
4. AI Tooling Disclosures
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SourceEntry(BaseModel):
    """Verifiable reference entry with authoritative provenance."""

    source_name: str = Field(..., description="Canonical reference identifier")
    source_type: str = Field(..., description="Regulatory Reference, Financial Document, Model Constraint, or AI Tool")
    reference_locator: str = Field(..., description="Gazette notification, circular number, file path, or URL")
    purpose: str = Field(..., description="Specific purpose and application in the advisory engine")
    date_or_version: str = Field(..., description="Official publication date or version")


# Authoritative central registry
SOURCE_REGISTRY: Dict[str, SourceEntry] = {
    # 1. Statutory & Regulatory References
    "SEBI_IA_REG_16_2013": SourceEntry(
        source_name="SEBI (Investment Advisers) Regulations, 2013 - Regulation 16 (Risk Profiling)",
        source_type="Regulatory Reference",
        reference_locator="SEBI (Investment Advisers) Regulations, 2013, Chapter III, Regulation 16",
        purpose="Designed with reference to regulatory risk profiling requirements: mandates obtaining client information regarding financial situation, investment objectives, and capacity to absorb losses prior to advice.",
        date_or_version="Notification No. LAD-NRO/GN/2012-13/31/1778 (January 21, 2013)",
    ),
    "SEBI_IA_REG_17_2013": SourceEntry(
        source_name="SEBI (Investment Advisers) Regulations, 2013 - Regulation 17 (Suitability)",
        source_type="Regulatory Reference",
        reference_locator="SEBI (Investment Advisers) Regulations, 2013, Chapter III, Regulation 17",
        purpose="Designed with reference to regulatory suitability requirements: mandates that advisers have a reasonable basis for believing recommendations are suitable to the client's risk profile, objectives, and situation.",
        date_or_version="Notification No. LAD-NRO/GN/2012-13/31/1778 (January 21, 2013)",
    ),
    "SEBI_IA_REG_19_2013": SourceEntry(
        source_name="SEBI (Investment Advisers) Regulations, 2013 - Regulation 19 (Maintenance of Records)",
        source_type="Regulatory Reference",
        reference_locator="SEBI (Investment Advisers) Regulations, 2013, Chapter III, Regulation 19",
        purpose="Designed with reference to regulatory record maintenance requirements: mandates maintaining client KYC, risk assessment, suitability rationale, and advisory audit trail for a minimum of 5 years.",
        date_or_version="Notification No. LAD-NRO/GN/2012-13/31/1778 (January 21, 2013)",
    ),
    "SEBI_MF_CATEGORIZATION_2017": SourceEntry(
        source_name="Categorization and Rationalization of Mutual Fund Schemes",
        source_type="Regulatory Reference",
        reference_locator="SEBI Circular SEBI/HO/IMD/DF3/CIR/P/2017/114",
        purpose="Authoritative scheme categorization definitions: defines Large Cap (top 100 stocks), Mid Cap (101st-250th stocks), Corporate Bond (min 80% in AA+ and above rated paper), and Liquid Fund categories.",
        date_or_version="Circular dated October 06, 2017",
    ),
    "SEBI_CODE_OF_CONDUCT_2013": SourceEntry(
        source_name="Code of Conduct for Investment Advisers",
        source_type="Regulatory Reference",
        reference_locator="SEBI (Investment Advisers) Regulations, 2013, Third Schedule",
        purpose="Statutory conduct standards: prohibits promising guaranteed market returns and mandates honest and fair fiduciary representation.",
        date_or_version="January 21, 2013",
    ),
    "SEBI_GRADED_EXIT_LOAD_2019": SourceEntry(
        source_name="Review of Investment Norms for Mutual Funds for Liquid Schemes",
        source_type="Regulatory Reference",
        reference_locator="SEBI Circular SEBI/HO/IMD/DF2/CIR/P/2019/101",
        purpose="Prescribes the official 7-day graded exit load schedule for liquid funds cited in factsheet Q&A.",
        date_or_version="Circular dated September 20, 2019",
    ),

    # 2. Financial Documents (SIDs)
    "HDFC_TOP_100_SID": SourceEntry(
        source_name="Scheme Information Document: HDFC Top 100 Fund",
        source_type="Financial Document",
        reference_locator="data/raw/HDFC_Top_100_Fund_SID.pdf",
        purpose="Official Large Cap equity SID: verifiable facts on benchmark (NIFTY 100 TRI), 80-100% large cap asset allocation, and 1.00% exit load within 365 days (Page 3).",
        date_or_version="SEBI SID Model Format / AMC Filing",
    ),
    "ICICI_CORP_BOND_SID": SourceEntry(
        source_name="Scheme Information Document: ICICI Prudential Corporate Bond Fund",
        source_type="Financial Document",
        reference_locator="data/raw/ICICI_Pru_Corporate_Bond_Fund_SID.pdf",
        purpose="Official Corporate Bond debt SID: verifiable facts on AA+ credit mandate, Macaulay duration of 2 to 4 years (Page 2), and nil exit load (Page 3).",
        date_or_version="SEBI SID Model Format / AMC Filing",
    ),
    "SBI_LIQUID_SID": SourceEntry(
        source_name="Scheme Information Document: SBI Liquid Fund",
        source_type="Financial Document",
        reference_locator="data/raw/SBI_Liquid_Fund_SID.pdf",
        purpose="Official Liquid Fund SID: verifiable facts on 91-day maturity constraint, 7-day graded exit load (Page 3), and 1:30 PM purchase cut-off (Page 4).",
        date_or_version="SEBI SID Model Format / AMC Filing",
    ),

    # 3. Model-Imposed Constraints & Methodologies
    "MODEL_LIQUIDITY_BUFFER": SourceEntry(
        source_name="System Liquidity Guardrail: 3 to 6 Months Non-Discretionary Buffer",
        source_type="Model Constraint",
        reference_locator="Model-Imposed Constraint (src/suitability/engine.py)",
        purpose="Standard financial planning liquidity practice: ensures client has an adequate emergency reserve before long-term risk asset deployment. Not represented as a universal statutory SEBI rule.",
        date_or_version="Model Methodology v1.2",
    ),
    "MODEL_ASSET_CAPS": SourceEntry(
        source_name="Model-Imposed Maximum Equity and Minimum Debt/Liquid Limits",
        source_type="Model Constraint",
        reference_locator="Quantitative Risk Budgeting Matrix (src/suitability/engine.py)",
        purpose="Constraint imposed by the portfolio model for suitability/risk control: Conservative (max 20% equity), Moderate (max 45%), Mod. Aggressive (max 70%), Aggressive (max 85%). Not represented as a universal SEBI limit.",
        date_or_version="Model Methodology v1.2",
    ),

    # 4. AI Tooling & Disclosures
    "AI_COPILOT_TOOL": SourceEntry(
        source_name="AI Advisory Co-Pilot: Local Deterministic Synthesizer with LLM Adapter",
        source_type="AI Tool",
        reference_locator="src/llm/copilot.py",
        purpose="AI used strictly for plain-language communication, explanation of calculated results, and page-level cited factsheet summarization. Prohibited from computing risk scores or inventing portfolio percentages.",
        date_or_version="Python 3.14 / Local Grounded Engine",
    ),
}


def get_source_registry() -> Dict[str, SourceEntry]:
    """Retrieve all registered sources."""
    return dict(SOURCE_REGISTRY)


def get_sources_by_type(source_type: str) -> List[SourceEntry]:
    """Filter sources by source type."""
    return [s for s in SOURCE_REGISTRY.values() if s.source_type == source_type]
