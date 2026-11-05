from datetime import datetime, timedelta, timezone

from safesignal.classify import classify_event, is_allowlisted
from safesignal.models import ActivityEvent
from safesignal.pipeline import SafetyPipeline
from safesignal.routing import route_alert


def event(**kwargs):
    base = dict(event_id="E1", student_id="S1", class_id="C1", device_id="D1",
                url="https://example.com", title="", text_excerpt="",
                occurred_at=datetime(2026, 11, 5, 9, 0, tzinfo=timezone.utc))
    base.update(kwargs)
    return ActivityEvent(**base)


def test_classification_and_allowlist():
    assert classify_event(event(text_excerpt="I want to die"))[0] == "self_harm"
    assert classify_event(event(text_excerpt="I will beat you up"))[0] == "violence"
    assert classify_event(event(url="https://docs.google.com/document/1", title="YouTube lesson"))[0] == "neutral"
    assert is_allowlisted("https://classroom.google.com/c/1")


def test_routing():
    assert route_alert("self_harm", "critical") == "wellness_review"
    assert route_alert("off_task", "low") == "teacher_nudge"
    assert route_alert("neutral", "none") == "none"


def test_dedupe_and_digest():
    pipeline = SafetyPipeline(dedupe_minutes=10)
    alerts, digests = pipeline.ingest([
        event(event_id="E1", text_excerpt="I want to die"),
        event(event_id="E2", text_excerpt="I want to die", occurred_at=datetime(2026, 11, 5, 9, 5, tzinfo=timezone.utc)),
        event(event_id="E3", text_excerpt="I will beat you up", student_id="S2"),
    ])
    assert len(alerts) == 2
    assert len(digests) == 1
    assert digests[0].alerts_by_category == {"self_harm": 1, "violence": 1}
    assert any(a["action"] == "deduped" for a in pipeline.audit)


def test_allowlisted_off_task_is_suppressed():
    pipeline = SafetyPipeline()
    alerts, _ = pipeline.ingest([event(url="https://classroom.google.com/c/1", title="YouTube lesson")])
    assert alerts == []
