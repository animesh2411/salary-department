"""
Shared helper functions across modules.
"""

from typing import Dict, Any


def get_module_info() -> Dict[str, Any]:
    """Get information about all available modules.

    Returns:
        Dictionary with module metadata.
    """
    return {
        "tax_calculator": {
            "name": "Tax Calculator",
            "description": "Calculate and compare income tax under Old vs New Regime (FY 2026-27)",
            "icon": "💰",
            "path": "tax_calculator",
            "status": "active",
        },
        "hra_calculator": {
            "name": "HRA Calculator",
            "description": "Calculate HRA deduction based on metro/non-metro city rules (FY 2026-27)",
            "icon": "🏠",
            "path": "hra_calculator",
            "status": "active",
        },
        # Placeholder for future modules
        "salary_analyzer": {
            "name": "Salary Analyzer",
            "description": "Analyze salary structure and compensation trends",
            "icon": "📊",
            "path": "salary_analyzer",
            "status": "coming_soon",
        },
        "retirement_planner": {
            "name": "Retirement Planner",
            "description": "Plan your retirement and calculate corpus needed",
            "icon": "🏖️",
            "path": "retirement_planner",
            "status": "coming_soon",
        },
    }


def get_active_modules() -> Dict[str, Any]:
    """Get only active modules.

    Returns:
        Dictionary with active modules only.
    """
    all_modules = get_module_info()
    return {k: v for k, v in all_modules.items() if v["status"] == "active"}


def get_coming_soon_modules() -> Dict[str, Any]:
    """Get only coming soon modules.

    Returns:
        Dictionary with coming soon modules only.
    """
    all_modules = get_module_info()
    return {k: v for k, v in all_modules.items() if v["status"] == "coming_soon"}
