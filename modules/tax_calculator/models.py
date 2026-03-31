"""
Data models for the Tax Calculator module.
Defines the structure of inputs and outputs.
"""

from dataclasses import dataclass


@dataclass
class SalaryInput:
    """Input data structure for tax calculation."""

    gross_salary: float
    """Gross annual salary in rupees."""

    # Old Regime specific deductions
    deduction_80c: float = 0.0
    """Section 80C deduction (Life Insurance, PPF, etc.)."""

    deduction_80d: float = 0.0
    """Section 80D deduction (Health Insurance)."""

    hra_deduction: float = 0.0
    """HRA deduction (applicable in old regime)."""

    other_deductions: float = 0.0
    """Other eligible deductions for old regime."""

    def __post_init__(self):
        """Validate input values."""
        if self.gross_salary < 0:
            raise ValueError("Gross salary cannot be negative")
        if self.deduction_80c < 0:
            raise ValueError("Deduction 80C cannot be negative")
        if self.deduction_80d < 0:
            raise ValueError("Deduction 80D cannot be negative")
        if self.hra_deduction < 0:
            raise ValueError("HRA deduction cannot be negative")
        if self.other_deductions < 0:
            raise ValueError("Other deductions cannot be negative")


@dataclass
class TaxResult:
    """Output data structure for tax calculation results."""

    regime: str
    """Tax regime name (e.g., 'New Regime', 'Old Regime')."""

    gross_income: float
    """Gross annual income."""

    total_deductions: float
    """Total eligible deductions."""

    taxable_income: float
    """Income after deductions and standard deduction."""

    tax_amount: float
    """Tax to be paid."""

    effective_tax_rate: float
    """Effective tax rate as a percentage."""

    take_home: float
    """Take-home salary after tax and deductions."""


@dataclass
class TaxComparison:
    """Tax comparison between two regimes."""

    new_regime_result: TaxResult
    """Tax calculation for new regime."""

    old_regime_result: TaxResult
    """Tax calculation for old regime."""

    savings: float
    """Savings with the recommended regime."""

    recommended_regime: str
    """Which regime is beneficial."""

    recommendation_text: str
    """Human-readable recommendation."""

    savings_percentage: float
    """Savings as percentage of income."""
