import streamlit as st

from frontend.styles import apply
from frontend.views import (
    dashboard,
    integrations,
    events,
    incidents,
    investigations,
    retries,
    reports,
    settings,
    simulator,
)

st.set_page_config(
    page_title="Integration Intelligence Platform",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply()

PAGES = {
    "Overview": ("◫", dashboard.render),
    "Integrations": ("▦", integrations.render),
    "Events": ("⌁", events.render),
    "Incidents": ("⚠", incidents.render),
    "AI Investigations": ("✧", investigations.render),
    "Retries": ("↻", retries.render),
    "Reports": ("▤", reports.render),
    "Demo Simulator": ("▷", simulator.render),
    "Settings": ("⚙", settings.render),
}

if "active_page" not in st.session_state:
    st.session_state["active_page"] = "Overview"

if st.session_state["active_page"] not in PAGES:
    st.session_state["active_page"] = "Overview"

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <span class="brand-mark">⌁</span>
            Integration<br>Intelligence Platform
        </div>
        <div class="sidebar-caption">SHOPEASE DEMONSTRATION WORKSPACE</div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    for name, (symbol, render_page) in PAGES.items():
        selected = st.session_state["active_page"] == name

        if st.button(
            f"{symbol}   {name}",
            key=f"nav-{name}",
            use_container_width=True,
            type="primary" if selected else "secondary",
        ):
            st.session_state["active_page"] = name
            st.rerun()

    st.divider()

    st.markdown(
        """
        <div style="padding: 10px 5px 3px;">
            <div style="color:#91A5C0;font-size:11px;font-weight:700;
                        letter-spacing:1px;">ENVIRONMENT</div>
            <div style="color:#FFFFFF;font-size:13px;margin-top:7px;">
                ● Local demo environment
            </div>
            <div style="color:#91A5C0;font-size:11px;margin-top:5px;">
                Version 1.0.0
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

PAGES[st.session_state["active_page"]][1]()