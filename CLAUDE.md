# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Awesome-Marp-AI is a toolkit for AI-powered PDF to Marp presentation conversion. It provides a consulting-grade theme, PDF extraction, quantified content limits, and 12 interactive components. Any AI can use the docs to generate presentations; Claude Code gets a dedicated slash command.

## Key Commands

- PDF extraction: `python scripts/extract_pdf.py <pdf_path> [output_dir]`
- HTML export: `marp <file>.md --theme-set themes/am_consulting.scss --html -o <file>.html`
- PDF export: `marp <file>.md --theme-set themes/am_consulting.scss --html --pdf --allow-local-files -o <file>.pdf`
- Must use `--theme-set` (not `--theme`) because SCSS uses `@import 'default'`

## Critical Rules

- Content must NEVER overflow page boundaries. Always check `docs/content-limits.md` for limits before choosing layouts and writing content.
- Prefer `cols-2` layouts over `rows-2` layouts (rows have very limited vertical capacity).
- Asymmetric column layouts: the narrow side needs dense, compact content (indicators, small tables, KPI lists); the wide side gets the main narrative.
- After generating output, always tell the user exact file paths (.md, .html, .pdf) and ask whether modifications are needed.
- Theme uses CSS Grid layouts with div classes: `ldiv`/`rdiv` (columns), `tdiv`/`bdiv` (rows), `mdiv` (middle in cols-3).
- Image div variants (`limg`/`rimg`/`mimg`/`timg`/`bimg`) center images with flexbox.
- Interactive components with JS only work in HTML output. For PDF output, they degrade to static display.

## Documentation

- `docs/sop.md` -- Full generation SOP (start here for the PDF -> PPT workflow)
- `docs/content-limits.md` -- Quantified content limits per layout (DOE-tested)
- `docs/theme-reference.md` -- All CSS class references, combinability rules, examples
- `components/` -- 12 interactive component HTML files (6 CSS-only + 6 JS-interactive)

## Architecture

- **Theme**: `themes/am_consulting.scss` -- Self-contained, imports Marp `default` directly. Green consulting palette (#1a5c38 primary). Fonts: Calibri + KaiTi.
- **PDF parser**: `scripts/extract_pdf.py` -- Uses PyMuPDF (fitz), outputs JSON (`extracted.json`) + images to `output/images/`.
- **Components**: CSS-only (progress-bars, hover-cards, animated-counters, timeline, tooltips, charts-css) + JS-interactive (sortable-table, collapsible, tab-switch, modal-popup, filter-list, flip-card). All self-contained with inline styles and scripts. Use `{{PLACEHOLDER}}` parameters for AI to fill.
- **Skill**: `.claude/commands/generate-ppt.md` -- Wraps the full SOP workflow into a `/generate-ppt` slash command.

## Slide Class Quick Reference

```
COVERS:     cover_a | cover_b | cover_c
DIVIDERS:   trans | lastpage
TOC:        toc_a
COLUMNS:    cols-2 | cols-2-64 | cols-2-73 | cols-2-46 | cols-2-37 | cols-3
ROWS:       rows-2 | rows-2-64 | rows-2-73 | rows-2-46 | rows-2-37
NAVIGATION: navbar
CALLOUTS:   bq-green | bq-red | bq-blue | bq-black
UTILITIES:  footnote | caption | smalltext | largetext
IMG ALIGN:  #l (left) | #r (right) | #c (center) -- in alt text
```

Classes can be combined: e.g. `<!-- _class: cols-2 navbar smalltext -->`. Do NOT combine column + row layouts, or multiple cover types.
