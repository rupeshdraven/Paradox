"""PS4: AI Co-Pilot for SEBI-Registered Investment Advisers.

Prototype designed around the Zeckathon PS4 requirements; not SEBI-approved or certified.

Architecture & Functional Separation:
1. Client Profiling & 6 Target Rulebook Personas + Custom Profile Builder
2. Inspectable Rules-Based Suitability Engine
3. Goal-Based Deterministic Mutual Fund Allocation
4. Page-Level Grounded SID/Factsheet Q&A
5. Compliance & Regulatory Guardrails
6. Full 5-Layer End-to-End Audit Trail with JSON Export
7. Deterministic Validation Runner (Test Cases A to H)
8. Central Source Registry & AI Tooling Disclosures
"""

import json
import sys
from pathlib import Path

# Ensure project root is always in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from src.profiling import (
    CashFlowStability,
    ClientProfile,
    GoalType,
    RiskTolerance,
    get_all_personas,
    get_persona,
)
from src.suitability import SuitabilityEngine
from src.portfolio import PortfolioEngine
from src.guardrails import ComplianceGuardrails
from src.documents import BM25Retriever, DocumentParser
from src.llm import AICopilot
from src.validation import ValidationRunner
from src.registry import get_source_registry

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Co-Pilot for SEBI-Registered Investment Advisers | PS4",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for high-contrast professional styling
st.markdown(
    """
    <style>
    .metric-badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-data { background-color: #EBF8FF; color: #2B6CB0; border: 1px solid #BEE3F8; }
    .badge-rule { background-color: #F0FFF4; color: #276749; border: 1px solid #C6F6D5; }
    .badge-llm { background-color: #FAF5FF; color: #6B46C1; border: 1px solid #E9D8FD; }
    .badge-warn { background-color: #FFFAF0; color: #DD6B20; border: 1px solid #FEEBC8; }
    .badge-danger { background-color: #FFF5F5; color: #C53030; border: 1px solid #FED7D7; }
    .pipeline-box {
        background-color: #F7FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 12px;
        font-family: monospace;
        font-size: 0.95rem;
        margin-bottom: 15px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] { padding-top: 8px; padding-bottom: 8px; font-weight: 600; font-size: 0.9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_document_knowledge_base():
    """Parse and index official Scheme Information Documents (SIDs)."""
    raw_dir = Path("data/raw")
    if not raw_dir.exists() or len(list(raw_dir.glob("*.pdf"))) == 0:
        from src.documents.generate_sample_sids import generate_all_sample_sids
        generate_all_sample_sids(raw_dir)
    chunks = DocumentParser.parse_directory(raw_dir)
    retriever = BM25Retriever(chunks)
    return chunks, retriever


chunks, retriever = load_document_knowledge_base()

# --- SIDEBAR: PERSONA SELECTOR & CONTROLS ---
st.sidebar.title("⚖️ SEBI RIA Co-Pilot")
st.sidebar.caption("PS4: AI-Powered Advisory | IIT Patna × Zetheta Hackathon")

persona_options = {
    "fresh_graduate": "1. Fresh Graduate (Age 23)",
    "young_couple": "2. Young Couple (Dual Income, Age 31)",
    "small_business": "3. Small Business Owner (Age 44)",
    "doctor_patna": "4. Doctor, Patna (High Earner, Age 38)",
    "retiree_chennai": "5. Retiree, Chennai (Corpus ₹80L, Age 68)",
    "aggressive_trader": "6. Aggressive Trader (F&O History, Age 29)",
    "custom": "➕ Custom Profile Builder",
}

selected_persona_key = st.sidebar.selectbox(
    "Select Client Persona (Rulebook):",
    options=list(persona_options.keys()),
    format_func=lambda k: persona_options[k],
    index=0,
)

# Load profile
if selected_persona_key == "custom":
    st.sidebar.markdown("### 📝 Custom Client Profile Inputs")
    c_name = st.sidebar.text_input("Client Name", value="Aditi Singhania")
    c_age = int(st.sidebar.number_input("Age", min_value=18, max_value=95, value=32))
    c_income = float(st.sidebar.number_input("Monthly Income (₹)", min_value=0.0, value=120_000.0, step=5000.0))
    c_expenses = float(st.sidebar.number_input("Monthly Expenses (₹)", min_value=0.0, value=45_000.0, step=2000.0))
    c_debt = float(st.sidebar.number_input("Monthly Debt / EMI (₹)", min_value=0.0, value=15_000.0, step=1000.0))
    c_savings = float(st.sidebar.number_input("Liquid Savings (₹)", min_value=0.0, value=150_000.0, step=10000.0))
    c_investments = float(st.sidebar.number_input("Existing Investments (₹)", min_value=0.0, value=400_000.0, step=25000.0))
    c_liabilities = float(st.sidebar.number_input("Total Liabilities (₹)", min_value=0.0, value=1_500_000.0, step=50000.0))
    c_inv_amt = float(st.sidebar.number_input("Investment Capacity (₹)", min_value=500.0, value=30_000.0, step=1000.0))
    c_is_sip = st.sidebar.radio("Investment Type", ["Monthly SIP", "Lump Sum"]) == "Monthly SIP"
    c_horizon = float(st.sidebar.slider("Investment Horizon (Years)", min_value=0.5, max_value=35.0, value=10.0, step=0.5))

    goal_options = list(GoalType)
    c_goal = st.sidebar.selectbox(
        "Primary Goal",
        options=goal_options,
        format_func=lambda g: g.value.replace("_", " ").title(),
        index=goal_options.index(GoalType.LONG_TERM_WEALTH),
    )

    risk_options = list(RiskTolerance)
    c_risk = st.sidebar.selectbox(
        "Stated Risk Appetite",
        options=risk_options,
        format_func=lambda r: r.value.replace("_", " ").title(),
        index=risk_options.index(RiskTolerance.MODERATE),
    )

    stability_options = list(CashFlowStability)
    c_stability = st.sidebar.selectbox(
        "Cash Flow Stability",
        options=stability_options,
        format_func=lambda s: s.value.replace("_", " ").title(),
        index=stability_options.index(CashFlowStability.STABLE_SALARIED),
    )

    c_fo = st.sidebar.checkbox("Past F&O Speculative Drawdown History", value=False)

    active_profile = ClientProfile(
        client_id="custom_client",
        name=c_name,
        age=c_age,
        monthly_income=c_income,
        monthly_expenses=c_expenses,
        monthly_debt_obligations=c_debt,
        existing_savings=c_savings,
        existing_investments=c_investments,
        total_liabilities=c_liabilities,
        investment_amount=c_inv_amt,
        is_sip=c_is_sip,
        investment_horizon_years=c_horizon,
        primary_goal=c_goal,
        stated_risk_tolerance=c_risk,
        cash_flow_stability=c_stability,
        has_emergency_fund=(c_savings >= c_expenses * 3.0),
        past_fo_drawdown=c_fo,
        notes="Custom client profile entered directly by adviser.",
    )
else:
    active_profile = get_persona(selected_persona_key)
    with st.sidebar.expander("⚙️ Fine-Tune Persona Inputs"):
        st.caption("Stress-test parameters live:")
        t_savings = st.number_input(
            "Existing Savings (₹)",
            value=float(active_profile.existing_savings),
            step=25000.0,
            key=f"t_sav_{active_profile.client_id}",
        )
        t_inv_amt = st.number_input(
            "Investment Amount (₹)",
            value=float(active_profile.investment_amount),
            step=5000.0,
            key=f"t_inv_{active_profile.client_id}",
        )
        t_horizon = st.number_input(
            "Horizon (Years)",
            value=float(active_profile.investment_horizon_years),
            step=1.0,
            key=f"t_hor_{active_profile.client_id}",
        )
        active_profile.existing_savings = t_savings
        active_profile.investment_amount = t_inv_amt
        active_profile.investment_horizon_years = t_horizon

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Operational Separation**:<br/>"
    "<span class='metric-badge badge-data'>DATA-DERIVED</span> Input verification<br/>"
    "<span class='metric-badge badge-rule'>RULE-BASED</span> Math & Suitability<br/>"
    "<span class='metric-badge badge-llm'>LLM-GENERATED</span> Grounded Synthesis",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
st.sidebar.caption("Prototype designed around the Zeckathon PS4 requirements; not SEBI-approved or certified.")

# --- RUN DETERMINISTIC PIPELINE ---
suitability = SuitabilityEngine.assess(active_profile)
portfolio = PortfolioEngine.construct_portfolio(active_profile, suitability)
guardrails = ComplianceGuardrails.evaluate_all(profile=active_profile, assessment=suitability)
copilot_explanation = AICopilot.generate_recommendation_explanation(
    profile=active_profile,
    assessment=suitability,
    portfolio=portfolio,
    guardrails=guardrails,
)
audit_record = AICopilot.create_audit_record(
    profile=active_profile,
    assessment=suitability,
    portfolio=portfolio,
    guardrails=guardrails,
    explanation_text=copilot_explanation,
)

# --- MAIN DASHBOARD HEADER ---
st.title("📈 AI Co-Pilot for SEBI-Registered Investment Advisers")
st.warning("⚠️ Prototype developed for the Zeckathon PS4 problem statement. This system is not SEBI-approved or certified and does not constitute independent investment advice.")

# Summary Top Metrics
mcol1, mcol2, mcol3, mcol4, mcol5 = st.columns(5)
with mcol1:
    st.metric("Age", f"{active_profile.age} yrs")
with mcol2:
    mode = "SIP" if active_profile.is_sip else "Lump Sum"
    st.metric(f"Invest Capacity ({mode})", f"₹{active_profile.investment_amount:,.0f}")
with mcol3:
    st.metric("Horizon", f"{active_profile.investment_horizon_years:.1f} yrs")
with mcol4:
    st.metric(
        "Emergency Buffer",
        f"{active_profile.computed_emergency_buffer_months:.1f} mo",
        delta="Deficit (<3 mo)" if suitability.requires_emergency_carveout else "Adequate",
        delta_color="inverse" if suitability.requires_emergency_carveout else "normal",
    )
with mcol5:
    st.metric("Suitability Score", f"{suitability.composite_score:.1f}/100")

# Guardrail Warning Banners
if guardrails.warnings:
    for w in guardrails.warnings:
        st.warning(f"⚠️ {w}")

st.markdown("---")

# --- TABS INTERFACE ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "1. Client Profiling",
    "2. Suitability Assessment",
    "3. Goal-Based Portfolio",
    "4. Page-Level Grounded Q&A",
    "5. Full Audit Trail",
    "6. Validation / Test Cases",
    "7. Source Registry & AI Disclosures",
])

# ==================== TAB 1: CLIENT PROFILING ====================
with tab1:
    st.subheader("Client Financial Profiling & Cash Flow Analysis")
    st.caption("Layer: DATA-DERIVED RESULT | Designed with reference to SEBI Regulation 16 (Risk Profiling) requirements")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("#### Cash Flow & Balance Sheet")
        st.write(f"- **Monthly Take-Home Income**: ₹{active_profile.monthly_income:,.2f}")
        st.write(f"- **Essential Monthly Expenses**: ₹{active_profile.monthly_expenses:,.2f}")
        st.write(f"- **Monthly Debt Servicing (EMIs)**: ₹{active_profile.monthly_debt_obligations:,.2f}")
        st.write(f"- **Net Monthly Investable Surplus**: **₹{active_profile.net_monthly_surplus:,.2f}**")
        st.write(f"- **Liquid Cash / Savings**: ₹{active_profile.existing_savings:,.2f}")
        st.write(f"- **Existing Investments**: ₹{active_profile.existing_investments:,.2f}")
        st.write(f"- **Total Outstanding Liabilities**: ₹{active_profile.total_liabilities:,.2f}")

    with col_right:
        st.markdown("#### Goal, Horizon & Stated Risk Appetite")
        st.write(f"- **Primary Goal**: `{active_profile.primary_goal.value.replace('_', ' ').title()}`")
        if active_profile.secondary_goals:
            sec_goals = ", ".join([g.value.replace('_', ' ').title() for g in active_profile.secondary_goals])
            st.write(f"- **Secondary Goals**: {sec_goals}")
        st.write(f"- **Investment Horizon**: {active_profile.investment_horizon_years:.1f} years")
        st.write(f"- **Stated Risk Tolerance**: `{active_profile.stated_risk_tolerance.value.replace('_', ' ').title()}`")
        st.write(f"- **Income Stream Stability**: `{active_profile.cash_flow_stability.value.replace('_', ' ').title()}`")
        st.write(f"- **Past F&O Drawdown History**: {'🚨 Yes (High Risk Flag)' if active_profile.past_fo_drawdown else '✅ None reported'}")
        if active_profile.notes:
            st.info(f"**Persona Notes**: {active_profile.notes}")

    st.markdown("#### Computed Financial Health Indicators")
    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        st.metric("Savings Rate", f"{active_profile.savings_rate:.1%}")
    with fcol2:
        st.metric("Debt-to-Income (DTI)", f"{active_profile.debt_to_income_ratio:.1%}")
    with fcol3:
        st.metric("Liquid Emergency Buffer", f"{active_profile.computed_emergency_buffer_months:.1f} months")

# ==================== TAB 2: SUITABILITY ASSESSMENT ====================
with tab2:
    st.subheader("Deterministic Suitability Assessment")
    st.caption("Layer: RULE-BASED RESULT | Designed with reference to SEBI Regulation 17 (Suitability) requirements | Inspectable mathematical scoring")

    scol1, scol2, scol3, scol4 = st.columns(4)
    with scol1:
        st.metric("Capacity Score (30%)", f"{suitability.capacity_score:.1f}/100")
        st.progress(suitability.capacity_score / 100.0)
    with scol2:
        st.metric("Tolerance Score (25%)", f"{suitability.tolerance_score:.1f}/100")
        st.progress(suitability.tolerance_score / 100.0)
    with scol3:
        st.metric("Horizon Score (25%)", f"{suitability.horizon_score:.1f}/100")
        st.progress(suitability.horizon_score / 100.0)
    with scol4:
        st.metric("Liquidity Score (20%)", f"{suitability.liquidity_score:.1f}/100")
        st.progress(suitability.liquidity_score / 100.0)

    st.markdown("---")
    st.markdown("#### Exact Arithmetic Breakdown")
    st.code(suitability.score_formula, language="text")

    res_col1, res_col2 = st.columns([1, 1])

    with res_col1:
        st.markdown("#### Risk Categorization Result")
        st.write(f"- **Raw Calculated Category**: `{suitability.raw_category.value.replace('_', ' ').title()}`")
        st.write(f"- **Final Approved Category**: **`{suitability.final_category.value.replace('_', ' ').title()}`**")
        st.write(f"- **Model-Imposed Maximum Equity Exposure**: **{suitability.max_equity_pct:.0f}%**")
        st.write(f"- **Model-Imposed Minimum Debt/Liquid Exposure**: **{suitability.min_debt_pct:.0f}%**")
        st.caption("Constraint imposed by the portfolio model for suitability/risk control; not represented as a universal SEBI limit.")

    with res_col2:
        st.markdown("#### System Suitability Guardrails Applied")
        if suitability.active_overrides:
            for override in suitability.active_overrides:
                st.error(f"⚖️ {override}")
        else:
            st.success("✅ Standard profile: No model overrides required.")

    with st.expander("🔍 Inspect Dimensional Scoring Rationale"):
        for item in suitability.scoring_breakdown:
            st.write(f"- {item}")

# ==================== TAB 3: GOAL-BASED PORTFOLIO ====================
with tab3:
    st.subheader("Goal-Based Mutual Fund Allocation")
    st.caption("Layer: RULE-BASED RESULT | SEBI Mutual Fund Scheme Categorization (Circular 2017/114)")

    # Visible Portfolio Construction Methodology Section
    st.markdown("#### Portfolio Construction Methodology")
    st.markdown(
        """
        <div class="pipeline-box">
        <b>Deterministic Pipeline Flow:</b><br/>
        Risk Profile (Scored) + Stated Goal + Horizon + Liquidity Buffer + Model Constraints<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;▼<br/>
        Deterministic Allocation Engine (Inspectable Mathematical Rules)<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;▼<br/>
        Final Portfolio (Weights sum to exactly 100.0% | Zero LLM percentage fabrication)
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Broad Asset Class Weights
    st.markdown("#### Broad Asset Class Distribution (Must sum to 100.0%)")
    wcol1, wcol2, wcol3, wcol4 = st.columns(4)
    with wcol1:
        st.metric("Equity", f"{portfolio.equity_pct:.0f}%")
        st.progress(portfolio.equity_pct / 100.0)
    with wcol2:
        st.metric("Debt", f"{portfolio.debt_pct:.0f}%")
        st.progress(portfolio.debt_pct / 100.0)
    with wcol3:
        st.metric("Liquid / Cash", f"{portfolio.liquid_pct:.0f}%")
        st.progress(portfolio.liquid_pct / 100.0)
    with wcol4:
        st.metric("Gold / Commodities", f"{portfolio.gold_pct:.0f}%")
        st.progress(portfolio.gold_pct / 100.0)

    if portfolio.emergency_carveout_amount > 0:
        st.warning(f"🚨 **Liquidity Buffer Priority**: {portfolio.emergency_carveout_instruction}")

    st.markdown("#### Regulated Mutual Fund Scheme Category Breakdown")
    cat_rows = []
    for c in portfolio.category_allocations:
        cat_rows.append({
            "Asset Class": c.asset_class,
            "SEBI Scheme Category": c.sebi_category,
            "Target Weight": f"{c.target_weight_pct:.1f}%",
            "Monthly SIP (INR)": f"₹{c.monthly_sip_amount:,.2f}" if c.monthly_sip_amount else "-",
            "Lump Sum (INR)": f"₹{c.lump_sum_amount:,.2f}" if c.lump_sum_amount else "-",
            "Rationale": c.rationale,
            "Applicable Constraints": "; ".join(c.applicable_constraints[:2]),
        })
    st.dataframe(pd.DataFrame(cat_rows), use_container_width=True, hide_index=True)

    st.markdown("#### Horizon Glidepath Strategy")
    st.info(f"🛡️ **De-risking Schedule**: {portfolio.glidepath_strategy}")

# ==================== TAB 4: PAGE-LEVEL GROUNDED Q&A ====================
with tab4:
    st.subheader("Page-Level Grounded Q&A (Factsheets & SIDs)")
    st.caption("Layer: DATA-DERIVED CITATIONS | Answers grounded strictly in official scheme document text")

    st.write(f"**Knowledge Base Corpus**: {len(chunks)} chunks indexed across official Scheme Information Documents:")
    doc_summary_col1, doc_summary_col2, doc_summary_col3 = st.columns(3)
    with doc_summary_col1:
        st.markdown("📄 **HDFC Top 100 Fund SID**<br/>Category: Large Cap Equity<br/>Pages: 4", unsafe_allow_html=True)
    with doc_summary_col2:
        st.markdown("📄 **ICICI Corporate Bond SID**<br/>Category: Corporate Debt<br/>Pages: 4", unsafe_allow_html=True)
    with doc_summary_col3:
        st.markdown("📄 **SBI Liquid Fund SID**<br/>Category: Liquid Fund<br/>Pages: 4", unsafe_allow_html=True)

    with st.expander("📥 Ingest Additional Scheme Information Document (PDF)"):
        uploaded_pdf = st.file_uploader("Upload Scheme PDF (e.g., SID / Factsheet):", type=["pdf"])
        if uploaded_pdf is not None:
            save_dest = Path("data/raw") / uploaded_pdf.name
            if not save_dest.exists():
                with open(save_dest, "wb") as f:
                    f.write(uploaded_pdf.getbuffer())
                load_document_knowledge_base.clear()
                st.success(f"Successfully uploaded and indexed {uploaded_pdf.name}! Refreshing...")
                st.rerun()

    st.markdown("---")
    st.markdown("#### Ask a Scheme Question")

    preset_queries = [
        "What is the exit load for HDFC Top 100 Fund?",
        "What is the Day 1 exit load for SBI Liquid Fund?",
        "What is the Macaulay duration for ICICI Prudential Corporate Bond Fund?",
        "Can you guarantee a 15% return on equity funds?",
        "What is the minimum application amount for HDFC Top 100?",
        "What is the quarterly revenue of Tesla electric vehicle sales?",
    ]

    selected_query = st.selectbox("Select a benchmark query or type your own below:", options=[""] + preset_queries)
    custom_query = st.text_input("Enter scheme query:", value=selected_query)

    if custom_query:
        q_guardrail = ComplianceGuardrails.evaluate_all(query=custom_query)
        q_retrieval = retriever.query(custom_query)
        doc_answer = AICopilot.answer_document_query(custom_query, q_retrieval, q_guardrail)

        st.markdown("#### Grounded Response")
        if doc_answer.is_grounded:
            st.success(doc_answer.status_message)
            st.markdown(doc_answer.answer)
            st.markdown("##### Verifiable Citation Metadata")
            st.write(f"- **Document**: `{doc_answer.document_name}`")
            st.write(f"- **Physical Page Number**: **Page {doc_answer.page_number}**")
            st.markdown("##### Verbatim Retrieved Chunk")
            st.code(doc_answer.retrieved_evidence, language="text")
        else:
            if not q_guardrail.is_compliant:
                st.error(doc_answer.answer)
            else:
                st.warning(f"ℹ️ **{doc_answer.answer}**")
                st.caption("Under PS4 guidelines, ungrounded speculation or fabricated citations are strictly barred.")

# ==================== TAB 5: FULL REGULATORY AUDIT TRAIL ====================
with tab5:
    st.subheader("End-to-End RIA Compliance Audit Record")
    st.caption("Layer: REGULATORY AUDITABILITY | Designed with reference to SEBI Regulation 19 (Maintenance of Records) requirements")

    st.markdown(
        """
        <div class="pipeline-box">
        <b>Trace Flow:</b> INPUT → CALCULATION → RISK PROFILE → SUITABILITY → GUARDRAIL → PORTFOLIO → AI EXPLANATION → SOURCE
        </div>
        """,
        unsafe_allow_html=True,
    )

    tcol1, tcol2 = st.columns([1, 1])
    with tcol1:
        st.markdown("#### 1. Input & Calculations")
        st.write(f"- **Request ID**: `{audit_record.request_id}`")
        st.write(f"- **Timestamp (UTC)**: `{audit_record.timestamp_utc}`")
        st.write(f"- **Calculated Suitability Score**: **{audit_record.calculated_suitability_score:.1f}/100**")
        st.write(f"- **Raw Risk Category**: `{audit_record.raw_risk_category}`")
        st.write(f"- **Guardrail-Adjusted Risk Category**: **`{audit_record.risk_category}`**")

    with tcol2:
        st.markdown("#### 2. Sources & Guardrails")
        st.write(f"- **AI Execution Mode**: `{audit_record.ai_execution_mode}`")
        st.write(f"- **Compliance Status**: {'✅ Compliant' if audit_record.guardrail_decisions.get('is_compliant') else '🚨 Refused'}")
        st.write(f"- **Referenced Source Documents**: {len(audit_record.source_documents)} documents")

    st.markdown("---")
    st.markdown("#### AI Advisory Co-Pilot Synthesized Explanation")
    st.markdown(
        f"<div style='background-color:#F7FAFC; padding:15px; border-radius:6px; border-left:4px solid #6B46C1;'>"
        f"{copilot_explanation}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("#### Structured JSON Audit Record (Traceable 5-Layer Output)")
    audit_json = audit_record.model_dump_json(indent=2)
    st.code(audit_json, language="json")

    st.download_button(
        label=f"📥 Download Audit Record JSON ({audit_record.request_id})",
        data=audit_json,
        file_name=f"{audit_record.request_id}.json",
        mime="application/json",
    )

# ==================== TAB 6: VALIDATION / TEST CASES ====================
with tab6:
    st.subheader("Deterministic Validation Test Cases (A to H)")
    st.caption("Verifiable test suite executing all mandatory scenarios from the PS4 Rulebook")

    if st.button("▶️ Execute All 8 Validation Test Cases"):
        st.session_state["validation_results"] = ValidationRunner.run_all_cases()

    val_results = st.session_state.get("validation_results", None)
    if val_results is None:
        val_results = ValidationRunner.run_all_cases()
        st.session_state["validation_results"] = val_results

    # Summary metric
    pass_count = sum(1 for r in val_results if r.status == "PASS")
    st.metric(label="Validation Suite Status", value=f"{pass_count} / {len(val_results)} Cases PASSED")

    for case in val_results:
        with st.container():
            badge_color = "badge-rule" if case.status == "PASS" else "badge-danger"
            st.markdown(
                f"### {case.case_id}: {case.case_name} "
                f"<span class='metric-badge {badge_color}'>{case.status}</span>",
                unsafe_allow_html=True,
            )
            st.write(f"**Target / Scenario**: {case.target_persona_or_scenario}")
            st.write(f"**Expected Behaviour**: {case.expected_behaviour}")
            st.write(f"**Actual Behaviour**: {case.actual_behaviour}")
            if case.audit_details:
                with st.expander("🔍 View Test Audit Details"):
                    for d in case.audit_details:
                        st.write(f"- `{d}`")
            st.markdown("---")

# ==================== TAB 7: SOURCE REGISTRY & AI DISCLOSURES ====================
with tab7:
    st.subheader("Central Source Registry & AI Disclosures")
    st.caption("Statutory references, scheme documents, model methodologies, and AI tooling limits")

    st.markdown("#### 1. Central Source Registry")
    registry = get_source_registry()
    registry_rows = []
    for s_id, entry in registry.items():
        registry_rows.append({
            "Source ID": s_id,
            "Type": entry.source_type,
            "Source Name": entry.source_name,
            "Reference Locator": entry.reference_locator,
            "Date / Version": entry.date_or_version,
            "Purpose in Application": entry.purpose,
        })
    st.dataframe(pd.DataFrame(registry_rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 2. AI Tooling & LLM Disclosure")

    dcol1, dcol2 = st.columns(2)
    with dcol1:
        st.markdown(
            """
            ##### ✅ What the AI Tool is Used For:
            - **Plain-Language Explanation**: Translating deterministic suitability scores and portfolio weights into transparent narrative summaries for the client.
            - **Factsheet Summarization**: Synthesizing answers to investor questions using **only** retrieved verbatim text chunks from ingested SIDs.
            - **Advisory Rationale**: Highlighting why an asset class was chosen based on horizon and risk capacity.
            - **Guardrail Clarification**: Communicating statutory restrictions (e.g. why guaranteed return requests are prohibited under SEBI regulations).
            """
        )
    with dcol2:
        st.markdown(
            """
            ##### 🚫 What the AI Tool is NOT Allowed to Decide:
            - **Cannot Determine Risk Scores**: Suitability scoring is 100% computed via deterministic mathematical arithmetic in `SuitabilityEngine`.
            - **Cannot Assign Portfolio Weights**: Asset class and category percentages are computed by deterministic rules in `PortfolioEngine`.
            - **Cannot Fabricate Citations**: When a document does not contain verifiable evidence, the system is strictly barred from inventing facts or citations.
            - **Cannot Override Guardrails**: The LLM cannot bypass emergency fund buffer requirements or stated risk tolerance ceilings.
            """
        )

    st.markdown("---")
    st.info(
        "**Statutory Non-Endorsement Notice**: "
        "This software is a student prototype developed for the Zetheta × IIT Patna Trading & Investment Club "
        "Hackathon (Problem Statement 4: AI-Powered Advisory). It is not approved, licensed, or certified by SEBI."
    )
