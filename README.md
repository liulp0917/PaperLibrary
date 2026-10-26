# Paper Reading Library

一个用于整理论文原文、阅读摘要和讨论交流笔记的个人知识库。

> 网页版入口：<https://liulp0917.github.io/PaperLibrary/>

## 使用方式

- 论文元数据统一维护在 `docs/data/papers.json`。
- 每篇阅读笔记放在 `docs/notes/<year>/<slug>/index.html`。
- 运行 `python scripts/generate_readme.py` 更新下方论文表格。
- 运行 `python scripts/validate.py` 检查数据和笔记链接。
- 运行 `python scripts/sync_meta_notes.py` 从相邻的 Meta 项目归档已筛选笔记、生成 HTML，并更新论文元数据。
- 本地预览：在仓库根目录运行 `python -m http.server 8000 -d docs`，然后访问 `http://localhost:8000/`。
- 第一次推送到 GitHub 后，在仓库 `Settings → Pages → Source` 中选择 **GitHub Actions**；此后推送到 `main` 会自动检查并部署网页。
- 当前架构、数据模型及长期扩展路线见 [DESIGN.md](DESIGN.md)。

## Paper Library

<!-- PAPERS_TABLE_START -->

| Paper | Year / Venue | Category | Method | Key Idea | Resources | Reading Notes | Status |
|---|---|---|---|---|---|---|---|
| [Agentic FinTech: A Comprehensive Survey on AI Agents in Finance in the Era of LLMs](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6136529) | 2026 / SSRN | Agentic Finance | Survey | 系统梳理金融智能体的能力、工作流、架构、优化方法与评测体系。 | [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6136529) · [Code](https://github.com/agentic-fintech/Agentic_FinTech_Survey) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2026/agentic-fintech-survey/) | To Read |
| [Addressing Misspecification in Simulation-based Inference through Data-driven Calibration](https://proceedings.mlr.press/v267/wehenkel25a.html) | 2025 / ICML | Simulation-based Inference | Optimal Transport Calibration | 用少量带真实参数标签的校准样本与最优传输修正错设模拟器下的 SBI 后验。 | [Paper](https://proceedings.mlr.press/v267/wehenkel25a.html) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2025/rope-sbi-calibration/) | Reading |
| [Consistent Sampling and Simulation: Molecular Dynamics with Energy-Based Diffusion Models](https://papers.nips.cc/paper_files/paper/2025/file/231be94eaf8dcbc49a95b256c9b6b8b5-Paper-Conference.pdf) | 2025 / NeurIPS | Generative Dynamics | Energy-Based Diffusion + Fokker–Planck Regularization | 揭示独立采样正确并不保证递归动力学正确，并以 Fokker–Planck 残差约束两者一致。 | [Paper](https://papers.nips.cc/paper_files/paper/2025/file/231be94eaf8dcbc49a95b256c9b6b8b5-Paper-Conference.pdf) · [Code](https://github.com/noegroup/ScoreMD) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2025/consistent-sampling-simulation/) | Reading |
| [G-Sim: Generative Simulations with Large Language Models and Gradient-Free Calibration](https://proceedings.mlr.press/v267/holt25b.html) | 2025 / ICML | Simulation & Calibration | LLM Simulator + Calibration | 让 LLM 提议模拟器结构，并以无梯度优化或模拟型推断校准参数和反馈修订结构。 | [Paper](https://proceedings.mlr.press/v267/holt25b.html) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2025/g-sim/) | Reading |
| [The Limits of Predicting Agents from Behaviour](https://proceedings.mlr.press/v267/bellot25a.html) | 2025 / ICML | Agent Modeling | Theoretical Analysis | 给出仅从历史行为预测代理在新干预或新制度中行动的理论边界与不可识别条件。 | [Paper](https://proceedings.mlr.press/v267/bellot25a.html) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2025/limits-predicting-agents/) | Reading |
| [TwinMarket: A Scalable Behavioral and Social Simulation for Financial Markets](https://proceedings.neurips.cc/paper_files/paper/2025/hash/5bf234ecf83cd77bc5b77a24ba9338b0-Abstract-Conference.html) | 2025 / NeurIPS | Multi-Agent Finance | Behavioral Market Simulation | 以 BDI 认知、异质交易者和动态社交网络模拟金融市场中的群体行为与宏观涌现。 | [Paper](https://proceedings.neurips.cc/paper_files/paper/2025/hash/5bf234ecf83cd77bc5b77a24ba9338b0-Abstract-Conference.html) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2025/twinmarket/) | Reading |
| [Agent-Specific Effects: A Causal Effect Propagation Analysis in Multi-Agent MDPs](https://proceedings.mlr.press/v235/triantafyllou24a.html) | 2024 / ICML | Causal Multi-Agent Systems | Causal Effect Attribution | 定义多智能体 MDP 中经由其他代理反应传播的路径特定因果效应及其识别条件。 | [Paper](https://proceedings.mlr.press/v235/triantafyllou24a.html) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2024/agent-specific-effects/) | Reading |
| [Characterising Interventions in Causal Games](https://proceedings.mlr.press/v244/mishra24a.html) | 2024 / UAI | Causal Multi-Agent Systems | Causal Games | 刻画因果博弈中的干预原语、知情时序与策略重算，澄清多智能体反事实的语义。 | [Paper](https://proceedings.mlr.press/v244/mishra24a.html) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2024/causal-games-interventions/) | Reading |
| [Efficient Bayesian Inference Using Physics-Informed Invertible Neural Networks for Inverse Problems](https://arxiv.org/html/2304.12541) | 2023 / arXiv | Bayesian Inverse Problems | Physics-Informed Invertible Neural Network | 以可逆网络把观测可解释部分与潜在自由度分开，从单点反演转向多解后验分布。 | [Paper](https://arxiv.org/html/2304.12541) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2023/pi-inn-bayesian-inverse-problems/) | Reading |
| [Reaction Coordinate Flows for Model Reduction of Molecular Kinetics](https://arxiv.org/html/2309.05878) | 2023 / arXiv | Dynamical Model Reduction | Normalizing Flow + Reduced Kinetics | 以时间滞后转移和慢松弛模式学习保留未来信息的低维反应坐标。 | [Paper](https://arxiv.org/html/2309.05878) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2023/reaction-coordinate-flows/) | Reading |
| [Causal Inference under Networked Interference and Intervention Policy Enhancement](https://proceedings.mlr.press/v130/ma21c.html) | 2021 / AISTATS | Causal Inference | Graph Neural Causal Estimation | 在网络干扰下估计直接与溢出效应，并研究容量约束下的干预政策优化。 | [Paper](https://proceedings.mlr.press/v130/ma21c.html) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2021/network-interference-policy/) | Reading |
| [The Spread of Behavior in an Online Social Network Experiment](https://doi.org/10.1126/science.1185231) | 2010 / Science | Social Networks | Randomized Network Experiment | 通过保持度数的网络拓扑随机实验检验聚类结构和多重社会强化对行为传播的影响。 | [Paper](https://doi.org/10.1126/science.1185231) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2010/complex-contagion-network-experiment/) | Reading |
| [Biodiversity and Ecosystem Stability in a Decade-long Grassland Experiment](https://doi.org/10.1038/nature04742) | 2006 / Nature | Complex Systems | Longitudinal Field Experiment | 利用十年草地随机实验分解多样性、物种波动与群落总体稳定性之间的关系。 | [Paper](https://doi.org/10.1038/nature04742) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2006/biodiversity-ecosystem-stability/) | Reading |
| [Experimental Study of Inequality and Unpredictability in an Artificial Cultural Market](https://doi.org/10.1126/science.1121066) | 2006 / Science | Social Influence | Parallel-world Experiment | 以多个随机平行世界识别社会信息如何提高结果不平等，并放大成功的不可预测性。 | [Paper](https://doi.org/10.1126/science.1121066) | [Notes](https://liulp0917.github.io/PaperLibrary/notes/2006/musiclab-social-influence/) | Reading |

<!-- PAPERS_TABLE_END -->

## Repository Structure

```text
PaperLibrary/
├─ README.md
├─ sources/meta-notes/       # Meta 原始 Markdown 笔记归档
├─ docs/
│  ├─ index.html
│  ├─ data/papers.json
│  ├─ assets/
│  └─ notes/
└─ scripts/
   ├─ generate_readme.py
   ├─ sync_meta_notes.py
   └─ validate.py
```

