# Paper Reading Library：设计与扩展文档

更新日期：2026-10-22

## 1. 项目定位

Paper Reading Library 不是单纯的论文链接收藏夹，而是一个可长期积累的个人研究知识库。它需要同时回答四个问题：

1. 我收藏了哪些论文？
2. 我是否真正阅读并形成了自己的理解？
3. 我围绕这些论文与谁讨论过、产生了哪些新问题？
4. 多篇论文之间形成了怎样的主题、方法和引用关系？

当前版本优先保证信息可读、数据可迁移、Git 可追踪和 GitHub Pages 可部署，不在第一阶段引入账号、数据库或服务端。

## 2. 设计原则

- **数据与展示分离**：论文元数据存放在 JSON，网页只负责读取和呈现。
- **原文与理解分离**：论文标题链接出版源，个人笔记使用独立页面。
- **阅读与讨论分离**：阅读进度是生命周期，是否讨论是独立维度。
- **稳定标识优先**：优先保存 DOI、arXiv ID、Zotero Key，而不是依赖标题匹配。
- **静态优先、渐进增强**：能用构建脚本解决的问题，暂不引入数据库。
- **保留可迁移性**：所有核心数据使用开放格式，避免锁定到单一平台。

## 3. 当前架构

```text
docs/data/papers.json
        │
        ├── 浏览器读取 ──→ docs/index.html 论文目录
        │
        └── Python 生成 ─→ README.md 论文表格

docs/notes/<year>/<slug>/index.html
        └── 独立阅读与讨论笔记
```

核心文件职责：

| 文件 | 职责 |
|---|---|
| `docs/data/papers.json` | 当前论文元数据的唯一来源 |
| `docs/index.html` | GitHub Pages 文库入口 |
| `docs/assets/js/library.js` | 搜索、筛选、统计和渲染 |
| `docs/notes/` | 每篇论文的个人笔记 |
| `scripts/generate_readme.py` | 生成 GitHub 首页表格 |
| `scripts/validate.py` | 校验字段、状态、URL 和笔记路径 |
| `.github/workflows/pages.yml` | 校验并发布 GitHub Pages |

### 当前优势

- 没有运行时服务器和数据库成本。
- 数据与笔记都能通过 Git 查看历史。
- GitHub Pages 可以直接缓存和分发全部内容。
- JSON 可以继续被统计页面、知识图谱或同步脚本复用。

### 当前限制

- GitHub Pages 不能直接把浏览器修改写回 `papers.json`。
- 每篇笔记目前是手写 HTML，论文数量很多后维护成本会上升。
- 单一 `papers.json` 适合元数据，不适合保存大量阅读事件和关系网络。
- 当前统计是“状态快照”，不能准确还原每周、每月的阅读历史。

## 4. 当前数据模型

论文的阅读状态使用：

```text
planned → reading → read
```

讨论不属于这条线性流程。一篇论文可能在阅读过程中就和他人讨论，也可能阅读完成后从未讨论。因此当前开始采用两个维度：

```json
{
  "status": "reading",
  "discussed": true,
  "last_discussed_at": "2026-10-22",
  "discussion_count": 2
}
```

建议论文记录逐步包含：

| 字段 | 说明 |
|---|---|
| `id` | 仓库内稳定 slug |
| `doi` / `arxiv_id` | 外部稳定标识 |
| `zotero_key` | Zotero 条目对应键 |
| `status` | `planned`、`reading`、`read` |
| `discussed` | 是否至少讨论过一次 |
| `discussion_count` | 讨论次数快照 |
| `last_discussed_at` | 最近讨论日期 |
| `added_date` / `updated_date` | 加入和更新日期 |
| `tags` | 自由标签 |

## 5. 网页内增删改的可选方案

### 方案 A：静态管理表单，不需要数据库（推荐下一步）

增加一个仅用于本地打开的 `admin.html`：

- 表单录入或修改论文字段；
- 即时校验 DOI、URL、状态和重复 ID；
- 自动生成 JSON 条目与笔记目录模板；
- 下载更新后的 `papers.json`，由用户确认后提交 Git。

优点是简单、安全、无账号；缺点是不能在线直接保存，也不能自动跨设备同步。预计工程量较小。

### 方案 B：通过 GitHub API 写回仓库，不需要传统数据库

网页使用 GitHub OAuth 登录，将修改转换成 commit 或 pull request。

优点是仍以 Git 为唯一数据源；缺点是需要 OAuth 应用、令牌安全、权限管理、冲突处理和错误恢复。不能把 Personal Access Token 直接写在前端。预计工程量中等。

### 方案 C：动态应用与数据库

使用 Supabase、Cloudflare D1 或其他数据库，并增加认证 API：

- 在线增删改论文和阅读事件；
- 多设备即时同步；
- 私有笔记和公开笔记分层；
- 服务端 Zotero 同步和定时任务。

优点是体验完整；缺点是需要数据库迁移、鉴权、备份、部署和安全维护。预计工程量最大。

### 当前决策

保持 GitHub Pages 静态架构，下一阶段优先实现方案 A。只有当“必须从任意设备直接保存”成为稳定需求时，再评估方案 B 或 C。

## 6. 阅读统计扩展

周报和月报不应只根据论文当前状态推断，而应记录事件。建议新增：

```text
docs/data/activity.json
```

事件示例：

```json
{
  "id": "evt-20261022-001",
  "paper_id": "agentic-fintech-survey",
  "type": "discussion",
  "occurred_at": "2026-10-22T20:00:00+08:00",
  "minutes": 45,
  "context": "peer-discussion",
  "note": "讨论了评测体系与监管风险"
}
```

可支持的统计：

- 每周/月新增、开始、读完和讨论的论文数量；
- 阅读时长与活跃天数；
- 各主题阅读投入；
- 从收藏到读完的平均周期；
- 最近持续关注的研究方向；
- 阅读与讨论之间的转化关系。

第一阶段可以由 JavaScript 或 Python 从 JSON 静态生成统计，无需数据库。

## 7. 知识图谱扩展

建议把图谱拆成“节点”和“关系”，不要把大量关系直接塞进论文对象。

```text
docs/data/relations.json
```

节点类型：

- Paper
- Author
- Topic
- Method
- Dataset
- Venue
- Project

关系类型：

- `CITES`
- `EXTENDS`
- `CONTRADICTS`
- `USES_METHOD`
- `EVALUATED_ON`
- `RELATED_TO`
- `AUTHORED_BY`
- `DISCUSSED_WITH`

初期可用 Cytoscape.js 或 D3 在浏览器中渲染 JSON。只有当关系达到数万条、需要复杂图查询时，才考虑 Neo4j 等图数据库。

## 8. Zotero 联动

推荐按以下顺序演进：

1. **导入**：本地脚本读取 Zotero 导出的 Better BibTeX、BibTeX 或 CSL JSON，规范化写入 `papers.json`。
2. **稳定映射**：保存 `zotero_key`、DOI 和 arXiv ID，避免重复导入。
3. **增量同步**：本地脚本或 GitHub Action 使用 Zotero Web API，只同步有指定 collection/tag 的条目。
4. **附件处理**：默认只保存原文链接，不把受版权保护的 PDF 推到公开仓库。
5. **写回 Zotero**：如果确有需要，通过本地脚本把阅读状态或笔记链接写回 Zotero；API Key 仅放在环境变量或 GitHub Secret 中。

对于个人知识库，推荐将 Zotero 作为“文献元数据与附件管理器”，将本仓库作为“阅读理解、讨论记录和知识关系层”。

## 9. 笔记格式演进

当前 HTML 模板适合直接控制排版，但论文数量增多后建议迁移为：

```text
notes-src/<year>/<slug>/index.md
                     ↓ 静态生成
docs/notes/<year>/<slug>/index.html
```

Markdown Front Matter 保存标题、paper_id、更新时间和标签，正文专注内容。这样可以统一模板、全局改版并生成全文搜索索引。

## 10. 分阶段路线

### Phase 0：当前静态文库

- JSON 论文目录；
- README 自动生成；
- HTML 笔记；
- 搜索、筛选、明暗主题；
- GitHub Pages 自动部署。

### Phase 1：本地管理工具

- 新增/编辑论文表单；
- JSON 导入导出；
- 自动生成笔记目录；
- 重复论文检测；
- BibTeX/CSL JSON 导入。

### Phase 2：活动与统计

- `activity.json` 事件模型；
- 周报、月报、年度统计；
- 阅读热力图；
- 状态变化时间线。

### Phase 3：关系与搜索

- Markdown 笔记源文件；
- 全文搜索索引；
- `relations.json`；
- 主题网络和知识图谱。

### Phase 4：外部同步与动态保存

- Zotero 增量同步；
- GitHub OAuth 写回或后端数据库；
- 私有/公开内容分层；
- 自动备份和冲突解决。

## 11. 下一步建议

1. 先用当前结构录入 10–20 篇真实论文，验证字段和笔记模板是否自然。
2. 实现方案 A 的本地管理页，减少手写 JSON 的错误。
3. 在有至少一个月真实使用数据后，再确定阅读事件和统计口径。
4. 在积累足够交叉关系后再做知识图谱，避免先有图形、后补语义。
5. Zotero 联动优先从单向导入开始，不急于双向同步。

