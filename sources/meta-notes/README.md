# Meta Reading Notes Archive

本目录保存从 `D:\AAAAclasses\Meta\docs\literature-reading-notes` 同步进入 PaperLibrary 的原始 Markdown 笔记。网页展示版本由 `scripts/sync_meta_notes.py` 生成到 `docs/notes/<year>/<paper-id>/index.html`。

## 2026-10-22 筛选口径

本轮采用“已正式发表，并进入顶级综合期刊、顶级机器学习会议或公认强专业会议”的严格口径，共归档 10 篇：

- NeurIPS：TwinMarket；
- ICML：Agent-Specific Effects、G-Sim、RoPE、The Limits of Predicting Agents from Behaviour；
- AISTATS：Causal Inference under Networked Interference and Intervention Policy Enhancement；
- UAI：Characterising Interventions in Causal Games；
- Science：复杂传染网络实验、MusicLab；
- Nature：Biodiversity and Ecosystem Stability。

所有入选论文在 `papers.json` 中统一标记为 `reading`。原始 Markdown 保留版本辨析、审稿质疑与 Meta Dev 连接，生成 HTML 时不删减正文。

## 本轮暂缓

- StockSim、Lopez-Lira market simulation、LLM Agents Do Not Replicate Human Market Traders：尚未核得正式发表版本；
- StockAgent：虽已记录 ACM TIST 正式版，但当前笔记主要依据 arXiv v5，待正式版内容对齐后再加入；
- FCLAgent：PRIMA 正式发表，但不属于本轮严格顶会集合；
- Statistically Validated Network of Portfolio Overlaps and Systemic Risk：Scientific Reports 正式发表，但不属于本轮严格顶刊集合。

“暂缓”仅表示未进入本轮精选目录，不代表论文质量低或以后不再收录。
