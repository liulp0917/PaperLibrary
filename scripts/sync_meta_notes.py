#!/usr/bin/env python3
"""Archive selected Meta reading notes and publish them as PaperLibrary HTML notes."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT.parent.parent / "Meta" / "docs" / "literature-reading-notes"
DATA_FILE = ROOT / "docs" / "data" / "papers.json"
ARCHIVE_DIR = ROOT / "sources" / "meta-notes"


PAPERS = [
    {
        "source": "02-twinmarket.md",
        "id": "twinmarket",
        "title": "TwinMarket: A Scalable Behavioral and Social Simulation for Financial Markets",
        "authors": ["Yuzhe Yang", "Yifei Zhang", "Minghao Wu", "Kaidi Zhang", "Yunmiao Zhang", "Honghai Yu", "Yan Hu", "Benyou Wang"],
        "year": 2025,
        "venue": "NeurIPS",
        "category": "Multi-Agent Finance",
        "method": "Behavioral Market Simulation",
        "summary": "以 BDI 认知、异质交易者和动态社交网络模拟金融市场中的群体行为与宏观涌现。",
        "paper_url": "https://proceedings.neurips.cc/paper_files/paper/2025/hash/5bf234ecf83cd77bc5b77a24ba9338b0-Abstract-Conference.html",
        "doi": "10.52202/085713-2132",
        "arxiv_id": "2502.01506",
        "tags": ["LLM Agents", "Financial Markets", "Social Simulation", "BDI"],
    },
    {
        "source": "07-agent-specific-effects.md",
        "id": "agent-specific-effects",
        "title": "Agent-Specific Effects: A Causal Effect Propagation Analysis in Multi-Agent MDPs",
        "authors": ["Stelios Triantafyllou", "Aleksa Sukovic", "Debmalya Mandal", "Goran Radanovic"],
        "year": 2024,
        "venue": "ICML",
        "category": "Causal Multi-Agent Systems",
        "method": "Causal Effect Attribution",
        "summary": "定义多智能体 MDP 中经由其他代理反应传播的路径特定因果效应及其识别条件。",
        "paper_url": "https://proceedings.mlr.press/v235/triantafyllou24a.html",
        "doi": "",
        "arxiv_id": "2310.11334",
        "tags": ["Multi-Agent Systems", "Causal Inference", "MDP", "Counterfactuals"],
    },
    {
        "source": "08-network-interference.md",
        "id": "network-interference-policy",
        "title": "Causal Inference under Networked Interference and Intervention Policy Enhancement",
        "authors": ["Yunpu Ma", "Volker Tresp"],
        "year": 2021,
        "venue": "AISTATS",
        "category": "Causal Inference",
        "method": "Graph Neural Causal Estimation",
        "summary": "在网络干扰下估计直接与溢出效应，并研究容量约束下的干预政策优化。",
        "paper_url": "https://proceedings.mlr.press/v130/ma21c.html",
        "doi": "",
        "arxiv_id": "",
        "tags": ["Network Interference", "Causal Inference", "GNN", "Policy Learning"],
    },
    {
        "source": "09-causal-games.md",
        "id": "causal-games-interventions",
        "title": "Characterising Interventions in Causal Games",
        "authors": ["Manuj Mishra", "James Fox", "Michael Wooldridge"],
        "year": 2024,
        "venue": "UAI",
        "category": "Causal Multi-Agent Systems",
        "method": "Causal Games",
        "summary": "刻画因果博弈中的干预原语、知情时序与策略重算，澄清多智能体反事实的语义。",
        "paper_url": "https://proceedings.mlr.press/v244/mishra24a.html",
        "doi": "",
        "arxiv_id": "2406.09318",
        "tags": ["Causal Games", "Interventions", "Game Theory", "Multi-Agent Systems"],
    },
    {
        "source": "10-g-sim.md",
        "id": "g-sim",
        "title": "G-Sim: Generative Simulations with Large Language Models and Gradient-Free Calibration",
        "authors": ["Samuel Holt", "Max Ruiz Luyten", "Antonin Berthon", "Mihaela van der Schaar"],
        "year": 2025,
        "venue": "ICML",
        "category": "Simulation & Calibration",
        "method": "LLM Simulator + Calibration",
        "summary": "让 LLM 提议模拟器结构，并以无梯度优化或模拟型推断校准参数和反馈修订结构。",
        "paper_url": "https://proceedings.mlr.press/v267/holt25b.html",
        "doi": "",
        "arxiv_id": "2506.09272",
        "tags": ["LLM", "Simulation", "Calibration", "Simulation-based Inference"],
    },
    {
        "source": "11-sbi-misspecification.md",
        "id": "rope-sbi-calibration",
        "title": "Addressing Misspecification in Simulation-based Inference through Data-driven Calibration",
        "authors": ["Antoine Wehenkel", "Juan L. Gamella", "Ozan Sener", "Jens Behrmann", "Guillermo Sapiro", "Joern-Henrik Jacobsen", "Marco Cuturi"],
        "year": 2025,
        "venue": "ICML",
        "category": "Simulation-based Inference",
        "method": "Optimal Transport Calibration",
        "summary": "用少量带真实参数标签的校准样本与最优传输修正错设模拟器下的 SBI 后验。",
        "paper_url": "https://proceedings.mlr.press/v267/wehenkel25a.html",
        "doi": "",
        "arxiv_id": "2405.08719",
        "tags": ["Simulation-based Inference", "Misspecification", "Optimal Transport", "Calibration"],
    },
    {
        "source": "12-agent-prediction-limits.md",
        "id": "limits-predicting-agents",
        "title": "The Limits of Predicting Agents from Behaviour",
        "authors": ["Alexis Bellot", "Jonathan Richens", "Tom Everitt"],
        "year": 2025,
        "venue": "ICML",
        "category": "Agent Modeling",
        "method": "Theoretical Analysis",
        "summary": "给出仅从历史行为预测代理在新干预或新制度中行动的理论边界与不可识别条件。",
        "paper_url": "https://proceedings.mlr.press/v267/bellot25a.html",
        "doi": "",
        "arxiv_id": "2506.02923",
        "tags": ["Agent Modeling", "Behavior Prediction", "Causal Models", "Identifiability"],
    },
    {
        "source": "13-complex-contagion.md",
        "id": "complex-contagion-network-experiment",
        "title": "The Spread of Behavior in an Online Social Network Experiment",
        "authors": ["Damon Centola"],
        "year": 2010,
        "venue": "Science",
        "category": "Social Networks",
        "method": "Randomized Network Experiment",
        "summary": "通过保持度数的网络拓扑随机实验检验聚类结构和多重社会强化对行为传播的影响。",
        "paper_url": "https://doi.org/10.1126/science.1185231",
        "doi": "10.1126/science.1185231",
        "arxiv_id": "",
        "tags": ["Complex Contagion", "Social Networks", "Randomized Experiment", "Diffusion"],
    },
    {
        "source": "14-musiclab.md",
        "id": "musiclab-social-influence",
        "title": "Experimental Study of Inequality and Unpredictability in an Artificial Cultural Market",
        "authors": ["Matthew J. Salganik", "Peter Sheridan Dodds", "Duncan J. Watts"],
        "year": 2006,
        "venue": "Science",
        "category": "Social Influence",
        "method": "Parallel-world Experiment",
        "summary": "以多个随机平行世界识别社会信息如何提高结果不平等，并放大成功的不可预测性。",
        "paper_url": "https://doi.org/10.1126/science.1121066",
        "doi": "10.1126/science.1121066",
        "arxiv_id": "",
        "tags": ["Social Influence", "Cultural Markets", "Parallel Worlds", "Experiment"],
    },
    {
        "source": "15-biodiversity-stability.md",
        "id": "biodiversity-ecosystem-stability",
        "title": "Biodiversity and Ecosystem Stability in a Decade-long Grassland Experiment",
        "authors": ["David Tilman", "Peter B. Reich", "Johannes M. H. Knops"],
        "year": 2006,
        "venue": "Nature",
        "category": "Complex Systems",
        "method": "Longitudinal Field Experiment",
        "summary": "利用十年草地随机实验分解多样性、物种波动与群落总体稳定性之间的关系。",
        "paper_url": "https://doi.org/10.1038/nature04742",
        "doi": "10.1038/nature04742",
        "arxiv_id": "",
        "tags": ["Biodiversity", "Stability", "Complex Systems", "Field Experiment"],
    },
]


def inline_markdown(value: str) -> str:
    placeholders: dict[str, str] = {}

    def keep(rendered: str) -> str:
        token = f"@@HTML{len(placeholders)}@@"
        placeholders[token] = rendered
        return token

    value = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        lambda match: keep(
            f'<a href="{html.escape(match.group(2), quote=True)}" target="_blank" rel="noreferrer">'
            f"{html.escape(match.group(1))}</a>"
        ),
        value,
    )
    value = re.sub(r"`([^`]+)`", lambda match: keep(f"<code>{html.escape(match.group(1))}</code>"), value)
    value = html.escape(value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", value)
    for token, rendered in placeholders.items():
        value = value.replace(token, rendered)
    return value


def blocks_to_html(lines: list[str]) -> str:
    output: list[str] = []
    paragraph: list[str] = []
    list_kind = ""

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_kind
        if list_kind:
            output.append(f"</{list_kind}>")
            list_kind = ""

    for raw_line in [*lines, ""]:
        line = raw_line.strip()
        ordered = re.match(r"^\d+\.\s+(.+)$", line)
        unordered = re.match(r"^-\s+(.+)$", line)
        if ordered or unordered:
            flush_paragraph()
            kind = "ol" if ordered else "ul"
            if list_kind != kind:
                close_list()
                output.append(f"<{kind}>")
                list_kind = kind
            match = ordered or unordered
            output.append(f"<li>{inline_markdown(match.group(1))}</li>")
        elif not line:
            flush_paragraph()
            close_list()
        else:
            close_list()
            paragraph.append(line)
    return "\n".join(output)


def parse_note(markdown: str) -> tuple[str, list[tuple[str, list[str]]]]:
    lines = markdown.splitlines()
    citation_lines: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    current_title = ""
    current_lines: list[str] = []

    for line in lines[1:]:
        if line.startswith("## "):
            if current_title:
                sections.append((current_title, current_lines))
            current_title = line[3:].strip()
            current_lines = []
        elif current_title:
            current_lines.append(line)
        elif line.strip():
            citation_lines.append(line)
    if current_title:
        sections.append((current_title, current_lines))
    return blocks_to_html(citation_lines), sections


def render_note(paper: dict, markdown: str) -> str:
    citation_html, sections = parse_note(markdown)
    toc = ['<a href="#bibliography">01 书目与版本</a>']
    section_html: list[str] = []
    for index, (title, lines) in enumerate(sections, start=2):
        section_id = f"section-{index}"
        toc.append(f'<a href="#{section_id}">{index:02d} {html.escape(title)}</a>')
        section_html.append(
            f'<section class="note-section" id="{section_id}">'
            f"<h2>{index:02d}. {html.escape(title)}</h2>{blocks_to_html(lines)}</section>"
        )

    authors = ", ".join(paper["authors"])
    return f"""<!doctype html>
<html lang="zh-CN" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(paper['title'], quote=True)} 阅读笔记。">
  <title>{html.escape(paper['title'])} · Reading Note</title>
  <link rel="icon" href="../../../assets/favicon.svg" type="image/svg+xml">
  <script>document.documentElement.dataset.theme = localStorage.getItem('paper-library-theme') || 'dark';</script>
  <link rel="stylesheet" href="../../../assets/css/notes.css">
  <script src="../../../assets/js/note.js" defer></script>
</head>
<body>
  <div class="reading-progress" aria-hidden="true"></div>
  <div class="ambient ambient--teal" aria-hidden="true"></div>
  <div class="ambient ambient--gold" aria-hidden="true"></div>
  <div class="note-shell">
    <header class="note-header">
      <a href="../../../">← Paper Library</a>
      <div class="note-header__actions">
        <a href="{html.escape(paper['paper_url'], quote=True)}" target="_blank" rel="noreferrer">Original Paper</a>
        <button class="theme-toggle" type="button" aria-label="切换明暗主题"><span class="theme-toggle__sun">☀</span><span class="theme-toggle__moon">☾</span></button>
      </div>
    </header>
    <div class="note-layout">
      <nav class="note-toc" aria-label="笔记目录">
        <strong>ON THIS PAGE</strong>
        {''.join(toc)}
      </nav>
      <main class="note-article">
        <header class="note-hero">
          <p class="note-kicker">Reading · Meta Research Note</p>
          <h1>{html.escape(paper['title'])}</h1>
          <p class="note-meta"><span>{html.escape(authors)}</span><span>{html.escape(paper['venue'])}</span><span>{paper['year']}</span></p>
          <div class="draft-banner">状态：阅读中。由 Meta 双人独立阅读笔记同步，正式发表版本与所读版本的差异按下文说明核对。</div>
        </header>
        <section class="note-section" id="bibliography"><h2>01. 书目与阅读版本</h2>{citation_html}</section>
        {''.join(section_html)}
        <footer class="note-footer">Status: Reading · Synced from Meta · 2026-10-22</footer>
      </main>
    </div>
  </div>
</body>
</html>
"""


def paper_record(paper: dict) -> dict:
    return {
        "id": paper["id"],
        "title": paper["title"],
        "authors": paper["authors"],
        "year": paper["year"],
        "venue": paper["venue"],
        "category": paper["category"],
        "method": paper["method"],
        "summary": paper["summary"],
        "paper_url": paper["paper_url"],
        "code_url": "",
        "data_url": "",
        "notes_url": f"notes/{paper['year']}/{paper['id']}/",
        "status": "reading",
        "discussed": False,
        "read_date": "",
        "last_discussed_at": "",
        "discussion_count": 0,
        "added_date": "2026-10-22",
        "updated_date": "2026-10-22",
        "doi": paper["doi"],
        "arxiv_id": paper["arxiv_id"],
        "zotero_key": "",
        "source_note": f"sources/meta-notes/{paper['source']}",
        "tags": paper["tags"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()
    source_dir = args.source.resolve()
    if not source_dir.is_dir():
        raise SystemExit(f"Meta note directory not found: {source_dir}")

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []
    for paper in PAPERS:
        source_file = source_dir / paper["source"]
        markdown = source_file.read_text(encoding="utf-8")
        shutil.copy2(source_file, ARCHIVE_DIR / paper["source"])
        note_dir = ROOT / "docs" / "notes" / str(paper["year"]) / paper["id"]
        note_dir.mkdir(parents=True, exist_ok=True)
        (note_dir / "index.html").write_text(render_note(paper, markdown), encoding="utf-8", newline="\n")
        records.append(paper_record(paper))

    papers = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    selected_ids = {paper["id"] for paper in records}
    papers = [paper for paper in papers if paper.get("id") not in selected_ids]
    papers.extend(records)
    DATA_FILE.write_text(json.dumps(papers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Synced {len(records)} selected Meta notes from {source_dir}")


if __name__ == "__main__":
    main()
