"""
Utility functions for the Tax Calculator module.
Contains formatting, validation, and helper functions.
"""

from .constants import CURRENCY_FORMAT


def format_currency(amount: float) -> str:
    """Format amount as Indian currency string.

    Args:
        amount: Amount in rupees.

    Returns:
        Formatted currency string (e.g., "₹1,00,000").
    """
    return CURRENCY_FORMAT.format(amount)


def format_percentage(value: float, decimal_places: int = 2) -> str:
    """Format value as percentage string.

    Args:
        value: Value as decimal (e.g., 0.15 for 15%).
        decimal_places: Number of decimal places to show.

    Returns:
        Formatted percentage string (e.g., "15.00%").
    """
    return f"{value * 100:.{decimal_places}f}%"


def round_to_nearest(amount: float, nearest: int = 1) -> float:
    """Round amount to nearest rupee (or other value).

    Args:
        amount: Amount to round.
        nearest: Round to nearest value (default: 1 rupee).

    Returns:
        Rounded amount.
    """
    return round(amount / nearest) * nearest


def validate_salary(salary: float) -> bool:
    """Validate if salary is within reasonable limits.

    Args:
        salary: Salary amount.

    Returns:
        True if valid, False otherwise.
    """
    # Reasonable upper limit for validation
    MAX_SALARY = 100_000_000  # 10 crore

    return 0 <= salary <= MAX_SALARY


def validate_deduction(deduction: float, max_limit: float) -> bool:
    """Validate if deduction is within limits.

    Args:
        deduction: Deduction amount.
        max_limit: Maximum allowed deduction.

    Returns:
        True if valid, False otherwise.
    """
    return 0 <= deduction <= max_limit


def get_slab_info(amount: float, slabs: list) -> dict:
    """Get tax slab information for a given amount.

    Args:
        amount: Taxable amount.
        slabs: List of tax slab dictionaries.

    Returns:
        Dictionary with slab min, max, and rate.
    """
    for slab in slabs:
        if slab["min"] <= amount < slab["max"]:
            return slab
    return slabs[-1]  # Return highest slab if amount exceeds all


def calculate_income_in_slab(amount: float, slab: dict) -> float:
    """Calculate income portion that falls in a given slab.

    Args:
        amount: Total amount.
        slab: Slab dictionary with min and max.

    Returns:
        Income portion within the slab.
    """
    if amount <= slab["min"]:
        return 0
    if amount <= slab["max"]:
        return amount - slab["min"]
    return slab["max"] - slab["min"]


def inr_to_words(amount: int) -> str:
    """Convert INR amount to words (simplified).

    Args:
        amount: Amount in rupees (integer).

    Returns:
        Amount in words (e.g., "1 Lakh" for 100000).
    """
    if amount >= 10_000_000:
        return f"{amount / 10_000_000:.1f} Crore"
    elif amount >= 100_000:
        return f"{amount / 100_000:.1f} Lakh"
    elif amount >= 1_000:
        return f"{amount / 1_000:.1f}K"
    else:
        return f"{amount}"
