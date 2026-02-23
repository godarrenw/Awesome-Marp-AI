# Awesome-Marp-AI

基于 Marp consulting 主题，让任何 AI 将 PDF 自动转化为高质量演示文稿。

---

## 特性

- **PDF 解析（文字 + 图片提取）-> AI 智能生成 -> 多格式输出（Markdown / HTML / PDF）**
- **内容不超出页面** -- 基于 DOE 实验得出的量化内容上限规则，杜绝内容溢出
- **交互组件库** -- HTML 输出支持动画、排序、切换等 12 种交互效果
- **完整 SOP 流程** -- 任何 AI 均可按步骤执行，无需人工干预

---

## 快速开始

### 安装依赖

```bash
# Marp CLI（Markdown 转 HTML/PDF 的核心引擎）
npm install -g @marp-team/marp-cli

# Python PDF 解析库
pip install PyMuPDF>=1.24.0
```

### 使用方式

**方式一：Claude Code（推荐）**

```
/generate-ppt <pdf文件路径>
```

Claude Code 会自动执行完整的 SOP 流程：解析 PDF、询问偏好、生成方案、导出文件。

**方式二：任何 AI 工具**

1. 将本仓库提供给 AI（克隆到本地或将文件内容发送给 AI）
2. AI 阅读 `docs/sop.md` 了解完整流程
3. AI 按 SOP 执行 PDF -> PPT 转换

> AI 只需要阅读 `docs/` 目录下的三份文档，即可掌握所有生成规则。

---

## 仓库结构

```
Awesome-Marp-AI/
├── README.md                       # 项目介绍（本文件）
├── CLAUDE.md                       # Claude Code 专用引导文件
├── requirements.txt                # Python 依赖
│
├── docs/
│   ├── sop.md                      # 生成标准操作流程（SOP）
│   ├── content-limits.md           # 各布局内容上限规则（DOE 实验结果）
│   └── theme-reference.md          # 主题所有 CSS 样式类完整参考
│
├── themes/
│   └── am_consulting.scss          # Marp 主题（自包含，import default）
│
├── scripts/
│   └── extract_pdf.py              # PDF 解析脚本：提取文字 + 图片
│
├── components/                     # 12 个交互组件（HTML 文件）
│   ├── progress-bars.html          # 进度条
│   ├── hover-cards.html            # 悬停卡片
│   ├── animated-counters.html      # 动画计数器
│   ├── timeline.html               # 时间线
│   ├── tooltips.html               # 工具提示
│   ├── charts-css.html             # CSS 图表
│   ├── sortable-table.html         # 可排序表格
│   ├── collapsible.html            # 折叠面板
│   ├── tab-switch.html             # 标签页切换
│   ├── modal-popup.html            # 弹窗浮层
│   ├── filter-list.html            # 可筛选列表
│   └── flip-card.html              # 翻转卡片
│
├── examples/                       # 示例文件
│
├── tests/                          # DOE 测试文件
│
└── .claude/
    └── commands/
        └── generate-ppt.md         # Claude Code slash command 定义
```

---

## 文档索引

| 文档 | 说明 |
|------|------|
| `docs/sop.md` | 生成标准操作流程 -- AI 从这里开始，了解完整的 PDF -> PPT 工作流 |
| `docs/content-limits.md` | 各布局内容上限规则 -- 通过 DOE 实验确定的量化限制，防止页面溢出 |
| `docs/theme-reference.md` | 主题样式类完整参考 -- 所有 CSS class、布局、组件的用法与示例 |

---

## 交互组件库

12 个自包含的交互组件，分为纯 CSS 和 JS 交互两类：

| 组件 | 文件 | 类型 | 交互方式 | PDF 降级 |
|------|------|------|---------|---------|
| 进度条 | `progress-bars.html` | CSS-only | @keyframes 动画 | 静态显示最终状态 |
| 悬停卡片 | `hover-cards.html` | CSS-only | :hover 悬浮效果 | 显示默认状态 |
| 动画计数器 | `animated-counters.html` | CSS-only | CSS animation | 显示最终数字 |
| 时间线 | `timeline.html` | CSS-only | CSS animation | 正常展示 |
| 工具提示 | `tooltips.html` | CSS-only | :hover 提示 | 无提示文字 |
| CSS 图表 | `charts-css.html` | CSS-only | CSS animation | 静态图表 |
| 可排序表格 | `sortable-table.html` | JS-interactive | 点击表头排序 | 普通表格 |
| 折叠面板 | `collapsible.html` | JS-interactive | 点击展开/收起 | 全部展开 |
| 标签页切换 | `tab-switch.html` | JS-interactive | 点击切换内容 | 显示第一个标签 |
| 弹窗浮层 | `modal-popup.html` | JS-interactive | 点击弹出详情 | 无弹窗，内联展示 |
| 可筛选列表 | `filter-list.html` | JS-interactive | 点击标签过滤 | 显示全部条目 |
| 翻转卡片 | `flip-card.html` | JS-interactive | 点击翻转 | 显示正面 |

> **CSS-only 组件** 兼容 HTML 和 PDF 输出；**JS-interactive 组件** 仅在 HTML 输出中生效，PDF 自动降级为静态展示。

每个组件文件内含参数化占位符（如 `{{LABEL}}`、`{{VALUE}}`），AI 替换参数后直接嵌入 Marp Markdown 即可使用。

---

## 主题预览

consulting 主题提供丰富的页面类型：

| 类别 | 可用样式类 |
|------|-----------|
| 封面页 | `cover_a` / `cover_b` / `cover_c` |
| 过渡页 | `trans` |
| 目录页 | `toc_a` |
| 左右分栏 | `cols-2` / `cols-2-64` / `cols-2-73` / `cols-2-46` / `cols-2-37` / `cols-3` |
| 上下分栏 | `rows-2` / `rows-2-64` / `rows-2-73` / `rows-2-46` / `rows-2-37` |
| 导航栏 | `navbar` |
| 引用框 | `bq-green` / `bq-red` / `bq-blue` / `bq-black` |
| 工具类 | `footnote` / `caption` / `smalltext` / `largetext` |
| 结束页 | `lastpage` |

详细用法请参阅 `docs/theme-reference.md`。

---

## 导出命令

```bash
# 导出为 HTML（支持交互组件）
marp output.md --theme-set themes/am_consulting.scss --html -o output.html

# 导出为 PDF（通用分享，交互组件降级为静态）
marp output.md --theme-set themes/am_consulting.scss --html --pdf --allow-local-files -o output.pdf
```

> **注意**：必须使用 `--theme-set`（而非 `--theme`），因为 SCSS 文件内部使用了 `@import 'default'`。同时需要 `--html` 参数以启用 HTML 标签渲染。

---

## License

MIT
