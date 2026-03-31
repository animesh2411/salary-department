"""
Constants for the Tax Calculator module.
Contains tax slabs, deduction limits, and other configuration values.
Years are dynamically calculated based on current date.
"""

from .year_utils import get_fiscal_year_display

# Standard Deduction (applicable to both regimes)
STANDARD_DEDUCTION = 75_000
STANDARD_DEDUCTION_OLD = 75_000

# ==============================================================================
# NEW REGIME TAX SLABS
# ==============================================================================
NEW_REGIME_SLABS = [
    {"min": 0, "max": 4_00_000, "rate": 0.0},
    {"min": 4_00_000, "max": 8_00_000, "rate": 0.05},
    {"min": 8_00_000, "max": 12_00_000, "rate": 0.10},
    {"min": 12_00_000, "max": 16_00_000, "rate": 0.15},
    {"min": 16_00_000, "max": 20_00_000, "rate": 0.20},
    {"min": 20_00_000, "max": 24_00_000, "rate": 0.25},
    {"min": 24_00_000, "max": float("inf"), "rate": 0.30},
]

# New Regime Rebate: Tax becomes 0 if taxable income <= 12L
NEW_REGIME_REBATE_LIMIT = 12_00_000

# ==============================================================================
# OLD REGIME TAX SLABS
# ==============================================================================
OLD_REGIME_SLABS = [
    {"min": 0, "max": 2_50_000, "rate": 0.0},
    {"min": 2_50_000, "max": 5_00_000, "rate": 0.05},
    {"min": 5_00_000, "max": 10_00_000, "rate": 0.20},
    {"min": 10_00_000, "max": float("inf"), "rate": 0.30},
]

# ==============================================================================
# OLD REGIME DEDUCTION LIMITS
# ==============================================================================
DEDUCTION_80C_MAX = 1_50_000  # Life Insurance, PPF, etc.
DEDUCTION_80D_MAX = 1_00_000  # Health Insurance (self only)
DEDUCTION_80D_MAX_FAMILY = 2_00_000  # Health Insurance (with family)

# HRA Deduction - simplified as a percentage of salary
HRA_PERCENTAGE_MIN = 0.0  # User can customize between 0-50% typically
HRA_PERCENTAGE_MAX = 0.50  # Max 50% of salary typically

# ==============================================================================
# DISPLAY NAMES & UI CONSTANTS
# ==============================================================================
CURRENCY_SYMBOL = "₹"
CURRENCY_FORMAT = "₹{:,.0f}"

REGIME_NEW = "New Regime"
REGIME_OLD = "Old Regime"

# ==============================================================================
# FISCAL YEAR CONSTANTS (DYNAMIC)
# Automatically calculates based on current date (April-March)
# ==============================================================================
FY_DISPLAY = get_fiscal_year_display()
FY_START = get_fiscal_year_display().replace("FY ", "FY starting 1st April ")

FY_END = "31st March 2027"
