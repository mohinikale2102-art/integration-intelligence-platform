import json
from app.database import connect

def all_rows(sql, params=()):
    with connect() as db:
        return [dict(r) for r in db.execute(sql, params).fetchall()]

def one(sql, params=()):
    result = all_rows(sql, params)
    return result[0] if result else None

def insert_event(e):
    with connect() as db:
        db.execute("""INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            e["id"], e["event_type"], e["source"], e["destination"], e.get("order_id"),
            e["status"], e["scenario"], json.dumps(e["request_payload"]),
            json.dumps(e["response_payload"]), e["http_status"], e["duration_ms"],
            e["created_at"], e["updated_at"]))

def add_attempt(event_id, number, status, code, request, response, duration, stamp):
    with connect() as db:
        db.execute("""INSERT INTO attempts
        (event_id,attempt_number,status,http_status,request_payload,response_payload,duration_ms,created_at)
        VALUES(?,?,?,?,?,?,?,?)""",
        (event_id, number, status, code, json.dumps(request), json.dumps(response), duration, stamp))

def events(limit=300, status=None, search=None):
    sql, params = "SELECT * FROM events WHERE 1=1", []
    if status and status != "All":
        sql += " AND status=?"
        params.append(status.lower())
    if search:
        sql += " AND (id LIKE ? OR event_type LIKE ? OR order_id LIKE ?)"
        params.extend([f"%{search}%"] * 3)
    return all_rows(sql + " ORDER BY created_at DESC LIMIT ?", (*params, limit))

def event(event_id):
    return one("SELECT * FROM events WHERE id=?", (event_id,))

def attempts(event_id):
    return all_rows("SELECT * FROM attempts WHERE event_id=? ORDER BY attempt_number", (event_id,))

def integrations():
    return all_rows("SELECT * FROM integrations ORDER BY name")

def incidents():
    return all_rows("SELECT * FROM events WHERE status='failed' ORDER BY created_at DESC")

def investigation(event_id):
    return one("SELECT * FROM investigations WHERE event_id=? ORDER BY id DESC LIMIT 1", (event_id,))

def investigations():
    return all_rows("SELECT * FROM investigations ORDER BY id DESC LIMIT 100")

def save_investigation(event_id, summary, evidence, cause, steps, provider, stamp):
    with connect() as db:
        db.execute("""INSERT INTO investigations
        (event_id,summary,evidence,likely_cause,recommendations,provider,created_at)
        VALUES(?,?,?,?,?,?,?)""",
        (event_id, summary, json.dumps(evidence), cause, json.dumps(steps), provider, stamp))

def update_event(event_id, status, request, response, code, duration, stamp):
    with connect() as db:
        db.execute("""UPDATE events SET status=?,request_payload=?,response_payload=?,
        http_status=?,duration_ms=?,updated_at=? WHERE id=?""",
        (status, json.dumps(request), json.dumps(response), code, duration, stamp, event_id))

def metrics():
    with connect() as db:
        total = db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        ok = db.execute("SELECT COUNT(*) FROM events WHERE status='success'").fetchone()[0]
        failed = db.execute("SELECT COUNT(*) FROM events WHERE status='failed'").fetchone()[0]
        avg = db.execute("SELECT COALESCE(AVG(duration_ms),0) FROM events").fetchone()[0]
    return {"total": total, "successful": ok, "failed": failed,
            "success_rate": round(ok * 100 / total, 1) if total else 100.0,
            "average_ms": round(avg, 1)}

def trend():
    return all_rows("""SELECT substr(created_at,1,13) AS hour, COUNT(*) AS total,
    SUM(status='success') AS successful, SUM(status='failed') AS failed
    FROM events GROUP BY hour ORDER BY hour""")
