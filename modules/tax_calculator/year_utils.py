"""
Dynamic year utilities for Tax Calculator.
Automatically calculates fiscal year based on current date.
"""

from datetime import datetime


def get_current_year() -> int:
    """Get the current calendar year (e.g., 2026).

    Returns:
        int: Current year.
    """
    return datetime.now().year


def get_fiscal_year_start() -> int:
    """Get the fiscal year start year.

    In India, fiscal year runs from April 1 to March 31.
    - If current month is Jan-Mar: FY starts in previous year
    - If current month is Apr-Dec: FY starts in current year

    Returns:
        int: Fiscal year start year.
    """
    today = datetime.now()
    if today.month < 4:  # Jan, Feb, Mar
        return today.year - 1
    else:  # Apr-Dec
        return today.year


def get_fiscal_year_end() -> int:
    """Get the fiscal year end year.

    Returns:
        int: Fiscal year end year (start year + 1).
    """
    return get_fiscal_year_start() + 1


def get_fiscal_year_display() -> str:
    """Get fiscal year in display format (e.g., 'FY 2026-27').

    Returns:
        str: Formatted fiscal year string.
    """
    start = get_fiscal_year_start()
    end = get_fiscal_year_end()
    end_short = str(end)[-2:]  # Get last 2 digits (e.g., '27' from 2027)
    return f"FY {start}-{end_short}"


def get_fiscal_year_range() -> tuple[str, str]:
    """Get fiscal year date range (April 1 to March 31).

    Returns:
        tuple: (start_date, end_date) as strings.
    """
    start_year = get_fiscal_year_start()
    end_year = get_fiscal_year_end()
    return (f"1st April {start_year}", f"31st March {end_year}")

