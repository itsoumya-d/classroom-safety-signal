from __future__ import annotations

import json
from pathlib import Path


def demo() -> list[dict]:
    return [
        {"event_id": "E1", "student_id": "S1", "class_id": "C1", "device_id": "D1", "url": "https://www.youtube.com/watch?v=1", "title": "Fortnite highlights", "text_excerpt": "", "occurred_at": "2026-11-05T09:00:00+00:00"},
        {"event_id": "E2", "student_id": "S1", "class_id": "C1", "device_id": "D1", "url": "https://docs.google.com/document/d/1", "title": "Science report", "text_excerpt": "I want to die", "occurred_at": "2026-11-05T09:05:00+00:00"},
        {"event_id": "E3", "student_id": "S2", "class_id": "C1", "device_id": "D2", "url": "https://classroom.google.com/c/1", "title": "YouTube video lesson", "text_excerpt": "", "occurred_at": "2026-11-05T09:06:00+00:00"},
        {"event_id": "E4", "student_id": "S2", "class_id": "C1", "device_id": "D2", "url": "https://chat.example.com", "title": "Chat", "text_excerpt": "I will beat you up", "occurred_at": "2026-11-05T09:07:00+00:00"},
        {"event_id": "E5", "student_id": "S1", "class_id": "C1", "device_id": "D1", "url": "https://docs.google.com/document/d/1", "title": "Science report", "text_excerpt": "I want to die", "occurred_at": "2026-11-05T09:08:00+00:00"},
    ]


def main() -> None:
    path = Path("data/demo.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(demo(), indent=2))
    print(path)


if __name__ == "__main__":
    main()
