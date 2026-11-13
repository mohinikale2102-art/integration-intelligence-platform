from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.database import initialize
from app import repository as repo
from app.services.simulator import seed, create_order, retry_event
from app.services.investigation import investigate

@asynccontextmanager
async def lifespan(app):
    initialize()
    seed()
    yield

app = FastAPI(title="Integration Intelligence API", version="1.0.0", lifespan=lifespan)

class OrderRequest(BaseModel):
    customer_name: str = Field(min_length=2, max_length=80)
    amount: float = Field(gt=0, le=1_000_000)
    scenario: str = "success"

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/dashboard")
def dashboard():
    return {"metrics": repo.metrics(), "trend": repo.trend(),
            "recent_events": repo.events(limit=8), "open_incidents": repo.incidents()[:5]}

@app.get("/integrations")
def integrations():
    return repo.integrations()

@app.get("/events")
def events(status: str | None = None, search: str | None = None, limit: int = 300):
    return repo.events(min(max(limit, 1), 500), status, search)

@app.get("/events/{event_id}")
def event_detail(event_id: str):
    item = repo.event(event_id)
    if not item:
        raise HTTPException(404, "Event not found.")
    return {"event": item, "attempts": repo.attempts(event_id),
            "investigation": repo.investigation(event_id)}

@app.get("/incidents")
def incidents():
    return repo.incidents()

@app.get("/investigations")
def investigations():
    return repo.investigations()

@app.get("/reports")
def reports():
    return {"metrics": repo.metrics(), "trend": repo.trend(), "events": repo.events(limit=500)}

@app.post("/simulate/order")
def simulate(request: OrderRequest):
    allowed = {"success", "missing_order_id", "invalid_auth", "timeout", "duplicate", "payment_declined"}
    if request.scenario not in allowed:
        raise HTTPException(400, f"Choose one of: {', '.join(sorted(allowed))}")
    try:
        return create_order(request.customer_name, request.amount, request.scenario)
    except ValueError as exc:
        raise HTTPException(422, str(exc))

@app.post("/events/{event_id}/investigate")
def event_investigation(event_id: str):
    item = repo.event(event_id)
    if not item:
        raise HTTPException(404, "Event not found.")
    if item["status"] != "failed":
        raise HTTPException(400, "Only failed events can be investigated.")
    return investigate(item)

@app.post("/events/{event_id}/retry")
def retry(event_id: str):
    try:
        return retry_event(event_id)
    except LookupError as exc:
        raise HTTPException(404, str(exc))
    except ValueError as exc:
        raise HTTPException(400, str(exc))
