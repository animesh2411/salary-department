"""
Business logic for HRA calculations.
Based on Indian income tax rules for FY 2026-27.
"""

from .models import HRAInput, HRACalculation
from .constants import (
    HRA_PERCENTAGE_METRO,
    HRA_PERCENTAGE_NON_METRO,
    RENT_THRESHOLD_PERCENTAGE,
    CITY_TYPE_METRO,
    CITY_TYPE_NON_METRO,
)


def calculate_hra(hra_input: HRAInput) -> HRACalculation:
    """Calculate HRA deductible amount.

    HRA is minimum of:
    1. Actual HRA received (house_rent)
    2. Percentage limit based on city type:
       - Metro: 50% of basic salary
       - Non-Metro: 40% of basic salary
    3. Rent paid minus 10% of basic salary
       (If rent < 10% of basic, HRA = 0)

    Args:
        hra_input: HRAInput object with salary, rent, and city type.

    Returns:
        HRACalculation object with detailed breakdown.
    """
    basic = hra_input.basic_salary
    rent = hra_input.house_rent
    is_metro = hra_input.is_metro

    # Determine HRA percentage based on city type
    hra_percentage = HRA_PERCENTAGE_METRO if is_metro else HRA_PERCENTAGE_NON_METRO
    city_type = CITY_TYPE_METRO if is_metro else CITY_TYPE_NON_METRO

    # Calculate rent threshold (10% of basic)
    rent_threshold = basic * RENT_THRESHOLD_PERCENTAGE

    # Rule 1: Maximum by city type
    max_by_city = basic * hra_percentage

    # Rule 2: Rent minus 10% of basic
    # If rent is less than 10% of basic, no HRA
    if rent <= rent_threshold:
        max_by_rent = 0
        is_eligible = False
        hra_deductible = 0
        explanation = (
            f"Rent (₹{rent:,.0f}) is less than or equal to 10% of basic "
            f"(₹{rent_threshold:,.0f}). No HRA deductible."
        )
    else:
        max_by_rent = rent - rent_threshold
        is_eligible = True
        # HRA = minimum of city type limit and rent limit
        hra_deductible = min(max_by_city, max_by_rent)
        explanation = (
            f"{city_type} city: 50% of basic = ₹{max_by_city:,.0f}, "
            f"Rent - 10% = ₹{max_by_rent:,.0f}. "
            f"HRA deductible = ₹{hra_deductible:,.0f} (minimum of both)"
        )

    return HRACalculation(
        basic_salary=basic,
        house_rent=rent,
        city_type=city_type,
        hra_percentage=hra_percentage,
        max_hra_by_city=max_by_city,
        max_hra_by_rent=max_by_rent,
        hra_deductible=hra_deductible,
        rent_threshold=rent_threshold,
        is_eligible=is_eligible,
        explanation=explanation,
    )
