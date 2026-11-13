import streamlit as st
from frontend.api import get, post
from frontend.components import event_detail
from frontend.styles import header

def render():
    header("Incidents", "Review failed deliveries and the evidence available for investigation.")
    items = get("/incidents") or []
    if not items:
        st.success("No open incidents. Use Demo Simulator to create a failure.")
        return
    options = {f"{e['id']} · HTTP {e['http_status']} · {e['event_type']}": e["id"] for e in items}
    selected = st.selectbox("Select incident", list(options))
    event_id = options[selected]
    event_detail(event_id)
    if st.button("Generate investigation", type="primary"):
        if post(f"/events/{event_id}/investigate"):
            st.session_state["investigation_event"] = event_id
            st.session_state["active_page"] = "AI Investigations"
            st.rerun()
