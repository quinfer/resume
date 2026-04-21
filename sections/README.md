# `sections/` — Shared content partials

Included via Quarto `{{< include >}}` by the files in `src/`.

## Convention

- `_name.md` — pure markdown; no R chunks.
- `_name.qmd` — contains R chunks that execute in the parent document's context.
- Every partial is a **body block** only. It does **not** open with a header (`#` / `##`). The parent `src/*.qmd` file owns the document outline and writes the header immediately before the include, so each variant can choose its own heading text and level.
- Relative paths inside partials (e.g. `read.csv("../data/Grant_income.csv")`) are resolved relative to the **parent** file's location at render time, which is `src/`.

## What is shared vs. what is not

The four CV variants in `src/` differ intentionally in register, audience, and depth. The partials here cover only the **factual spine** — items that must be identical across variants or the public record diverges. Editorial blocks (personal statement, executive summary, value proposition, teaching philosophy) remain inline in each variant because they are deliberately audience-specific.

## Chunk-label rule

R chunks inside partials are labelled with a `part-` prefix (e.g. `part-grants-table`) so they do not collide with inline chunks named `setup` or `tbl-*` in the parent file.
