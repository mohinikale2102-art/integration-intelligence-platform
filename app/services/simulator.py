import json
import random
import time
import uuid
from datetime import datetime, timezone

from app.database import connect
from app import repository as repo

SYSTEMS = {
    "store": "ShopEase Online Store",
    "payment": "Payment Gateway Simulator",
    "oms": "Order Management System",
}

def timestamp():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

def seed():
    with connect() as db:
        if db.execute("SELECT COUNT(*) FROM integrations").fetchone()[0]:
            return
        stamp = timestamp()
        db.executemany("INSERT INTO integrations VALUES(?,?,?,?,?,?)", [
            ("INT-STORE", SYSTEMS["store"], "ecommerce", "Creates customer orders", "healthy", stamp),
            ("INT-PAY", SYSTEMS["payment"], "payments", "Processes simulated payments", "healthy", stamp),
            ("INT-OMS", SYSTEMS["oms"], "order_management", "Receives order notifications", "healthy", stamp),
        ])

def receive(payload, scenario):
    if scenario == "timeout":
        return {"error": "Receiver did not respond within the allowed time."}, 504
    if scenario == "invalid_auth":
        return {"error": "Authentication failed."}, 401
    missing = [key for key in ("payment_id", "order_id", "status") if not payload.get(key)]
    if missing:
        return {"error": "Required fields are missing.", "missing_fields": missing}, 400
    return {"status": "accepted", "order_id": payload["order_id"]}, 200

def create_order(customer, amount, scenario):
    if amount <= 0:
        raise ValueError("Order amount must be greater than zero.")
    order_id = "ORD-" + uuid.uuid4().hex[:8].upper()
    payment_id = "PAY-" + uuid.uuid4().hex[:8].upper()
    stamp = timestamp()
    payment_status = "declined" if scenario == "payment_declined" else "success"
    with connect() as db:
        db.execute("INSERT INTO orders VALUES(?,?,?,?,?,?)",
                   (order_id, customer, amount, "payment_failed" if payment_status == "declined" else "paid",
                    payment_id, stamp))
    if payment_status == "declined":
        return {"order_id": order_id, "payment_id": payment_id,
                "payment": {"status": "declined", "amount": amount}, "event": None}

    payload = {"payment_id": payment_id, "order_id": order_id,
               "status": "success", "amount": amount, "customer": customer}
    if scenario == "missing_order_id":
        payload.pop("order_id")
    started = time.perf_counter()
    response, code = receive(payload, scenario)
    duration = round((time.perf_counter() - started) * 1000 + random.randint(25, 85))
    status = "success" if code == 200 else "failed"
    event_id = "EVT-" + uuid.uuid4().hex[:8].upper()
    event = {"id": event_id, "event_type": "payment.succeeded",
             "source": SYSTEMS["payment"], "destination": SYSTEMS["oms"],
             "order_id": order_id, "status": status, "scenario": scenario,
             "request_payload": payload, "response_payload": response,
             "http_status": code, "duration_ms": duration,
             "created_at": stamp, "updated_at": stamp}
    repo.insert_event(event)
    repo.add_attempt(event_id, 1, status, code, payload, response, duration, stamp)
    if scenario == "duplicate" and code == 200:
        duplicate = {"status": "duplicate_ignored", "message": "Event already processed."}
        repo.add_attempt(event_id, 2, "success", 200, payload, duplicate, 22, timestamp())
    if status == "success":
        with connect() as db:
            db.execute("UPDATE orders SET status='confirmed' WHERE id=?", (order_id,))
    return {"order_id": order_id, "payment_id": payment_id,
            "payment": {"status": "success", "amount": amount}, "event": repo.event(event_id)}

def retry_event(event_id):
    current = repo.event(event_id)
    if not current:
        raise LookupError("Event not found.")
    if current["status"] != "failed":
        raise ValueError("Only failed events can be retried.")
    payload = json.loads(current["request_payload"])
    payload["order_id"] = current["order_id"]
    response, code = receive(payload, "success")
    stamp = timestamp()
    duration = random.randint(35, 110)
    status = "success" if code == 200 else "failed"
    repo.add_attempt(event_id, len(repo.attempts(event_id)) + 1, status, code,
                     payload, response, duration, stamp)
    repo.update_event(event_id, status, payload, response, code, duration, stamp)
    if status == "success":
        with connect() as db:
            db.execute("UPDATE orders SET status='confirmed' WHERE id=?", (current["order_id"],))
    return repo.event(event_id)
