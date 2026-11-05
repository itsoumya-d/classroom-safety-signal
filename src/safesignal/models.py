from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ActivityEvent:
    event_id: str
    student_id: str
    class_id: str
    device_id: str
    url: str
    title: str
    text_excerpt: str
    occurred_at: datetime


@dataclass
class Alert:
    alert_id: str
    event_id: str
    student_id: str
    class_id: str
    category: str
    severity: str
    action: str
    reason: str
    occurred_at: datetime
    reviewer_required: bool = True
    status: str = "open"


@dataclass
class Digest:
    class_id: str
    day: str
    total_events: int
    alerts_by_category: dict[str, int] = field(default_factory=dict)
    alerts_by_severity: dict[str, int] = field(default_factory=dict)
