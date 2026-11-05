from __future__ import annotations


def route_alert(category: str, severity: str) -> str:
    if severity == "none" or category == "neutral":
        return "none"
    if category == "self_harm":
        return "wellness_review"
    if category in {"violence", "bullying"}:
        return "wellness_and_safeguarding_review"
    if category == "drugs":
        return "teacher_review"
    if category == "off_task":
        return "teacher_nudge"
    return "teacher_review"


def reviewer_required(action: str) -> bool:
    return action != "none"
