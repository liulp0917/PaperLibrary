#!/usr/bin/env python3
"""Validate paper metadata and local note paths."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "docs" / "data" / "papers.json"
REQUIRED = {"id", "title", "authors", "year", "venue", "category", "method", "summary", "paper_url", "notes_url", "status", "discussed", "tags"}
STATUSES = {"planned", "reading", "read"}


def is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> int:
    errors: list[str] = []
    papers = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    ids: set[str] = set()

    if not isinstance(papers, list):
        errors.append("papers.json must contain a JSON array")
        papers = []

    for index, paper in enumerate(papers, start=1):
        label = paper.get("id", f"row {index}")
        missing = REQUIRED - paper.keys()
        if missing:
            errors.append(f"{label}: missing fields {sorted(missing)}")
        if label in ids:
            errors.append(f"{label}: duplicate id")
        ids.add(label)
        if paper.get("status") not in STATUSES:
            errors.append(f"{label}: invalid status {paper.get('status')!r}")
        if not isinstance(paper.get("discussed"), bool):
            errors.append(f"{label}: discussed must be true or false")
        if not is_http_url(paper.get("paper_url", "")):
            errors.append(f"{label}: paper_url must be an http(s) URL")
        for key in ("code_url", "data_url"):
            if paper.get(key) and not is_http_url(paper[key]):
                errors.append(f"{label}: {key} must be an http(s) URL")
        note_url = paper.get("notes_url", "")
        if note_url:
            note_file = ROOT / "docs" / note_url / "index.html"
            if not note_file.is_file():
                errors.append(f"{label}: missing note file {note_file.relative_to(ROOT)}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Validation passed: {len(papers)} paper(s), {len(ids)} unique id(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

