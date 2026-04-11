---
name: markitdown
description: Convert documents (DOCX, XLSX, PPTX, PDF, HTML, URLs) to clean Markdown for LLM consumption. Use when the user shares or references Office docs, spreadsheets, slide decks, or web pages that need to be read and understood.
allowed-tools: Bash(markitdown:*), Bash(pip3 install*markitdown*), Bash(which markitdown*)
---

# Document → Markdown Converter

Convert any document format to clean Markdown that Claude can read and reason about.

## When to Use

- User shares a `.docx`, `.xlsx`, `.pptx`, `.pdf` file
- User asks to "read this doc" or "what's in this spreadsheet"
- User references a design doc, PRD, or slide deck
- Need to ingest a web page as structured text
- Converting documents for storage in memory/ or learnings/

## Auto-install

```bash
which markitdown 2>/dev/null || pip3 install "markitdown[all]"
```

## Usage

### Convert a file
```bash
markitdown path/to/file.docx
markitdown path/to/file.xlsx
markitdown path/to/file.pptx
markitdown path/to/file.pdf
```

### Convert a URL
```bash
markitdown "https://example.com/page"
```

### Convert and save to memory
```bash
markitdown path/to/design-doc.docx > ~/claude-knowledge/memory/projects/connected-projects/design-doc.md
```

### Preview first N lines
```bash
markitdown path/to/file.docx | head -50
```

## Format-Specific Notes

### DOCX (Best results)
- Preserves heading hierarchy, tables, bullet lists, links
- Much better than copy-pasting from Google Docs
- Images are described if LLM vision is configured

### XLSX
- Each sheet becomes a `## SheetName` section
- Data rendered as markdown tables
- Empty sheets are skipped

### PPTX
- Each slide becomes a section
- Text, tables, and speaker notes preserved
- Images described if LLM vision configured

### PDF
- Text extraction via pdfminer
- Note: Claude's built-in Read tool handles PDFs natively — use markitdown only when Read fails or for batch processing

### URL / HTML
- Fetches page and converts HTML to markdown
- Strips navigation, ads, scripts
- For JS-heavy pages: use playwright-cli instead (renders JS first)

## Integration with Memory System

When converting a document that should persist across sessions:

```bash
# Convert and save to project memory
markitdown "PRD.docx" > ~/claude-knowledge/memory/projects/connected-projects/prd.md

# Convert and save to reference
markitdown "API-Reference.xlsx" > ~/claude-knowledge/memory/reference/api-reference.md
```

Add YAML frontmatter to the saved file for dream.py indexing:
```markdown
---
name: Phase 2 PRD
description: Product requirements for Connected Projects Phase 2 bidirectional sync
type: reference
source: PRD_ LinkedIn Connected Projects (2).docx
converted: 2026-04-11
---
```

## Comparison with Other Tools

| Task | Use markitdown | Use instead |
|------|---------------|-------------|
| Read DOCX/XLSX/PPTX | Yes — only option | — |
| Read PDF | Works, but... | Claude's Read tool (native, no install) |
| Read URL (static) | Yes — clean output | — |
| Read URL (JS-heavy) | No | playwright-cli (renders JS) |
| Read image text | Optional (needs LLM) | Claude's Read tool (native vision) |

## Troubleshooting

- **pydub warning about ffmpeg**: harmless, ignore. Only affects audio conversion.
- **Empty output for XLSX**: the sheet may be empty. Check with `markitdown file.xlsx | wc -l`.
- **URL fails**: site may block bots. Fall back to playwright-cli or WebFetch.
- **Import error**: run `pip3 install "markitdown[all]"` for all format support.
