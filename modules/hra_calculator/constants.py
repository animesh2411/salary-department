"""
Constants for the HRA Calculator module.
Contains HRA rules for metro and non-metro cities.
Years are dynamically calculated based on current date.
"""

from .year_utils import get_fiscal_year_start, get_fiscal_year_end, get_fiscal_year_display, get_fiscal_year_range

# ============================================================================
# HRA DEDUCTION RULES (DYNAMIC - Current Fiscal Year)
# ============================================================================

# HRA is the MINIMUM of:
# 1. Actual HRA received
# 2. Based on city type (metro/non-metro)
# 3. Rent paid - 10% of basic salary
# 4. Rent paid - 0 if no house rent
#
# Note: These rules are automatically applied for the current fiscal year
# (April - March) based on system date. Will automatically update next year.

# Metro Cities: 50% of basic salary
HRA_PERCENTAGE_METRO = 0.50

# Non-Metro Cities: 40% of basic salary
HRA_PERCENTAGE_NON_METRO = 0.40

# Rent threshold for no HRA: if rent < 10% of basic, no HRA
RENT_THRESHOLD_PERCENTAGE = 0.10

# ============================================================================
# METRO CITIES (50% of Basic)
# As per current FY rules, only 8 cities qualify for 50% HRA exemption
# ============================================================================
METRO_CITIES = [
    "Delhi",
    "Mumbai",
    "Kolkata",
    "Chennai",
    "Bengaluru",
    "Hyderabad",
    "Pune",
    "Ahmedabad",
]

# ============================================================================
# NON-METRO CITIES (40% of Basic)
# All other cities fall under non-metro for 40% HRA exemption
# ============================================================================
NON_METRO_CITIES = [
    "Others",
]

# ============================================================================
# FINANCIAL YEAR INFORMATION (DYNAMIC)
# Automatically calculates based on current date
# ============================================================================
FY_START = get_fiscal_year_range()[0]
FY_END = get_fiscal_year_range()[1]
FY_DISPLAY = get_fiscal_year_display()
FY_START_YEAR = get_fiscal_year_start()
FY_END_YEAR = get_fiscal_year_end()

# ============================================================================
# DISPLAY CONSTANTS
# ============================================================================
CURRENCY_SYMBOL = "₹"
CURRENCY_FORMAT = "₹{:,.0f}"

CITY_TYPE_METRO = "Metro"
CITY_TYPE_NON_METRO = "Non-Metro"
