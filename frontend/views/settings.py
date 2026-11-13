import streamlit as st

from app.config import API_URL, GEMINI_API_KEY, GEMINI_MODEL
from frontend.api import get
from frontend.styles import header


def render():
    header(
        "Settings",
        "Manage workspace configuration, AI services and environment information.",
    )

    st.markdown("### Workspace configuration")

    with st.container(border=True):
        st.markdown("#### Workspace details")

        st.text_input(
            "Workspace name",
            value="ShopEase Demo Environment",
            disabled=True,
        )

        st.text_input(
            "Backend service URL",
            value=API_URL,
            disabled=True,
        )

        st.caption(
            "These values are currently configured for the local demonstration environment."
        )

    st.markdown("")

    st.markdown("### AI configuration")

    with st.container(border=True):
        st.markdown("#### Gemini integration")

        col1, col2 = st.columns(2)

        with col1:
            st.text_input(
                "AI model",
                value=GEMINI_MODEL,
                disabled=True,
            )

        with col2:
            st.text_input(
                "API key status",
                value="Configured" if GEMINI_API_KEY else "Not configured",
                disabled=True,
            )

        if GEMINI_API_KEY:
            st.success("Gemini API key detected in the environment.")
        else:
            st.info(
                "Gemini is optional. Evidence-based rule explanations remain available without an API key."
            )

        st.caption(
            "The API key is stored in the local environment and is not displayed here."
        )

    st.markdown("")

    st.markdown("### Service health")

    health = get("/health")

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Backend service")

            if health:
                st.success("Connected and healthy")
            else:
                st.error("Unable to connect to the backend")

        with col2:
            st.markdown("#### Application environment")
            st.info("Local demonstration environment")

    st.markdown("")

    st.markdown("### Demo environment")

    with st.container(border=True):
        st.markdown("#### Simulation and data")

        st.write(
            "This workspace uses simulated business systems to demonstrate "
            "integration monitoring, webhook delivery, failure investigation "
            "and manual retries."
        )

        st.warning(
            "All orders, customer information and payment transactions are fictional. "
            "No real payment is processed."
        )

        st.caption(
            "Integration Intelligence Platform · Version 1.0.0"
        )