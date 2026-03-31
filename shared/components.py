"""
Reusable Streamlit UI components.
"""

import streamlit as st


def render_header(title: str, subtitle: str = "", icon: str = ""):
    """Render a consistent header for pages.

    Args:
        title: Main heading text.
        subtitle: Optional subtitle.
        icon: Optional emoji/icon.
    """
    if icon:
        st.title(f"{icon} {title}")
    else:
        st.title(title)

    if subtitle:
        st.markdown(f"_{subtitle}_")


def render_metric_card(label: str, value: str, delta: str = None):
    """Render a metric card with label and value.

    Args:
        label: Label for the metric.
        value: Value to display.
        delta: Optional change indicator.
    """
    st.metric(label=label, value=value, delta=delta)


def render_info_box(text: str, box_type: str = "info"):
    """Render an info box with message.

    Args:
        text: Message text.
        box_type: Type of box ('info', 'success', 'warning', 'error').
    """
    if box_type == "info":
        st.info(text)
    elif box_type == "success":
        st.success(text)
    elif box_type == "warning":
        st.warning(text)
    elif box_type == "error":
        st.error(text)
    else:
        st.info(text)


def render_section_divider():
    """Render a visual section divider."""
    st.markdown("---")


def render_footer():
    """Render a consistent footer."""
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: gray; font-size: 0.85em; padding: 20px 0;">
        <p>
        <strong>Salary Department</strong> — Your Personal Salary Assistant
        </p>
        <p style="font-size: 0.8em;">
        Built with ❤️ using Streamlit | Disclaimer: For educational purposes only
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
