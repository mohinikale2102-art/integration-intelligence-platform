import json
import streamlit as st
from frontend.api import get, post
from frontend.styles import header

def render():
    header("AI Investigations", "Evidence-based explanations and recommended troubleshooting steps.")
    failed = get("/events", params={"status": "failed", "limit": 500}) or []
    preferred = st.session_state.get("investigation_event")
    options = {f"{e['id']} · {e['event_type']} · HTTP {e['http_status']}": e["id"] for e in failed}
    if not options:
        st.info("No failed events are available. Create a failure from Demo Simulator.")
        return
    labels = list(options)
    default = next((i for i, label in enumerate(labels) if options[label] == preferred), 0)
    selected = st.selectbox("Select failed event", labels, index=default)
    event_id = options[selected]
    if st.button("Analyse event", type="primary"):
        post(f"/events/{event_id}/investigate")
    data = get(f"/events/{event_id}")
    if not data:
        return
    analysis = data.get("investigation")
    if not analysis:
        st.warning("Select Analyse event to generate an investigation.")
        return
    st.markdown("### Investigation summary")
    st.write(analysis["summary"])
    left, right = st.columns(2)
    with left:
        st.markdown("### Evidence")
        for item in json.loads(analysis["evidence"]):
            st.markdown(f"- {item}")
    with right:
        st.markdown("### Likely cause")
        st.write(analysis["likely_cause"])
        st.markdown("### Recommended next steps")
        for step in json.loads(analysis["recommendations"]):
            st.markdown(f"- {step}")
    st.caption(f"Explanation provider: {analysis['provider']}. Recommendations do not modify either connected system.")
