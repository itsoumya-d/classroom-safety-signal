# classroom-safety-signal

[![ci](https://github.com/itsoumya-d/classroom-safety-signal/actions/workflows/ci.yml/badge.svg)](https://github.com/itsoumya-d/classroom-safety-signal/actions/workflows/ci.yml)

A privacy-first reference for K-12 classroom safety signals:

- Browser/device activity events (synthetic; Google Workspace/Chrome/Edge-shaped).
- Risk classification for self-harm, violence, bullying, drugs and off-task
  behaviour.
- Allowlisted learning domains suppress off-task noise while still surfacing
  safety risks.
- Human-in-the-loop routing to wellness, safeguarding, teacher review or a
  teacher nudge.
- Deduplication within a time window.
- Audit entries and class/day digests without raw student excerpts.

This is a **reference implementation**, not a claim of production classroom
monitoring or child-safety experience. There is no live Chrome/Edge extension,
Google Workspace API or student data in CI. The policy is "protect, not
police": every alert requires a human reviewer.

## Run

```bash
uv venv --python 3.12
source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn safesignal.api:app --reload
python -m safesignal.generate
```

## License

MIT
