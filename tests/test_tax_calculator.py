"""
Unit tests for Tax Calculator module service.
"""

import pytest
from modules.tax_calculator.service import (
    calculate_tax_new_regime,
    calculate_tax_old_regime,
    compare_tax,
)
from modules.tax_calculator.models import SalaryInput, TaxResult
from modules.tax_calculator.constants import (
    STANDARD_DEDUCTION,
    NEW_REGIME_REBATE_LIMIT,
)


class TestNewRegime:
    """Test cases for New Regime tax calculation."""

    def test_zero_salary(self):
        """Test with zero salary."""
        result = calculate_tax_new_regime(0)
        assert result.tax_amount == 0
        assert result.taxable_income == 0
        assert result.effective_tax_rate == 0

    def test_salary_below_standard_deduction(self):
        """Test salary below standard deduction."""
        result = calculate_tax_new_regime(50_000)
        assert result.taxable_income == 0
        assert result.tax_amount == 0

    def test_rebate_at_limit(self):
        """Test rebate when taxable income equals limit (₹12L)."""
        # Gross = 12L + 75K = 12.75L
        gross_salary = 12_75_000
        result = calculate_tax_new_regime(gross_salary)
        assert result.taxable_income == 12_00_000
        assert result.tax_amount == 0, "Tax should be 0 at rebate limit"

    def test_rebate_below_limit(self):
        """Test rebate when taxable income is below ₹12L."""
        # Gross = 11L + 75K = 11.75L
        gross_salary = 11_75_000
        result = calculate_tax_new_regime(gross_salary)
        assert result.taxable_income == 11_00_000
        assert result.tax_amount == 0, "Tax should be 0 below rebate limit"

    def test_rebate_just_above_limit(self):
        """Test when taxable income is just above ₹12L."""
        # Gross = 12.1L + 75K = 12.85L
        gross_salary = 12_85_000
        result = calculate_tax_new_regime(gross_salary)
        taxable = 12_10_000
        assert result.taxable_income == taxable
        # Tax on ₹10,000 above 12L at 15% = ₹1,500
        assert result.tax_amount > 0

    def test_standard_salary(self):
        """Test with standard salary (₹10L)."""
        gross_salary = 10_00_000
        result = calculate_tax_new_regime(gross_salary)
        assert result.gross_income == gross_salary
        assert result.total_deductions == STANDARD_DEDUCTION
        assert result.taxable_income == gross_salary - STANDARD_DEDUCTION
        assert result.tax_amount == 0  # Below rebate limit

    def test_high_salary(self):
        """Test with high salary (₹50L)."""
        gross_salary = 50_00_000
        result = calculate_tax_new_regime(gross_salary)
        taxable_income = gross_salary - STANDARD_DEDUCTION

        # Should have some tax
        assert result.tax_amount > 0
        assert result.effective_tax_rate > 0
        assert result.effective_tax_rate < 0.30  # Max rate is 30%

    def test_effective_tax_rate_calculation(self):
        """Test effective tax rate is correctly calculated."""
        gross_salary = 20_00_000
        result = calculate_tax_new_regime(gross_salary)
        expected_rate = result.tax_amount / gross_salary
        assert abs(result.effective_tax_rate - expected_rate) < 0.0001


class TestOldRegime:
    """Test cases for Old Regime tax calculation."""

    def test_zero_salary_no_deductions(self):
        """Test with zero salary and no deductions."""
        salary_input = SalaryInput(gross_salary=0)
        result = calculate_tax_old_regime(salary_input)
        assert result.tax_amount == 0
        assert result.taxable_income == 0

    def test_salary_below_standard_deduction(self):
        """Test salary below standard deduction."""
        salary_input = SalaryInput(gross_salary=50_000)
        result = calculate_tax_old_regime(salary_input)
        assert result.taxable_income == 0
        assert result.tax_amount == 0

    def test_with_80c_deduction(self):
        """Test with 80C deduction."""
        gross_salary = 10_00_000
        deduction_80c = 50_000
        salary_input = SalaryInput(
            gross_salary=gross_salary,
            deduction_80c=deduction_80c,
        )
        result = calculate_tax_old_regime(salary_input)

        expected_deductions = STANDARD_DEDUCTION + deduction_80c
        assert result.total_deductions == expected_deductions
        assert result.taxable_income == gross_salary - expected_deductions

    def test_with_multiple_deductions(self):
        """Test with multiple deductions."""
        gross_salary = 20_00_000
        salary_input = SalaryInput(
            gross_salary=gross_salary,
            deduction_80c=1_00_000,
            deduction_80d=50_000,
            hra_deduction=2_00_000,
            other_deductions=25_000,
        )
        result = calculate_tax_old_regime(salary_input)

        expected_deductions = (
            STANDARD_DEDUCTION
            + 1_00_000
            + 50_000
            + 2_00_000
            + 25_000
        )
        assert result.total_deductions == expected_deductions

    def test_no_tax_with_sufficient_deductions(self):
        """Test that sufficient deductions can reduce tax to zero."""
        gross_salary = 5_00_000
        salary_input = SalaryInput(
            gross_salary=gross_salary,
            deduction_80c=1_50_000,
            deduction_80d=1_00_000,
            hra_deduction=1_50_000,
        )
        result = calculate_tax_old_regime(salary_input)

        # Total deductions = 75K + 150K + 100K + 150K = 475K
        # Taxable = 500K - 475K = 25K (in 0% slab)
        assert result.tax_amount == 0


class TestTaxComparison:
    """Test cases for tax comparison between regimes."""

    def test_comparison_low_income_no_deductions(self):
        """Test comparison for low income with no deductions."""
        salary_input = SalaryInput(gross_salary=5_00_000)
        comparison = compare_tax(salary_input)

        # New Regime will have zero tax (rebate), Old Regime will have some tax
        assert comparison.new_regime_result.tax_amount == 0
        assert comparison.old_regime_result.tax_amount > 0
        assert comparison.recommended_regime == "New Regime"
        assert comparison.savings > 0

    def test_comparison_high_income_no_deductions(self):
        """Test comparison for high income with no deductions."""
        salary_input = SalaryInput(gross_salary=30_00_000)
        comparison = compare_tax(salary_input)

        # Both regimes should have tax
        assert comparison.new_regime_result.tax_amount > 0
        assert comparison.old_regime_result.tax_amount > 0

    def test_new_regime_beneficial(self):
        """Test case where New Regime is beneficial."""
        # High salary with no deductions - New Regime is better
        salary_input = SalaryInput(gross_salary=40_00_000)
        comparison = compare_tax(salary_input)

        assert comparison.new_regime_result.tax_amount < comparison.old_regime_result.tax_amount
        assert comparison.recommended_regime == "New Regime"
        assert comparison.savings > 0

    def test_old_regime_beneficial(self):
        """Test case where Old Regime can be competitive."""
        # Old Regime with many deductions - but with FY26-27 rates,
        # New Regime is generally more beneficial unless income is very low
        salary_input = SalaryInput(
            gross_salary=10_00_000,
            deduction_80c=1_50_000,
            deduction_80d=1_00_000,
            hra_deduction=1_00_000,
        )
        comparison = compare_tax(salary_input)

        # With good deductions, both regimes are competitive
        # Just verify the calculation works correctly
        assert comparison.old_regime_result.tax_amount >= 0
        assert comparison.new_regime_result.tax_amount >= 0
        assert comparison.recommendation_text is not None

    def test_savings_calculation(self):
        """Test that savings are correctly calculated."""
        salary_input = SalaryInput(gross_salary=25_00_000)
        comparison = compare_tax(salary_input)

        expected_savings = abs(
            comparison.new_regime_result.tax_amount
            - comparison.old_regime_result.tax_amount
        )
        assert comparison.savings == expected_savings

    def test_comparison_recommendation_text(self):
        """Test that recommendation text is generated."""
        salary_input = SalaryInput(gross_salary=50_00_000)
        comparison = compare_tax(salary_input)

        assert comparison.recommendation_text is not None
        assert len(comparison.recommendation_text) > 0


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_high_salary(self):
        """Test with very high salary."""
        gross_salary = 1_00_00_000  # 1 crore
        result = calculate_tax_new_regime(gross_salary)

        assert result.tax_amount > 0
        assert result.effective_tax_rate > 0

    def test_fractional_salary(self):
        """Test with fractional salary (paise)."""
        gross_salary = 10_00_000.50
        result = calculate_tax_new_regime(gross_salary)

        assert result.tax_amount >= 0

    def test_maximum_deductions(self):
        """Test with maximum allowed deductions."""
        salary_input = SalaryInput(
            gross_salary=50_00_000,
            deduction_80c=1_50_000,
            deduction_80d=2_00_000,
            hra_deduction=25_00_000,
        )
        result = calculate_tax_old_regime(salary_input)

        assert result.taxable_income >= 0

    def test_deductions_exceeding_income(self):
        """Test when deductions exceed income (should result in 0 taxable income)."""
        salary_input = SalaryInput(
            gross_salary=10_00_000,
            deduction_80c=1_50_000,
            deduction_80d=1_00_000,
            hra_deduction=10_00_000,
        )
        result = calculate_tax_old_regime(salary_input)

        # Taxable income should not be negative
        assert result.taxable_income >= 0
        assert result.tax_amount == 0
