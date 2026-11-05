from __future__ import annotations

import re
from urllib.parse import urlparse

from safesignal.models import ActivityEvent

ALLOWLIST = {
    "classroom.google.com", "docs.google.com", "drive.google.com", "slides.google.com",
    "khanacademy.org", "wikipedia.org", "desmos.com", "scratch.mit.edu", "google.com",
}
RULES = [
    ("self_harm", "critical", re.compile(r"\b(kill myself|suicide|self[- ]?harm|want to die|end my life)\b", re.I)),
    ("violence", "high", re.compile(r"\b(shoot|bomb|weapon|stab|fight you|beat you up)\b", re.I)),
    ("bullying", "high", re.compile(r"\b(kill you|hate you|you are ugly|nobody likes you|loser)\b", re.I)),
    ("drugs", "medium", re.compile(r"\b(weed|vape|drugs|meth|cocaine)\b", re.I)),
    ("off_task", "low", re.compile(r"\b(roblox|tiktok|netflix|fortnite|minecraft|youtube)\b", re.I)),
]


def domain(url: str) -> str:
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def is_allowlisted(url: str) -> bool:
    host = domain(url)
    return any(host == d or host.endswith("." + d) for d in ALLOWLIST)


def classify_event(event: ActivityEvent) -> tuple[str, str, str]:
    blob = f"{event.title} {event.text_excerpt} {event.url}"
    for category, severity, pattern in RULES:
        match = pattern.search(blob)
        if match:
            if category == "off_task" and is_allowlisted(event.url):
                return "neutral", "none", "off_task suppressed on allowlisted learning domain"
            return category, severity, f"matched:{match.group(0).lower()}"
    return "neutral", "none", "no_rule_matched"
