import pandas as pd
import plotly.express as px
import streamlit as st

from frontend.api import get
from frontend.components import event_table, status_badge
from frontend.styles import header


def render():
    header(
        "Overview",
        "Real-time visibility into your integration ecosystem.",
    )

    data = get("/dashboard")

    if not data:
        st.error("Unable to load dashboard information.")
        return

    metrics = data["metrics"]

    st.markdown("### Platform overview")

    cards = st.columns(4)

    cards[0].metric(
        "Total events",
        f"{metrics['total']:,}",
    )

    cards[1].metric(
        "Successful deliveries",
        f"{metrics['successful']:,}",
        f"{metrics['success_rate']}% success rate",
    )

    cards[2].metric(
        "Failed deliveries",
        f"{metrics['failed']:,}",
    )

    cards[3].metric(
        "Average delivery time",
        f"{metrics['average_ms']} ms",
    )

    st.markdown("")

    left, right = st.columns([1.65, 1])

    with left:
        with st.container(border=True):
            st.markdown("### Integration health over time")

            if data["trend"]:
                frame = pd.DataFrame(data["trend"])

                chart = px.line(
                    frame,
                    x="hour",
                    y=["total", "successful", "failed"],
                    color_discrete_sequence=[
                        "#12A89D",
                        "#168B72",
                        "#DC6464",
                    ],
                    labels={
                        "value": "Events",
                        "hour": "Time",
                        "variable": "Outcome",
                    },
                )

                chart.update_layout(
                    height=310,
                    margin=dict(l=10, r=10, t=20, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(
                        family="Inter, sans-serif",
                        color="#718096",
                        size=11,
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1,
                    ),
                    xaxis=dict(
                        showgrid=False,
                        title=None,
                    ),
                    yaxis=dict(
                        gridcolor="#EDF0F4",
                        title=None,
                    ),
                )

                st.plotly_chart(
                    chart,
                    use_container_width=True,
                )
            else:
                st.info(
                    "Event trends will appear after you run your first simulation."
                )

    with right:
        with st.container(border=True):
            st.markdown("### Connected systems")

            integrations = get("/integrations") or []

            if integrations:
                for item in integrations:
                    st.markdown(
                        f"""
                        <div class="system-row">
                            <span class="system-name">{item['name']}</span>
                            {status_badge(item['status'])}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No integrations available.")

        with st.container(border=True):
            st.markdown("### Open incidents")

            incidents = data.get("open_incidents", [])

            if incidents:
                for item in incidents:
                    st.markdown(
                        f"""
                        <div class="info-card">
                            <div class="info-card-title">
                                Incident {item['id']}
                            </div>
                            <div class="info-card-description">
                                HTTP {item['http_status']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.success("No open incidents.")

    st.markdown("")

    with st.container(border=True):
        st.markdown("### Recent integration events")
        st.caption("Latest activity recorded across connected systems.")

        event_table(
            data.get("recent_events", []),
            "dashboard-events",
        )