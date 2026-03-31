"""
Business logic for tax calculations.
Pure functions that handle all tax computation.
"""

from .models import SalaryInput, TaxResult, TaxComparison
from .constants import (
    STANDARD_DEDUCTION,
    NEW_REGIME_SLABS,
    NEW_REGIME_REBATE_LIMIT,
    OLD_REGIME_SLABS,
    REGIME_NEW,
    REGIME_OLD,
    STANDARD_DEDUCTION_OLD,
)
from .utils import calculate_income_in_slab, round_to_nearest


def calculate_tax_new_regime(gross_salary: float) -> TaxResult:
    """Calculate tax under New Regime (FY 2026-27).

    New Regime Rules:
    - Standard Deduction: ₹75,000
    - No other deductions allowed
    - Rebate: If taxable income ≤ ₹12L, tax = 0
    - Progressive tax slabs apply

    Args:
        gross_salary: Gross annual salary in rupees.

    Returns:
        TaxResult object with detailed calculation.
    """
    # Calculate taxable income
    taxable_income = max(0, gross_salary - STANDARD_DEDUCTION)

    # Check for rebate: if taxable income <= 12L, no tax
    if taxable_income <= NEW_REGIME_REBATE_LIMIT:
        tax_amount = 0.0
    else:
        # Calculate tax based on slabs
        tax_amount = 0.0
        for slab in NEW_REGIME_SLABS:
            income_in_slab = calculate_income_in_slab(taxable_income, slab)
            tax_in_slab = income_in_slab * slab["rate"]
            tax_amount += tax_in_slab

    # Round to nearest rupee
    tax_amount = round_to_nearest(tax_amount)

    # Calculate effective tax rate
    if gross_salary > 0:
        effective_tax_rate = tax_amount / gross_salary
    else:
        effective_tax_rate = 0.0

    # Take-home salary (no deductions in new regime)
    take_home = gross_salary - tax_amount

    return TaxResult(
        regime=REGIME_NEW,
        gross_income=gross_salary,
        total_deductions=STANDARD_DEDUCTION,
        taxable_income=taxable_income,
        tax_amount=tax_amount,
        effective_tax_rate=effective_tax_rate,
        take_home=take_home,
    )


def calculate_tax_old_regime(salary_input: SalaryInput) -> TaxResult:
    """Calculate tax under Old Regime (FY 2026-27).

    Old Regime Rules:
    - Standard Deduction: ₹75,000
    - Allow deductions: 80C, 80D, HRA, other
    - Progressive tax slabs apply
    - No rebate (must pay tax if taxable income > ₹0)

    Args:
        salary_input: SalaryInput object with salary and deductions.

    Returns:
        TaxResult object with detailed calculation.
    """
    gross_salary = salary_input.gross_salary

    # Total deductions (standard + eligible deductions)
    total_deductions = (
        STANDARD_DEDUCTION_OLD
        + salary_input.deduction_80c
        + salary_input.deduction_80d
        + salary_input.hra_deduction
        + salary_input.other_deductions
    )

    # Calculate taxable income
    taxable_income = max(0, gross_salary - total_deductions)

    # Calculate tax based on slabs
    tax_amount = 0.0
    for slab in OLD_REGIME_SLABS:
        income_in_slab = calculate_income_in_slab(taxable_income, slab)
        tax_in_slab = income_in_slab * slab["rate"]
        tax_amount += tax_in_slab

    # Round to nearest rupee
    tax_amount = round_to_nearest(tax_amount)

    # Calculate effective tax rate
    if gross_salary > 0:
        effective_tax_rate = tax_amount / gross_salary
    else:
        effective_tax_rate = 0.0

    # Take-home salary
    take_home = gross_salary - tax_amount - (total_deductions - STANDARD_DEDUCTION_OLD)

    return TaxResult(
        regime=REGIME_OLD,
        gross_income=gross_salary,
        total_deductions=total_deductions,
        taxable_income=taxable_income,
        tax_amount=tax_amount,
        effective_tax_rate=effective_tax_rate,
        take_home=take_home,
    )


def compare_tax(salary_input: SalaryInput) -> TaxComparison:
    """Compare tax between New and Old regimes.

    Args:
        salary_input: SalaryInput object with salary and deductions.

    Returns:
        TaxComparison object with results and recommendation.
    """
    new_result = calculate_tax_new_regime(salary_input.gross_salary)
    old_result = calculate_tax_old_regime(salary_input)

    # Calculate savings
    if new_result.tax_amount < old_result.tax_amount:
        savings = old_result.tax_amount - new_result.tax_amount
        recommended_regime = REGIME_NEW
        recommendation_text = (
            f"New Regime is beneficial! "
            f"You save {savings:,.0f} with New Regime."
        )
    elif old_result.tax_amount < new_result.tax_amount:
        savings = new_result.tax_amount - old_result.tax_amount
        recommended_regime = REGIME_OLD
        recommendation_text = (
            f"Old Regime is better! "
            f"You save {savings:,.0f} with Old Regime."
        )
    else:
        savings = 0.0
        recommended_regime = "Both"
        recommendation_text = "Both regimes result in same tax. Choose based on preference."

    # Calculate savings percentage
    if max(new_result.tax_amount, old_result.tax_amount) > 0:
        savings_percentage = savings / max(new_result.tax_amount, old_result.tax_amount)
    else:
        savings_percentage = 0.0

    return TaxComparison(
        new_regime_result=new_result,
        old_regime_result=old_result,
        savings=savings,
        recommended_regime=recommended_regime,
        recommendation_text=recommendation_text,
        savings_percentage=savings_percentage,
    )
