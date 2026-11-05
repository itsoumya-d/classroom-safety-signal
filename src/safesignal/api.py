from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

from safesignal.models import ActivityEvent
from safesignal.pipeline import SafetyPipeline

app = FastAPI(title="Classroom safety signal", version="0.1.0")
pipeline = SafetyPipeline()


class EventIn(BaseModel):
    event_id: str
    student_id: str
    class_id: str
    device_id: str = ""
    url: str = ""
    title: str = ""
    text_excerpt: str = ""
    occurred_at: str


def parse(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest")
def ingest(events: list[EventIn]) -> dict[str, object]:
    parsed = [ActivityEvent(e.event_id, e.student_id, e.class_id, e.device_id, e.url, e.title, e.text_excerpt, parse(e.occurred_at)) for e in events]
    new_alerts, digests = pipeline.ingest(parsed)
    return {
        "alerts": [a.__dict__ | {"occurred_at": a.occurred_at.isoformat()} for a in new_alerts],
        "digests": [d.__dict__ for d in digests],
        "audit": pipeline.audit[-len(parsed):],
    }


@app.get("/alerts")
def alerts() -> list[dict]:
    return [a.__dict__ | {"occurred_at": a.occurred_at.isoformat()} for a in pipeline.alerts]


@app.get("/digest/{class_id}")
def digest(class_id: str) -> list[dict]:
    return [d.__dict__ for d in pipeline.digests() if d.class_id == class_id]
