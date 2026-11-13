import streamlit as st
from frontend.api import post
from frontend.styles import header

SCENARIOS = {
    "Successful delivery": "success",
    "Missing required order_id": "missing_order_id",
    "Invalid authentication": "invalid_auth",
    "Receiver timeout": "timeout",
    "Duplicate delivery": "duplicate",
    "Payment declined": "payment_declined",
}

def render():
    header("Demo Simulator", "Create fictional business events and reproduce integration scenarios.")
    st.info("This simulator does not connect to a real payment provider and does not move money.")
    with st.form("order-simulator"):
        customer = st.text_input("Customer name", "Mohini Kale")
        amount = st.number_input("Order amount (₹)", min_value=1.0, value=2500.0, step=100.0)
        scenario = st.selectbox("Scenario", list(SCENARIOS))
        submitted = st.form_submit_button("Create order and run integration", type="primary")
    if submitted:
        result = post("/simulate/order", json={"customer_name": customer, "amount": amount,
                                               "scenario": SCENARIOS[scenario]})
        if result:
            st.success(f"Order created: {result['order_id']}")
            st.write({"Payment reference": result["payment_id"], "Payment result": result["payment"]})
            event = result.get("event")
            if event:
                if event["status"] == "success":
                    st.success(f"Webhook delivered · {event['id']} · HTTP {event['http_status']}")
                else:
                    st.error(f"Webhook failed · {event['id']} · HTTP {event['http_status']}")
                st.session_state["last_event"] = event["id"]
                if st.button("Open this event"):
                    st.session_state["selected_event"] = event["id"]
                    st.session_state["active_page"] = "Events"
                    st.rerun()
            else:
                st.warning("Payment was declined. No payment webhook was sent.")
