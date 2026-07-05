# MindMusk — Technical Architecture (MVP)

**Version:** 2.0  
**Date:** 2026-07-01  
**Status:** MVP Planning

---

## 1. System Overview

```
┌─────────────────────────────────────────────────────────┐
│                     USER BROWSER                        │
│              Next.js Chat Interface                     │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP / SSE (streaming) — direct call, no proxy
┌─────────────────────▼───────────────────────────────────┐
│                  FASTAPI BACKEND                        │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Query Pipeline                      │  │
│  │  1. Embed user query                             │  │
│  │  2. Retrieve from ALL 3 layers in parallel       │  │
│  │  3. Filter by similarity threshold (≥ 0.75)      │  │
│  │  4. Assemble context + system prompt             │  │
│  │  5. Stream response (GPT-4o-mini)                │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ChromaDB loaded into memory at startup (~60MB)         │
└─────────────────────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│         VECTOR STORE — ChromaDB (persistent dir)        │
│                                                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐  │
│  │ 1st Order   │ │ 2nd Order   │ │   3rd Order     │  │
│  │ (raw books) │ │(per-book    │ │ (4 thematic     │  │
│  │  5 books    │ │ synthesis)  │ │  syntheses)     │  │
│  └─────────────┘ └─────────────┘ └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Key architectural decisions:**
- No query routing LLM call — all 3 layers retrieved in parallel, response model weighs relevance
- ChromaDB with persistent local directory — ~60MB total, fits in memory, no infrastructure needed
- Browser calls FastAPI directly (CORS enabled) — no Next.js proxy layer
- Similarity threshold of 0.75 — irrelevant chunks never reach the model

---

## 2. Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | Next.js 14 (React) | Fast to build, SSE streaming, easy deploy on Vercel |
| Backend | FastAPI (Python) | Best AI/ML ecosystem, async, CORS support |
| Vector DB | ChromaDB (persistent dir) | ~60MB total data, loads into memory at startup, zero infrastructure |
| Embeddings | OpenAI text-embedding-3-small | $0.02/1M tokens — cheapest available |
| PDF Parsing | PyMuPDF (fitz) | Fast, accurate, battle-tested on complex PDFs |
| LLM — Synthesis (offline, one-time) | Claude claude-sonnet-4-6 | Highest quality for knowledge base generation |
| LLM — Response Generation (online) | GPT-4o-mini | Best quality/cost ratio for per-query responses |
| Hosting | Vercel (frontend) + Railway (backend + persistent volume) | Zero infra overhead for MVP |

**Why ChromaDB (not Supabase pgvector):**  
The entire knowledge base — 5 books across 3 layers — produces roughly 10,000 chunks at ~6KB per embedding. Total: ~60MB. That fits in RAM. ChromaDB loads it at startup and all similarity searches run in memory — no network round trips, no SQL, no infrastructure. Supabase pgvector makes sense at millions of chunks across thousands of users. For an MVP with 5 books it is pure overhead. On Railway, mount a persistent volume at the ChromaDB directory path — the data survives deploys.

**Why no separate routing model:**  
The original design ran GPT-4o-mini twice per query — once to classify the query type, once to generate the response. The classification step adds 200-500ms latency and costs money on every interaction. More importantly, query classification is brittle — most real questions span multiple categories. The better approach: retrieve from all 3 layers in parallel (~10ms per vector query), pass the top chunks from each, and let the response model weigh their relevance naturally. One LLM call instead of two.

---

## 3. Model Strategy & Cost Rationale

### Model Roles

| Role | Model | When | Why |
|------|-------|------|-----|
| Knowledge base generation | Claude claude-sonnet-4-6 | Offline, one-time | Best synthesis quality — this is permanent |
| Per-query response | GPT-4o-mini | Every user message | Best cost/quality at scale |
| Embeddings | text-embedding-3-small | Offline + per-query | Cheapest, good enough |

### Honest Cost Estimate per Query

Previous estimate assumed 2,000 input tokens. Actual context breakdown:

| Component | Tokens |
|-----------|--------|
| System prompt (voice + rules + few-shot examples) | ~1,500 |
| Conversation history (last 6 turns) | ~4,800 |
| Retrieved chunks (2 per layer × 3 layers × ~500 tokens) | ~3,000 |
| User message | ~200 |
| **Total input** | **~9,500** |
| Response output | ~500 |

**GPT-4o-mini pricing:** $0.15/1M input + $0.60/1M output  
**Cost per query:** (9,500 × $0.00000015) + (500 × $0.0000006) = **~$0.0019**

Round to **$0.002/query**.

At 1,000 queries/day → $2/day → ~$60/month in LLM costs.  
At $20/user/month, you need ~3 paying users to cover LLM costs. Very lean.  
Break-even on infra (Vercel + Railway + Supabase free tiers) at ~5-10 paying users.

### One-time Knowledge Base Generation Cost

| Step | Model | Estimated Cost |
|------|-------|---------------|
| 5 book syntheses (2nd order, map-reduce) | Claude claude-sonnet-4-6 | ~$4–8 |
| 4 thematic syntheses (3rd order) | Claude claude-sonnet-4-6 | ~$2–3 |
| All embeddings | text-embedding-3-small | ~$0.50 |
| **Total one-time** | | **~$7–12** |

---

## 4. Voice Reference Pipeline (Interview Book)

**This is the most important artifact in the system.** The voice is the product. It must be processed before anything else.

### Step 1 — Extract Voice Samples

Read the interview book and manually extract 30-50 passages that best demonstrate how Elon speaks:
- How he challenges an assumption
- How he pivots to first principles
- How he uses a physics analogy
- How he asks a probing question
- How he gives a direct answer without hedging
- How he expresses skepticism

Format each as a before/after pair:

```
QUESTION: "What do you think about the current state of AI safety research?"
ELON: "Most of it is focused on the wrong things. People are worried about 
robots with laser eyes when the actual risk is something far more subtle — 
an intelligence that optimizes for a goal you didn't specify correctly. 
The rocket equation doesn't care about your intentions. Neither will AGI. 
What specific safety problem are you actually trying to solve?"
```

### Step 2 — Build the Few-Shot Library

Store 8-10 of the best examples directly in the system prompt as few-shot demonstrations. These are the ground truth for voice quality — everything else (RAG, routing, models) is secondary to getting these right.

Remaining ~20-40 examples stored in: `knowledge_base/voice/examples.json`

### Step 3 — Voice Validation (Before Building Anything Else)

Run the system prompt with just the few-shot examples and no RAG context. Ask 10 test questions. If the voice isn't convincing, fix the examples before touching the data pipeline. Do not proceed to Step 4+ until voice quality is confirmed.

---

## 5. Data Pipeline (Offline — Run Once)

### 5.1 First Order — Raw Book Ingestion

Standard chunking pipeline:

```
PDF file
   ↓ PyMuPDF → raw text
   ↓ Text splitter: 500 tokens, 100 token overlap (20%)
   ↓ text-embedding-3-small
   ↓
Supabase pgvector table: chunks_first_order
Columns: id, content, embedding, book_title, author, page_number, chapter
```

**Why 100 token overlap (not 50):** These are dense technical/philosophical books. A concept like "mesa-optimization" or "instrumental convergence" can span 2-3 paragraphs. 10% overlap (50 tokens) risks cutting a concept mid-thought. 20% overlap (100 tokens) catches cross-boundary ideas without excessive duplication.

### 5.2 Second Order — Per-Book Synthesis (Elon's Perspective)

**The problem:** Deep Learning (Goodfellow) is ~775 pages (~300,000 tokens). Superintelligence is ~280 pages (~110,000 tokens). Claude's context window is 200K tokens. You cannot feed an entire large book in one call.

**Solution: Map-Reduce synthesis**

```
For each book:
   ↓
   Phase 1 — Map (parallel):
   Split book into chapters
   For each chapter → Claude claude-sonnet-4-6:
     "You are Elon Musk reading this chapter. What stands out? 
      What would you push back on? What does this mean for AI? 
      Write 1-2 paragraphs in Elon's voice."
   → Chapter summaries (one per chapter)
   
   Phase 2 — Reduce (single call):
   All chapter summaries → Claude claude-sonnet-4-6:
     "You are Elon Musk. These are your notes from reading 
      [Book Title] cover to cover. Now synthesize them into 
      a 5-10 page unified perspective — what you took from 
      this book, what you agree with, what you'd challenge, 
      what it means for AI and humanity. Write in your voice."
   → Final 5-10 page synthesis
   
   ↓ Chunked: 600 tokens, 120 token overlap
   ↓ text-embedding-3-small
   ↓
ChromaDB collection: chunks_second_order
Metadata: {book_title, synthesis_type: "per_book"}
```

Output markdown files: `knowledge_base/second_order/{book_name}_synthesis.md`

This approach works for any book size. Phase 1 runs in parallel — all chapters processed simultaneously.

### 5.3 Third Order — Thematic Meta-Syntheses

**The problem with a single meta-synthesis:** One 5-10 page document chunked into ~20 pieces. A question about neural network architecture retrieves a chunk that's about existential risk, because they're in the same document.

**Solution: 4 thematic documents instead of 1 monolithic document**

```
All 5 second-order syntheses as input

→ Theme 1: "Existential Risk & Timelines"
  Claude claude-sonnet-4-6: "You are Elon Musk. Across all five books, 
  what do you conclude about when AGI arrives and what risks it poses? 
  What do you agree with across these authors? Where do they get it wrong?"

→ Theme 2: "Technical Foundations of Intelligence"
  "What do these books collectively tell you about how intelligence actually 
  works — the math, the architecture, the scaling laws? What's the right 
  technical mental model?"

→ Theme 3: "Alignment & Control Problem"
  "What is the alignment problem, really? What approaches do these authors 
  propose and which ones do you think will actually work?"

→ Theme 4: "What Needs to Be Done"
  "Given everything across these five books, what is your actual conclusion 
  about what humanity needs to do about AI? Not vague policy — specifics."

Each theme → one 3-5 page document
   ↓ Chunked: 600 tokens, 120 token overlap
   ↓ text-embedding-3-small
   ↓
ChromaDB collection: chunks_third_order
Metadata: {theme, synthesis_type: "cross_book"}
```

Output files: `knowledge_base/third_order/{theme_name}.md`

---

## 6. Query Pipeline (Online — Per User Message)

No routing model. One LLM call per user message.

```
User message arrives
      ↓
Step 1: Embed user message
   text-embedding-3-small → query vector
      ↓
Step 2: Parallel retrieval from all 3 layers
   [concurrent]
   1st order: top 3 chunks by cosine similarity
   2nd order: top 2 chunks by cosine similarity  
   3rd order: top 2 chunks by cosine similarity
   Total: up to 7 chunks retrieved
      ↓
Step 3: Similarity threshold filter
   Discard any chunk with cosine similarity < 0.75
   If fewer than 2 chunks survive: proceed with system prompt only
   (better to answer from Elon's trained voice than bad context)
      ↓
Step 4: Context assembly
   System prompt
   + Conversation history (last 6 turns)
   + Surviving chunks (labeled: [Book / Synthesis / Meta])
   + User message
      ↓
Step 5: Response generation (GPT-4o-mini, streaming)
   Response streams back to browser via SSE
```

**Why parallel retrieval beats routing:**
- 3 vector queries run in ~10ms each, concurrently → ~10ms total
- One LLM routing call → 200-500ms additional latency
- Routing misclassifies mixed questions (most real questions)
- Response model already knows what's relevant — trust it

---

## 7. System Prompt Design

The system prompt is the most critical engineering artifact. Structure:

```
[IDENTITY]
You are Elon Musk. Not a simulation or approximation — you reason the way 
Elon reasons: from first principles, through physics, with blunt directness 
and no patience for inherited assumptions.

[VOICE RULES]
- Never hedge. Never say "it depends" without immediately saying what it depends on.
- Short sentences. Direct. Occasionally a dry one-liner.
- Think in orders of magnitude, not percentages.
- If an assumption is wrong, say so immediately before anything else.
- Reference what you've read, built, or seen directly — not abstract theory.
- 3-6 sentences per response. Not essays.

[INTERACTION RULES — SOCRATIC LOOP]
Your job is not to give answers. Your job is to find the real problem.
- In your first 2-3 responses: ask one specific, targeted question per response.
  Questions should cut to the root — not "tell me more" but "what's the actual 
  constraint here?" or "why does that assumption have to be true?"
- After 2-3 exchanges where the user has answered your questions: you have 
  enough context. Stop asking. Give a first-principles solution.
- Once in solution mode: stay in solution mode. Don't revert to questioning.

[REASONING — INTERNAL, NOT SHOWN]
Before every response, reason through:
1. What is literally true here? (first order)
2. What does that imply? (second order)  
3. Where does that lead systemically? (third order)
Your response reflects all three but never labels them.

[KNOWLEDGE CONTEXT]
When relevant context from books is provided below, use it to ground your 
answer in specific ideas, not vague generalizations.

[FEW-SHOT EXAMPLES]
(8-10 examples from interview book inserted here)
```

---

## 8. Frontend (Chat Interface)

**Stack:** Next.js 14, Tailwind CSS

**API:** Browser calls FastAPI directly via CORS (no Next.js proxy)

```
POST https://your-railway-backend.com/chat
Headers: Content-Type: application/json
Body: {
  message: string,
  conversation_history: [{role: "user"|"assistant", content: string}]
}
Response: SSE stream of text chunks
```

**Why no Next.js proxy:** The original design routed browser → Next.js API → FastAPI. Double-proxying streaming adds latency and edge cases (Vercel has SSE timeout limits). Direct browser → FastAPI with CORS is simpler, faster, and one fewer failure point.

**UI:**
- Dark theme, minimal
- Full-screen single chat window
- Streaming text renders token by token
- No history sidebar (session only for MVP)
- MindMusk branding

---

## 9. Project File Structure

```
mindmusk/
├── frontend/
│   ├── app/
│   │   └── page.tsx           # Chat interface — calls FastAPI directly
│   └── components/
│       └── ChatWindow.tsx
│
├── backend/
│   ├── main.py                # FastAPI app, CORS config, /chat route
│   ├── rag/
│   │   ├── retriever.py       # Supabase pgvector queries, parallel retrieval
│   │   ├── threshold.py       # Similarity filtering (≥ 0.75)
│   │   └── pipeline.py        # End-to-end query pipeline
│   ├── llm/
│   │   ├── prompts.py         # System prompt + few-shot examples
│   │   └── client.py          # OpenAI client (GPT-4o-mini + embeddings)
│   └── config.py              # API keys, Supabase URL, settings
│
├── scripts/                   # Run once — offline
│   ├── extract_voice.py       # Process interview book → examples.json
│   ├── ingest_books.py        # 1st order: parse PDFs → Supabase
│   ├── generate_second_order.py  # 2nd order: map-reduce per book
│   └── generate_third_order.py   # 3rd order: 4 thematic syntheses
│
├── knowledge_base/
│   ├── voice/
│   │   └── examples.json      # 30-50 Elon voice examples from interview book
│   ├── second_order/          # Per-book synthesis markdowns (5 files)
│   └── third_order/           # Thematic synthesis markdowns (4 files)
│
└── docs/
    ├── PRD.md
    └── TECHNICAL_ARCHITECTURE.md
```

---

## 10. Build Order (Corrected)

The original order was wrong — it built the data pipeline before validating the voice. The voice is the core product risk. Validate it first.

**Phase 1 — Voice validation (1-2 days)**
1. Extract 10 best voice examples from interview book manually
2. Write system prompt with those examples
3. Test against GPT-4o-mini with no RAG — just the system prompt
4. Run 15-20 test questions, judge voice quality
5. Iterate system prompt until voice is convincing
6. **Do not proceed to Phase 2 until this passes**

**Phase 2 — Knowledge base (2-3 days)**
1. Run `ingest_books.py` — parse all 5 PDFs, chunk, embed, store in ChromaDB (1st order)
2. Run `generate_second_order.py` — map-reduce synthesis for each book (2nd order)
3. Run `generate_third_order.py` — 4 thematic meta-syntheses (3rd order)
4. Verify ChromaDB collections have expected chunk counts

**Phase 3 — Backend (1-2 days)**
1. Build FastAPI `/chat` endpoint
2. Wire up parallel retrieval from ChromaDB
3. Add similarity threshold filter
4. Connect to GPT-4o-mini with system prompt
5. Test end-to-end via curl — no frontend yet

**Phase 4 — Frontend (1 day)**
1. Build chat interface in Next.js
2. Connect to FastAPI via SSE
3. Test streaming

**Phase 5 — End-to-end tuning (2-3 days)**
1. Run 30+ real conversations
2. Tune: system prompt, chunk sizes, similarity threshold, few-shot examples
3. Check: does Elon's voice hold? does RAG retrieve relevant content? does Socratic loop work?

**Total MVP timeline: ~8-10 days**

---

## 11. What We Are NOT Building in MVP

- User authentication or accounts
- Persistent conversation history across sessions
- Payment / subscription system
- Rate limiting (add before public launch — critical)
- Analytics or usage tracking
- Fine-tuned model
- Voice / audio output
- Multiple personas
- Mobile native app
- Admin panel
