#!/usr/bin/env python3
"""Generate the README paper table from docs/data/papers.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "docs" / "data" / "papers.json"
README_FILE = ROOT / "README.md"
START = "<!-- PAPERS_TABLE_START -->"
END = "<!-- PAPERS_TABLE_END -->"
STATUS = {"planned": "To Read", "reading": "Reading", "read": "Read"}


def clean(value: object) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ").strip()


def make_link(label: str, url: str) -> str:
    return f"[{label}]({url})" if url else "—"


def build_table(papers: list[dict]) -> str:
    lines = [
        "| Paper | Year / Venue | Category | Method | Key Idea | Resources | Reading Notes | Status |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for paper in sorted(papers, key=lambda item: (-int(item["year"]), item["title"].lower())):
        resources = [make_link("Paper", paper.get("paper_url", ""))]
        if paper.get("code_url"):
            resources.append(make_link("Code", paper["code_url"]))
        if paper.get("data_url"):
            resources.append(make_link("Data", paper["data_url"]))
        notes_url = paper.get("notes_url", "")
        notes_link = make_link("Notes", f"https://liulp0917.github.io/PaperLibrary/{notes_url}") if notes_url else "—"
        status = STATUS.get(paper.get("status", ""), clean(paper.get("status", "")))
        if paper.get("discussed") is True:
            status = f"{status} · Discussed"
        lines.append(
            "| {paper} | {year} / {venue} | {category} | {method} | {summary} | {resources} | {notes} | {status} |".format(
                paper=make_link(clean(paper["title"]), paper.get("paper_url", "")),
                year=clean(paper["year"]), venue=clean(paper["venue"]), category=clean(paper["category"]),
                method=clean(paper["method"]), summary=clean(paper["summary"]), resources=" · ".join(resources),
                notes=notes_link, status=status,
            )
        )
    return "\n".join(lines)


def main() -> None:
    papers = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    readme = README_FILE.read_text(encoding="utf-8")
    before, remainder = readme.split(START, 1)
    _, after = remainder.split(END, 1)
    generated = f"{before}{START}\n\n{build_table(papers)}\n\n{END}{after}"
    README_FILE.write_text(generated, encoding="utf-8", newline="\n")
    print(f"Updated {README_FILE} with {len(papers)} paper(s).")


if __name__ == "__main__":
    main()

