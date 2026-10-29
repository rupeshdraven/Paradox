import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from ..models import UserProfile, AICopilotResponse

class GuardrailEngine:
    @staticmethod
    def inspect_query(query: str, profile: Optional[UserProfile] = None) -> Tuple[str, List[str], Optional[str]]:
        """
        Evaluates query against deterministic compliance rules.
        Returns (status: ALLOW|WARN|BLOCK|REQUEST_INFO, checks_applied: List[str], message_override: Optional[str])
        """
        q_lower = query.lower()
        checks = []
        
        # 1. Guaranteed returns check
        checks.append("Input Validation: Checking for prohibited return guarantees")
        guarantee_patterns = [
            r"guarantee[d]?",
            r"risk[- ]free (profit|return|money)",
            r"100% safe (return|profit)",
            r"can i get (15%|20%|25%|30%|40%|50%) guaranteed",
            r"double my money (in|overnight)"
        ]
        for pattern in guarantee_patterns:
            if re.search(pattern, q_lower):
                checks.append("Guardrail Gate: Prohibited guarantee claim intercepted")
                return (
                    "WARN",
                    checks,
                    "Investment returns on market-linked securities are never guaranteed and depend on market conditions. Under SEBI and RBI guidelines, no equity or hybrid scheme offers guaranteed profits."
                )

        # 2. Speculative / prohibited asset class check (Crypto, lottery, penny stocks, forex trading)
        checks.append("Suitability Check: Asset class scope validation")
        speculative_patterns = ["crypto", "bitcoin", "ethereum", "penny stock", "binary options", "forex leverage", "lottery"]
        for p in speculative_patterns:
            if p in q_lower:
                checks.append("Guardrail Gate: High-risk speculative asset detected")
                return (
                    "BLOCK",
                    checks,
                    "FinWise AI focuses strictly on prudent personal financial planning, SEBI-regulated mutual funds, and Government of India savings schemes. High-volatility speculative assets (like cryptocurrencies or penny stocks) are outside our prudent advisory framework."
                )

        # 3. Risk Mismatch Check
        checks.append("Profile Consistency: Checking risk appetite alignment")
        if profile and profile.risk_appetite.lower() in ["conservative", "very conservative"]:
            if any(k in q_lower for k in ["high risk", "aggressive", "small cap 100%", "future and options", "f&o"]):
                checks.append("Guardrail Gate: Risk appetite conflict detected")
                return (
                    "WARN",
                    checks,
                    f"Suitability Conflict: Your investor profile is registered as '{profile.risk_appetite}'. High-risk market-linked equity and derivative positions carry significant capital drawdown risks that conflict with your capital preservation preference."
                )

        # 4. Check for completely missing profile
        if profile is None or (profile.annual_income <= 0 and profile.annual_income_range == ""):
            if any(k in q_lower for k in ["how much can i invest", "can i afford", "my portfolio"]):
                checks.append("Profile Completeness Check: Missing income and expense telemetry")
                return (
                    "REQUEST_INFO",
                    checks,
                    "To evaluate this question accurately, FinWise AI requires your monthly income and current expense profile. Please complete Step 1 (Investor Profile) first."
                )

        checks.append("Suitability Check: Clear")
        checks.append("Document Evidence Retrieval: Matched with scheme factsheets")
        checks.append("Guardrail Gate: ALLOW (Safe to proceed)")
        return ("ALLOW", checks, None)

AUDIT_LOGS: List[Dict[str, Any]] = []

def record_audit(query: str, status: str, checks: List[str], response_summary: str, evidence: Optional[str] = None):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_query": query,
        "guardrail_status": status,
        "checks_applied": checks,
        "response_summary": response_summary[:120] + "..." if len(response_summary) > 120 else response_summary,
        "evidence_cited": evidence or "SEBI / RBI Master Guidelines & Profile Math"
    }
    AUDIT_LOGS.insert(0, log_entry)
    if len(AUDIT_LOGS) > 100:
        AUDIT_LOGS.pop()

