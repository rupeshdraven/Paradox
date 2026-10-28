"""Client profiling module adhering to SEBI RIA standards."""

from src.profiling.models import (
    CashFlowStability,
    ClientProfile,
    GoalType,
    RiskTolerance,
)
from src.profiling.personas import TARGET_PERSONAS, get_all_personas, get_persona

__all__ = [
    "ClientProfile",
    "GoalType",
    "RiskTolerance",
    "CashFlowStability",
    "TARGET_PERSONAS",
    "get_persona",
    "get_all_personas",
]
