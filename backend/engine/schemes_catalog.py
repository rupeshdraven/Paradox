from typing import List, Dict, Any
from ..models import InvestmentScheme

SCHEMES_DB: List[InvestmentScheme] = [
    InvestmentScheme(
        id="sbi_bluechip",
        name="SBI Bluechip Fund",
        provider="SBI Mutual Fund",
        category="Mutual Funds",
        risk_level="Moderate",
        indicative_return="10–12% p.a.",
        indicative_rate_num=11.5,
        min_investment="₹500",
        min_investment_num=500,
        time_horizon_min_years=5,
        time_horizon_ideal="5–10 Years",
        tax_benefit=False,
        lock_in_period="None",
        liquidity="High",
        best_for="Long-term wealth creation",
        description="Invests in top large-cap companies offering long-term growth with relatively lower risk.",
        badge="Highly Recommended",
        why_recommended=[
            "Matches your moderate risk tolerance with established large-cap stability",
            "Optimal for long-term (5-10 years) wealth compounding",
            "High liquidity allows seamless rebalancing without lock-in penalties",
            "Fits comfortable monthly SIP contribution from your disposable surplus"
        ],
        things_to_consider=[
            "Returns are market-linked and not guaranteed",
            "Short-term market volatility may impact portfolio value temporarily",
            "Long-Term Capital Gains (LTCG) above ₹1.25 Lakh per fiscal year taxed at 12.5%"
        ],
        source_evidence={
            "document": "Scheme Information Document (SID) - SBI Bluechip Fund",
            "regulator": "SEBI Registered Mutual Fund",
            "benchmark": "S&P BSE 100 TRI",
            "risk_o_meter": "Very High (Equity Market Standard) / Moderate in Equities"
        }
    ),
    InvestmentScheme(
        id="ppf_gov",
        name="Public Provident Fund (PPF)",
        provider="Government of India",
        category="Government Schemes",
        risk_level="Very Low",
        indicative_return="7.1% p.a.",
        indicative_rate_num=7.1,
        min_investment="₹500",
        min_investment_num=500,
        time_horizon_min_years=15,
        time_horizon_ideal="15 Years (Partial withdrawals after 6 yrs)",
        tax_benefit=True,
        tax_section="Section 80C (EEE status)",
        lock_in_period="15 Years",
        liquidity="Low",
        best_for="Long-term savings / tax planning",
        description="A safe, long-term investment with guaranteed sovereign backing and tax-free maturity amount.",
        badge="Tax Benefits",
        why_recommended=[
            "Zero default risk backed by the sovereign guarantee of Government of India",
            "Triple Exempt (EEE) tax status: investment, interest, and maturity are 100% tax-free",
            "Provides ballast and risk mitigation against market fluctuations",
            "Guarantees compounding baseline for critical future goals"
        ],
        things_to_consider=[
            "15-year statutory lock-in period limits emergency liquidity",
            "Maximum annual investment limit of ₹1,50,000",
            "Interest rates are reviewed and set quarterly by the Ministry of Finance"
        ],
        source_evidence={
            "document": "Government Savings Promotion General Rules, Ministry of Finance Gazette",
            "regulator": "Ministry of Finance, Government of India",
            "tax_status": "Exempt-Exempt-Exempt (Section 10(11) of Income Tax Act)",
            "rate_notification": "MoF Notification Q3-Q4 FY2025-26 (7.1% compounded annually)"
        }
    ),
    InvestmentScheme(
        id="elss_tax_saver",
        name="ELSS Tax Saver Fund",
        provider="Various Fund Houses (Mirae / Parag Parikh)",
        category="Tax Saving",
        risk_level="High",
        indicative_return="12–15% p.a.",
        indicative_rate_num=13.5,
        min_investment="₹500",
        min_investment_num=500,
        time_horizon_min_years=3,
        time_horizon_ideal="3–5 Years",
        tax_benefit=True,
        tax_section="Section 80C",
        lock_in_period="3 Years (Lowest in 80C)",
        liquidity="Moderate",
        best_for="Long-term tax-efficient investing",
        description="Equity-linked fund with potential for high returns and tax benefits under Section 80C.",
        badge="Section 80C",
        why_recommended=[
            "Dual benefit of tax deduction up to ₹1.5L under Sec 80C plus equity appreciation",
            "Shortest lock-in period (3 years) among all tax-saving instruments in India",
            "Diversified exposure across large, mid, and value stocks for inflation-beating returns"
        ],
        things_to_consider=[
            "Subject to equity market movements with high risk rating",
            "Cannot withdraw capital before 3 years under any circumstance",
            "LTCG above ₹1.25 Lakh per year attracts 12.5% tax upon redemption"
        ],
        source_evidence={
            "document": "SEBI Master Circular for Mutual Funds (Categorization - ELSS)",
            "regulator": "SEBI & Central Board of Direct Taxes (CBDT)",
            "lock_in": "36 Months Mandatory Lock-in per Section 80C(2)(xiii)"
        }
    ),
    InvestmentScheme(
        id="bank_fd",
        name="Fixed Deposit (FD)",
        provider="Banks & Financial Institutions",
        category="Fixed Income",
        risk_level="Very Low",
        indicative_return="6.8–7.5% p.a.",
        indicative_rate_num=7.1,
        min_investment="₹1,000",
        min_investment_num=1000,
        time_horizon_min_years=1,
        time_horizon_ideal="1–3 Years",
        tax_benefit=False,
        lock_in_period="Flexible (Premature withdrawal available)",
        liquidity="High",
        best_for="Capital preservation for short to medium term goals",
        description="A safe investment option with guaranteed returns, suitable for short to medium term goals.",
        badge="Stable Returns",
        why_recommended=[
            "Predictable, guaranteed nominal returns unaffected by stock market gyrations",
            "DICGC insurance cover up to ₹5,00,000 per depositor per bank",
            "Ideal repository for near-term expense buffer and emergency reserves"
        ],
        things_to_consider=[
            "Interest earned is added to income and taxed according to your income slab",
            "Premature withdrawals may incur nominal penalty of 0.5%–1%",
            "Post-tax returns may lag inflation during elevated CPI periods"
        ],
        source_evidence={
            "document": "RBI Master Direction - Interest Rate on Deposits Directions",
            "regulator": "Reserve Bank of India (RBI)",
            "insurance": "DICGC Insured up to ₹5,00,000"
        }
    ),
    InvestmentScheme(
        id="nps_retirement",
        name="National Pension System (NPS)",
        provider="Government of India / PFRDA",
        category="Retirement",
        risk_level="Moderate",
        indicative_return="10–12% p.a.",
        indicative_rate_num=10.8,
        min_investment="₹500",
        min_investment_num=500,
        time_horizon_min_years=10,
        time_horizon_ideal="10+ Years (Till Age 60)",
        tax_benefit=True,
        tax_section="Sec 80CCD(1) & 80CCD(1B) extra ₹50,000",
        lock_in_period="Till Age 60",
        liquidity="Low",
        best_for="Long-term retirement planning",
        description="A long-term retirement savings scheme with market-linked returns and tax benefits.",
        badge="Retirement Planning",
        why_recommended=[
            "Exclusive additional ₹50,000 tax deduction over and above Sec 80C limit",
            "Ultra-low fund management fee (0.09%) maximizes compound growth",
            "Structured asset allocation between Equity (E), Corporate Debt (C), and Gov Bonds (G)",
            "Disciplined nest egg construction with annuity regular income post-retirement"
        ],
        things_to_consider=[
            "Funds locked until age 60; early exit requires 80% mandatory annuity purchase",
            "At retirement, 60% lump sum is tax-free, remaining 40% must buy taxable pension annuity"
        ],
        source_evidence={
            "document": "PFRDA Regulations & Income Tax Act Section 80CCD",
            "regulator": "Pension Fund Regulatory and Development Authority (PFRDA)"
        }
    ),
    InvestmentScheme(
        id="ssy_scheme",
        name="Sukanya Samriddhi Yojana (SSY)",
        provider="Government of India",
        category="Government Schemes",
        risk_level="Very Low",
        indicative_return="8.2% p.a.",
        indicative_rate_num=8.2,
        min_investment="₹250",
        min_investment_num=250,
        time_horizon_min_years=15,
        time_horizon_ideal="Till Child reaches 21 years",
        tax_benefit=True,
        tax_section="Section 80C (EEE)",
        lock_in_period="Until child attains 21 years",
        liquidity="Low",
        best_for="Daughter's higher education and marriage",
        description="A dedicated savings scheme for girl child with high government-notified interest rates and tax benefits.",
        badge="For Girl Child",
        why_recommended=[
            "Highest sovereign fixed interest rate (currently 8.2% p.a.) in small savings schemes",
            "EEE tax advantage: deduction under 80C, tax-free annual interest, tax-free maturity",
            "Strict lock-in guarantees protection of funds intended exclusively for the child's future"
        ],
        things_to_consider=[
            "Eligibility restricted to girl child under age 10 at account opening",
            "Annual deposit ceiling of ₹1,50,000"
        ],
        source_evidence={
            "document": "Sukanya Samriddhi Account Rules, Ministry of Finance",
            "regulator": "Department of Economic Affairs, Ministry of Finance"
        }
    ),
    InvestmentScheme(
        id="nifty50_index",
        name="Nifty 50 Index Fund",
        provider="Leading Asset Management Companies (UTI / HDFC)",
        category="Mutual Funds",
        risk_level="Moderate",
        indicative_return="11–13% p.a.",
        indicative_rate_num=12.0,
        min_investment="₹500",
        min_investment_num=500,
        time_horizon_min_years=5,
        time_horizon_ideal="5+ Years",
        tax_benefit=False,
        lock_in_period="None",
        liquidity="High",
        best_for="Low-cost passive long-term compounding",
        description="Tracks India's top 50 bluechip companies directly with minimal expense ratios and zero fund-manager bias.",
        badge="Low Cost Index",
        why_recommended=[
            "Ultra-low expense ratio (0.1%–0.2%) preserves more capital for long-term compounding",
            "Eliminates fund manager risk while capturing broad Indian economic growth",
            "High liquidity with T+1 redemption cycle"
        ],
        things_to_consider=[
            "Reflects 100% of stock market index drawdowns during corrections",
            "Equity taxation applies on gains upon redemption"
        ],
        source_evidence={
            "document": "NSE Indices Factsheet & SEBI Mutual Fund Scheme Information",
            "regulator": "SEBI",
            "benchmark": "Nifty 50 Total Returns Index (TRI)"
        }
    ),
    InvestmentScheme(
        id="hybrid_balanced",
        name="Balanced Advantage Fund",
        provider="ICICI Prudential / HDFC AMC",
        category="Mutual Funds",
        risk_level="Moderate",
        indicative_return="9–11% p.a.",
        indicative_rate_num=10.0,
        min_investment="₹500",
        min_investment_num=500,
        time_horizon_min_years=3,
        time_horizon_ideal="3–5 Years",
        tax_benefit=False,
        lock_in_period="None",
        liquidity="High",
        best_for="Dynamic asset allocation with downside protection",
        description="Dynamically shifts between equity and debt based on market valuations to buffer downside drops.",
        badge="Downside Cushion",
        why_recommended=[
            "Automated buying low and selling high across equity and debt market cycles",
            "Significantly lower volatility than pure equity funds while retaining equity taxation status",
            "Well-suited for first-time or moderate investors seeking growth without stomach-churning dips"
        ],
        things_to_consider=[
            "May slightly underperform runaway bull markets due to hedging positions",
            "Exit load typically applies if redeemed within 12 months"
        ],
        source_evidence={
            "document": "SEBI Categorization of Mutual Fund Schemes (Dynamic Asset Allocation)",
            "regulator": "SEBI"
        }
    ),
    InvestmentScheme(
        id="liquid_fund",
        name="Liquid / Ultra-Short Debt Fund",
        provider="Aditya Birla Sun Life / Nippon India",
        category="Fixed Income",
        risk_level="Very Low",
        indicative_return="6.5–7.2% p.a.",
        indicative_rate_num=6.8,
        min_investment="₹500",
        min_investment_num=500,
        time_horizon_min_years=0,
        time_horizon_ideal="1 Month to 1 Year",
        tax_benefit=False,
        lock_in_period="None (Insta-redemption up to ₹50k)",
        liquidity="High",
        best_for="Emergency buffer and surplus liquidity management",
        description="Invests in treasury bills and AAA commercial paper with maturities up to 91 days.",
        badge="Instant Liquidity",
        why_recommended=[
            "High safety rating with near-zero duration risk and high credit quality assets",
            "Instant redemption facility up to ₹50,000 within minutes to verified bank account",
            "Better returns and flexibility than typical idle savings accounts"
        ],
        things_to_consider=[
            "Gains are taxed at individual income tax slab rates as debt fund",
            "Modest return potential strictly suited for liquidity and capital preservation"
        ],
        source_evidence={
            "document": "SEBI Regulations on Liquid Schemes & RBI Money Market Guidelines",
            "regulator": "SEBI & Reserve Bank of India"
        }
    ),
    InvestmentScheme(
        id="sovereign_gold",
        name="Sovereign Gold / Gold ETF",
        provider="Reserve Bank of India / Leading AMCs",
        category="Others",
        risk_level="Moderate",
        indicative_return="2.5% p.a. + Gold Price Growth",
        indicative_rate_num=8.5,
        min_investment="₹100 (ETF) / 1 Gram",
        min_investment_num=100,
        time_horizon_min_years=5,
        time_horizon_ideal="5–8 Years",
        tax_benefit=True,
        tax_section="Capital gains exemption on SGB maturity",
        lock_in_period="5-8 Years for SGB / None for ETF",
        liquidity="Moderate",
        best_for="Inflation hedge and portfolio diversification",
        description="Paper gold securities backed by RBI offering additional interest and tax-free capital gains upon maturity.",
        badge="Inflation Hedge",
        why_recommended=[
            "Negative correlation to equity markets acts as an essential crisis buffer",
            "Zero storage, making, or purity deduction charges compared to physical gold",
            "SGBs offer fixed 2.5% annual cash interest credited semi-annually to bank account"
        ],
        things_to_consider=[
            "Gold price fluctuations driven by global macro factors and currency rates",
            "Secondary market trading volumes can sometimes trade at small discounts/premiums"
        ],
        source_evidence={
            "document": "RBI Notification - Sovereign Gold Bond Scheme",
            "regulator": "Reserve Bank of India & Ministry of Finance"
        }
    )
]

def get_all_schemes() -> List[InvestmentScheme]:
    # Return copies
    return [s.model_copy() for s in SCHEMES_DB]

