import streamlit as st
from frontend.api import get, post
from frontend.styles import header

def render():
    header("Retries", "Review delivery attempts and manually retry eligible failed events.")
    failed = get("/events", params={"status": "failed", "limit": 500}) or []
    st.metric("Failed events eligible for retry", len(failed))
    if not failed:
        st.success("There are no failed events waiting for retry.")
        return
    options = {f"{e['id']} · HTTP {e['http_status']} · {e['event_type']}": e["id"] for e in failed}
    selected = st.selectbox("Select failed event", list(options))
    event_id = options[selected]
    st.warning("Retry creates a new delivery attempt. The original event and its history are retained.")
    if st.button("Retry selected event", type="primary"):
        if st.session_state.get("retry_confirmation") != event_id:
            st.session_state["retry_confirmation"] = event_id
            st.warning("Click Retry again to confirm this action.")
        else:
            result = post(f"/events/{event_id}/retry")
            st.session_state.pop("retry_confirmation", None)
            if result:
                st.success(f"Retry completed. Current status: {result['status']}.")
                st.rerun()
    st.markdown("### Attempt history")
    detail = get(f"/events/{event_id}")
    if detail and detail["attempts"]:
        st.dataframe(detail["attempts"], use_container_width=True, hide_index=True)
