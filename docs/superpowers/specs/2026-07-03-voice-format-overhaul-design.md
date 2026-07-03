# MindMusk Voice & Format Overhaul — Design

**Date:** 2026-07-03
**Status:** Approved (pending final spec review)
**Goal:** Make MindMusk's responses read like the reference ChatGPT "MindMusk" conversation — varied structure driven by the question, real visual hierarchy, grounded in a concrete style example — instead of the current flat, uniformly-formatted output.

---

## Diagnosis (first principles)

The reference conversation's style comes from three separate systems, each of which we're currently missing or only half-implementing:

1. **Writing habit** — GPT's register naturally mixes free reasoning (single-sentence paragraphs for pacing) with structured enumeration, and follows a scaffold: open with a stance → reason/enumerate → close with a named synthesis + one provocative question. Claude defaults to flowing prose or uniform bullets unless told otherwise. *Prompt problem.*
2. **Real markdown hierarchy** — ChatGPT's client renders actual heading levels (`##`, `###`) at genuinely different type scales. Our frontend only understands `**bold**` and `- bullets`; every "header" the model writes gets wrapped in `**` and rendered at one fixed size, so a major section and a minor aside look identical. *Rendering problem — this is the root cause of "all headings look the same."*
3. **A grounded example** — telling the model "vary your structure" abstractly is weak steering. The actual transcript, retrievable via RAG, is strong steering.

All three must ship together. Fixing the prompt alone produces good markdown that still renders flat. Fixing the renderer alone correctly displays what is still flat output.

---

## Component A — Persona prompt rewrite

**File:** `backend/orchestrator.py` (`PRESENTATION_PROMPT`)

Replace the single rigid "Label — Description, 2-4 short lines" template with:

- **Real markdown**: `## ` for major section headers (used when the response enumerates a framework — numbered items get `## 1. Idea Selection` style headers), `### ` for an occasional minor sub-header, `**bold**` reserved for inline emphasis on specific words/phrases — never as a fake header substitute.
- **Three structural registers**, chosen by the model per-question (no explicit routing field — confirmed decision):
  - *Conversational-essay*: opinion/reflection questions. Opens with a stance sentence, reasons in short paragraphs and isolated single-line "punch" paragraphs, no forced headers.
  - *Numbered framework*: "what are the bottlenecks/reasons/steps" questions. `##`-level numbered headers, each followed by 1-3 supporting lines or `- ` bullets.
  - *Hybrid*: opens conversationally, transitions into a numbered breakdown, closes with a named synthesis + one question. This is the dominant shape in the reference transcript.
- **Permit reasoning transitions** between structured chunks ("Let's reason from first principles.", "Now ask:") — the current "never write paragraphs" rule is removed; short paragraphs are allowed when they serve pacing, not banned outright.
- **Scaffold**: every substantive response should roughly open with a stance/frame, develop the idea, and close with either a direct answer or a synthesis + one provocative question — not mechanically on every message (e.g. a one-line factual answer doesn't need the full scaffold).

MODE_1 (SOCRATIC) and MODE_2 (FIRST PRINCIPLES) routing is untouched — this changes *how* MODE_2 responses are structured, not the routing logic itself.

---

## Component B — True markdown renderer

**File:** `frontend/app/page.tsx` (`MarkdownBlock`, `renderInline`)

Current renderer treats the first line of any blank-line-separated block as "the header" and renders it at one fixed size regardless of whether it's a major section or a minor aside. Replace with a renderer that recognizes:

| Markdown | Render |
|---|---|
| `## Heading` | Largest tier — bigger, semibold, extra top margin before it (except first block) |
| `### Heading` | Middle tier — modestly larger/semibold, smaller top margin |
| `**bold**` (inline, not a whole-line header) | Inline emphasis — bold, body size |
| `- item` / `• item` | Bullet line, body size |
| Plain line | Body text, body size |
| A block containing exactly one plain line | Slightly more vertical margin than a multi-line block, to reproduce the reference transcript's staccato pacing for isolated punch-lines |

This is an extension of the existing `MarkdownBlock`/`renderInline` functions built for the earlier bold/bullet fix — not a rewrite from scratch. Existing inline-bold and bullet handling stays; heading-level detection and the punch-line spacing rule are additions.

---

## Component C — RAG ingestion of the reference transcript

**New file:** `knowledge_base/conversation_style/chatgpt_reference_conversations.md` — the pasted transcript, saved verbatim as the source of truth for future re-ingestion.

**Chunking:** by natural section boundaries (blank-line-separated blocks / heading boundaries in the source), not the fixed 1600-char/320-overlap chunker used elsewhere in layer 5 — a fixed-size chunker risks cutting a numbered item or a reasoning transition mid-thought, destroying exactly the structural pattern we're trying to surface.

**Embedding:** same model as the rest of layer 5 (`voyage-3-lite`, Voyage AI). New chunks are **appended** to the existing `vector_db/fifth__embeddings.npy` / `fifth__metadata.json` (not regenerated from scratch) — load existing arrays, embed only the new chunks, concatenate, save. This avoids re-spending API calls on the existing 103 chunks and avoids touching `elon_qa_pairs.jsonl` / `elon_speech_patterns.md`, which stay as-is.

**Metadata:** new chunks tagged `"source": "chatgpt_reference_conversations"`, `"layer": "fifth"`, so they're retrieved through the exact same path as the rest of layer 5 — no special-casing in `retriever.py`.

**Deploy:** re-commit updated `vector_db/fifth__*` files and push — Railway picks up the new vectors on redeploy, same as the earlier 5-layer ingestion.

---

## Data flow (unchanged shape, changed content)

```
user message
  → route_query (Sonnet, unchanged: MODE_1/MODE_2 + layer weights + reformulated query)
  → retriever.retrieve() (unchanged mechanism; now also returns chatgpt_reference_conversations
     chunks when semantically relevant)
  → PRESENTATION_PROMPT (rewritten: real markdown, 3 registers, scaffold)
  → Sonnet streams response with real ## / ### / **bold** / - bullets
  → frontend MarkdownBlock (rewritten: renders heading levels distinctly)
```

---

## Testing / verification plan

1. **Local orchestrator test** (as done for the earlier SSE fix): run 3 sample questions locally — one opinion-style ("what's your take on X"), one list-style ("what are the bottlenecks in X"), one short factual — confirm each produces markdown appropriate to its register and that `##` headers actually appear where expected.
2. **Retrieval check**: query with wording close to the pasted transcript's topics (e.g. "what bottlenecks appear when content becomes abundant") and confirm `chatgpt_reference_conversations` chunks are retrieved (`layer: fifth`, `source: chatgpt_reference_conversations`).
3. **Frontend render check**: via `preview_*` tools, send a numbered-framework-style question, screenshot, confirm `##` headers are visually distinct from `**bold**` inline emphasis and from body text — three distinguishable tiers, not one.
4. **Regression check**: confirm the SOCRATIC-mode drilling-question behavior and the earlier SSE-framing fix (no dropped text) still hold — this touches the same prompt and renderer files.
5. **Live deploy check**: after push, re-run the same three sample questions against the deployed Railway backend and the deployed Vercel frontend.

---

## Global constraints

- Do not overwrite `elon_qa_pairs.jsonl` or `elon_speech_patterns.md` — append-only to layer 5.
- Do not touch `route_query` / MODE_1 vs MODE_2 classification logic.
- Preserve the JSON-encoded SSE chunk format (fixed earlier this session) — chunks must remain JSON-encoded strings server-side and JSON-decoded client-side.
- Preserve existing `**bold**` inline and `- bullet` rendering — extend, don't replace.
- No explicit `structure_mode` routing field — the presentation model chooses register itself (confirmed decision).
