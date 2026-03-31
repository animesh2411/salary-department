"""
Unit tests for HRA Calculator module.
"""

import pytest
from modules.hra_calculator.service import calculate_hra
from modules.hra_calculator.models import HRAInput


class TestMetroHRA:
    """Test HRA calculation for metro cities (50%)."""

    def test_zero_salary(self):
        """Test with zero salary."""
        hra_input = HRAInput(basic_salary=0, house_rent=0, is_metro=True)
        result = calculate_hra(hra_input)
        assert result.hra_deductible == 0
        assert not result.is_eligible

    def test_zero_rent(self):
        """Test with zero rent."""
        hra_input = HRAInput(basic_salary=50_000, house_rent=0, is_metro=True)
        result = calculate_hra(hra_input)
        assert result.hra_deductible == 0
        assert not result.is_eligible

    def test_rent_below_threshold(self):
        """Test rent below 10% threshold."""
        hra_input = HRAInput(
            basic_salary=50_000,  # 10% = 5000
            house_rent=4_000,  # Less than 10%
            is_metro=True,
        )
        result = calculate_hra(hra_input)
        assert result.hra_deductible == 0
        assert not result.is_eligible

    def test_rent_at_threshold(self):
        """Test rent exactly at 10% threshold."""
        hra_input = HRAInput(
            basic_salary=50_000,  # 10% = 5000
            house_rent=5_000,  # Exactly at threshold
            is_metro=True,
        )
        result = calculate_hra(hra_input)
        assert result.hra_deductible == 0
        assert not result.is_eligible

    def test_standard_metro_case(self):
        """Test standard metro case."""
        hra_input = HRAInput(
            basic_salary=60_000,
            house_rent=40_000,
            is_metro=True,
        )
        result = calculate_hra(hra_input)
        # Metro 50% = 30,000
        # Rent - 10% = 40,000 - 6,000 = 34,000
        # HRA = min(30,000, 34,000) = 30,000
        assert result.max_hra_by_city == 30_000
        assert result.max_hra_by_rent == 34_000
        assert result.hra_deductible == 30_000
        assert result.is_eligible

    def test_rent_limited_metro(self):
        """Test metro case where rent is less than 50% of salary."""
        hra_input = HRAInput(
            basic_salary=100_000,
            house_rent=35_000,  # Less than 50%
            is_metro=True,
        )
        result = calculate_hra(hra_input)
        # Metro 50% = 50,000
        # Rent - 10% = 35,000 - 10,000 = 25,000
        # HRA = min(50,000, 25,000) = 25,000
        assert result.max_hra_by_city == 50_000
        assert result.max_hra_by_rent == 25_000
        assert result.hra_deductible == 25_000
        assert result.is_eligible

    def test_high_salary_metro(self):
        """Test metro with high salary."""
        hra_input = HRAInput(
            basic_salary=200_000,
            house_rent=150_000,
            is_metro=True,
        )
        result = calculate_hra(hra_input)
        # Metro 50% = 100,000
        # Rent - 10% = 150,000 - 20,000 = 130,000
        # HRA = min(100,000, 130,000) = 100,000
        assert result.hra_deductible == 100_000


class TestNonMetroHRA:
    """Test HRA calculation for non-metro cities (40%)."""

    def test_standard_non_metro_case(self):
        """Test standard non-metro case."""
        hra_input = HRAInput(
            basic_salary=50_000,
            house_rent=25_000,
            is_metro=False,
        )
        result = calculate_hra(hra_input)
        # Non-metro 40% = 20,000
        # Rent - 10% = 25,000 - 5,000 = 20,000
        # HRA = min(20,000, 20,000) = 20,000
        assert result.max_hra_by_city == 20_000
        assert result.max_hra_by_rent == 20_000
        assert result.hra_deductible == 20_000
        assert result.is_eligible

    def test_rent_limited_non_metro(self):
        """Test non-metro case where rent is less than 40% of salary."""
        hra_input = HRAInput(
            basic_salary=100_000,
            house_rent=25_000,  # Less than 40%
            is_metro=False,
        )
        result = calculate_hra(hra_input)
        # Non-metro 40% = 40,000
        # Rent - 10% = 25,000 - 10,000 = 15,000
        # HRA = min(40,000, 15,000) = 15,000
        assert result.max_hra_by_city == 40_000
        assert result.max_hra_by_rent == 15_000
        assert result.hra_deductible == 15_000
        assert result.is_eligible

    def test_non_metro_zero_rent(self):
        """Test non-metro with zero rent."""
        hra_input = HRAInput(
            basic_salary=50_000,
            house_rent=0,
            is_metro=False,
        )
        result = calculate_hra(hra_input)
        assert result.hra_deductible == 0
        assert not result.is_eligible


class TestComparison:
    """Compare metro vs non-metro for same inputs."""

    def test_metro_vs_non_metro_same_salary_rent(self):
        """Test same salary and rent in metro vs non-metro."""
        salary = 60_000
        rent = 40_000

        metro_input = HRAInput(basic_salary=salary, house_rent=rent, is_metro=True)
        non_metro_input = HRAInput(
            basic_salary=salary, house_rent=rent, is_metro=False
        )

        metro_result = calculate_hra(metro_input)
        non_metro_result = calculate_hra(non_metro_input)

        # Metro 50% = 30,000; Rent - 10% = 34,000; HRA = 30,000
        # Non-metro 40% = 24,000; Rent - 10% = 34,000; HRA = 24,000
        assert metro_result.hra_deductible == 30_000
        assert non_metro_result.hra_deductible == 24_000
        assert metro_result.hra_deductible > non_metro_result.hra_deductible


class TestEdgeCases:
    """Test edge cases."""

    def test_very_high_salary(self):
        """Test with very high salary."""
        hra_input = HRAInput(
            basic_salary=10_00_000,  # 10 lakh
            house_rent=6_00_000,  # 6 lakh
            is_metro=True,
        )
        result = calculate_hra(hra_input)
        # Metro 50% = 5,00,000
        # Rent - 10% = 6,00,000 - 1,00,000 = 5,00,000
        # HRA = min(5,00,000, 5,00,000) = 5,00,000
        assert result.hra_deductible == 5_00_000
        assert result.is_eligible

    def test_fractional_values(self):
        """Test with fractional rupees."""
        hra_input = HRAInput(
            basic_salary=50_500.50,
            house_rent=30_000.75,
            is_metro=True,
        )
        result = calculate_hra(hra_input)
        assert result.hra_deductible >= 0

    def test_rent_much_higher_than_salary(self):
        """Test when rent is much higher than salary."""
        hra_input = HRAInput(
            basic_salary=20_000,
            house_rent=80_000,  # 4x salary
            is_metro=True,
        )
        result = calculate_hra(hra_input)
        # Metro 50% = 10,000
        # Rent - 10% = 80,000 - 2,000 = 78,000
        # HRA = min(10,000, 78,000) = 10,000
        assert result.hra_deductible == 10_000
        assert result.is_eligible


class TestMetricsAndCalculations:
    """Test specific metrics and calculations."""

    def test_rent_threshold_calculation(self):
        """Test rent threshold is 10% of basic."""
        hra_input = HRAInput(basic_salary=100_000, house_rent=0, is_metro=True)
        result = calculate_hra(hra_input)
        assert result.rent_threshold == 10_000  # 10% of 100,000

    def test_city_type_label(self):
        """Test city type labels."""
        metro_input = HRAInput(basic_salary=50_000, house_rent=30_000, is_metro=True)
        non_metro_input = HRAInput(
            basic_salary=50_000, house_rent=30_000, is_metro=False
        )

        metro_result = calculate_hra(metro_input)
        non_metro_result = calculate_hra(non_metro_input)

        assert metro_result.city_type == "Metro"
        assert non_metro_result.city_type == "Non-Metro"

    def test_hra_percentage_values(self):
        """Test HRA percentage values."""
        metro_input = HRAInput(basic_salary=50_000, house_rent=30_000, is_metro=True)
        non_metro_input = HRAInput(
            basic_salary=50_000, house_rent=30_000, is_metro=False
        )

        metro_result = calculate_hra(metro_input)
        non_metro_result = calculate_hra(non_metro_input)

        assert metro_result.hra_percentage == 0.50
        assert non_metro_result.hra_percentage == 0.40

