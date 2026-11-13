import html
import json

import pandas as pd
import streamlit as st

from frontend.api import get


def status_badge(status):
    value = str(status or "unknown").lower()

    if value in {"success", "successful", "healthy", "delivered"}:
        css_class = "status-healthy"
    elif value in {"warning", "pending", "retrying"}:
        css_class = "status-warning"
    elif value in {"failed", "failure", "error"}:
        css_class = "status-error"
    else:
        css_class = "status-info"

    return (
        f'<span class="status-pill {css_class}">'
        f'{html.escape(value.title())}</span>'
    )


def event_table(items, key):
    if not items:
        st.info("No events found. Create a simulated order to generate activity.")
        return

    frame = pd.DataFrame(items)

    columns = [
        "created_at",
        "id",
        "event_type",
        "source",
        "destination",
        "status",
        "http_status",
        "duration_ms",
    ]

    frame = frame[[column for column in columns if column in frame.columns]]

    frame = frame.rename(columns={
        "created_at": "Time",
        "id": "Event ID",
        "event_type": "Event type",
        "source": "Source",
        "destination": "Destination",
        "status": "Status",
        "http_status": "HTTP",
        "duration_ms": "Duration (ms)",
    })

    st.dataframe(
        frame,
        use_container_width=True,
        hide_index=True,
        key=key,
    )


def event_detail(event_id):
    data = get(f"/events/{event_id}")

    if not data:
        st.warning("Event details could not be loaded.")
        return

    event = data["event"]

    a, b, c = st.columns(3)

    a.metric("Delivery status", event["status"].title())
    b.metric("HTTP response", event["http_status"] or "—")
    c.metric(
        "Duration",
        f"{event['duration_ms']} ms"
        if event["duration_ms"] is not None else "—",
    )

    st.markdown("### Event information")

    details = {
        "Event ID": event["id"],
        "Type": event["event_type"],
        "Source": event["source"],
        "Destination": event["destination"],
        "Order ID": event["order_id"],
        "Created": event["created_at"],
        "Scenario": event["scenario"],
    }

    st.json(details)

    left, right = st.columns(2)

    with left:
        st.markdown("#### Request payload")
        try:
            request = json.loads(event["request_payload"])
        except (TypeError, json.JSONDecodeError):
            request = event["request_payload"]

        st.code(
            json.dumps(request, indent=2)
            if isinstance(request, (dict, list))
            else str(request),
            language="json",
        )

    with right:
        st.markdown("#### Response payload")
        try:
            response = json.loads(event["response_payload"] or "{}")
        except (TypeError, json.JSONDecodeError):
            response = event["response_payload"]

        st.code(
            json.dumps(response, indent=2)
            if isinstance(response, (dict, list))
            else str(response),
            language="json",
        )

    st.markdown("### Delivery attempts")

    if data.get("attempts"):
        st.dataframe(
            pd.DataFrame(data["attempts"]),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.caption("No delivery attempts recorded.")