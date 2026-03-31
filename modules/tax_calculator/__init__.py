"""
Tax Calculator Module for Salary Department.

This module provides tax calculation functionality for the Indian Tax System (FY 2026-27).
Supports both New and Old tax regimes with detailed comparison and analysis.
"""

from .models import SalaryInput, TaxResult, TaxComparison
from .service import calculate_tax_new_regime, calculate_tax_old_regime, compare_tax
from . import ui

__all__ = [
    "SalaryInput",
    "TaxResult",
    "TaxComparison",
    "calculate_tax_new_regime",
    "calculate_tax_old_regime",
    "compare_tax",
    "ui",
]
