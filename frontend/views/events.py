import streamlit as st
from frontend.api import get, post
from frontend.components import event_table, event_detail
from frontend.styles import header

def render():
    header("Events", "Search, filter and inspect requests exchanged between connected applications.")
    a, b = st.columns([1, 2])
    with a:
        status = st.selectbox("Delivery status", ["All", "success", "failed"])
    with b:
        search = st.text_input("Search event ID, type or order ID")
    items = get("/events", params={"status": status, "search": search, "limit": 500}) or []
    event_table(items, "event-table")
    if items:
        options = {f"{item['id']} · {item['event_type']} · {item['status']}": item["id"] for item in items}
        selected = st.selectbox("Inspect event", list(options))
        event_detail(options[selected])
        chosen = next(item for item in items if item["id"] == options[selected])
        if chosen["status"] == "failed" and st.button("Investigate this event", type="primary"):
            result = post(f"/events/{chosen['id']}/investigate")
            if result:
                st.session_state["investigation_event"] = chosen["id"]
                st.session_state["active_page"] = "AI Investigations"
                st.rerun()
