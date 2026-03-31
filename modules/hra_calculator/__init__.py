"""
HRA Calculator Module for Salary Department.

Calculates HRA deduction based on metro/non-metro city rules for FY 2026-27.
"""

from .models import HRAInput, HRACalculation
from .service import calculate_hra
from . import ui

__all__ = [
    "HRAInput",
    "HRACalculation",
    "calculate_hra",
    "ui",
]
