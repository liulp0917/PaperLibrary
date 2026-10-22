# 07｜Agent-Specific Effects：多智能体“经他人传播”的因果效应

**书目。** Stelios Triantafyllou、Aleksa Sukovic、Debmalya Mandal、Goran Radanovic，*Agent-Specific Effects: A Causal Effect Propagation Analysis in Multi-Agent MDPs*，ICML 2024，PMLR 235:48578–48607，[官方 proceedings](https://proceedings.mlr.press/v235/triantafyllou24a.html)。章节/公式核读[同名 arXiv v3 全文](https://arxiv.org/html/2310.11334v3)，如与会议版有修订应以正式 PDF 复核。

## 聚焦问题与文章结构

一个代理的行动影响结果，其中多少经由其他代理的**反应行动**传播，而非环境直接传递？§1 问题；§2 MMDP、结构因果模型；§3 agent-specific effect（ASE）与反事实版本；§4 识别条件；§5 抽样算法；§6 与路径特定效应关系；§7 图任务和败血症管理实验；§8 结论；附录为证明与补充。

## 关键定义、识别与实验

论文将多智能体 MDP 写成带外生噪声的 SCM，在嵌套反事实世界中指定“哪一组代理沿处理世界的反应行动、其余沿基准世界行动”，测特定代理传播路径（§3）。作者明确证明一般情况下这种反事实效应**不可识别**；在外生噪声有已知统一顺序且机制对噪声单调等条件下，cf-ASE 可识别（§4 定理）。§5 算法从事实轨迹推断外生噪声再模拟嵌套世界；§7 图任务与 AI 推荐/临床医生接管的败血症场景用于检验归因。图 4 显示政策估错或噪声顺序弄错会产生偏差。

## 双读审稿结论

本文的贡献是严密定义**模型内、路径特定**效应及其条件，不是宣布“多代理溢出都可从观察数据识别”。跨世界反应行动在真实市场难直接实施；LLM 黑箱、全局价格、异步撮合及内生网络使噪声模型与单调顺序条件更难满足。将统计可识别定理搬到错误的市场 SCM，并不能获得现实因果性。总市场冲击效应与经特定代理传播的机制效应必须分开。

## 接到 Meta Dev

先用整座市场随机化得到总效应。若进一步归因“新闻→某类交易者订单→价格”，应记录代理政策、外生随机源、撮合状态及可重复干预接口，并报告不同合理 SCM 下机制效应是否变号。对现实数据只可提出条件性机制解释。

**证据定位：**[ICML 正式条目](https://proceedings.mlr.press/v235/triantafyllou24a.html)；[arXiv 全文 §2–7、定理与图 4–5](https://arxiv.org/html/2310.11334v3)。
