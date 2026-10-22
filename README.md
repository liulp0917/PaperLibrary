# Paper Reading Library

一个用于整理论文原文、阅读摘要和讨论交流笔记的个人知识库。

> 网页版入口将在启用 GitHub Pages 后显示为：
> `https://liulp0917.github.io/PaperLibrary/`

## 使用方式

- 论文元数据统一维护在 `docs/data/papers.json`。
- 每篇阅读笔记放在 `docs/notes/<year>/<slug>/index.html`。
- 运行 `python scripts/generate_readme.py` 更新下方论文表格。
- 运行 `python scripts/validate.py` 检查数据和笔记链接。
- 本地预览：在仓库根目录运行 `python -m http.server 8000 -d docs`，然后访问 `http://localhost:8000/`。
- 第一次推送到 GitHub 后，在仓库 `Settings → Pages → Source` 中选择 **GitHub Actions**；此后推送到 `main` 会自动检查并部署网页。
- 当前架构、数据模型及长期扩展路线见 [DESIGN.md](DESIGN.md)。

## Paper Library

<!-- PAPERS_TABLE_START -->

| Paper | Year / Venue | Category | Method | Key Idea | Resources | Reading Notes | Status |
|---|---|---|---|---|---|---|---|
| [Agentic FinTech: A Comprehensive Survey on AI Agents in Finance in the Era of LLMs](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6136529) | 2026 / SSRN | Agentic Finance | Survey | 系统梳理金融智能体的能力、工作流、架构、优化方法与评测体系。 | [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6136529) · [Code](https://github.com/agentic-fintech/Agentic_FinTech_Survey) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2026/agentic-fintech-survey/) | To Read |

<!-- PAPERS_TABLE_END -->

## Repository Structure

```text
PaperLibrary/
├─ README.md
├─ docs/
│  ├─ index.html
│  ├─ data/papers.json
│  ├─ assets/
│  └─ notes/
└─ scripts/
   ├─ generate_readme.py
   └─ validate.py
```

