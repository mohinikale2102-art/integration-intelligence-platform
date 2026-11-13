
import pandas as pd
import plotly.express as px
import streamlit as st

from frontend.api import get
from frontend.styles import header


def render():
    header(
        "Reports",
        "Understand delivery performance and recurring integration failures.",
    )

    data = get("/reports")

    if not data:
        st.error("Unable to load report data.")
        return

    metrics = data["metrics"]

    # Performance overview
    a, b, c, d = st.columns(4)

    a.metric("Total events", f"{metrics['total']:,}")
    b.metric("Success rate", f"{metrics['success_rate']}%")
    c.metric("Failed events", f"{metrics['failed']:,}")
    d.metric("Average duration", f"{metrics['average_ms']} ms")

    st.markdown("")

    if not data["events"]:
        st.info("Reports will populate as simulated events are generated.")
        return

    frame = pd.DataFrame(data["events"])

    # Delivery outcomes
    st.markdown("### Delivery outcomes")
    st.caption("Distribution of successful and failed webhook deliveries.")

    counts = (
        frame["status"]
        .value_counts()
        .rename_axis("status")
        .reset_index(name="events")
    )

    chart = px.bar(
        counts,
        x="status",
        y="events",
        color="status",
        color_discrete_map={
            "success": "#12A89D",
            "failed": "#DC6464",
        },
        text="events",
        labels={
            "status": "Delivery status",
            "events": "Number of events",
        },
    )

    chart.update_traces(
        textposition="outside",
        marker_line_width=0,
        cliponaxis=False,
    )

    chart.update_layout(
        height=320,
        autosize=True,
        showlegend=False,
        margin=dict(l=35, r=25, t=25, b=45),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, sans-serif",
            color="#718096",
            size=12,
        ),
        xaxis=dict(
            title=None,
            showgrid=False,
            tickfont=dict(size=12),
        ),
        yaxis=dict(
            title="Events",
            rangemode="tozero",
            gridcolor="#E9EEF4",
            zeroline=False,
        ),
    )

    with st.container(border=True):
        st.plotly_chart(
            chart,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
            },
        )

    # Event data export
    st.markdown("### Export report")
    st.caption(
        "Download the recorded integration events for further analysis."
    )

    csv_data = frame.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download event data (CSV)",
        data=csv_data,
        file_name="integration-events.csv",
        mime="text/csv",
        type="primary",
    )
