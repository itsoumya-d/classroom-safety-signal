from __future__ import annotations

import hashlib
from collections import Counter, defaultdict
from datetime import timedelta

from safesignal.classify import classify_event
from safesignal.models import ActivityEvent, Alert, Digest
from safesignal.routing import reviewer_required, route_alert


class SafetyPipeline:
    def __init__(self, dedupe_minutes: int = 10) -> None:
        self.dedupe_window = timedelta(minutes=dedupe_minutes)
        self.alerts: list[Alert] = []
        self.audit: list[dict] = []
        self._last_alert: dict[tuple[str, str], object] = {}

    def ingest(self, events: list[ActivityEvent]) -> tuple[list[Alert], list[Digest]]:
        new_alerts: list[Alert] = []
        for event in events:
            category, severity, reason = classify_event(event)
            action = route_alert(category, severity)
            if action == "none":
                self.audit.append({"event_id": event.event_id, "action": "no_alert", "reason": reason})
                continue
            key = (event.student_id, category)
            previous = self._last_alert.get(key)
            if previous and event.occurred_at - previous <= self.dedupe_window:
                self.audit.append({"event_id": event.event_id, "action": "deduped", "reason": f"duplicate {category} within window"})
                continue
            self._last_alert[key] = event.occurred_at
            alert_id = "AL-" + hashlib.sha256(f"{event.event_id}|{category}".encode()).hexdigest()[:12]
            alert = Alert(alert_id, event.event_id, event.student_id, event.class_id, category, severity, action, reason,
                          event.occurred_at, reviewer_required(action))
            self.alerts.append(alert)
            new_alerts.append(alert)
            self.audit.append({"event_id": event.event_id, "alert_id": alert_id, "action": action, "reason": reason})
        return new_alerts, self.digests()

    def digests(self) -> list[Digest]:
        by_class_day: dict[tuple[str, str], list[Alert]] = defaultdict(list)
        for alert in self.alerts:
            by_class_day[(alert.class_id, alert.occurred_at.date().isoformat())].append(alert)
        out = []
        for (class_id, day), alerts in sorted(by_class_day.items()):
            out.append(Digest(
                class_id=class_id,
                day=day,
                total_events=len(alerts),
                alerts_by_category=dict(Counter(a.category for a in alerts)),
                alerts_by_severity=dict(Counter(a.severity for a in alerts)),
            ))
        return out
