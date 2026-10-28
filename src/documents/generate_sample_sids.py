"""Generate authentic SEBI-standard Scheme Information Document (SID) PDFs for testing and inspection."""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def create_hdfc_top_100_sid(output_path: Path):
    """Create authentic 4-page Scheme Information Document for HDFC Top 100 Fund."""
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Title"],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1A365D"),
    )
    h2_style = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"),
    )
    body_style = styles["Normal"]

    # --- PAGE 1 ---
    story.append(Paragraph("SCHEME INFORMATION DOCUMENT (SID)", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>HDFC Top 100 Fund</b>", h2_style))
    story.append(Paragraph("<i>An open-ended equity scheme predominantly investing in large cap stocks</i>", body_style))
    story.append(Spacer(1, 15))

    p1_data = [
        ["Key Parameter", "Scheme Specification"],
        ["Scheme Category", "Large Cap Fund (SEBI Defined)"],
        ["Benchmark Index", "NIFTY 100 Total Returns Index (TRI)"],
        ["Investment Objective", "To provide long-term capital appreciation and income by predominantly investing in large cap companies."],
        ["Riskometer Level", "Very High Risk (Principal will be at very high risk)"],
        ["Type of Scheme", "Open-Ended Growth & IDCW Scheme"],
    ]
    t1 = Table(p1_data, colWidths=[160, 320])
    t1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDF2F7")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1A202C")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t1)
    story.append(PageBreak())

    # --- PAGE 2 ---
    story.append(Paragraph("SECTION II: ASSET ALLOCATION PATTERN", h2_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Under normal circumstances, the asset allocation of the Scheme will be as follows:", body_style))
    story.append(Spacer(1, 10))

    p2_data = [
        ["Instruments", "Indicative Allocation (% of Total Assets)", "Risk Profile"],
        ["Equity & Equity-related instruments of Large Cap companies", "80% to 100%", "Very High"],
        ["Equity & Equity-related instruments of other companies", "0% to 20%", "Very High"],
        ["Debt Securities and Money Market Instruments", "0% to 20%", "Low to Moderate"],
        ["Units issued by REITs and InvITs", "0% to 10%", "Medium to High"],
    ]
    t2 = Table(p2_data, colWidths=[200, 160, 120])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDF2F7")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t2)
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "<b>Definition of Large Cap:</b> As defined by SEBI circular SEBI/HO/IMD/DF3/CIR/P/2017/114 dated October 06, 2017, "
        "Large Cap companies are the 1st to 100th companies in terms of full market capitalization listed on recognized stock exchanges.",
        body_style,
    ))
    story.append(PageBreak())

    # --- PAGE 3 ---
    story.append(Paragraph("SECTION III: FEES, EXPENSES & EXIT LOAD", h2_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Exit Load Structure:</b><br/>"
        "• In respect of each purchase / switch-in of Units, an Exit Load of <b>1.00%</b> is payable if Units are redeemed or switched out within <b>1 year (365 days)</b> from the date of allotment.<br/>"
        "• No Exit Load (<b>Nil</b>) is payable if Units are redeemed or switched out after 1 year (365 days) from the date of allotment.<br/>"
        "• No entry load will be charged by the Scheme pursuant to SEBI circular no. SEBI/IMD/CIR No. 4/168230/09.",
        body_style,
    ))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "<b>Total Expense Ratio (TER):</b><br/>"
        "As per Regulation 52(6)(c) of SEBI (Mutual Funds) Regulations, 1996, the maximum recurring expenses permissible under the Regular Plan is up to 2.25% on the first ₹500 crores of daily average net assets, reducing progressively with AUM scale. Direct Plan features a lower expense ratio excluding distribution commissions.",
        body_style,
    ))
    story.append(PageBreak())

    # --- PAGE 4 ---
    story.append(Paragraph("SECTION IV: APPLICATION DETAILS & FUND MANAGERS", h2_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Minimum Application Amount:</b><br/>"
        "• Lump Sum Purchase: Minimum ₹1,000 and in multiples of ₹1 thereafter.<br/>"
        "• Additional Purchase: Minimum ₹1,000 and in multiples of ₹1 thereafter.<br/>"
        "• Systematic Investment Plan (SIP): Minimum ₹500 per month with minimum 6 installments.<br/>"
        "• Minimum Redemption Amount: ₹500 or 50 units or account balance, whichever is lower.",
        body_style,
    ))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "<b>Fund Management & Mandate:</b><br/>"
        "Managed with disciplined bottom-up stock selection focusing on industry leaders with competitive moats, solid return on equity (ROE), and conservative debt-to-equity ratios. The Scheme does not invest in unhedged foreign securities exceeding 10% of total AUM.",
        body_style,
    ))
    doc.build(story)


def create_corporate_bond_sid(output_path: Path):
    """Create authentic 4-page Scheme Information Document for ICICI Prudential Corporate Bond Fund."""
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle("DocTitle", parent=styles["Title"], fontSize=18, leading=22, textColor=colors.HexColor("#1A365D"))
    h2_style = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, leading=16, textColor=colors.HexColor("#2B6CB0"))
    body_style = styles["Normal"]

    # PAGE 1
    story.append(Paragraph("SCHEME INFORMATION DOCUMENT (SID)", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>ICICI Prudential Corporate Bond Fund</b>", h2_style))
    story.append(Paragraph("<i>An open-ended debt scheme predominantly investing in AA+ and above rated corporate bonds</i>", body_style))
    story.append(Spacer(1, 15))

    p1_data = [
        ["Key Parameter", "Scheme Specification"],
        ["Scheme Category", "Corporate Bond Fund (SEBI Defined)"],
        ["Benchmark Index", "NIFTY Corporate Bond Index B-III"],
        ["Investment Objective", "To generate regular income and capital appreciation through investments predominantly in corporate debt securities."],
        ["Riskometer Level", "Moderate Risk"],
        ["Credit Quality Mandate", "Minimum 80% in AA+ and equivalent highest-rated corporate bonds."],
    ]
    t1 = Table(p1_data, colWidths=[160, 320])
    t1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDF2F7")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t1)
    story.append(PageBreak())

    # PAGE 2
    story.append(Paragraph("SECTION II: ASSET ALLOCATION & DURATION PROFILE", h2_style))
    story.append(Spacer(1, 10))
    p2_data = [
        ["Instruments", "Indicative Allocation (% of Total Assets)", "Risk Profile"],
        ["Corporate Debt securities rated AA+ and above", "80% to 100%", "Low to Moderate"],
        ["Other Debt and Money Market Instruments", "0% to 20%", "Low"],
        ["Government Securities and Treasury Bills", "0% to 20%", "Low"],
    ]
    t2 = Table(p2_data, colWidths=[200, 160, 120])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDF2F7")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t2)
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "<b>Macaulay Duration Mandate:</b> The Macaulay duration of the portfolio is managed generally between <b>2 years and 4 years</b> depending on the interest rate environment and yield curve outlook.",
        body_style,
    ))
    story.append(PageBreak())

    # PAGE 3
    story.append(Paragraph("SECTION III: FEES & EXIT LOAD", h2_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Exit Load Structure:</b><br/>"
        "• Exit Load: <b>Nil</b>.<br/>"
        "• Investors can redeem or switch out units on any Business Day without incurring any exit load penalty.<br/>"
        "• Entry Load: Nil as per SEBI regulations.",
        body_style,
    ))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "<b>Credit Risk Mitigation Policy:</b> The Scheme strictly enforces issuer exposure limits and avoids credit downgrades by investing exclusively in instruments rated by accredited rating agencies (CRISIL, ICRA, CARE, India Ratings).",
        body_style,
    ))
    story.append(PageBreak())

    # PAGE 4
    story.append(Paragraph("SECTION IV: APPLICATION DETAILS", h2_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Investment Amounts:</b><br/>"
        "• Minimum Initial Application Amount: ₹5,000 and in multiples of ₹1 thereafter.<br/>"
        "• Minimum Monthly SIP Amount: ₹1,000 per month (minimum 6 installments).<br/>"
        "• Systematic Withdrawal Plan (SWP): Available for monthly, quarterly, or semi-annual payouts with minimum ₹500 per tranche.",
        body_style,
    ))
    doc.build(story)


def create_liquid_fund_sid(output_path: Path):
    """Create authentic 4-page Scheme Information Document for SBI Liquid Fund."""
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle("DocTitle", parent=styles["Title"], fontSize=18, leading=22, textColor=colors.HexColor("#1A365D"))
    h2_style = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, leading=16, textColor=colors.HexColor("#2B6CB0"))
    body_style = styles["Normal"]

    # PAGE 1
    story.append(Paragraph("SCHEME INFORMATION DOCUMENT (SID)", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>SBI Liquid Fund</b>", h2_style))
    story.append(Paragraph("<i>An open-ended liquid scheme with high liquidity and capital preservation</i>", body_style))
    story.append(Spacer(1, 15))

    p1_data = [
        ["Key Parameter", "Scheme Specification"],
        ["Scheme Category", "Liquid Fund (SEBI Defined)"],
        ["Benchmark Index", "CRISIL Liquid Debt Index"],
        ["Investment Objective", "To provide reasonable returns commensurate with low risk and high degree of liquidity."],
        ["Riskometer Level", "Low to Moderate Risk"],
        ["Maximum Maturity", "Residual maturity of all securities does not exceed 91 days."],
    ]
    t1 = Table(p1_data, colWidths=[160, 320])
    t1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDF2F7")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t1)
    story.append(PageBreak())

    # PAGE 2
    story.append(Paragraph("SECTION II: ASSET ALLOCATION", h2_style))
    story.append(Spacer(1, 10))
    p2_data = [
        ["Instruments", "Indicative Allocation (% of Total Assets)", "Risk Profile"],
        ["Money market and debt instruments with maturity up to 91 days", "100%", "Low"],
        ["Commercial Paper (CP), Certificate of Deposit (CD), T-Bills", "100%", "Low"],
    ]
    t2 = Table(p2_data, colWidths=[240, 140, 100])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDF2F7")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t2)
    story.append(PageBreak())

    # PAGE 3
    story.append(Paragraph("SECTION III: GRADED EXIT LOAD STRUCTURE", h2_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "In accordance with SEBI circular SEBI/HO/IMD/DF2/CIR/P/2019/101, a graded exit load is levied on redemptions within 7 days of allotment:",
        body_style,
    ))
    story.append(Spacer(1, 10))

    exit_load_data = [
        ["Investor Exit Upon Allotment", "Exit Load as % of Redemption NAV"],
        ["Day 1", "0.0070%"],
        ["Day 2", "0.0065%"],
        ["Day 3", "0.0060%"],
        ["Day 4", "0.0055%"],
        ["Day 5", "0.0050%"],
        ["Day 6", "0.0045%"],
        ["Day 7 onwards", "Nil (0.0000%)"],
    ]
    t3 = Table(exit_load_data, colWidths=[240, 240])
    t3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDF2F7")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t3)
    story.append(PageBreak())

    # PAGE 4
    story.append(Paragraph("SECTION IV: APPLICATION DETAILS & CUT-OFF TIMINGS", h2_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Cut-off Timings for Liquid Funds:</b><br/>"
        "• Purchases: 1:30 PM (Funds realization before cut-off gets previous day's closing NAV).<br/>"
        "• Redemptions: 3:00 PM (Processed on same business day NAV; funds credited by T+1 business day).<br/>"
        "• Minimum Investment: ₹500 and in multiples of ₹1 thereafter.",
        body_style,
    ))
    doc.build(story)


def generate_all_sample_sids(target_dir: Path):
    """Generate all three authentic SID files into target directory."""
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    hdfc_path = target_dir / "HDFC_Top_100_Fund_SID.pdf"
    icici_path = target_dir / "ICICI_Pru_Corporate_Bond_Fund_SID.pdf"
    sbi_path = target_dir / "SBI_Liquid_Fund_SID.pdf"

    create_hdfc_top_100_sid(hdfc_path)
    create_corporate_bond_sid(icici_path)
    create_liquid_fund_sid(sbi_path)
    print(f"Generated 3 authentic SIDs in {target_dir}")


if __name__ == "__main__":
    generate_all_sample_sids(Path("data/raw"))

