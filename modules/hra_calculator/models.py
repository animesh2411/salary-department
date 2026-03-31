"""
Data models for the HRA Calculator module.
"""

from dataclasses import dataclass


@dataclass
class HRAInput:
    """Input data for HRA calculation."""

    basic_salary: float
    """Basic salary in rupees (per month or per annum)."""

    house_rent: float
    """House rent paid in same period as basic salary."""

    is_metro: bool
    """True if city is metro, False if non-metro."""

    def __post_init__(self):
        """Validate input values."""
        if self.basic_salary < 0:
            raise ValueError("Basic salary cannot be negative")
        if self.house_rent < 0:
            raise ValueError("House rent cannot be negative")


@dataclass
class HRACalculation:
    """Output of HRA calculation."""

    basic_salary: float
    """Basic salary (same period as other values)."""

    house_rent: float
    """House rent paid."""

    city_type: str
    """Metro or Non-Metro."""

    hra_percentage: float
    """HRA percentage for the city type."""

    max_hra_by_city: float
    """Maximum HRA allowed by city type (% of basic)."""

    max_hra_by_rent: float
    """Maximum HRA allowed by rent rule (Rent - 10% of basic)."""

    hra_deductible: float
    """Final HRA deductible amount (minimum of city type and rent)."""

    rent_threshold: float
    """10% of basic salary (minimum rent to claim HRA)."""

    is_eligible: bool
    """Whether HRA is deductible (rent > 10% of salary)."""

    explanation: str
    """Explanation of calculation."""
