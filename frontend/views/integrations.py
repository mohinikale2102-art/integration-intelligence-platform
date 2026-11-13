import streamlit as st
from frontend.api import get
from frontend.styles import header

def render():
    header("Integrations", "Applications connected to the ShopEase demonstration environment.")
    items = get("/integrations") or []
    cols = st.columns(3)
    for index, item in enumerate(items):
        with cols[index % 3]:
            with st.container(border=True):
                st.markdown(f"### {item['name']}")
                st.success(item["status"].title())
                st.caption(item["system_type"])
                st.write(item["description"])
                st.caption(item["id"])
    st.info("Version 1.0 uses local application simulators. External SaaS connections are outside the MVP.")
