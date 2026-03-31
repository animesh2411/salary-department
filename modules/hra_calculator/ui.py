"""
Streamlit UI for the HRA Calculator module.
"""

import streamlit as st

from .service import calculate_hra
from .models import HRAInput
from .constants import (
    FY_DISPLAY,
    METRO_CITIES,
    NON_METRO_CITIES,
)


def render():
    """Render the HRA Calculator module in Streamlit."""
    st.set_page_config(
        page_title="HRA Calculator",
        page_icon="🏠",
        layout="wide",
    )

    st.title("🏠 HRA Calculator – Metro vs Non-Metro Cities")
    st.markdown(f"**Financial Year {FY_DISPLAY}**")
    st.markdown("---")

    # Create two columns
    col1, col2 = st.columns([1, 1], gap="large")

    # ===========================================================================
    # LEFT COLUMN: INPUT SECTION
    # ===========================================================================
    with col1:
        st.subheader("📋 Input Details")

        # Salary period selector
        salary_period = st.radio(
            "Select Salary Period:",
            options=["Monthly", "Annual"],
            horizontal=True,
            help="Choose whether you want to calculate monthly or annual HRA",
        )

        # Basic salary input
        if salary_period == "Monthly":
            basic_salary = st.number_input(
                "Monthly Basic Salary (₹)",
                min_value=0,
                max_value=10_000_000,
                value=50_000,
                step=1_000,
                help="Enter your basic salary per month",
            )
            house_rent = st.number_input(
                "Monthly House Rent (₹)",
                min_value=0,
                max_value=10_000_000,
                value=30_000,
                step=1_000,
                help="Enter your monthly house rent",
            )
        else:
            basic_salary = st.number_input(
                "Annual Basic Salary (₹)",
                min_value=0,
                max_value=100_000_000,
                value=600_000,
                step=10_000,
                help="Enter your basic salary per annum",
            )
            house_rent = st.number_input(
                "Annual House Rent (₹)",
                min_value=0,
                max_value=100_000_000,
                value=360_000,
                step=10_000,
                help="Enter your annual house rent",
            )

        st.markdown("---")

        # City selection
        st.markdown("**Select City:**")

        city_type_selection = st.radio(
            "City Type:",
            options=["Metro", "Non-Metro"],
            horizontal=True,
            help="Select whether your city is metro or non-metro",
        )

        is_metro = city_type_selection == "Metro"

        # City dropdown
        if is_metro:
            available_cities = METRO_CITIES
            default_index = 0  # Delhi
        else:
            available_cities = NON_METRO_CITIES
            default_index = 0

        selected_city = st.selectbox(
            "Choose City:",
            options=available_cities,
            index=default_index,
            help="Select your city of residence",
        )

        # Note: selected_city variable can be used to show city-specific tax implications
        st.caption(f"📍 Selected: {selected_city} ({city_type_selection})")
        hra_input = HRAInput(
            basic_salary=basic_salary,
            house_rent=house_rent,
            is_metro=is_metro,
        )

    # ===========================================================================
    # RIGHT COLUMN: OUTPUT SECTION
    # ===========================================================================
    with col2:
        st.subheader("📊 HRA Calculation Results")

        # Calculate HRA
        calculation = calculate_hra(hra_input)

        # Display results
        st.markdown("---")

        # Result box
        if calculation.is_eligible:
            st.success(
                f"✅ **HRA Deductible: ₹{calculation.hra_deductible:,.0f}**"
            )
        else:
            st.warning(
                "⚠️ **No HRA Deductible** (Rent < 10% of Basic)"
            )

        st.markdown("---")

        # Detailed breakdown
        st.markdown("**Detailed Breakdown:**")

        col_a, col_b = st.columns(2)

        with col_a:
            st.metric(
                label="Basic Salary",
                value=f"₹{calculation.basic_salary:,.0f}",
            )
            st.metric(
                label="House Rent Paid",
                value=f"₹{calculation.house_rent:,.0f}",
            )
            st.metric(
                label="Rent Threshold (10% of Basic)",
                value=f"₹{calculation.rent_threshold:,.0f}",
            )

        with col_b:
            st.metric(
                label="City Type",
                value=calculation.city_type,
            )
            st.metric(
                label=f"Max by {calculation.city_type} ({int(calculation.hra_percentage*100)}%)",
                value=f"₹{calculation.max_hra_by_city:,.0f}",
            )
            st.metric(
                label="Max by Rent Rule",
                value=f"₹{calculation.max_hra_by_rent:,.0f}",
            )

        st.markdown("---")

        # Yearly breakdown (if salary period is monthly)
        if salary_period == "Monthly":
            st.markdown("**Yearly Equivalent:**")
            col_y1, col_y2 = st.columns(2)

            with col_y1:
                st.metric(
                    label="Annual Basic Salary",
                    value=f"₹{calculation.basic_salary * 12:,.0f}",
                )
                st.metric(
                    label="Annual Max by Rent Rule",
                    value=f"₹{calculation.max_hra_by_rent * 12:,.0f}",
                )

            with col_y2:
                st.metric(
                    label="Annual HRA Deductible",
                    value=f"₹{calculation.hra_deductible * 12:,.0f}",
                )

        st.markdown("---")

        # Explanation
        st.info(f"**Calculation:** {calculation.explanation}")

    # ===========================================================================
    # FOOTER SECTION
    # ===========================================================================
    st.markdown("---")

    with st.expander("ℹ️ How HRA Deduction Works", expanded=False):
        st.markdown("""
        ### HRA (House Rent Allowance) Rules – FY 2026-27

        **HRA is the MINIMUM of:**

        1. **Actual HRA Received**
           - The HRA amount given by your employer

        2. **City Type Limit:**
           - **Metro Cities:** 50% of Basic Salary
           - **Non-Metro Cities:** 40% of Basic Salary

        3. **Rent Rule:**
           - Rent paid minus 10% of Basic Salary
           - If rent ≤ 10% of basic, then HRA = ₹0

        ### Metro Cities (50%)
        """)
        st.write(", ".join(METRO_CITIES))

        st.markdown("### Non-Metro Cities (40%)")
        st.write(", ".join(NON_METRO_CITIES))

        st.markdown("""
        ### Examples

        #### Example 1: Metro City (50%)
        ```
        Basic Salary: ₹60,000/month
        House Rent: ₹40,000/month
        City: Delhi (Metro)

        Calculation:
        • Limit by city (50%): ₹60,000 × 50% = ₹30,000
        • Limit by rent: ₹40,000 - (10% × ₹60,000) = ₹40,000 - ₹6,000 = ₹34,000
        • HRA deductible: Min(₹30,000, ₹34,000) = ₹30,000
        ```

        #### Example 2: Non-Metro City (40%)
        ```
        Basic Salary: ₹50,000/month
        House Rent: ₹25,000/month
        City: Bhopal (Non-Metro)

        Calculation:
        • Limit by city (40%): ₹50,000 × 40% = ₹20,000
        • Limit by rent: ₹25,000 - (10% × ₹50,000) = ₹25,000 - ₹5,000 = ₹20,000
        • HRA deductible: Min(₹20,000, ₹20,000) = ₹20,000
        ```

        #### Example 3: Low Rent
        ```
        Basic Salary: ₹80,000/month
        House Rent: ₹6,000/month
        City: Any City

        Calculation:
        • Rent threshold (10%): ₹80,000 × 10% = ₹8,000
        • House rent (₹6,000) < Threshold (₹8,000)
        • HRA deductible: ₹0 (No HRA)
        ```

        ### Important Notes

        - HRA is **deductible only from salary income**, not other income
        - Rent must be **paid for accommodation** where you stay
        - You must have **proof of rent payment**
        - Maximum deduction is limited to **actual HRA received**
        - If you own your house, **no HRA deduction**
        """)

    st.markdown("""
    <div style="text-align: center; color: gray; font-size: 0.8em; margin-top: 20px;">
    💡 This calculator follows Indian Income Tax Rules for FY 2026-27.
    For residential accommodation only. Consult a CA for complex scenarios.
    </div>
    """, unsafe_allow_html=True)
