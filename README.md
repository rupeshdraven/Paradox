# FinWise AI — AI-Powered Financial Advisory & Planning Copilot

**FinWise AI** is a modern, responsive, end-to-end **AI-powered financial advisory web application** designed to help investors understand their financial position, define multi-milestone goals, assess their risk appetite objectively, receive personalized suitability-scored investment recommendations, and interact with a profile-grounded AI decision copilot.

---

## 🏛️ System Architecture: One Copilot, Two Engines, One Controlled Output

> **"Deterministic financial logic controls the decision. AI explains the decision."**

```
 ┌──────────────────────┐      ┌─────────────────────────┐
 │    Client Profile    │      │  Document Intelligence  │
 │  Structured Profile, │      │    SIDs, Factsheets,    │
 │ Income/Expense, Goals│      │   RBI/SEBI Regulations  │
 └──────────┬───────────┘      └────────────┬────────────┘
            │                               │
            ▼                               ▼
 ┌──────────────────────┐      ┌─────────────────────────┐
 │   Financial Engine   │      │    Guardrail Engine     │
 │  Deterministic math, │      │ Decision Gate: ALLOW,   │
 │   Suitability matrix,│      │ WARN, BLOCK, REQUEST    │
 │   Health score 0-100 │      │  Compliance Audit Trail │
 └──────────┬───────────┘      └────────────┬────────────┘
            │                               │
            └───────────────┬───────────────┘
                            ▼
              ┌───────────────────────────┐
              │  Advisory Copilot Output  │
              │  • Goal-aware Allocation  │
              │  • Structured 4-Part AI   │
              │  • Evidence & Citations   │
              └───────────────────────────┘
```

1. **Financial Engine (Deterministic Logic)**
   - Calculates exact surplus, savings rate, emergency fund coverage in months, and debt-to-income (DTI) ratio.
   - Computes a holistic **Financial Health Score (0–100)** across 5 weighted pillars: Savings (20%), Expense Control (20%), Emergency Cushion (20%), Debt Burden (20%), and Goal Feasibility (20%).
   - Transparent recommendation scoring engine weighing Risk Match (25%), Goal Fit (25%), Horizon (20%), Liquidity (15%), and Tax Advantage (15%).

2. **Guardrail Engine (Compliance & Safety Gate)**
   - **ALLOW**: Safe to proceed; answers grounded in profile telemetry with citations.
   - **WARN**: Intercepts return guarantee claims (e.g. "Can I get 25% guaranteed returns?") or risk mismatches (e.g. conservative user asking for high-risk assets).
   - **BLOCK**: Refuses speculative unregulated products (e.g. cryptocurrencies, penny stocks, binary trading).
   - **REQUEST_INFO**: Prompts for required inputs if profile data is incomplete.
   - **Audit Trail**: Every request, check applied, and evidence source is logged into an auditable compliance table.

3. **AI Financial Copilot (Structured 4-Part Response)**
   - **Short Answer**: Direct, clear verdict.
   - **Why?**: Concrete profile calculations (monthly surplus, cost as months of savings).
   - **Better Option**: Actionable strategic alternatives.
   - **Scenario Impact**: Quantified comparison (goal completion with vs. without purchase).

---

## 🚀 Key Features & Pages

| Page / Step | Description | Visual Inspiration |
| :--- | :--- | :--- |
| **01 Investor Profile** | Comprehensive profile intake: age, income bracket, expense range, horizon, and liabilities. | Inspired directly by Reference Screenshot 1 (card graphic, feature pills, encryption badge) |
| **02 Financial Goals** | Create and track multiple goals (Emergency Fund, Car, Home, Retirement) with linear and compounded monthly requirements. | High-priority badges, progress bars, and remaining target meters |
| **03 Risk Assessment** | 5-question multi-dimensional questionnaire evaluating loss resilience, time horizon, and capital preservation. | Live visual gauge (0–100 score) and Conservative / Moderate / Aggressive classification |
| **04 Review & Analysis** | 360° financial snapshot with animated 5-step checkpoint analyzer. | Real-time cash flow metrics & surplus coverage ratio |
| **05 Recommended Schemes** | Curated catalog of Indian mutual funds, PPF, NPS, ELSS, FD, SSY, Gold ETFs, and Liquid Funds. | Inspired directly by Reference Screenshot 2 (badges, metrics, and "Why this recommendation?" modal) |
| **06 Investment Plan** | Visual goal-aware asset allocation (Growth, Debt, Sovereign, Reserve) and monthly SIP distribution. | Recharts donut chart with automated monthly plan |
| **07 Financial Dashboard** | Main hub featuring 78/100 Financial Health Score, Net Position, Cash Flow, and Goal Milestones. | Clean fintech typography, soft borders, and quick prompt chips |
| **08 Financial What-If** | Standout interactive simulator with real-time sliders for income, expenses, and monthly investment. | Interactive compound growth curve & time-saved calculator |
| **09 Guardrail Inspector** | Live compliance visualizer showing the Decision Gate and chronological audit logs. | Direct implementation of Slide 6 architecture |
| **10 Learn Academy** | Plain-English financial guides (SIP, PPF, NPS, 50/30/20 rule) with one-click "Ask AI to Explain" triggers. | Educational empowerment for beginner investors |

---

## 🛠️ Tech Stack

- **Frontend**: React 19, TypeScript, Tailwind CSS, Lucide React, Recharts, Vite.
- **Backend**: Python 3.14, FastAPI, Pydantic v2, Uvicorn, SQLite3.
- **Communication**: REST API with transparent Vite dev server proxy (`/api` → `http://127.0.0.1:8000`).

---

## 🏃 Quick Start Guide

### 1. Prerequisites
- **Node.js**: v18+ (verified with Node v24)
- **Python**: 3.10+ (verified with Python 3.14)

### 2. Run the Backend
```bash
# In project root:
py -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend runs on: `http://127.0.0.1:8000` (Swagger docs available at `http://127.0.0.1:8000/docs`)*

### 3. Run the Frontend
```bash
# In frontend directory:
cd frontend
npm run dev
```
*Frontend runs on: `http://localhost:5173`*

*(Or simply double click `run_backend.bat` and `run_frontend.bat` on Windows!)*

---

## 👤 Demo Profile (Rupesh)

The application comes pre-loaded with a demonstration profile:
- **Name**: Rupesh
- **Age**: 21
- **Annual Income**: ₹6,00,000 (₹5–10 Lakh bracket)
- **Monthly Expenses**: ₹30,000 (₹25,000–₹50,000 bracket)
- **Monthly Surplus**: ₹20,000
- **Existing Savings**: ₹1,00,000 (3.3 months emergency buffer)
- **Risk Score**: 67 / 100 (Moderate Profile)
- **Primary Goal**: Wealth Creation (₹10 Lakh over 5 years)

*To reset the demo to this default state at any time, click the user avatar in the top right and select **"Reset to Rupesh Demo"**.*

---

## 🔒 Responsible Financial Advisory Notice

FinWise AI provides educational and decision-support information for demonstration purposes. Investment values and returns are subject to market conditions and are not guaranteed. Projections, indicative return rates, and financial health scores are illustrative estimations. This platform is an educational prototype and does not constitute certified statutory financial advisory under SEBI (Investment Advisers) Regulations.

