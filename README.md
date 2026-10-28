# PS4: AI Co-Pilot for SEBI-Registered Investment Advisers

> **Zetheta Algorithms × IIT Patna Trading & Investment Club 24-Hour Fintech Hackathon**  
> Problem Statement 4: AI-Powered Advisory — AI Co-Pilot for SEBI-Registered Investment Advisers (RIAs)

> [!NOTE]
> **Regulatory Notice**: Prototype developed for the Zeckathon PS4 problem statement. This system is not SEBI-approved or certified and does not constitute independent investment advice.

---

## 1. Overview & Regulatory Rationale

SEBI (Investment Advisers) Regulations, 2013 and Master Circulars mandate strict fiduciary responsibility and suitability standards:
1. **Regulation 16 (Risk Profiling)**: Advisers must obtain necessary information regarding client financial situation, investment objectives, and capacity to absorb losses prior to advice.
2. **Regulation 17 (Suitability)**: Advisers must have a reasonable basis for believing recommendations are suitable to the client's risk profile, objectives, and situation.
3. **Regulation 19 (Maintenance of Records)**: Complete audit trail of client profiling, suitability assessment, risk scoring, rationale for advice, and product disclosures maintained for minimum 5 years.
4. **Transparent & Inspectable Calculations**: Advisory algorithms must not be a "black box". AI/LLMs cannot independently fabricate asset allocations, expected returns, or client risk categories.

This application acts as a **decision-support co-pilot** for SEBI RIAs. It enforces clear operational separation:
- **Data-Derived**: Verifiable facts, scheme attributes, and NAV/risk metrics extracted with page-level citations from official Scheme Information Documents (SID) and Key Information Memorandums (KIM).
- **Rule-Based**: Deterministic, inspectable suitability scoring and asset allocation mathematics based on quantitative risk budgeting.
- **LLM-Generated**: Plain-language advisory summaries, rationale explanations, and page-level grounded document Q&A—strictly constrained by guardrails.

---

## 2. System Architecture & Methodology

```text
CLIENT / RIA INPUT
       │
       ▼
Client Profiling Module (Schema validation, persona parsing, emergency fund check)
       │
       ▼
Rule-Based Suitability Engine (Deterministic scoring: Conservative / Moderate / Mod. Aggressive / Aggressive)
       │
       ▼
Goal & Horizon Analyzer (Short-term <=3y / Medium-term 3-7y / Long-term 7y+)
       │
       ▼
Portfolio Construction Engine (Deterministic asset class weights & SEBI category allocation)
       │
       ▼
Document Knowledge Base (SID factsheet chunks with exact page-level citations)
       │
       ▼
Compliance Guardrails (Refuses guaranteed returns, excessive risk, or missing data)
       │
       ▼
AI Advisory Co-Pilot (Grounded explanation generation + RIA audit logging)
       │
       ▼
Web Dashboard (Streamlit interactive tabs, inspectable math, and validation runner)
```

### Portfolio Construction Methodology
```text
Risk Profile (Scored) + Stated Goal + Horizon + Liquidity Buffer + Model Constraints
                                    ▼
       Deterministic Allocation Engine (Inspectable Mathematical Rules)
                                    ▼
       Final Portfolio (Weights sum to exactly 100.0% | Zero LLM fabrication)
```

---

## 3. Target Personas (From Rulebook)

| # | Persona | Age | Profile Summary | Key Constraints / Suitability Focus |
|---|---------|-----|-----------------|-------------------------------------|
| 1 | **Fresh Graduate** | 23 | ₹55k/mo take-home, early career | System Suitability Guardrail triggers emergency buffer carveout (₹25k) before equity compounding. |
| 2 | **Young Couple** | 31 | Dual income, home loan liabilities | Goal in 15 yrs (child education); debt obligations accounted for; balanced wealth accumulation. |
| 3 | **Small Business** | 44 | Irregular cash flow, retirement at 58 | High liquidity buffer required (6 mo); moderate retirement accumulation over 14-year horizon. |
| 4 | **Doctor (Patna)** | 38 | High income, risk-averse | Fiduciary stated-risk cap enforced; secondary parent healthcare corpus (20% liquid debt). |
| 5 | **Retiree (Chennai)**| 68 | ₹80L corpus + pension | Senior citizen capital preservation constraint; 70% Debt, 15% Liquid SWP cash flow for 25 yrs. |
| 6 | **Aggressive Trader**| 29 | F&O drawdown history | **Suitability enforcement**: Flag high-risk mismatch; cap equity at 10% due to short 3-yr horizon. |

---

## 4. Central Source Registry

| Source ID | Category | Title | Reference / Locator |
|---|---|---|---|
| `SEBI_IA_REG_16_2013` | Regulatory Reference | SEBI (Investment Advisers) Regulations, 2013 | Reg 16 (Risk Profiling) |
| `SEBI_IA_REG_17_2013` | Regulatory Reference | SEBI (Investment Advisers) Regulations, 2013 | Reg 17 (Suitability) |
| `SEBI_IA_REG_19_2013` | Regulatory Reference | SEBI (Investment Advisers) Regulations, 2013 | Reg 19 (Maintenance of Records) |
| `SEBI_MF_CATEGORIZATION_2017` | Regulatory Reference | Categorization of Mutual Fund Schemes | SEBI Circular SEBI/HO/IMD/DF3/CIR/P/2017/114 |
| `SEBI_CODE_OF_CONDUCT` | Regulatory Reference | Code of Conduct for Investment Advisers | SEBI (IA) Regulations, 2013, Third Schedule |
| `HDFC_TOP_100_SID` | Financial Document | HDFC Top 100 Fund SID | `data/raw/HDFC_Top_100_Fund_SID.pdf` (Page 3 for Exit Load) |
| `ICICI_CORP_BOND_SID` | Financial Document | ICICI Pru Corporate Bond Fund SID | `data/raw/ICICI_Pru_Corporate_Bond_Fund_SID.pdf` (Page 2 for Duration) |
| `SBI_LIQUID_SID` | Financial Document | SBI Liquid Fund SID | `data/raw/SBI_Liquid_Fund_SID.pdf` (Page 3 for Graded Exit Load) |
| `MODEL_LIQUIDITY_BUFFER` | Model Methodology | Liquidity Buffer Sizing: 3-6 mo expenses | Model-Imposed Constraint (Standard financial planning practice) |
| `MODEL_ASSET_CAPS` | Model Methodology | Risk-Budgeted Asset Allocation Boundaries | Model-Imposed Constraint (`src/portfolio/engine.py`) |
| `AI_TOOL_COPILOT` | AI Tool Disclosure | Local Deterministic Synthesizer / LLM Adapter | `src/llm/copilot.py` (Explanation synthesis only) |

---

## 5. Setup & Reproducibility

### Prerequisites
- Python 3.10+ (tested on Python 3.14.2 64-bit)
- Windows / macOS / Linux

### Installation & Launch
```bash
# 1. Activate virtual environment
.\.venv\Scripts\Activate.ps1   # On Windows
# source .venv/bin/activate    # On Linux/macOS

# 2. Run deterministic unit & integration tests
pytest tests/

# 3. Launch Web Application
.\run_app.ps1                  # On PowerShell
# Or run_app.bat
```
App runs at `http://localhost:8501`.

---

## 6. AI Tooling & LLM Disclosures
- **What the AI Tool is Used For**: Generating plain-language explanations from deterministic mathematical results, summarizing verbatim text chunks from official SIDs, and explaining regulatory constraints to clients.
- **What the AI Tool is NOT Allowed to Decide**: Client risk scoring (computed deterministically via `SuitabilityEngine`), portfolio asset allocation percentages (computed via `PortfolioEngine`), generating ungrounded facts or citations.
- **Page-Level Grounded Q&A**: Every answer returns exact document name, physical page number, and verbatim excerpt. If evidence is not present, returns `"Evidence not found in the indexed documents."`
