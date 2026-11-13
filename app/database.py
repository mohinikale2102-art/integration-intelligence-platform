
import sqlite3
from contextlib import contextmanager

from app.config import DB_PATH


SCHEMA = """
CREATE TABLE IF NOT EXISTS integrations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    system_type TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT NOT NULL,
    payment_id TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    order_id TEXT,
    status TEXT NOT NULL,
    scenario TEXT NOT NULL,
    request_payload TEXT NOT NULL,
    response_payload TEXT,
    http_status INTEGER,
    duration_ms INTEGER,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL,
    attempt_number INTEGER NOT NULL,
    status TEXT NOT NULL,
    http_status INTEGER,
    request_payload TEXT NOT NULL,
    response_payload TEXT,
    duration_ms INTEGER,
    created_at TEXT NOT NULL,
    FOREIGN KEY(event_id) REFERENCES events(id)
);

CREATE TABLE IF NOT EXISTS investigations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL,
    summary TEXT NOT NULL,
    evidence TEXT NOT NULL,
    likely_cause TEXT NOT NULL,
    recommendations TEXT NOT NULL,
    provider TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(event_id) REFERENCES events(id)
);

CREATE TABLE IF NOT EXISTS processed_events (
    event_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    processed_at TEXT NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id)
);
"""


@contextmanager
def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    db = sqlite3.connect(DB_PATH, timeout=15)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")

    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def initialize():
    with connect() as db:
        db.executescript(SCHEMA)
