# Marp Consulting Theme Reference (`am_consulting`)

Comprehensive reference for every custom CSS class defined in the `am_consulting` theme.
Source file: `themes/am_consulting.scss`

---

## Table of Contents

1. [Frontmatter Setup](#1-frontmatter-setup)
2. [Cover Pages](#2-cover-pages)
   - [cover_a](#cover_a--full-width-color-band)
   - [cover_b](#cover_b--left-bar-accent)
   - [cover_c](#cover_c--image-background-with-overlay)
3. [Transition Page](#3-transition-page)
4. [Table of Contents](#4-table-of-contents)
5. [Column Layouts](#5-column-layouts)
6. [Row Layouts](#6-row-layouts)
7. [Navigation Bar](#7-navigation-bar)
8. [Callout Boxes](#8-callout-boxes)
9. [Footnote](#9-footnote)
10. [Font Sizes](#10-font-sizes)
11. [Last Page](#11-last-page)
12. [Caption](#12-caption)
13. [Image Alignment](#13-image-alignment)
14. [Combinability](#14-combinability)

---

## 1. Frontmatter Setup

Every presentation using this theme must begin with a YAML frontmatter block.

### Required Fields

| Field            | Value / Format                                              | Notes                                           |
|------------------|-------------------------------------------------------------|-------------------------------------------------|
| `marp`           | `true`                                                      | Enables the Marp engine.                        |
| `size`           | `16:9`                                                      | Standard widescreen aspect ratio.               |
| `theme`          | `am_consulting`                                             | Activates this theme.                           |
| `paginate`       | `true`                                                      | Shows page numbers (format: `N / Total`).       |
| `headingDivider` | `[2,3]`                                                     | Auto-creates a new slide before every `##` or `###`. |
| `footer`         | `\ *Section* *Subtitle* *Date*`                             | Three `*em*` items render as a space-between footer row. |

### Minimal Frontmatter

```yaml
---
marp: true
size: 16:9
theme: am_consulting
paginate: true
headingDivider: [2,3]
footer: \ *Department* *Report Title* *2026-02*
---
```

### Footer Format Details

The footer uses flexbox with `justify-content: space-between`. Write three `*italic*` segments separated by spaces inside the `footer` value. Each segment becomes one flex item distributed evenly across the bottom of every slide.

To hide the footer on a specific slide (e.g., covers, transitions), add:

```markdown
<!-- _footer: "" -->
```

To hide pagination on a specific slide, add:

```markdown
<!-- _paginate: "" -->
```

---

## 2. Cover Pages

### `cover_a` -- Full-Width Color Band

**Purpose:** Title slide with the top 57% filled by the primary green color and the bottom 43% white.

**Directive:**

```markdown
<!-- _class: cover_a -->
```

**Layout:** `h1` is absolutely positioned over the green band; `h6` renders as a subtitle below it; `p` text sits at the bottom in the white area.

**Minimal Example:**

```markdown
---
(frontmatter)
---

<!-- _class: cover_a -->
<!-- _header: "" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

# <!-- fit --> Presentation Title

###### Subtitle or tagline

Author Name
Date / Confidentiality Notice
```

**Notes:**
- `<!-- fit -->` inside `h1` auto-scales the title to fill the width.
- `<!-- _header: "" -->` hides any header/navbar on this slide.
- Strong text (`**bold**`) renders in dark text color instead of the default emphasis red.
- Link icons (`a::after`) are suppressed on this class.

---

### `cover_b` -- Left Bar Accent

**Purpose:** Title slide with a vertical green bar on the left (7% width) and content right-aligned.

**Directive:**

```markdown
<!-- _class: cover_b -->
```

**Layout:** The slide has a green left border via a CSS gradient. `h1` displays with a decorative gradient underline (120px bar). `h6` acts as a subtitle. `p` renders as body text.

**Minimal Example:**

```markdown
<!-- _class: cover_b -->
<!-- _header: "" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

# <!-- fit --> Presentation Title

###### Subtitle line

Author / Department
Additional description text
```

**Notes:**
- The `h1::after` pseudo-element draws a 120px gradient bar (green to teal) below the title.
- Link icons are suppressed.

---

### `cover_c` -- Image Background with Overlay

**Purpose:** Full-bleed background image with a dark green gradient overlay; text anchored to the bottom.

**Directive:**

```markdown
<!-- _class: cover_c -->
```

**Layout:** Uses `![bg](url)` for the background image. A gradient overlay (`::before`) darkens from bottom (92% opacity) to top (30% opacity). Content is pushed to `flex-end` (bottom).

**Required Structure:**

```markdown
<!-- _class: cover_c -->
<!-- _header: "" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

![bg](https://example.com/photo.jpg)

# <!-- fit --> Presentation Title

###### Subtitle text

Author / Date / Notes
```

**Notes:**
- `h1` and `h6` have `z-index: 1` to sit above the overlay.
- `h1::after` draws a subtle 100px white translucent bar.
- Strong text and links render in translucent white.

---

## 3. Transition Page

### `trans`

**Purpose:** Section divider slide with a solid green background and centered white text.

**Directive:**

```markdown
<!-- _class: trans -->
```

**Layout:** Full green (`--color-primary`) background. `h2` is centered, white, 46px, with no border. `p` text is centered in translucent white. Pagination is hidden (`::after` content is empty).

**Minimal Example:**

```markdown
## 1. Section Title

<!-- _class: trans -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
```

**Notes:**
- When using `headingDivider: [2,3]`, the `## heading` automatically starts a new slide, so the directives apply to that same slide.
- No pagination counter is rendered on this slide.

---

## 4. Table of Contents

### `toc_a`

**Purpose:** Numbered table-of-contents slide with auto-incrementing circled numbers and a large watermark header.

**Directive:**

```markdown
<!-- _class: toc_a -->
```

**Layout:** The `ul` list gets custom styling: no bullet markers, a green top border (6px), rounded card with shadow. Each `li` is auto-numbered with a green circle via CSS `counter-increment`. The `header` renders as a giant outlined watermark text (900% font size, transparent fill, stroked border).

**Required Structure:**

```markdown
## Table of Contents

<!-- _class: toc_a -->
<!-- _header: "CONTENTS" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

- [Section One](#5)
- [Section Two](#10)
- [Section Three](#15)
- [Section Four](#20)
```

**Notes:**
- The `header` value (e.g., `"CONTENTS"`) becomes the background watermark text.
- List items can be plain text or Marp internal links (`[text](#page)`).
- The counter resets per slide automatically.

---

## 5. Column Layouts

All column layouts use CSS Grid. The heading (`h2` or `h3`) spans the full width as a top row. Content is placed inside `<div>` elements with specific class names.

### Div Class Names (Columns)

| Class   | Purpose                                    |
|---------|--------------------------------------------|
| `ldiv`  | Left column -- text/mixed content          |
| `rdiv`  | Right column -- text/mixed content         |
| `mdiv`  | Middle column (cols-3 only)                |
| `limg`  | Left column -- centered image container    |
| `rimg`  | Right column -- centered image container   |
| `mimg`  | Middle column -- centered image container  |

The `*img` variants add `display: flex; align-items: center; justify-content: center` so images are perfectly centered in the column.

### Available Column Classes

| Class         | Split Ratio | Grid Columns        |
|---------------|-------------|----------------------|
| `cols-2`      | 50% / 50%   | `1fr 1fr`           |
| `cols-2-64`   | 60% / 40%   | `60% 40%`           |
| `cols-2-73`   | 70% / 30%   | `70% 30%`           |
| `cols-2-46`   | 40% / 60%   | `40% 60%`           |
| `cols-2-37`   | 30% / 70%   | `30% 70%`           |
| `cols-3`      | 33% / 33% / 33% | `1fr 1fr 1fr`   |

### `cols-2` -- Equal Two Columns (50/50)

**Directive:**

```markdown
<!-- _class: cols-2 -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: cols-2 -->

<div class="ldiv">

#### Left Heading

- Left content item 1
- Left content item 2

</div>

<div class="rdiv">

#### Right Heading

- Right content item 1
- Right content item 2

</div>
```

### `cols-2-64` -- 60/40 Split

**Directive:**

```markdown
<!-- _class: cols-2-64 -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: cols-2-64 -->

<div class="ldiv">

#### Wider Left Column (60%)

Content here gets more horizontal space.

</div>

<div class="rdiv">

#### Narrower Right Column (40%)

Supporting content here.

</div>
```

### `cols-2-73` -- 70/30 Split

**Directive:**

```markdown
<!-- _class: cols-2-73 -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: cols-2-73 -->

<div class="ldiv">

Main content area (70% width).

</div>

<div class="rdiv">

Sidebar content (30% width).

</div>
```

### `cols-2-46` -- 40/60 Split

**Directive:**

```markdown
<!-- _class: cols-2-46 -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: cols-2-46 -->

<div class="limg">

![w:400](image.png)

</div>

<div class="rdiv">

#### Right-heavy content area (60%)

Detailed text content alongside the image.

</div>
```

### `cols-2-37` -- 30/70 Split

**Directive:**

```markdown
<!-- _class: cols-2-37 -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: cols-2-37 -->

<div class="ldiv">

#### Sidebar (30%)

| Metric | Value |
|--------|-------|
| A      | 100   |
| B      | 200   |

</div>

<div class="rdiv">

#### Main Content (70%)

Extended analysis and discussion goes here.

</div>
```

### `cols-3` -- Three Equal Columns

**Directive:**

```markdown
<!-- _class: cols-3 -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: cols-3 -->

<div class="ldiv">

#### Column 1

- Item A
- Item B

</div>

<div class="mdiv">

#### Column 2

- Item C
- Item D

</div>

<div class="rdiv">

#### Column 3

- Item E
- Item F

</div>
```

---

## 6. Row Layouts

All row layouts use CSS Grid with a full-width heading row on top, followed by a top panel and a bottom panel stacked vertically.

### Div Class Names (Rows)

| Class  | Purpose                                    |
|--------|--------------------------------------------|
| `tdiv` | Top panel -- text/mixed content            |
| `bdiv` | Bottom panel -- text/mixed content         |
| `timg` | Top panel -- centered image container      |
| `bimg` | Bottom panel -- centered image container   |

### Available Row Classes

| Class         | Split Ratio       | Grid Rows            |
|---------------|-------------------|----------------------|
| `rows-2`      | 50% / 50%         | `auto 1fr 1fr`      |
| `rows-2-64`   | 60% / 40%         | `auto 3fr 2fr`      |
| `rows-2-73`   | 70% / 30%         | `auto 7fr 3fr`      |
| `rows-2-46`   | 40% / 60%         | `auto 2fr 3fr`      |
| `rows-2-37`   | 30% / 70%         | `auto 3fr 7fr`      |

### `rows-2` -- Equal Two Rows (50/50)

**Directive:**

```markdown
<!-- _class: rows-2 -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: rows-2 -->

<div class="tdiv">

#### Top Section

| Col A | Col B | Col C |
|-------|-------|-------|
| 1     | 2     | 3     |

</div>

<div class="bdiv">

- Analysis point about the data above.
- Another observation.

</div>
```

### `rows-2-64` -- Top 60% / Bottom 40%

**Directive:**

```markdown
<!-- _class: rows-2-64 -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: rows-2-64 -->

<div class="tdiv">

#### Main Content (top 60%)

Detailed multi-paragraph content here.

</div>

<div class="bdiv">

#### Supporting Data (bottom 40%)

| Metric | Value |
|--------|-------|
| X      | 100   |

</div>
```

### `rows-2-73` -- Top 70% / Bottom 30%

**Directive:**

```markdown
<!-- _class: rows-2-73 -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: rows-2-73 -->

<div class="tdiv">

#### Primary content area (70%)

Large table or detailed content goes here.

</div>

<div class="bdiv">

**Key takeaway:** Summary sentence in the compact bottom strip.

</div>
```

### `rows-2-46` -- Top 40% / Bottom 60%

**Directive:**

```markdown
<!-- _class: rows-2-46 -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: rows-2-46 -->

<div class="tdiv">

#### Brief summary or conclusion (40%)

> Key insight blockquote here.

</div>

<div class="bdiv">

#### Detailed evidence table (60%)

| Dimension | Score | Benchmark |
|-----------|-------|-----------|
| A         | 4.5   | 3.8       |
| B         | 3.2   | 3.0       |

</div>
```

### `rows-2-37` -- Top 30% / Bottom 70%

**Directive:**

```markdown
<!-- _class: rows-2-37 -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: rows-2-37 -->

<div class="tdiv">

#### Overview (top 30%)

- Brief bullet points introducing the data below.

</div>

<div class="bdiv">

#### Detailed Data Table (bottom 70%)

| Year | Revenue | Growth | Margin |
|------|---------|--------|--------|
| 2023 | 100     | 10%    | 60%    |
| 2024 | 120     | 20%    | 62%    |
| 2025 | 150     | 25%    | 65%    |

</div>
```

---

## 7. Navigation Bar

### `navbar`

**Purpose:** Renders a horizontal navigation bar at the top of the slide, showing the current section highlighted and other sections grayed out.

**Directive:**

```markdown
<!-- _class: navbar -->
```

**Header Format:**

```markdown
<!-- _header: \ **Active Section** *Inactive 1* *Inactive 2* *Inactive 3* -->
```

**Format rules:**
- The header value must start with `\ ` (backslash + space).
- The **currently active** section name is wrapped in `**bold**` -- it renders as a white pill-shaped button with green text.
- All **inactive** section names are wrapped in `*italic*` -- they render as plain gray text.
- Each item is separated by a space.

**Layout:** The navbar is a 38px tall bar with a light green background (`--color-primary-lighter`), flex-centered with a 2.5em gap between items. The slide content gets extra top padding (52px) to avoid overlapping the bar.

**Minimal Example:**

```markdown
## Current Section Title

<!-- _class: navbar -->
<!-- _header: \ *Section A* **Section B** *Section C* *Section D* -->

- Content for this slide.
- The navbar shows "Section B" as the active tab.
```

**Notes:**
- Move the `**bold**` wrapper to whichever section is currently active as you progress through the deck.
- The `header::before` and `header::after` are set to empty to avoid any default Marp header decorations.

---

## 8. Callout Boxes

Callout boxes restyle Marp's `> blockquote` syntax into colored header+body card layouts with FontAwesome icons.

### Common Structure

All four callout classes share the same HTML structure. The **first paragraph** inside the blockquote becomes the colored header bar; all **subsequent paragraphs** become the light-gray body.

```markdown
> **Header Title**
> Body text paragraph 1.
> Body text paragraph 2.
```

**Important:** The first line of the blockquote (first `> paragraph`) becomes the colored title bar. Each subsequent `> paragraph` becomes a body row. Use a blank `>` line between paragraphs to separate them.

---

### `bq-green`

**Purpose:** Green callout box for insights, recommendations, or positive highlights.

**Icon:** Lightbulb (FontAwesome `\f0eb`)

**Header color:** `--color-primary` (#1a5c38)

**Directive:**

```markdown
<!-- _class: bq-green -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: bq-green -->

> **Key Insight: Growth Opportunity**
> The data services segment shows 22% CAGR with only 18% penetration, indicating significant untapped potential.

- Additional bullet points outside the callout.
```

---

### `bq-red`

**Purpose:** Red callout box for warnings, risks, or critical alerts.

**Icon:** Exclamation circle (FontAwesome `\f06a`)

**Header color:** `--color-emphasis` (#8b3a2a)

**Directive:**

```markdown
<!-- _class: bq-red -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: bq-red -->

> **Risk Alert: Competitive Pressure**
> Top-tier companies are accelerating M&A activity. Mid-size firms face a 24-month window before consolidation reshapes the market.
```

---

### `bq-blue`

**Purpose:** Blue/teal callout box for informational notes, strategies, or neutral highlights.

**Icon:** Brain (FontAwesome `\f518`)

**Header color:** `--color-accent` (#0c4c52)

**Directive:**

```markdown
<!-- _class: bq-blue -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: bq-blue -->

> **Strategic Direction: Platform Transformation**
> Transition from a product company to a platform company by opening core APIs and building an ISV ecosystem with 500+ partners.
```

---

### `bq-black`

**Purpose:** Dark/black callout box for summaries, conclusions, or executive overviews.

**Icon:** Comment-alt (FontAwesome `\f5ad`)

**Header color:** `#3c3c3c`

**Directive:**

```markdown
<!-- _class: bq-black -->
```

**Minimal Example:**

```markdown
## Slide Title

<!-- _class: bq-black -->

> **Executive Summary**
> Three core risks have been identified, each with specific mitigation measures and early-warning trigger conditions.

- Macro risk (High impact / Medium probability)
- Technology risk (High impact / Medium probability)
- Competitive risk (Medium impact / High probability)
```

---

## 9. Footnote

### `footnote`

**Purpose:** Splits the slide into a main content area (top) and a footnote area (bottom) separated by a thin horizontal rule.

**Directive:**

```markdown
<!-- _class: footnote -->
```

**Required HTML Structure:**

```html
<div class="tdiv">
  (main content with headings, lists, etc.)
</div>

<div class="bdiv">
  (footnote text -- renders at 80% font size in gray)
</div>
```

**Layout:** Uses CSS Grid with `grid-template-rows: 1fr auto`. The `bdiv` has a `::before` pseudo-element that draws a 25%-width top border line as a visual separator. Text inside `bdiv` is 80% size and colored `--color-text-secondary`.

**Minimal Example:**

```markdown
## Research Methodology

<!-- _class: footnote -->

<div class="tdiv">

#### Data Sources

- Primary data from 30+ expert interviews covering investors, executives, and technical leads.
- Market size figures cross-validated against public filings and industry white papers.

</div>

<div class="bdiv">

1. China Academy of Information and Communications Technology. Digital Economy White Paper (2025).
2. Forecast model assumptions detailed in Appendix B.

</div>
```

**Notes:**
- The `tdiv` can contain headings (`h2`-`h5`), which receive adjusted margins (`margin-bottom: 0.8em`, `margin-top: -0.6em`).
- Combine with `navbar` for a footnoted slide with navigation (see [Combinability](#14-combinability)).

---

## 10. Font Sizes

### `smalltext`

**Purpose:** Reduces font size for dense content slides (tables, long lists, detailed data).

**Directive:**

```markdown
<!-- _class: smalltext -->
```

**Effect on elements:**

| Element      | Size Change |
|--------------|-------------|
| `p`, `ul`, `ol`, `table`, `blockquote` | 85% of base |
| `code`       | 90%         |
| `strong`     | 100% (unchanged) |
| `pre`        | 80%         |

**Minimal Example:**

```markdown
## Dense Data Slide

<!-- _class: smalltext -->

| Year | Revenue | Growth | Margin | NPS | NDR  |
|------|---------|--------|--------|-----|------|
| 2023 | 4,200   | 10.2%  | 62%    | 58  | 105% |
| 2024 | 4,850   | 15.5%  | 64%    | 62  | 112% |
| 2025 | 5,400   | 11.3%  | 65%    | 65  | 118% |

- This text will appear smaller than the default 24px body size.
```

---

### `largetext`

**Purpose:** Increases font size for slides with minimal content that should have greater visual impact.

**Directive:**

```markdown
<!-- _class: largetext -->
```

**Effect on elements:**

| Element      | Size Change |
|--------------|-------------|
| `p`, `ul`, `ol`, `table`, `blockquote` | 115% of base |
| `code`       | 90%         |
| `strong`     | 100% (unchanged) |
| `pre`        | 105%        |

**Minimal Example:**

```markdown
## Key Takeaway

<!-- _class: largetext -->

- Companies that complete digital transformation first gain a **20% market share advantage**.
- Customer retention rates are **15 percentage points higher** for digitally mature firms.
```

---

## 11. Last Page

### `lastpage`

**Purpose:** Closing slide with a solid green background and centered white text, suitable for "Thank You" or Q&A endings.

**Directive:**

```markdown
<!-- _class: lastpage -->
```

**Layout:** Full green background. `h2` is white, 48px, no border. `h6` is white, 48px, bold. `p` is translucent white (75% opacity), 22px. Pagination is suppressed. Link icons are suppressed.

**Minimal Example:**

```markdown
---

<!-- _class: lastpage -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

## Thank You

Questions and discussion welcome
```

---

## 12. Caption

### `caption`

**Purpose:** Adds a centered, smaller, gray caption below an image or chart, typically used for figure labels or source attributions.

**Directive:**

```markdown
<!-- _class: caption -->
```

**Required HTML Structure:**

The caption text must be inside a `<div class="caption">` element.

```html
<div class="caption">
  Figure 1: Market size trend 2020-2025
</div>
```

**Styling:** `padding-top: 12px`, `text-align: center`, `font-size: smaller`, `color: --color-text-secondary`.

**Minimal Example:**

```markdown
## Market Overview

<!-- _class: caption -->

![w:800](chart.png)

<div class="caption">

Figure 1: Enterprise services market size (in billions RMB), 2020-2025

</div>
```

---

## 13. Image Alignment

Images can be aligned using special tags in the alt text. These are handled by CSS attribute selectors on `img[alt]`.

| Tag in Alt Text | CSS Rule                          | Effect                       |
|-----------------|-----------------------------------|------------------------------|
| `#l`            | `float: left`                     | Float image to the left      |
| `#r`            | `float: right`                    | Float image to the right     |
| `#c`            | `display: block; margin: auto`    | Center the image             |

### Usage

Place the tag anywhere in the image's alt text:

```markdown
![Photo #l](image.png)
![Chart #r w:400](chart.png)
![Diagram #c](diagram.png)
```

**Notes:**
- These tags can be combined with Marp's width/height directives (e.g., `w:400`, `h:300`).
- The `#l` and `#r` tags cause text to wrap around the image.
- The `#c` tag centers the image as a block element.

---

## 14. Combinability

Multiple classes can be combined by separating them with spaces in the `_class` directive. Below is a reference of which classes are designed to work together.

### Combination Syntax

```markdown
<!-- _class: classA classB -->
```

### Compatible Combinations

| Primary Class | Can Combine With | Notes |
|---------------|------------------|-------|
| `cols-2` / `cols-2-*` / `cols-3` | `navbar` | Navbar sits above the grid; grid content shifts down |
| `rows-2` / `rows-2-*` | `navbar` | Navbar sits above the grid; grid content shifts down |
| `cols-2` / `cols-2-*` / `cols-3` | `smalltext` | Reduces text size inside all column divs |
| `rows-2` / `rows-2-*` | `smalltext` | Reduces text size inside all row divs |
| `cols-2` / `cols-2-*` / `cols-3` | `largetext` | Increases text size inside all column divs |
| `rows-2` / `rows-2-*` | `largetext` | Increases text size inside all row divs |
| `bq-green` / `bq-red` / `bq-blue` / `bq-black` | `navbar` | Navbar on top, callout box in body |
| `footnote` | `navbar` | Navbar on top, footnote separator at bottom |
| `navbar` | `smalltext` | Smaller body text with navigation |
| `navbar` | `largetext` | Larger body text with navigation |
| `caption` | `cols-2` / `cols-2-*` | Caption div inside a column div |

### Example: `navbar` + `cols-3`

```markdown
## Three-Phase Methodology

<!-- _class: cols-3 navbar -->
<!-- _header: \ **Phase 1** *Phase 2* *Phase 3* -->

<div class="ldiv">

#### Diagnosis

- Industry scanning
- Current-state assessment

</div>

<div class="mdiv">

#### Analysis

- Market sizing (TAM/SAM/SOM)
- Competitive landscape

</div>

<div class="rdiv">

#### Recommendations

- Scenario-based strategy options
- Roadmap with milestones

</div>
```

### Example: `bq-green` + `navbar`

```markdown
## Short-Term Strategy

<!-- _class: bq-green navbar -->
<!-- _header: \ *Background* *Market* *Competition* **Strategy** *Risks* -->

> **Core Objective: Focus and Efficiency**
> Complete product line rationalization within 6 months, concentrating 80% of resources on the top 3 scenarios.

- Product: Evaluate ROI across all lines, cut low-performers.
- Operations: Build a lightweight data platform for real-time KPI monitoring.
```

### Example: `footnote` + `navbar`

```markdown
## Data Source Notes

<!-- _class: footnote navbar -->
<!-- _header: \ *Background* *Market* *Competition* *Strategy* **Risks** -->

<div class="tdiv">

#### About the Data

- Market size data sourced from CAICT Digital Economy White Paper (2025).
- Growth forecasts built on bottom-up CAGR trend models with expert adjustments.

</div>

<div class="bdiv">

1. CAICT. Digital Economy White Paper (2025). Beijing, 2025.
2. See Appendix B for full model assumptions.

</div>
```

### Classes That Should NOT Be Combined

| Combination | Reason |
|-------------|--------|
| `cover_a` + `cover_b` + `cover_c` | Each cover has conflicting absolute positioning and background styles |
| `trans` + any layout class | Transition slides are meant to be simple centered text only |
| `lastpage` + any layout class | Last page is a simple centered closing slide |
| `toc_a` + column/row layouts | TOC has its own specialized list styling |
| `cols-*` + `rows-*` | Column and row grids conflict with each other |
| `footnote` + `rows-*` | Both define grid layouts that would conflict |

---

## Quick Reference Card

```
COVERS:       cover_a | cover_b | cover_c
DIVIDERS:     trans | lastpage
TOC:          toc_a
COLUMNS:      cols-2 | cols-2-64 | cols-2-73 | cols-2-46 | cols-2-37 | cols-3
ROWS:         rows-2 | rows-2-64 | rows-2-73 | rows-2-46 | rows-2-37
NAVIGATION:   navbar
CALLOUTS:     bq-green | bq-red | bq-blue | bq-black
UTILITIES:    footnote | caption | smalltext | largetext
IMG ALIGN:    #l (left) | #r (right) | #c (center) -- in alt text
```

### Color Palette

| Variable                  | Hex       | Usage                          |
|---------------------------|-----------|--------------------------------|
| `--color-primary`         | `#1a5c38` | Headings, borders, green fills |
| `--color-primary-dark`    | `#0f3d25` | Overlay gradients              |
| `--color-primary-light`   | `#278050` | Accent elements                |
| `--color-primary-lighter` | `#e6f2ec` | Navbar background, light fills |
| `--color-accent`          | `#0c4c52` | h4/h5 headings, bq-blue       |
| `--color-accent-light`    | `#1a7a6d` | Links                          |
| `--color-emphasis`        | `#8b3a2a` | Bold text, bq-red              |
| `--color-text`            | `#1a1a1a` | Body text                      |
| `--color-text-secondary`  | `#6b6b6b` | Footer, captions, footnotes    |
| `--color-border`          | `#c8c8c8` | Table borders, dividers        |
| `--color-bg-light`        | `#f5f8f6` | Code blocks, table stripes     |

### Font Stack

| Variable                | Fonts                                         |
|-------------------------|-----------------------------------------------|
| `--font-family-main`    | Calibri, KaiTi, sans-serif                    |
| `--font-family-title`   | Calibri, KaiTi, sans-serif                    |
| `--font-family-code`    | Fira Code, Consolas, monospace                |
