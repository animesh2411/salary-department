"""
Main Streamlit Application - Salary Department Dashboard.

This is the home page and navigation hub for all salary-related tools.
"""

import streamlit as st
from shared.helpers import get_active_modules, get_coming_soon_modules
from modules.tax_calculator import ui as tax_calculator_ui
from modules.hra_calculator import ui as hra_calculator_ui


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Salary Department",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
st.sidebar.markdown("# 💼 Salary Department")
st.sidebar.markdown("Your Personal Salary Assistant")
st.sidebar.markdown("---")

# Initialize session state for navigation
if "navigation" not in st.session_state:
    st.session_state.navigation = "🏠 Home"

navigation = st.sidebar.radio(
    "Select a Tool:",
    options=["🏠 Home", "💰 Tax Calculator", "📊 HRA Calculator", "🎯 More Tools"],
    label_visibility="collapsed",
)
st.session_state.navigation = navigation

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    ### 📚 About

    **Salary Department** is your one-stop solution for:
    - Tax calculation and planning
    - Salary analysis
    - Retirement planning

    **Version:** 1.0.0
    **Last Updated:** April 2026
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="font-size: 0.8em; color: gray; text-align: center;">
    Made with ❤️ by Your Salary Buddy<br>
    <a href="https://www.linkedin.com/in/animesh2411" target="_blank">Animesh @LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# PAGE ROUTING
# ============================================================================

if navigation == "🏠 Home":
    # ========================================================================
    # HOME PAGE
    # ========================================================================
    st.title("💼 Welcome to Salary Department")
    st.markdown("---")

    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown(
            """
            ## Your Personal Salary Assistant 📊

            Welcome! **Salary Department** is a comprehensive platform designed to help you:

            - 💰 **Calculate Income Tax** under Old vs New Regime
            - 📈 **Analyze Your Salary** structure and components
            - 🏖️ **Plan Your Retirement** with confidence
            - 🎯 **Optimize Your Earnings** through smart financial planning

            ### Why Use Salary Department?

            ✅ **Accurate Tax Calculation** – Based on FY 2026-27 rules
            ✅ **Easy-to-Use Interface** – No technical knowledge needed
            ✅ **Detailed Analysis** – Understand every aspect of your salary
            ✅ **Multiple Tools** – Growing library of salary tools
            ✅ **Free & Open** – No hidden charges

            ---

            ## 🚀 Get Started

            Use the navigation menu on the left to explore tools:
            """
        )

    with col1:
        # Active modules showcase
        active_modules = get_active_modules()

        st.markdown("### 🟢 Active Tools")

        for module_key, module_info in active_modules.items():
            with st.container(border=True):
                col_icon, col_content = st.columns([1, 4], gap="small")

                with col_icon:
                    st.markdown(f"### {module_info['icon']}")

                with col_content:
                    st.markdown(f"**{module_info['name']}**")
                    st.markdown(module_info["description"])
                    st.markdown(f"👉 Select **{module_info['name']}** from the left sidebar to use this tool.")

            st.markdown("")

        # Coming soon modules
        coming_soon_modules = get_coming_soon_modules()

        if coming_soon_modules:
            st.markdown("### 🟡 Coming Soon")

            for module_key, module_info in coming_soon_modules.items():
                with st.container(border=True):
                    col_icon, col_content = st.columns([1, 4], gap="small")

                    with col_icon:
                        st.markdown(f"### {module_info['icon']}")

                    with col_content:
                        st.markdown(f"**{module_info['name']}**")
                        st.markdown(f"_{module_info['description']}_")
                        st.markdown("🔜 **Coming Soon**")

                st.markdown("")

    with col2:
        st.markdown("### 📊 Quick Stats")

        st.metric(label="Tools Available", value="1")
        st.metric(label="Tools in Development", value="2")
        st.metric(label="Financial Year", value="2026-27")

        st.markdown("---")

        st.markdown("### 💡 Tips")

        st.info(
            """
            **Pro Tip:** The Tax Calculator uses the latest FY 2026-27 tax rules.
            Make sure to update your deductions for accurate results!
            """
        )

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: gray; font-size: 0.85em; padding: 20px 0;">
        <p>
        <strong>Salary Department v1.0.0</strong>
        </p>
        <p style="font-size: 0.8em;">
        Built with ❤️ using Streamlit | For informational purposes only
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


elif navigation == "💰 Tax Calculator":
    # ========================================================================
    # TAX CALCULATOR PAGE
    # ========================================================================
    tax_calculator_ui.render()


elif navigation == "📊 HRA Calculator":
    # ========================================================================
    # HRA CALCULATOR PAGE
    # ========================================================================
    hra_calculator_ui.render()


elif navigation == "🎯 More Tools":
    # ========================================================================
    # MORE TOOLS PAGE (Placeholder)
    # ========================================================================
    st.title("📊 More Tools Coming Soon")
    st.markdown("---")

    st.info(
        "We're working on more salary tools to make your financial planning easier!"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            ### 📈 Salary Analyzer

            Analyze your salary structure:
            - Gross vs Net breakdown
            - Component-wise distribution
            - Year-on-year comparison

            **Status:** 🔜 Coming Soon
            """
        )

    with col2:
        st.markdown(
            """
            ### 🏖️ Retirement Planner

            Plan your retirement:
            - Corpus calculation
            - Investment recommendations
            - Life expectancy analysis

            **Status:** 🔜 Coming Soon
            """
        )

    with col3:
        st.markdown(
            """
            ### 💼 Benefits Optimizer

            Optimize benefits:
            - Insurance recommendations
            - Investment planning
            - Tax deduction strategies

            **Status:** 🔜 Coming Soon
            """
        )

    st.markdown("---")
    st.markdown(
        """
        ## 🤝 Want to Contribute?

        Salary Department is open for contributions!
        Help us build more salary tools.

        📧 **Contact us** or contribute on GitHub
        """
    )
