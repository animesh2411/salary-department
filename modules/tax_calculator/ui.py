"""
Streamlit UI for the Tax Calculator module.
Handles all user interface and interactions.
"""

import streamlit as st
import pandas as pd

from .service import compare_tax
from .models import SalaryInput
from .constants import (
    DEDUCTION_80C_MAX,
    DEDUCTION_80D_MAX_FAMILY,
    FY_DISPLAY,
    REGIME_NEW,
    REGIME_OLD,
)
from .utils import format_currency, format_percentage


def render():
    """Render the Tax Calculator module in Streamlit."""
    st.set_page_config(
        page_title="Tax Calculator",
        page_icon="💰",
        layout="wide",
    )

    st.title("💰 Tax Calculator – Old vs New Regime")
    st.markdown(f"**Financial Year {FY_DISPLAY}**")
    st.markdown("---")

    # Create two columns for input and output
    col1, col2 = st.columns([1, 1], gap="large")

    # ===========================================================================
    # LEFT COLUMN: INPUT SECTION
    # ===========================================================================
    with col1:
        st.subheader("📝 Income & Deductions")

        # Salary input
        gross_salary = st.number_input(
            "Gross Annual Salary (₹)",
            min_value=0,
            max_value=100_000_000,
            value=10_00_000,
            step=100_000,
            help="Your total annual salary before any deductions or taxes.",
        )

        st.markdown("---")

        # Old Regime Deductions
        with st.expander("🔧 Old Regime Deductions", expanded=True):
            st.markdown(
                "These deductions are **only applicable** in the Old Regime. "
                "They don't apply in the New Regime."
            )

            st.info(
                "💡 **Tip:** Enter exact amounts in rupees. "
                "Calculate HRA separately (typically: Rent – 10% of salary, max 50% of salary)"
            )

            col_80c, col_80d = st.columns(2)

            with col_80c:
                deduction_80c = st.number_input(
                    "80C – Insurance, PPF, etc. (₹)",
                    min_value=0,
                    max_value=int(DEDUCTION_80C_MAX),
                    value=0,
                    step=1000,
                    help=f"Max limit: ₹{DEDUCTION_80C_MAX:,.0f}. "
                    f"Includes Life Insurance, PPF, ELSS, etc.",
                )

            with col_80d:
                deduction_80d = st.number_input(
                    "80D – Health Insurance (₹)",
                    min_value=0,
                    max_value=int(DEDUCTION_80D_MAX_FAMILY),
                    value=0,
                    step=1000,
                    help=f"Max limit: ₹{DEDUCTION_80D_MAX_FAMILY:,.0f} for self + family.",
                )

            col_hra, col_other = st.columns(2)

            with col_hra:
                hra_deduction = st.number_input(
                    "HRA Deduction (₹)",
                    min_value=0,
                    max_value=int(gross_salary),
                    value=0,
                    step=1000,
                    help="Enter HRA amount in rupees. "
                    "Calculate as: Rent minus 10% of salary (max 50% of salary)",
                )

            with col_other:
                other_deductions = st.number_input(
                    "Other Eligible Deductions (₹)",
                    min_value=0,
                    max_value=int(gross_salary),
                    value=0,
                    step=1000,
                    help="Any other deductions like donations, etc.",
                )

        # Create SalaryInput object
        salary_input = SalaryInput(
            gross_salary=gross_salary,
            deduction_80c=deduction_80c,
            deduction_80d=deduction_80d,
            hra_deduction=hra_deduction,
            other_deductions=other_deductions,
        )

    # ===========================================================================
    # RIGHT COLUMN: OUTPUT SECTION
    # ===========================================================================
    with col2:
        st.subheader("📊 Tax Comparison")

        # Calculate taxes
        comparison = compare_tax(salary_input)

        # Display recommendation prominently
        st.markdown("---")
        recommendation = comparison.recommendation_text
        st.success(f"**✅ Recommendation:** {recommendation}")
        st.markdown("---")

        # Create tabs for detailed view
        tab1, tab2, tab3 = st.tabs(
            ["📈 Comparison", "🆕 New Regime", "🕰️ Old Regime"]
        )

        # TAB 1: Comparison
        with tab1:
            col_new, col_old = st.columns(2)

            with col_new:
                st.subheader("New Regime")
                st.metric(
                    "Tax Payable",
                    format_currency(comparison.new_regime_result.tax_amount),
                    delta=f"-{format_currency(comparison.savings)}"
                    if comparison.recommended_regime == REGIME_NEW
                    else None,
                )
                st.metric(
                    "Take-Home Salary",
                    format_currency(comparison.new_regime_result.take_home),
                )
                st.metric(
                    "Effective Tax Rate",
                    format_percentage(
                        comparison.new_regime_result.effective_tax_rate
                    ),
                )

            with col_old:
                st.subheader("Old Regime")
                st.metric(
                    "Tax Payable",
                    format_currency(comparison.old_regime_result.tax_amount),
                    delta=f"-{format_currency(comparison.savings)}"
                    if comparison.recommended_regime == REGIME_OLD
                    else None,
                )
                st.metric(
                    "Take-Home Salary",
                    format_currency(comparison.old_regime_result.take_home),
                )
                st.metric(
                    "Effective Tax Rate",
                    format_percentage(
                        comparison.old_regime_result.effective_tax_rate
                    ),
                )

            # Comparison chart
            st.markdown("---")
            comparison_data = {
                "Regime": ["New Regime", "Old Regime"],
                "Tax": [
                    comparison.new_regime_result.tax_amount,
                    comparison.old_regime_result.tax_amount,
                ],
                "Take-Home": [
                    comparison.new_regime_result.take_home,
                    comparison.old_regime_result.take_home,
                ],
            }
            comparison_df = pd.DataFrame(comparison_data)
            st.bar_chart(
                comparison_df.set_index("Regime"),
                height=300,
            )

        # TAB 2: New Regime Details
        with tab2:
            st.markdown("**New Regime Calculation:**")
            new_result = comparison.new_regime_result

            st.info(
                "**Rules:** "
                "Standard Deduction ₹75,000 | "
                "No other deductions | "
                "Rebate if taxable income ≤ ₹12L"
            )

            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Gross Income:** {format_currency(new_result.gross_income)}")
                st.write(f"**Standard Deduction:** {format_currency(75_000)}")
            with col_b:
                st.write(
                    f"**Taxable Income:** {format_currency(new_result.taxable_income)}"
                )
                st.write(f"**Tax:** {format_currency(new_result.tax_amount)}")

        # TAB 3: Old Regime Details
        with tab3:
            st.markdown("**Old Regime Calculation:**")
            old_result = comparison.old_regime_result

            st.info(
                "**Rules:** "
                "Standard Deduction ₹75,000 | "
                "Deductions: 80C, 80D, HRA, etc."
            )

            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Gross Income:** {format_currency(old_result.gross_income)}")
                st.write(f"**Standard Deduction:** {format_currency(75_000)}")
                st.write(f"**80C Deduction:** {format_currency(salary_input.deduction_80c)}")
                st.write(f"**80D Deduction:** {format_currency(salary_input.deduction_80d)}")
            with col_b:
                st.write(f"**HRA Deduction:** {format_currency(salary_input.hra_deduction)}")
                st.write(
                    f"**Other Deductions:** {format_currency(salary_input.other_deductions)}"
                )
                st.write(
                    f"**Total Deductions:** {format_currency(old_result.total_deductions)}"
                )
                st.write(f"**Taxable Income:** {format_currency(old_result.taxable_income)}")

            st.write(f"**Tax:** {format_currency(old_result.tax_amount)}")

    # ===========================================================================
    # FOOTER SECTION
    # ===========================================================================
    st.markdown("---")
    with st.expander("ℹ️ How it works", expanded=False):
        st.markdown("""
        ### Tax Regimes Explained

        **New Regime (Default):**
        - Simpler, no deductions allowed (except standard deduction)
        - Progressive tax slabs
        - ₹75,000 standard deduction
        - No tax if taxable income ≤ ₹12 Lakhs
        - Better for employees with fixed salary, no investments

        **Old Regime (Traditional):**
        - Allows deductions under 80C, 80D, HRA, etc.
        - Progressive tax slabs
        - ₹75,000 standard deduction
        - Better for investors, high earners with deductions

        ### Key Differences

        | Feature | New Regime | Old Regime |
        |---------|-----------|-----------|
        | Deductions | ❌ Not Allowed | ✅ Allowed |
        | Tax Slabs | More Progressive | Less Progressive |
        | Rebate | ✅ If ≤ ₹12L | ❌ No |
        | Complexity | ✅ Simple | ❌ Complex |

        ### Recommendations

        - **New Regime:** If you have minimal deductions and want simplicity
        - **Old Regime:** If you invest in insurance, PPF, health insurance, or pay rent (HRA)

        ### Disclaimer

        This calculator is for informational purposes only.
        Please consult with a CA for final tax planning decisions.
        """)

    st.markdown("""
    <div style="text-align: center; color: gray; font-size: 0.8em;">
    💡 Disclaimer: This tool is for educational purposes. Consult a CA for precise tax planning.
    </div>
    """, unsafe_allow_html=True)
