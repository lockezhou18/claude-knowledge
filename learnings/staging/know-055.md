---
id: know-055
track: knowledge
status: active
name: markitdown converts DOCX/XLSX/PPTX to clean markdown for LLM consumption
description: Microsoft's markitdown tool converts Office docs to markdown. Use for design docs, spreadsheets, slides that Claude can't read natively.
created: 2026-04-11
last_verified: 2026-04-11
repos: [memory-migration]
tags: [markitdown, docx, xlsx, pptx, tool, conversion]
use_count: 0
outcome_score: 0.0
rot_rate: slow
---

When needing to feed Office documents (DOCX, XLSX, PPTX) into Claude, use markitdown to convert them first. Install with `pip3 install "markitdown[all]"`. Claude's built-in Read handles PDFs natively, but DOCX/XLSX/PPTX need markitdown.

**Key results from eval:** DOCX preserves heading hierarchy + tables (241 lines from eng design doc). XLSX renders clean markdown tables. URLs work well for static pages.

**How to apply:** `markitdown file.docx` or pipe to save: `markitdown file.docx > memory/projects/<project>/docs/filename.md`
