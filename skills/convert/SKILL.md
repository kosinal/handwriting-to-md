---
name: convert
description: Use when converting a handwritten PDF (reMarkable export, tablet notes, scanned handwriting, hand-drawn diagrams or schemas) into editable Markdown, or when the user asks to transcribe handwritten notes into .md.
arguments: [file]
argument-hint: <file.pdf>
---

**File to convert:** `$file`

If that is empty, use the PDF the user named. If they named none, list the PDFs in the current folder and ask which one.

# Handwriting PDF to Markdown

## Overview

Handwritten PDF exports are drawings with no text layer. Read the pages directly (Read tool on the PDF, or the attached file) and write the Markdown yourself. No OCR is needed.

**Core principle:** transcribe what the author wrote, not what you think they meant.

**Paths:** `SKILL_DIR` is `${CLAUDE_SKILL_DIR}` and `DATA_DIR` is `${CLAUDE_PLUGIN_DATA}`. If either still shows `${...}`, find this skill's folder yourself and treat `DATA_DIR` as unavailable.

## Step 1: Load config

Read `DATA_DIR/config.yaml`.

If it is missing, ask the user once how diagrams should be output, then write the file:

```yaml
diagrams: mermaid   # mermaid | image
```

- `mermaid`: diagrams become editable Mermaid code blocks.
- `image`: diagrams become cropped PNGs embedded in the Markdown.

If `DATA_DIR` is unavailable or not writable, use the answer for this conversation only. If the user asks to switch diagram mode, update the file.

## Step 2: Read and transcribe

Read the whole PDF (use `pages` for more than 10 pages). Write `<pdf-name>.md` next to the PDF.

| On the page | In Markdown |
|---|---|
| Title / heading line | `#` / `##` heading |
| Dash or bullet lists | `-` list, nesting kept |
| Arrow from a note (`→ pip install x`) | nested list item or `→` on its own line |
| Commands, code, package names | `inline code` or a fenced block |
| Free-standing notes | `-` list |
| Highlighter / underline | **bold** |
| Math inside a sentence | `$...$` (see Math) |
| Math on its own line | `$$...$$` block (see Math) |
| Boxes + arrows (diagram) | per config (Step 3) |
| Doodles with no information | skip |

## Step 3: Diagrams

**mermaid:** `flowchart TD`. One node per box, with its list items inside the label (`A["Plotting<br>- matplotlib"]`). Nested boxes become `subgraph` (untitled outer box: `subgraph G[" "]`). Every arrow becomes an edge. Quote all labels.

**image:** uses `SKILL_DIR/render.py` (needs `pypdfium2` and `pillow`). Run it with `uv run SKILL_DIR/render.py ...` if `uv` exists, otherwise `python3 SKILL_DIR/render.py ...`. Install the two packages only if the import fails.
1. `render <pdf> <pdf-dir>/<pdf-name>.assets` renders `page-N.png`.
2. Read `page-N.png` and take crop coordinates from it, not from the PDF preview (sizes differ). Crop each diagram: `crop page-N.png <left> <top> <width> <height> <assets>/diagram-K.png`.
3. Read the crop. If it cuts a box or includes surrounding text, adjust and repeat.
4. Embed it with `![diagram K](<pdf-name>.assets/diagram-K.png)` and delete the `page-N.png` files.

## Math

Write formulas as LaTeX, exactly as written: same variables, notation and order of terms.

- Fractions `\frac{a}{b}`, roots `\sqrt{x}`, limits on sums and integrals `\sum_{i=1}^{n}`, matrices `\begin{pmatrix}...\end{pmatrix}`.
- Consecutive steps of one derivation: one `$$\begin{aligned} ... \end{aligned}$$` block, aligned on `&=`.
- Never simplify, solve, or fix a step, even if it looks wrong.
- Unclear symbol (`1` vs `l`, `x` vs `\times`, exponent or not): uncertain-word rule, with `[?]` after the closing `$`.

## Step 4: Uncertain words

When you can't read a word for sure:

1. Zoom in: `render` the page into a temp folder, `crop` the spot, Read the crop. Delete the temp files after. If `render.py` can't run, skip this step.
2. If it could be a real term (product, library, acronym, command), search the web to confirm the spelling.
3. Still unclear: write your best reading followed by `[?]` (`QT Cards[?]`) and keep going.
4. After the draft is written, ask the user about every `[?]` in one message: quote each line, the literal letters, and your best reading. Update the file with the answers and remove all `[?]`.

Never silently "correct" a word.

## Keep the author's wording

- Keep abbreviations exactly as written (`OA` stays `OA`, even if `OS` seems more likely).
- Keep the language mix (Czech and English on one line stays mixed). Don't translate.
- Keep the author's spelling of terms (`QT` stays `QT`, not `Qt`).
- Don't add explanations, summaries, or missing words.

## Common mistakes

| Mistake | Fix |
|---|---|
| "Fixing" an abbreviation or term | Write what's on the page |
| Correcting the author's math | Transcribe the error as written |
| Guessing an unclear word and moving on | Web search, then ask |
| Mermaid label with `(`, `/` or `&` breaks rendering | Quote every label |
| Image crop cuts a box | Read the crop, widen it |
