# RIA Suitability & Risk Profiling Matrix

> [!NOTE]
> **Prototype Notice**: Prototype developed for the Zeckathon PS4 problem statement. This system is not SEBI-approved or certified and does not constitute independent investment advice.

---

## 1. Regulatory Context & Fiduciary Scope
Designed with reference to **SEBI (Investment Advisers) Regulations, 2013**:
- **Regulation 16 (Risk Profiling)**: Advisers must obtain necessary information regarding client financial situation, investment objectives, and capacity to absorb losses prior to advice.
- **Regulation 17 (Suitability)**: Advisers must have a reasonable basis for believing recommendations are suitable to the client's risk profile, objectives, and situation.
- **Regulation 19 (Maintenance of Records)**: Complete audit trail of client profiling, suitability assessment, risk scoring, rationale for advice, and product disclosures maintained for minimum 5 years.

Algorithmic advisory must be deterministic, transparent, inspectable, and auditable.

---

## 2. Risk Profiling Dimensions & Arithmetic

Our deterministic scoring engine assesses client profiles along four fundamental dimensions:

| Dimension | Weight | Description | Source / Rationale |
|---|---|---|---|
| **Risk Capacity** | 30% | Financial ability to absorb losses (Age, Savings-to-Income, Expense-to-Income, Liabilities) | Reg 16 (Risk Profiling) Financial situation analysis |
| **Risk Tolerance** | 25% | Psychological willingness to tolerate volatility and drawdowns | Reg 16 (Risk Profiling) Client stated risk appetite |
| **Investment Horizon** | 25% | Time period before capital is required for the stated financial goal | Reg 16 (Risk Profiling) Investment objectives alignment |
| **Liquidity & Emergency Buffer** | 20% | Adequacy of emergency reserve (liquid funds covering 3 to 6 months of expenses) | Model-Imposed Constraint (Cash-flow stability sizing) |

### Verifiable Score Formula:
$$\text{Composite Score} = 0.30 \times \text{Capacity} + 0.25 \times \text{Tolerance} + 0.25 \times \text{Horizon} + 0.20 \times \text{Liquidity}$$

---

## 3. Risk Categories & Model-Imposed Exposure Limits

The composite score ranges from **0 to 100**:

| Score Range | Suitability Category | Model Equity Ceiling | Model Debt Floor | Primary Objective |
|---|---|---|---|---|
| **0 - 35** | **Conservative** | Max 20% | Min 75% | Capital Preservation & Liquidity |
| **36 - 55** | **Moderate** | Max 45% | Min 50% | Stable Income & Modest Growth |
| **56 - 75** | **Moderately Aggressive** | Max 70% | Min 25% | Long-Term Capital Appreciation |
| **76 - 100** | **Aggressive** | Max 85% | Min 15% | Maximum Growth (High Volatility Tolerance) |

*Note: These exposure limits are quantitative model risk-budgeting boundaries, not statutory caps written directly into SEBI circulars.*

---

## 4. System Suitability Guardrails & Model Constraints

The engine applies explicit rule-based constraints before finalizing any profile:

1. **System Suitability Guardrail (Liquidity Buffer Carve-out)**:
   - Threshold: 3 months of expenses for salaried individuals, 6 months for irregular business cash flows.
   - Action: If reserves are below the threshold, priority routing directs contributions to overnight/liquid funds before long-term equity accumulation.
2. **Model-Imposed Constraint (Senior Citizen Wealth Preservation)**:
   - Condition: Age >= 60 with monthly income or capital preservation objective.
   - Action: Categorization capped at Conservative (70% Debt, 15% Liquid SWP buffer, 15% Large Cap hedge).
3. **Model-Imposed Constraint (Horizon-Risk Alignment)**:
   - Condition: Investment horizon <= 3.0 years.
   - Action: High equity allocation is deemed unsuitable due to lack of market recovery runway; equity capped at 10-20%.
4. **System Suitability Guardrail (Derivatives Drawdown Protection)**:
   - Condition: History of severe F&O trading drawdowns.
   - Action: Aggressive stated tolerance capped at Moderate; leveraged or speculative instruments barred.
5. **Fiduciary Conservatism Guardrail (Stated Risk Ceiling)**:
   - Principle: An adviser must never recommend investments riskier than the client's self-declared risk appetite.
   - Action: Final risk category is capped at `profile.stated_risk_tolerance`.
