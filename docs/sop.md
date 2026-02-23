# Awesome-Marp-AI 生成 SOP

> 本文档是 AI 从 PDF 生成 Marp 演示文稿的标准操作流程。
> 任何 AI 工具（Claude Code / ChatGPT / Gemini 等）均可按此流程执行。
>
> **核心原则**：先问需求 → 解析 PDF → 生成方案 → 用户确认 → 生成文件 → 迭代修改。

---

## 前置要求

在开始之前，请确认以下环境已就绪：

| 依赖项 | 安装方式 | 验证命令 |
|--------|---------|---------|
| Node.js + marp-cli | `npm install -g @marp-team/marp-cli` | `marp --version` |
| Python 3 + PyMuPDF | `pip install PyMuPDF` （或 `pip install -r requirements.txt`） | `python -c "import fitz; print(fitz.__doc__)"` |
| 主题文件 | 已包含在仓库中 | 确认 `themes/am_consulting.scss` 存在 |

**项目关键文件位置（必须熟悉）：**

```
Awesome-Marp-AI/
├── themes/am_consulting.scss      ← 主题文件（生成时必须引用）
├── scripts/extract_pdf.py         ← PDF 解析脚本
├── docs/content-limits.md         ← 各布局的内容上限规则（防溢出）
├── docs/theme-reference.md        ← 所有 CSS 样式类完整参考
└── components/*.html              ← 12 个交互组件（HTML 输出可用）
```

---

## Phase 1: 快速了解需求

> **目标**：用 2-3 个简单问题，快速锁定用户需求，不要让用户思考太多。

### 必问 3 个问题

按顺序依次询问用户：

**问题 1 — 用途**

```
请问这份 PPT 的用途是什么？
  A. 汇报（给领导/客户看）
  B. 课件（教学/培训用）
  C. 招商（投融资/路演）
  D. 培训（内部分享/知识传递）
  E. 其他（请简要说明）
```

**问题 2 — 目标页数**

```
您希望生成大约多少页？
  A. 10 页以内（精简版）
  B. 10-20 页（标准版）
  C. 20-30 页（详细版）
  D. 30 页以上（完整版）
```

**问题 3 — 输出语言**

```
PPT 使用什么语言？
  A. 中文
  B. 英文
  C. 中英混合
```

### 用途对生成策略的影响

| 用途 | 页面节奏 | 内容密度 | 交互组件 | 封面风格 |
|------|---------|---------|---------|---------|
| 汇报 | 紧凑，结论先行 | 中高 | 可排序表格、进度条 | cover_a 或 cover_c |
| 课件 | 循序渐进 | 中低 | 标签页切换、折叠面板 | cover_b |
| 招商 | 数据驱动，强视觉 | 中 | 动画计数器、CSS 图表 | cover_c（背景图） |
| 培训 | 步骤清晰 | 中低 | 时间线、翻转卡片 | cover_b |

---

## Phase 2: PDF 解析与智能分析

### 2.1 运行 PDF 解析脚本

执行以下命令解析用户提供的 PDF 文件：

```bash
python scripts/extract_pdf.py <用户PDF路径> output
```

**脚本产出：**

| 产出文件 | 路径 | 说明 |
|---------|------|------|
| 结构化文本 | `output/extracted.json` | 按页提取的全部文字，保留页码信息 |
| 图片文件 | `output/images/` | 所有提取的图片，命名格式 `page{N}_img{M}.{ext}` |

**extracted.json 结构示例：**

```json
{
  "metadata": {
    "page_count": 42,
    "title": "行业分析报告"
  },
  "pages": [
    { "page": 1, "text": "第一页的文字内容..." },
    { "page": 2, "text": "第二页的文字内容..." }
  ],
  "images": [
    {
      "page": 3,
      "path": "output/images/page3_img1.png",
      "filename": "page3_img1.png",
      "width": 800,
      "height": 600
    }
  ]
}
```

### 2.2 分析提取内容

读取 `output/extracted.json` 后，AI 需要从以下 5 个维度进行分析：

#### 维度 1：章节结构识别

- 识别 PDF 中的章节层级（标题、小标题、段落）
- 判断哪些章节对应 PPT 中的「章节分隔页」（用 `trans` 样式）
- 判断哪些章节对应具体内容页
- 根据用户要求的页数，决定合并或拆分章节

**判断规则：**
- PDF 中的一级标题 → PPT 的 `trans` 过渡页
- PDF 中的二级标题 → PPT 的内容页标题（`##` 或 `###`）
- PDF 中的段落文字 → 提炼为列表要点或保留为段落

#### 维度 2：数据表格处理

- 识别 PDF 中的表格数据
- 判断是否值得保留为 Marp 表格
- 如果表格过大（超过 8 行 x 6 列），考虑拆分或精简
- 如果表格包含数值对比，考虑使用交互组件（如 CSS 图表、可排序表格）

#### 维度 3：图片筛选

- 检查 `output/images/` 中的所有图片
- 排除过小的图片（宽度 < 100px 或高度 < 100px，通常是图标或装饰）
- 排除纯色块或无意义的图片
- 保留图表、照片、示意图等有信息价值的图片
- 决定图片在 PPT 中的放置位置和大小

#### 维度 4：内容密度评估

**这是最关键的一步。** 必须参考 `docs/content-limits.md` 确保每页内容不溢出。

评估每个计划页面的内容量，匹配合适的布局：

| 内容量 | 推荐布局 | 说明 |
|--------|---------|------|
| 少（3-5 条要点） | 普通页或 `largetext` | 视觉舒适，重点突出 |
| 中（6-8 条要点） | 普通页 | 标准密度 |
| 较多（9-12 条要点） | `smalltext` 或分栏布局 | 利用分栏分散内容 |
| 大量（12+ 条要点） | 拆分为多页 | 绝不能强塞到一页 |

#### 维度 5：交互组件机会识别

扫描内容，识别适合使用交互组件的场景（详见 2.4 节）。

### 2.3 选择布局策略

**必须查阅 `docs/content-limits.md` 获取每种布局的精确内容上限。** 以下是布局选择的通用指导原则：

#### 布局选择决策树

```
内容类型是什么？
├── 纯文字列表
│   ├── ≤ 8 条 → 普通页
│   ├── 9-16 条 → cols-2（每栏 ≤ 8 条）
│   └── 17-24 条 → cols-3（每栏 ≤ 8 条）或拆多页
│
├── 表格数据
│   ├── ≤ 8 行 → 普通页
│   ├── 需要对比两组表格 → cols-2（每栏 ≤ 5 行）
│   └── 表格 + 结论 → rows-2（上方表格，下方结论）
│
├── 文字 + 图片
│   ├── 图片为主 → cols-2-37（左图右文）或 cols-2-46（左图右文）
│   ├── 文字为主 → cols-2-73（左文右图）或 cols-2-64（左文右图）
│   └── 上图下文 → rows-2-46 或 rows-2-37
│
├── 文字 + 表格混合
│   ├── 先文字后表格 → 普通页（文字 3-4 行 + 表格 5 行以内）
│   ├── 左文右表 → cols-2-64
│   └── 上表下结论 → rows-2-64
│
├── 重要结论/洞察
│   ├── 单条核心结论 → bq-green 或 bq-blue 配合列表
│   ├── 风险警告 → bq-red
│   └── 总结摘要 → bq-black
│
└── 需要 navbar 的页面
    └── 所有内容量减少约 15%（navbar 占用顶部空间）
```

#### navbar 使用规则

- 当 PPT 有 3 个以上章节时，建议使用 `navbar`
- navbar 格式：`<!-- _header: \ **当前章节** *其他章节1* *其他章节2* -->`
- 切换章节时，移动 `**粗体**` 到当前章节名称
- navbar 会占用顶部 38px 空间，内容区域相应减少，**所有内容上限需减少约 15%**

### 2.4 识别交互组件机会

**交互组件仅在 HTML 输出中生效。** PDF 输出会自动降级为静态展示。

扫描以下内容模式，匹配对应组件：

| 内容模式 | 推荐组件 | 文件路径 | PDF 降级方式 |
|---------|---------|---------|-------------|
| 数值型 KPI（营收、增长率等） | 动画计数器 | `components/animated-counters.html` | 显示最终数字 |
| 完成进度、达成率 | 进度条 | `components/progress-bars.html` | 静态显示最终状态 |
| 多维度数据对比 | CSS 图表 | `components/charts-css.html` | 静态图表 |
| 多项数据需排序比较 | 可排序表格 | `components/sortable-table.html` | 普通表格 |
| 时间序列/里程碑 | 时间线 | `components/timeline.html` | 正常展示 |
| 多个并列概念/方案 | 标签页切换 | `components/tab-switch.html` | 显示第一个标签 |
| 详细内容需展开查看 | 折叠面板 | `components/collapsible.html` | 全部展开 |
| 正反两面信息 | 翻转卡片 | `components/flip-card.html` | 显示正面 |
| 补充说明/术语解释 | 工具提示 | `components/tooltips.html` | 无提示 |
| 分类筛选 | 可筛选列表 | `components/filter-list.html` | 显示全部 |
| 并列信息卡片 | 悬停卡片 | `components/hover-cards.html` | 显示默认状态 |
| 详细信息弹窗 | 弹窗浮层 | `components/modal-popup.html` | 内联展示 |

**使用原则：**
- 交互组件不是越多越好，每份 PPT 使用 2-5 个即可
- 优先使用 CSS-only 组件（兼容性更好）
- 每个组件文件内有 `{{PLACEHOLDER}}` 参数，AI 替换为实际数据后嵌入 Markdown
- 组件的 `<style scoped>` 和 HTML 代码直接复制到 Marp 幻灯片中

### 2.5 生成方案

综合以上分析，AI 生成一份完整的「生成方案」，格式如下：

```
📋 生成方案

用途：汇报
目标页数：15 页
输出语言：中文

═══════════════════════════════════════

页面结构：

第 1 页 | 封面 | cover_c + 背景图
         标题：[从 PDF 提取的报告标题]

第 2 页 | 目录 | toc_a
         章节列表：1. XXX  2. XXX  3. XXX  4. XXX

第 3 页 | 过渡页 | trans
         章节标题：1. 市场概况

第 4 页 | 内容页 | navbar + 普通页
         内容：市场规模与增长数据（列表 8 条）

第 5 页 | 内容页 | navbar + cols-2
         左栏：驱动因素（列表 6 条）
         右栏：抑制因素（列表 6 条）

第 6 页 | 内容页 | navbar + bq-green
         洞察框：核心发现
         下方：补充数据列表 4 条

第 7 页 | 内容页 | navbar + rows-2-64
         上方：数据表格（6 行 5 列）
         下方：关键结论 3 条

  ... (依此类推)

第 14 页 | 内容页 | navbar + cols-3
          三个阶段的行动方案

第 15 页 | 结束页 | lastpage
          感谢语

═══════════════════════════════════════

交互组件计划：

- 第 4 页：使用动画计数器展示 3 个核心 KPI
- 第 7 页：使用可排序表格展示竞争对手数据
- 第 10 页：使用进度条展示各业务线达成率

═══════════════════════════════════════

图片使用计划：

- page3_img1.png → 第 1 页封面背景（如果适合）
- page8_img2.png → 第 9 页右栏（市场分布图）

说明：已根据 content-limits.md 检查，所有页面内容均在安全范围内。
```

---

## Phase 3: 用户确认方案

### 展示方式

将上述生成方案完整展示给用户，并明确询问：

```
以上是根据您的 PDF 内容和需求生成的方案。请确认：

1. 页面结构是否合理？是否需要增减页面？
2. 布局选择是否满意？某些页面是否需要更换布局？
3. 交互组件是否需要？是否需要增减？
4. 是否有需要特别强调或弱化的内容？

如果满意请回复「确认」，有修改请直接告诉我。
```

### 处理用户修改

- 如果用户要求增加页数 → 拆分内容较多的页面
- 如果用户要求减少页数 → 合并相关内容或删除次要内容
- 如果用户要求更换布局 → 重新检查 content-limits.md 确保内容不溢出
- 如果用户要求增减交互组件 → 调整方案后再次确认

**修改后需重新展示方案，直到用户确认。**

---

## Phase 4: 生成 + 导出 + 迭代

### 4.1 生成 Markdown 文件

#### Marp Frontmatter 模板

每个生成的 `.md` 文件必须以以下 frontmatter 开头：

```yaml
---
marp: true
size: 16:9
theme: am_consulting
paginate: true
headingDivider: [2,3]
footer: \ *部门/作者* *报告标题* *日期*
---
```

#### 关键生成规则（必须严格遵守）

**规则 1：内容上限**
- 在生成每一页之前，必须参考 `docs/content-limits.md` 中的规则
- 绝对不能让内容超出页面可见区域
- 宁可少放内容、多分页，也不能溢出

**规则 2：封面页格式**
- 封面页（cover_a / cover_b / cover_c）必须隐藏 footer、paginate、header
- 使用 `<!-- _header: "" -->` / `<!-- _footer: "" -->` / `<!-- _paginate: "" -->`

**规则 3：过渡页格式**
- 过渡页（trans）必须隐藏 footer 和 paginate
- 过渡页的 `##` 标题就是章节名

**规则 4：分栏页面的 div 结构**
- 列布局使用 `<div class="ldiv">` / `<div class="rdiv">` / `<div class="mdiv">`
- 行布局使用 `<div class="tdiv">` / `<div class="bdiv">`
- div 标签和内容之间必须有空行（Marp 要求）

**规则 5：navbar 格式**
- 当前章节用 `**粗体**`，其他章节用 `*斜体*`
- header 值以 `\ ` 开头（反斜杠 + 空格）
- 每换一个章节，移动粗体标记

**规则 6：交互组件嵌入**
- 从 `components/` 目录读取组件 HTML
- 替换 `{{PLACEHOLDER}}` 为实际数据
- 将 `<style scoped>` 和 HTML 代码块直接写入 Marp 幻灯片
- 交互组件需要 Marp 的 `--html` 参数才能生效

**规则 7：图片引用**
- 提取的图片使用相对路径引用：`![描述](output/images/page3_img1.png)`
- 可以使用 Marp 的尺寸控制：`![w:500](path)` 或 `![h:300](path)`
- 背景图使用 `![bg](url)` 语法

**规则 8：结束页**
- 最后一页使用 `lastpage` 样式
- 隐藏 footer 和 paginate
- 内容简洁（感谢语 + 可选联系方式）

### 4.2 导出多格式

生成 `.md` 文件后，执行以下命令导出：

#### 导出 HTML（支持交互组件）

```bash
marp output.md --theme-set themes/am_consulting.scss --html -o output.html
```

#### 导出 PDF（通用分享）

```bash
marp output.md --theme-set themes/am_consulting.scss --html --pdf --allow-local-files -o output.pdf
```

**参数说明：**

| 参数 | 作用 |
|------|------|
| `--theme-set themes/am_consulting.scss` | 指定使用 consulting 主题 |
| `--html` | 允许在 Markdown 中使用 HTML 标签（分栏 div、交互组件必需） |
| `--pdf` | 导出为 PDF 格式 |
| `--allow-local-files` | 允许引用本地图片文件（PDF 导出时必需） |

### 4.3 告知用户文件位置

导出完成后，明确告诉用户所有生成的文件路径：

```
生成完成！文件已保存到以下位置：

  Markdown 源文件：/完整路径/output.md
  HTML 演示文稿：  /完整路径/output.html  ← 支持交互组件，用浏览器打开
  PDF 演示文稿：   /完整路径/output.pdf   ← 通用格式，可直接分享

提示：
- HTML 版本支持交互功能（点击排序、展开折叠等），推荐用浏览器全屏演示
- PDF 版本为静态版本，交互组件会降级为默认状态显示
- 如需修改，请告诉我具体需要调整的页面和内容
```

### 4.4 迭代修改

用户查看后可能会要求修改。处理流程如下：

```
用户反馈
    │
    ├── 「某页内容溢出了」
    │   → 减少该页内容量或切换为更大的布局（参考 content-limits.md）
    │   → 重新生成该页并重新导出
    │
    ├── 「想更换某页的布局」
    │   → 切换布局类名，调整 div 结构
    │   → 检查新布局的内容上限是否满足
    │   → 重新导出
    │
    ├── 「内容需要修改/补充」
    │   → 修改 .md 文件中的文字内容
    │   → 检查修改后是否超出内容上限
    │   → 重新导出
    │
    ├── 「想增加/减少页面」
    │   → 调整页面结构
    │   → 如使用 navbar，更新所有页面的 header 内容
    │   → 重新导出
    │
    ├── 「交互组件不工作」
    │   → 确认是 HTML 版本（PDF 不支持交互）
    │   → 检查 marp 命令是否包含 --html 参数
    │   → 检查组件的 <script> 标签是否完整
    │
    └── 「满意，不需要修改」
        → 结束流程
```

每次修改后，都需要重新执行导出命令并告知用户新的文件位置。

---

## 附录 A：Marp 文件模板

以下是一个完整的最小化模板，包含封面、目录、过渡页、内容页和结束页：

```markdown
---
marp: true
size: 16:9
theme: am_consulting
paginate: true
headingDivider: [2,3]
footer: \ *部门名称* *报告标题* *2026年2月*
---


<!-- _class: cover_c -->
<!-- _header: "" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

![bg](https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920&q=80)

# <!-- fit --> 报告主标题

###### 副标题或描述文字

作者 · 日期 · 机密


## 目录

<!-- _class: toc_a -->
<!-- _header: "CONTENTS" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

- [第一章标题](#4)
- [第二章标题](#7)
- [第三章标题](#10)
- [总结与建议](#13)


## 1. 第一章标题

<!-- _class: trans -->
<!-- _footer: "" -->
<!-- _paginate: "" -->


## 核心发现

<!-- _class: navbar -->
<!-- _header: \ **第一章** *第二章* *第三章* *总结* -->

- 要点一：描述第一个核心发现
- 要点二：描述第二个核心发现
- 要点三：描述第三个核心发现
- 要点四：描述第四个核心发现
- 要点五：描述第五个核心发现


## 详细对比

<!-- _class: cols-2 navbar -->
<!-- _header: \ **第一章** *第二章* *第三章* *总结* -->

<div class="ldiv">

#### 优势

- 优势一
- 优势二
- 优势三

</div>

<div class="rdiv">

#### 劣势

- 劣势一
- 劣势二
- 劣势三

</div>


## 关键洞察

<!-- _class: bq-green navbar -->
<!-- _header: \ **第一章** *第二章* *第三章* *总结* -->

> **核心结论**
> 此处写入最重要的结论性文字，用引用框突出显示。

- 补充要点一
- 补充要点二
- 补充要点三


---

<!-- _class: lastpage -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

## 谢谢

欢迎提问与讨论
```

---

## 附录 B：布局选择速查表

根据内容类型快速选择合适的布局：

### 按内容类型选择

| 内容类型 | 首选布局 | 备选布局 | 说明 |
|---------|---------|---------|------|
| 单一主题要点列表 | 普通页 | `smalltext` | 6-8 条最佳 |
| 两组对比内容 | `cols-2` | `cols-2-64` | 每栏 6-8 条 |
| 主内容 + 侧栏指标 | `cols-2-73` | `cols-2-64` | 大区域放主体内容 |
| 指标面板 + 详细分析 | `cols-2-37` | `cols-2-46` | 小区域放数字 |
| 三阶段/三方案并列 | `cols-3` | - | 每栏 5-7 条 |
| 数据表 + 结论 | `rows-2-64` | `rows-2` | 上方表格，下方结论 |
| 总结 + 详细数据 | `rows-2-37` | `rows-2-46` | 小区域放总结 |
| 路线图 + 行动要点 | `rows-2-73` | `rows-2-64` | 大区域放路线图 |
| 重要洞察 + 列表 | `bq-green` | `bq-blue` | 洞察框 + 下方要点 |
| 风险提醒 + 分析 | `bq-red` | `bq-black` | 警告框 + 下方说明 |
| 带脚注的分析页 | `footnote` | - | 主体 + 底部引用 |
| 少量大字内容 | `largetext` | - | 3-5 条视觉冲击 |
| 高密度数据页 | `smalltext` | - | 比普通页多放 ~20% |

### 按页面角色选择

| 页面角色 | 样式类 | 必须隐藏 |
|---------|--------|---------|
| 封面（带背景图） | `cover_c` | header, footer, paginate |
| 封面（左侧竖条） | `cover_b` | header, footer, paginate |
| 封面（色块分割） | `cover_a` | header, footer, paginate |
| 目录 | `toc_a` | footer, paginate（header 设为 "CONTENTS"） |
| 章节过渡页 | `trans` | footer, paginate |
| 结束页 | `lastpage` | footer, paginate |
| 普通内容页 | （无特殊类 或 navbar） | 无需隐藏 |

---

## 附录 C：交互组件速查表

### CSS-only 组件（HTML 和 PDF 均可用）

| 组件 | 文件 | 适用场景 | 使用示例 |
|------|------|---------|---------|
| 进度条 | `components/progress-bars.html` | 完成率、达成率、占比展示 | 项目进度 85%、季度目标达成率 |
| 悬停卡片 | `components/hover-cards.html` | 并列展示 3-4 个 KPI 或方案 | 三大业务板块、核心指标面板 |
| 动画计数器 | `components/animated-counters.html` | 大数字展示、KPI 打点 | 营收 5400 亿、增长率 12.5% |
| 时间线 | `components/timeline.html` | 里程碑、发展历程、路线图 | 公司发展三阶段、项目时间线 |
| 工具提示 | `components/tooltips.html` | 术语解释、补充说明 | 专业术语悬停解释 |
| CSS 图表 | `components/charts-css.html` | 数据可视化（柱状/条形/饼图） | 市场份额分布、营收对比 |

### JS 交互组件（仅 HTML 输出可用）

| 组件 | 文件 | 适用场景 | PDF 降级 |
|------|------|---------|---------|
| 可排序表格 | `components/sortable-table.html` | 多维数据对比，需按不同维度排序 | 普通静态表格 |
| 折叠面板 | `components/collapsible.html` | 详细内容需展开查看 | 全部展开显示 |
| 标签页切换 | `components/tab-switch.html` | 多个并列方案/维度切换展示 | 显示第一个标签 |
| 弹窗浮层 | `components/modal-popup.html` | 详细信息按需查看 | 内联展示全部 |
| 可筛选列表 | `components/filter-list.html` | 多分类内容需筛选查看 | 显示全部条目 |
| 翻转卡片 | `components/flip-card.html` | 正反对比（问题/方案、现状/目标） | 显示正面 |

### 组件使用注意事项

1. **Marp 命令必须包含 `--html` 参数**，否则 HTML 组件不会被渲染
2. 每个组件文件顶部有注释说明参数列表（`{{LABEL}}`、`{{VALUE}}` 等）
3. 将组件的 `<style scoped>` 放在幻灯片顶部，HTML 结构紧跟其后
4. 不同组件使用了独立的 CSS 类名前缀，可以在同一页中使用多个组件
5. 如果 PDF 兼容性很重要，优先使用 CSS-only 组件

---

## 附录 D：常见问题与排错

### Q1：导出的 PDF 中页面内容溢出了

**原因**：内容超出了该布局的上限。
**解决**：参考 `docs/content-limits.md`，减少内容或切换到更大的布局。常见做法：
- 减少列表条目数量
- 缩短每条内容的文字长度
- 使用 `smalltext` 类减小字号
- 拆分为两页

### Q2：HTML 中的交互组件没有效果

**原因**：marp 导出时未加 `--html` 参数。
**解决**：确认命令包含 `--html`：
```bash
marp output.md --theme-set themes/am_consulting.scss --html -o output.html
```

### Q3：PDF 中图片没有显示

**原因**：PDF 导出时未加 `--allow-local-files` 参数。
**解决**：确认命令包含 `--allow-local-files`：
```bash
marp output.md --theme-set themes/am_consulting.scss --html --pdf --allow-local-files -o output.pdf
```

### Q4：分栏布局中内容没有分到两栏

**原因**：`<div>` 标签和内容之间缺少空行。
**解决**：确保 div 标签后有一个空行再写内容：
```markdown
<div class="ldiv">

#### 这里必须有空行

- 内容...

</div>
```

### Q5：navbar 没有显示

**原因**：`_header` 格式不对。
**解决**：确保 header 以 `\ ` 开头，当前章节用 `**粗体**`，其他用 `*斜体*`：
```markdown
<!-- _class: navbar -->
<!-- _header: \ **当前章节** *其他章节A* *其他章节B* -->
```

### Q6：封面页显示了页码和页脚

**原因**：封面页没有隐藏 footer 和 paginate。
**解决**：封面页必须包含以下三行：
```markdown
<!-- _header: "" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
```
