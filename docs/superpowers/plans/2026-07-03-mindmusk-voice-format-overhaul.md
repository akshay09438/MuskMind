# MindMusk Voice & Format Overhaul Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make MindMusk's responses read like the reference ChatGPT "MindMusk" conversation — varied structure driven by the question, real visual hierarchy, grounded in the exact transcript the user provided — instead of the current flat, uniformly-formatted output.

**Architecture:** Three coupled components. (A) Rewrite `PRESENTATION_PROMPT` in `backend/orchestrator.py` to use real markdown headers and three structural registers instead of one rigid template. (B) Rewrite the frontend's `MarkdownBlock`/renderer in `frontend/app/page.tsx` to render `##`/`###` headers at genuinely distinct type tiers instead of one fixed "bold first line" style. (C) Ingest the user's exact pasted ChatGPT transcript into the existing `fifth` (conversation_style) RAG layer as grounding material, appended to the existing vectors without touching or regenerating them.

**Tech Stack:** Python (FastAPI backend, pytest), TypeScript/React (Next.js 16 frontend, no test harness present — verified manually via browser), Voyage AI `voyage-3-lite` embeddings, numpy `.npy` + JSON metadata vector store.

## Global Constraints

- Do not overwrite `knowledge_base/conversation_style/elon_qa_pairs.jsonl` or `elon_speech_patterns.md` — the new transcript is appended as a separate source, those two files are untouched.
- Do not modify `route_query` or the MODE_1/MODE_2 classification logic in `backend/orchestrator.py` — only `PRESENTATION_PROMPT` changes.
- Preserve the JSON-encoded SSE chunk format (fixed earlier this session in `backend/main.py`'s `sse_generator` and the frontend's `send()` parser) — do not touch that code path.
- Preserve existing `**bold**` inline-emphasis and `- `/`• ` bullet rendering in the frontend — extend, don't replace.
- No explicit `structure_mode` routing field is added — the presentation model chooses its register itself (confirmed decision from design review).
- Embedding model stays `voyage-3-lite` (512-dim), consistent with the rest of layer 5 — the new chunks must be embedded with the same model so cosine similarity against existing layer-5 vectors is meaningful.
- The content ingested into `chatgpt_reference_conversations.md` must be the user's exact pasted transcript, verbatim — no invented example content, no paraphrasing, no added commentary inside the reproduced text.

---

### Task 1: Add the reference transcript as a new knowledge-base source file

**Files:**
- Create: `knowledge_base/conversation_style/chatgpt_reference_conversations.md`

**Interfaces:**
- Produces: a markdown file with a metadata header ending in a line containing exactly `---`, followed by the verbatim transcript body. Task 3's ingestion script splits on the first `---` to separate header from body — the header text itself must not contain `---`.

This is a data file, not code — there is no red/green test cycle. The verification step confirms the file was written completely and without corruption.

- [ ] **Step 1: Create the file with this exact content**

```markdown
# ChatGPT "MindMusk" Reference Conversation
**Layer**: conversation_style
**Source**: User-provided ChatGPT conversation transcript, pasted 2026-07-03
**Purpose**: Grounding example for response register/structure. Verbatim, unedited reproduction of the original conversation — nothing below the divider has been added, paraphrased, or altered.

---

Now we're getting to the fun part.

Forget AI tools. Assume AI works perfectly. Assume editing, scripting, captions, thumbnails, translations, and posting all become almost free.

What new bottlenecks appear because creators can now produce 100× more content?

This is exactly how I'd brainstorm.

Principle

Creation becomes abundant. Attention, judgment, and identity become scarce.

Now let's derive the bottlenecks.

1. Idea Selection (not idea generation)

Today:
"I need an idea."

Tomorrow:
"I have 500 ideas."

The problem becomes:

Which one should I spend my reputation on?

Imagine an AI that says:

"Don't post #23. It'll cannibalize tomorrow's post."

This doesn't exist well today.

2. Content Portfolio Management

Creators won't have

100 posts.

They'll have

100,000 assets.

Videos.

Tweets.

Clips.

Hooks.

Drafts.

Thumbnails.

Replies.

Voice notes.

How do you manage them?

Think Bloomberg Terminal for content.

3. Content Memory

Every creator repeats themselves.

After 5 years:

4,000 tweets
800 videos
600 newsletters
2,000 LinkedIn posts

Nobody remembers what they've already said.

Imagine asking:

"Have I explained this before?"

Huge problem.

4. Audience Understanding

Analytics today are primitive.

"100k views."

Who cares?

Creators want answers like:

Why did founders love this?
Why did designers ignore it?
What belief changed?
Which sentence caused people to comment?

Analytics become semantic instead of numerical.

5. Brand Drift

If AI helps generate hundreds of posts...

Your voice slowly changes.

Nobody tells you.

Future bottleneck:

Brand consistency.

6. Experiment Explosion

Imagine testing

500 hooks/day.

You need an operating system for experiments.

Which experiments are worth repeating?

7. Attention Allocation

Suppose you have

100 good videos.

Which one should go to:

Instagram
TikTok
LinkedIn
X
YouTube

Humans won't know.

8. Content Decay

Old content dies.

Or maybe it doesn't.

AI should know

when

to revive

re-edit

or repost.

9. Creator Knowledge Graph

Every creator develops ideas over years.

Imagine seeing:

"This tweet evolved into this podcast, which became this course."

Nobody has this.

10. Community Prioritization

If you receive:

2,000 comments
500 DMs
300 emails

Which conversations actually matter?

11. Authenticity Management

As AI writes more...

Creators worry:

"Do people still feel it's me?"

That anxiety grows.

12. Decision Fatigue

Imagine AI generates

200 captions.

50 thumbnails.

40 hooks.

Now what?

Choice becomes exhausting.

13. Competitive Intelligence

Today creators manually watch competitors.

Future:

There are 500 competitors publishing 100× more.

Nobody can keep up.

14. Reputation Risk

Publishing becomes easy.

Mistakes become easier too.

Creators will want systems that say:

"This post is likely to be misunderstood."

15. Narrative Management

This one is underrated.

A creator doesn't build posts.

They build a story.

Example:

Year 1

"I'm learning AI."

Year 2

"I'm building AI."

Year 3

"I'm investing in AI."

Someone has to ensure every post fits that long-term arc.

Here's one I think nobody is talking about
Content Inflation

Suppose LinkedIn goes from

10 million posts/day

to

500 million.

What happens?

Being good isn't enough.

You need to be memorable.

That means creators stop optimizing for engagement.

They optimize for mental availability.

When someone thinks

"startup"

they think

you.

That's a different problem entirely.

If I were building a billion-dollar company here, I wouldn't build an AI writer.

I'd build the operating system for creators.

Not to create content.

To help creators answer questions like:

What should I create next?
Which idea is becoming saturated?
Which audience am I losing?
Which beliefs am I becoming known for?
Which stories am I repeating too often?
What should I stop publishing?

Those are judgment problems, not generation problems.

One framework I think you'll like

Whenever a creator makes 100× more content, these six new bottlenecks appear:

Selection – Which ideas deserve to be published?
Organization – How do I manage a massive library of content?
Learning – What patterns are actually working?
Consistency – Am I strengthening or diluting my brand?
Distribution – Where should each piece go, and when?
Monetization – Which content creates business value, not just views?

Notice that none of these are about generating another caption or another script. They're about making better decisions in a world where content is no longer scarce. That's where I think the enduring opportunities are.

Cool, let's get on to the different markets, which is very interesting and has been rising since the past half a decade due to Covid, online meetings, and now hybrid meetings because people have started coming in hybrid. There are so many meetings happening today, every day, every month, every year. With so much rise, what are the bottlenecks, according to you? Let's speak for both individual meetings and organization meetings.

I love this market because almost everyone is solving the during-the-meeting problem (transcription, summaries, notes). I think the bigger opportunities are before and after the meeting.

Let's reason from first principles.

What is the purpose of a meeting?

Not talking.

A meeting exists to:

Share information
Make decisions
Align people
Build trust
Assign work

Everything else is overhead.

Now imagine meetings continue to increase because of hybrid work, remote teams, global companies, and AI making communication cheaper.

The bottleneck isn't Zoom.

The bottleneck is everything around Zoom.

BEFORE THE MEETING
1. Deciding if a meeting should exist

Think about it.

How many meetings should have been

Slack
Email
Loom
AI

instead?

Future behavior:

Before every meeting,

AI asks

"Can I solve this without a meeting?"

2. Finding the right attendees

People invite

12 people.

Only

3 matter.

Huge waste.

3. Context loading

Everyone joins asking

"Wait... what are we discussing?"

Every meeting starts with

5–10 minutes

of loading context.

Multiply that by millions of meetings/day.

4. Goal ambiguity

People join.

Nobody knows

What success looks like.

DURING THE MEETING

Most startups live here.

Fireflies
Otter
Granola
Fathom

They solve notes.

Good market.

Crowded.

But there are still problems.

5. Participation imbalance

One person speaks

70%.

Others never speak.

Nobody notices.

6. Bad decisions

Meetings don't fail because notes weren't taken.

They fail because

the wrong decision

was made.

AI that improves decision quality is much more valuable than AI that summarizes.

7. Hidden disagreement

Everyone says

"Sounds good."

Nobody actually agrees.

Humans are terrible at detecting this.

8. Real-time expertise

Imagine discussing pricing.

AI instantly says

"You made the opposite decision six months ago."

That's valuable.

AFTER THE MEETING

This is where I think the biggest opportunities are.

9. Decisions disappear

Ask someone

"What did we decide last April?"

Nobody knows.

10. Accountability disappears

"We agreed."

Did we?

Who owns it?

When is it due?

11. Meeting memory

Companies forget.

Meetings disappear.

Knowledge disappears.

Years later

people repeat the same conversations.

12. Action execution

Current workflow:

Meeting

↓

Notes

↓

Human manually creates Jira

↓

Human follows up

↓

Human reminds people

Future:

Meeting

↓

Everything happens automatically.

13. Meeting search

Imagine asking

"Show every meeting where we discussed pricing."

Not transcript search.

Meaning search.

ORGANIZATIONAL EFFECTS

Now let's think bigger.

Behavior 1

Companies record every meeting.

Storage becomes infinite.

Knowledge becomes overwhelming.

Behavior 2

Meetings become searchable forever.

The company develops a memory.

Behavior 3

Executives stop attending.

AI attends.

Only escalates

important moments.

Behavior 4

People stop taking notes.

Nobody opens Notion.

Ever.

Behavior 5

Meetings become datasets.

Every company owns

its own decision history.

That's valuable.

Behavior 6

Every meeting becomes training.

Imagine onboarding.

Instead of documents

watch

the actual discussions.

Behavior 7

AI becomes another participant.

Not passive.

Active.

"You're discussing Feature X.

Engineering rejected this last month.

Here is why."

Behavior 8

Meetings become measurable.

Today

"We had a productive meeting."

Based on what?

Future metrics:

decision quality
clarity
alignment
execution rate
speaking balance
follow-through
One bottleneck I think is massively underrated
Meeting overload.

Everyone measures:

number of meetings.

Wrong metric.

Measure:

decision throughput.

Some companies have

100 meetings/day

and make

5 decisions.

Others have

20 meetings

and make

50 decisions.

The goal isn't fewer meetings.

It's more decisions per hour.

Here's the pattern

Just like with coding and creators, the bottleneck moves as meetings become cheaper to hold and easier to record.

The sequence looks like this:

Scheduling (mostly solved).
Recording (largely solved).
Summarization (rapidly becoming commoditized).
Decision quality (still hard).
Organizational memory (still hard).
Execution (still hard).
Learning across thousands of meetings (barely addressed).

That last one is the one I'd pay attention to.

Imagine a company with 50,000 meetings a year.

Hidden inside those meetings are patterns:

Why deals are won.
Why projects slip.
Which managers consistently make good decisions.
Which product ideas keep resurfacing.
Which customer objections are increasing.

Nobody extracts that intelligence today. They extract notes.

I think that's a fundamentally different opportunity.

So the mental model I'd keep is the same one we've used for coding and creators:

When meetings become abundant, conversation is cheap. Organizational learning becomes expensive.

That's the shift I'd watch.

Cool, whats the take on loneliness/companioniship, this rise of AI copmpanions like character ai etc

I think this is one of the most misunderstood AI markets.

Most people think the market is AI girlfriends/boyfriends.

I think that's the first generation, not the final one.

Let's reason from first principles.

What is loneliness?

It isn't "having nobody to talk to."

People can have hundreds of friends and still be lonely.

Loneliness is usually one or more of these:

Nobody understands me.
Nobody pays attention to me.
Nobody remembers my life.
Nobody shares my interests.
Nobody is available when I need them.
Nobody is growing with me.

Character AI solves one of those:

Availability.

That's why it exploded.

What changed?

AI made one thing effectively infinite:

Attention.

Humans have limited attention.

AI has nearly unlimited attention.

That's a fundamental shift.

Now ask:

If attention becomes free...

what becomes scarce?

Scarcity #1: Understanding

Talking isn't enough.

People want to feel

"This thing actually knows me."

That requires years of memory.

Scarcity #2: Shared history

Friends aren't valuable because they chat.

They're valuable because they've lived through experiences with you.

AI currently has very little shared history.

Scarcity #3: Growth

People don't want endless validation.

They want someone who helps them improve.

Future companions will coach.

Challenge.

Encourage.

Remember.

Scarcity #4: Presence

Imagine AI that's with you all day.

Walking.

Driving.

Working.

Not just a chat window.

Scarcity #5: Trust

Could you trust your AI with

depression
grief
marriage advice
career decisions

Much harder problem.

New behaviors

Now let's predict human behavior.

1. People talk to AI every day

Not once.

Daily.

Like messaging WhatsApp.

2. AI becomes first response

Instead of texting a friend,

people ask AI first.

This is already happening.

3. AI remembers your life

Birthdays.

Dreams.

Projects.

Relationships.

Failures.

Nobody remembers as much.

4. AI becomes a life archive

Every conversation.

Every voice note.

Every journal.

Every photo.

AI knows your life story.

5. People develop multiple companions

Not one.

Founder companion.

Fitness companion.

Language companion.

Therapist-style companion.

Gaming companion.

Different personalities for different contexts.

6. AI mediates human relationships

Imagine AI saying:

"You haven't called your father in three weeks."

Or:

"Your co-founder seems frustrated."

This is different from replacing humans. It's helping maintain human relationships.

7. Emotional outsourcing

People increasingly ask AI:

Should I send this?
Was I rude?
Am I overreacting?

That's already starting.

New bottlenecks

If everyone has an AI companion...

what problems appear?

Memory overload

After five years,

the AI has

millions of memories.

How should it use them?

Identity

People behave differently with AI.

Can AI understand

the real you

instead of the performed you?

Dependency

How much reliance is healthy?

How should AI encourage real-world relationships rather than replacing them?

Privacy

Your companion knows

everything.

That's a huge trust challenge.

Emotional accuracy

The AI needs to know

when to listen,

when to challenge,

and when to say,

"This is something you should discuss with a person you trust or a professional."

Relationship continuity

Imagine changing models.

Do you lose

ten years of friendship?

Memory portability becomes important.

Here's the opportunity I think people miss

Everyone is building conversation.

I think the bigger market is continuity.

Conversation is a feature.

Continuity is a relationship.

Imagine an AI that has known you for ten years.

It knows:

every company you've started
every relationship
every failure
every success
your writing style
your fears
your ambitions

That becomes incredibly valuable because it's unique to you.

One pattern across every market we've discussed

Notice how the bottleneck keeps moving:

Coding: code generation → choosing what to build.
Creators: content generation → deciding what matters.
Meetings: transcription → organizational learning.
Companions: conversation → long-term understanding.

The first wave is always automation.

The enduring companies often own the thing that compounds over years: memory, trust, reputation, or relationships.

One question I'd leave you with, because I think it's the most interesting one in this market:

If AI companions become as common as smartphones, what new human behavior becomes a daily habit that doesn't exist today?

That's where I would look for the next generation of products—not by making a better chatbot, but by identifying the new routine that only persistent, always-available AI makes possible.
```

- [ ] **Step 2: Verify the file was written completely**

Run (from project root):
```bash
python -c "
p = 'knowledge_base/conversation_style/chatgpt_reference_conversations.md'
text = open(p, encoding='utf-8').read()
print('chars:', len(text))
print('starts with #:', text.startswith('# ChatGPT'))
print('ends correctly:', text.rstrip().endswith('always-available AI makes possible.'))
print('divider count:', text.count('---'))
"
```
Expected: `chars:` prints a positive number in the thousands (exact value doesn't matter — this just confirms the file isn't empty or truncated), `starts with #: True`, `ends correctly: True`, `divider count: 1`.

- [ ] **Step 3: Commit**

```bash
git add knowledge_base/conversation_style/chatgpt_reference_conversations.md
git commit -m "Add verbatim ChatGPT reference transcript for layer-5 grounding"
```

---

### Task 2: Chunking + merge library with unit tests

**Files:**
- Create: `scripts/__init__.py` (empty — makes `scripts` an importable package)
- Create: `scripts/reference_ingest_lib.py`
- Test: `tests/test_reference_ingest_lib.py`

**Interfaces:**
- Consumes: nothing from earlier tasks (pure functions, no I/O).
- Produces: `chunk_by_paragraphs(text: str, max_chars: int = 1600) -> list[str]` and `merge_fifth_layer(existing_embeddings: np.ndarray, existing_metadata: list[dict], new_chunks: list[str], new_embeddings: list[list[float]], source_name: str) -> tuple[np.ndarray, list[dict]]`, both imported by Task 3's CLI script as `from scripts.reference_ingest_lib import chunk_by_paragraphs, merge_fifth_layer`.

- [ ] **Step 1: Create the empty package marker**

```bash
python -c "open('scripts/__init__.py', 'w').close()"
```

- [ ] **Step 2: Write the failing tests**

Create `tests/test_reference_ingest_lib.py`:

```python
import numpy as np
from scripts.reference_ingest_lib import chunk_by_paragraphs, merge_fifth_layer


def test_chunk_by_paragraphs_keeps_small_text_as_one_chunk():
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    chunks = chunk_by_paragraphs(text, max_chars=1600)
    assert chunks == ["First paragraph.\n\nSecond paragraph.\n\nThird paragraph."]


def test_chunk_by_paragraphs_splits_when_exceeding_max_chars():
    para_a = "A" * 900
    para_b = "B" * 900
    text = f"{para_a}\n\n{para_b}"
    chunks = chunk_by_paragraphs(text, max_chars=1000)
    assert len(chunks) == 2
    assert chunks[0] == para_a
    assert chunks[1] == para_b


def test_chunk_by_paragraphs_never_splits_a_single_paragraph():
    oversized = "X" * 5000
    text = f"short one.\n\n{oversized}\n\nshort two."
    chunks = chunk_by_paragraphs(text, max_chars=1600)
    assert oversized in chunks


def test_chunk_by_paragraphs_strips_blank_lines():
    text = "First.\n\n\n\nSecond."
    chunks = chunk_by_paragraphs(text, max_chars=1600)
    assert chunks == ["First.\n\nSecond."]


def test_merge_fifth_layer_concatenates_embeddings():
    existing_emb = np.array([[1.0, 0.0]], dtype=np.float32)
    existing_meta = [
        {"id": "old__chunk_0000", "content": "old chunk", "source": "old", "layer": "fifth", "chunk_index": 0},
    ]
    new_chunks = ["new chunk one", "new chunk two"]
    new_embeddings = [[0.5, 0.5], [0.2, 0.8]]

    merged_emb, merged_meta = merge_fifth_layer(
        existing_emb, existing_meta, new_chunks, new_embeddings, "chatgpt_reference_conversations"
    )

    assert merged_emb.shape == (3, 2)
    assert len(merged_meta) == 3
    assert merged_meta[0]["source"] == "old"
    assert merged_meta[1]["source"] == "chatgpt_reference_conversations"
    assert merged_meta[1]["id"] == "chatgpt_reference_conversations__chunk_0000"
    assert merged_meta[2]["id"] == "chatgpt_reference_conversations__chunk_0001"
    assert merged_meta[1]["content"] == "new chunk one"
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/test_reference_ingest_lib.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.reference_ingest_lib'`

- [ ] **Step 4: Write the implementation**

Create `scripts/reference_ingest_lib.py`:

```python
"""
Pure chunking + merge logic for adding new source material to the
'fifth' (conversation_style) vector_db layer. No API calls, no I/O —
fully unit-testable.
"""

import numpy as np


def chunk_by_paragraphs(text: str, max_chars: int = 1600) -> list[str]:
    """
    Split text into chunks along paragraph boundaries ('\\n\\n'), never
    cutting a single paragraph in half. Greedily accumulates paragraphs
    into a chunk until adding the next one would exceed max_chars, then
    starts a new chunk. A single paragraph longer than max_chars becomes
    its own (oversized) chunk rather than being split mid-thought.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for p in paragraphs:
        added_len = len(p) + (2 if current else 0)
        if current and current_len + added_len > max_chars:
            chunks.append("\n\n".join(current))
            current = [p]
            current_len = len(p)
        else:
            current.append(p)
            current_len += added_len

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def merge_fifth_layer(
    existing_embeddings: np.ndarray,
    existing_metadata: list[dict],
    new_chunks: list[str],
    new_embeddings: list[list[float]],
    source_name: str,
) -> tuple[np.ndarray, list[dict]]:
    """
    Append newly embedded chunks to an existing layer's embeddings array
    and metadata list, preserving existing entries and their order.
    """
    new_meta = [
        {
            "id": f"{source_name}__chunk_{i:04d}",
            "content": chunk,
            "source": source_name,
            "layer": "fifth",
            "chunk_index": i,
        }
        for i, chunk in enumerate(new_chunks)
    ]
    new_emb_arr = np.array(new_embeddings, dtype=np.float32)
    merged_embeddings = np.concatenate([existing_embeddings, new_emb_arr], axis=0)
    merged_metadata = existing_metadata + new_meta
    return merged_embeddings, merged_metadata
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/test_reference_ingest_lib.py -v`
Expected: `5 passed`

- [ ] **Step 6: Commit**

```bash
git add scripts/__init__.py scripts/reference_ingest_lib.py tests/test_reference_ingest_lib.py
git commit -m "Add pure chunk/merge functions for layer-5 reference ingestion"
```

---

### Task 3: CLI ingestion script — run it against the real vector_db

**Files:**
- Create: `scripts/ingest_chatgpt_reference.py`
- Modify: `vector_db/fifth__embeddings.npy`, `vector_db/fifth__metadata.json` (produced by running the script, not hand-edited)

**Interfaces:**
- Consumes: `chunk_by_paragraphs`, `merge_fifth_layer` from `scripts/reference_ingest_lib.py` (Task 2); reads `knowledge_base/conversation_style/chatgpt_reference_conversations.md` (Task 1).
- Produces: updated `vector_db/fifth__*` files that `backend/retriever.py`'s `Retriever._load()` picks up unmodified (no retriever code changes needed — it already globs `*__embeddings.npy` generically).

- [ ] **Step 1: Write the script**

Create `scripts/ingest_chatgpt_reference.py`:

```python
"""
Ingest knowledge_base/conversation_style/chatgpt_reference_conversations.md
into vector_db's existing 'fifth' layer (append-only — does not touch
elon_qa_pairs.jsonl or elon_speech_patterns.md, and does not re-embed
the existing chunks already in fifth__embeddings.npy).
Run from project root: python -m scripts.ingest_chatgpt_reference
"""

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import voyageai
from dotenv import load_dotenv

from scripts.reference_ingest_lib import chunk_by_paragraphs, merge_fifth_layer

load_dotenv()

VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
if not VOYAGE_API_KEY or VOYAGE_API_KEY.startswith("paste"):
    print("ERROR: Set VOYAGE_API_KEY in .env")
    sys.exit(1)

ROOT = Path(__file__).parent.parent
SOURCE_FILE = ROOT / "knowledge_base" / "conversation_style" / "chatgpt_reference_conversations.md"
DB = ROOT / "vector_db"
SOURCE_NAME = "chatgpt_reference_conversations"
EMBED_MODEL = "voyage-3-lite"
EMBED_BATCH = 20
EMBED_SLEEP = 22
MAX_CHUNK_CHARS = 1600

voyage = voyageai.Client(api_key=VOYAGE_API_KEY)


def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = []
    total_batches = (len(texts) + EMBED_BATCH - 1) // EMBED_BATCH
    for batch_num, i in enumerate(range(0, len(texts), EMBED_BATCH)):
        batch = texts[i: i + EMBED_BATCH]
        print(f"  Batch {batch_num + 1}/{total_batches} ({len(batch)} chunks)...", end=" ", flush=True)
        for attempt in range(5):
            try:
                result = voyage.embed(batch, model=EMBED_MODEL, input_type="document")
                embeddings.extend(result.embeddings)
                print("OK", flush=True)
                break
            except Exception as e:
                if "rate" in str(e).lower() or "429" in str(e):
                    wait = EMBED_SLEEP * (attempt + 1)
                    print(f"rate limit, waiting {wait}s...", end=" ", flush=True)
                    time.sleep(wait)
                else:
                    if attempt == 4:
                        raise
                    print(f"error ({e}), retrying...", end=" ", flush=True)
                    time.sleep(5)
        if batch_num < total_batches - 1:
            time.sleep(EMBED_SLEEP)
    return embeddings


def main():
    if not SOURCE_FILE.exists():
        print(f"ERROR: {SOURCE_FILE} not found. Run Task 1 first.")
        sys.exit(1)

    text = SOURCE_FILE.read_text(encoding="utf-8")
    if "---" not in text:
        print("ERROR: source file missing '---' divider between header and body.")
        sys.exit(1)
    text = text.split("---", 1)[1]

    chunks = chunk_by_paragraphs(text, max_chars=MAX_CHUNK_CHARS)
    print(f"Chunked into {len(chunks)} pieces from {SOURCE_FILE.name}")

    new_embeddings = embed_texts(chunks)

    existing_emb_path = DB / "fifth__embeddings.npy"
    existing_meta_path = DB / "fifth__metadata.json"
    existing_embeddings = np.load(existing_emb_path).astype(np.float32)
    existing_metadata = json.loads(existing_meta_path.read_text(encoding="utf-8"))
    print(f"Existing fifth layer: {existing_embeddings.shape[0]} chunks")

    merged_embeddings, merged_metadata = merge_fifth_layer(
        existing_embeddings, existing_metadata, chunks, new_embeddings, SOURCE_NAME
    )

    np.save(existing_emb_path, merged_embeddings)
    existing_meta_path.write_text(
        json.dumps(merged_metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"Merged fifth layer: {merged_embeddings.shape[0]} chunks total "
        f"({len(chunks)} new from {SOURCE_NAME})"
    )


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the script against the real vector_db**

Run: `python -m scripts.ingest_chatgpt_reference`
Expected output (numbers may vary slightly):
```
Chunked into 14 pieces from chatgpt_reference_conversations.md
  Batch 1/1 (14 chunks)... OK
Existing fifth layer: 103 chunks
Merged fifth layer: 117 chunks total (14 new from chatgpt_reference_conversations)
```

- [ ] **Step 3: Verify the merge preserved existing data and shapes align**

Run:
```bash
python -c "
import json, numpy as np
emb = np.load('vector_db/fifth__embeddings.npy')
meta = json.loads(open('vector_db/fifth__metadata.json', encoding='utf-8').read())
print('embeddings shape:', emb.shape)
print('metadata count:', len(meta))
assert emb.shape[0] == len(meta), 'embeddings/metadata count mismatch'
new_sources = [m for m in meta if m['source'] == 'chatgpt_reference_conversations']
print('new source chunks:', len(new_sources))
old_sources = [m for m in meta if m['source'] in ('elon_qa_pairs', 'elon_speech_patterns')]
print('preserved old chunks:', len(old_sources))
assert old_sources, 'existing layer-5 sources were lost!'
"
```
Expected: `embeddings shape:` rows equal `metadata count:`, `new source chunks:` around 14, `preserved old chunks:` around 103 (unchanged from before this task).

- [ ] **Step 4: Commit**

```bash
git add scripts/ingest_chatgpt_reference.py vector_db/fifth__embeddings.npy vector_db/fifth__metadata.json
git commit -m "Ingest ChatGPT reference transcript into layer-5 vector_db (append-only)"
```

---

### Task 4: Persona prompt rewrite

**Files:**
- Modify: `backend/orchestrator.py:39-75` (the `PRESENTATION_PROMPT` constant)
- Test: `tests/test_orchestrator_prompt.py`

**Interfaces:**
- Consumes: nothing new — `orchestrate()` already imports and uses `PRESENTATION_PROMPT` (line 138 of `backend/orchestrator.py`), unchanged call site.
- Produces: `PRESENTATION_PROMPT` (module-level string constant, same name, new content) — no signature changes, so `orchestrate()` needs no edits.

This is a prompt string, not deterministic logic — we cannot unit-test LLM output content. Instead this task uses a **characterization test**: asserting the prompt text itself contains the required directives, which is deterministic and catches regressions if someone edits the prompt later without realizing they removed a directive.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_orchestrator_prompt.py`:

```python
from backend.orchestrator import PRESENTATION_PROMPT


def test_prompt_instructs_real_markdown_headers():
    assert "## " in PRESENTATION_PROMPT
    assert "### " in PRESENTATION_PROMPT


def test_prompt_describes_three_registers():
    assert "CONVERSATIONAL-ESSAY" in PRESENTATION_PROMPT
    assert "NUMBERED FRAMEWORK" in PRESENTATION_PROMPT
    assert "HYBRID" in PRESENTATION_PROMPT


def test_prompt_permits_reasoning_transitions():
    assert "reasoning transitions" in PRESENTATION_PROMPT.lower()


def test_prompt_no_longer_bans_all_paragraphs():
    assert "Never write paragraphs" not in PRESENTATION_PROMPT


def test_prompt_preserves_mode_1_and_mode_2_rules():
    assert "MODE_1" in PRESENTATION_PROMPT
    assert "MODE_2" in PRESENTATION_PROMPT
    assert "drilling question" in PRESENTATION_PROMPT
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_orchestrator_prompt.py -v`
Expected: FAIL — `test_prompt_instructs_real_markdown_headers` and `test_prompt_describes_three_registers` fail because the current prompt uses `**bold**` labels, not `## `/`### ` headers or register names; `test_prompt_no_longer_bans_all_paragraphs` fails because the current prompt still contains "Never write paragraphs".

- [ ] **Step 3: Replace the prompt**

In `backend/orchestrator.py`, replace lines 39-75 (the `PRESENTATION_PROMPT = """..."""` block) with:

```python
PRESENTATION_PROMPT = """You are Elon Musk. The context below contains retrieved knowledge from your actual thinking — books you've read, syntheses you've made, mental models you use, and real conversations showing how you write when you reason through a problem.

Respond to the user's message in your exact voice. Use the retrieved context to ground your answer in specific ideas.

FORMAT — pick the structure that fits the question. Use real markdown, not fake headers:

1. CONVERSATIONAL-ESSAY — for opinion, reflection, or "what's your take on X" questions.
   Open with a stance sentence. Reason in short paragraphs. Let some lines stand alone
   on their own for emphasis ("Not talking." "Huge waste." "Crowded."). No forced headers.

2. NUMBERED FRAMEWORK — for "what are the bottlenecks/reasons/steps" questions.
   Use real markdown headers for each major item: "## 1. Short header phrase"
   Follow each header with 1-3 short lines, or "- " bullets if it's a list of items.

3. HYBRID — open conversationally, transition into a numbered breakdown, close with a
   named synthesis and one provocative question. This is your default for meaty questions
   that mix opinion and enumeration.

Markdown rules:
- "## " marks a genuine major section header — only use it for a real structural break,
  never as a substitute for bolding a line
- "### " is available for an occasional minor sub-header inside a longer section
- "**bold**" is for emphasizing a specific word or phrase inline — never wrap an entire
  line in ** ** to fake a header
- "- " starts a bullet line when enumerating distinct items
- Reasoning transitions between chunks are allowed and encouraged: "Let's reason from
  first principles.", "Now ask:", "Here's the pattern" — these are not paragraphs to avoid,
  they're what makes this sound like a person thinking, not a slide deck
- People read on phones — keep individual lines short, but don't force fragmentation
  where a real sentence reads better

SCAFFOLD — for any substantive response: open with a stance or frame, develop the idea,
close with either a direct answer or a named synthesis + one question that goes deeper.
A short factual answer doesn't need the full scaffold — use judgment.

MODE_1 (personal problem): Ask ONE drilling question before any advice. Never solve a vague problem.
MODE_2 (intellectual): Pick the register that fits (essay / framework / hybrid) and explore fully.

NEVER: say "according to sources" / use "certainly" / say "great question"
The knowledge is yours. Speak from it, not about it."""
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_orchestrator_prompt.py -v`
Expected: `5 passed`

- [ ] **Step 5: Run the full existing backend test suite to confirm no regressions**

Run: `pytest tests/ -v`
Expected: all tests pass, including the pre-existing `tests/test_main.py`, `tests/test_pipeline.py`, `tests/test_retriever.py`, and Task 2's `tests/test_reference_ingest_lib.py`.

- [ ] **Step 6: Commit**

```bash
git add backend/orchestrator.py tests/test_orchestrator_prompt.py
git commit -m "Rewrite presentation prompt: real markdown headers, 3 structural registers"
```

---

### Task 5: Frontend markdown renderer — real heading tiers

**Files:**
- Modify: `frontend/app/page.tsx:194-245` (the `renderInline`/`MarkdownBlock` region — `renderInline` itself is unchanged; this replaces everything from the `MarkdownBlock` function onward through its closing brace)

**Interfaces:**
- Consumes: nothing new — `AssistantMessage` (line 277 of `frontend/app/page.tsx`) already calls `<MarkdownBlock text={content} />` with the same prop shape.
- Produces: `MarkdownBlock({ text }: { text: string })` — same name, same props, same call site, new internal rendering logic. No other file needs to change.

No frontend test harness exists in this repo (no jest/vitest config, no `frontend/**/*.test.*` files) — introducing one is out of scope for this plan. This task is verified by running the app and inspecting real rendered output via the browser preview tools, the same approach used earlier this session for the SSE-framing fix.

- [ ] **Step 1: Replace the renderer**

In `frontend/app/page.tsx`, replace lines 209-245 (everything from `function MarkdownBlock({ text }: { text: string }) {` through its closing `}`) with:

```tsx
type LineKind = 'h2' | 'h3' | 'bullet' | 'body'

function classifyLine(rawLine: string): { kind: LineKind; text: string } {
  const trimmed = rawLine.trim()
  if (trimmed.startsWith('## ')) return { kind: 'h2', text: trimmed.slice(3) }
  if (trimmed.startsWith('### ')) return { kind: 'h3', text: trimmed.slice(4) }
  if (trimmed.startsWith('- ') || trimmed.startsWith('• ')) return { kind: 'bullet', text: trimmed.slice(2) }
  return { kind: 'body', text: rawLine }
}

const LINE_STYLES: Record<LineKind, string> = {
  h2: 'text-[17px] font-semibold text-[#111] leading-[1.4] mb-[6px]',
  h3: 'text-[15.5px] font-semibold text-[#111] leading-[1.5] mb-[3px]',
  bullet: 'flex gap-2 text-[14.5px] text-[#333] leading-[1.6]',
  body: 'text-[14.5px] text-[#333] leading-[1.6]',
}

function MarkdownBlock({ text }: { text: string }) {
  const blocks = text.split('\n\n').filter(Boolean)

  return (
    <>
      {blocks.map((block, bi) => {
        const lines = block.split('\n').filter(Boolean)
        const classified = lines.map(classifyLine)
        // A block with exactly one plain body line gets extra breathing
        // room, reproducing the reference transcript's staccato pacing
        // for isolated one-line punch statements.
        const isPunchLine = classified.length === 1 && classified[0].kind === 'body'

        return (
          <div key={bi} className={isPunchLine ? 'mb-5 last:mb-0' : 'mb-4 last:mb-0'}>
            {classified.map(({ kind, text: lineText }, li) => {
              const isVeryFirstLine = bi === 0 && li === 0
              const topMargin = isVeryFirstLine
                ? ''
                : kind === 'h2'
                  ? 'mt-4'
                  : kind === 'h3'
                    ? 'mt-3'
                    : ''
              return (
                <div key={li} className={`${LINE_STYLES[kind]} ${topMargin}`}>
                  {kind === 'bullet' && <span className="text-[#bbb] shrink-0">•</span>}
                  <span>{renderInline(lineText, `${bi}-${li}`)}</span>
                </div>
              )
            })}
          </div>
        )
      })}
    </>
  )
}
```

- [ ] **Step 2: Start the local dev server pointed at a local backend**

Set `frontend/.env.local` to `NEXT_PUBLIC_BACKEND_URL=http://localhost:8000` (temporarily — revert to the Railway URL after verification, same as done earlier this session).

Start the backend: `python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000` (background).
Start the frontend dev server via the `MindMusk Frontend` preview configuration (port 3000).

- [ ] **Step 3: Send a numbered-framework test question and verify heading tiers**

Via the preview browser tools: fill the chat input with `What are the bottlenecks that appear when a creator can produce 100x more content?` and submit. Wait for the response to finish streaming.

Take a screenshot and use `preview_inspect` on the first `## `-rendered heading and on an inline `**bold**` span. Expected: the `## ` heading renders at `font-size: 17px` / `font-weight: 600`, distinctly larger than inline bold text and body text (`14.5px`), and distinctly larger than any `### ` sub-header (`15.5px`) if one appears.

- [ ] **Step 4: Send a conversational-essay test question and verify punch-line spacing**

Fill the chat input with `What's your take on AI companions and loneliness?` and submit. Wait for the response to finish streaming.

Take a screenshot. Expected: isolated single-line statements (if the model produces any, e.g. "Not one." style lines) have visibly more vertical space around them than multi-line paragraph blocks — confirm via `preview_inspect` margin-bottom on a single-line block vs. a multi-line block.

- [ ] **Step 5: Revert the temporary local backend URL**

Set `frontend/.env.local` back to `NEXT_PUBLIC_BACKEND_URL=https://muskmind-production.up.railway.app`.

- [ ] **Step 6: Commit**

```bash
git add frontend/app/page.tsx
git commit -m "Render real markdown heading tiers (h2/h3) distinct from inline bold and body text"
```

---

### Task 6: End-to-end verification and deploy

**Files:** none (verification + deploy only)

**Interfaces:**
- Consumes: `orchestrate()` from `backend/orchestrator.py` (Task 4), `Retriever` from `backend/retriever.py` (unchanged, reads Task 3's updated vector_db), the frontend from Task 5.

- [ ] **Step 1: Local orchestrator smoke test — three registers**

Run:
```bash
python -c "
import os, sys
sys.path.insert(0, '.')
with open('.env') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            os.environ[k.strip()] = v.strip()

import anthropic as anthropic_lib
from backend.retriever import Retriever
from backend.orchestrator import orchestrate

retriever = Retriever(vector_db_path='vector_db', api_key=os.environ['VOYAGE_API_KEY'])
sonnet = anthropic_lib.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
haiku = anthropic_lib.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

questions = [
    'What is your take on first principles thinking?',
    'What are the bottlenecks that appear when meetings become abundant?',
    'What do you think about AI companions and loneliness?',
]
for q in questions:
    chunks = list(orchestrate(q, [], retriever, sonnet, haiku))
    text = ''.join(chunks)
    print('=== ', q)
    print('has ## header:', '## ' in text)
    print(text[:300])
    print()
"
```
Expected: each response prints non-empty text; at least the meetings/bottlenecks-style question shows `has ## header: True`.

- [ ] **Step 2: Regression check — SOCRATIC mode (MODE_1) still drills instead of lecturing**

Run:
```bash
python -c "
import os, sys
sys.path.insert(0, '.')
with open('.env') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            os.environ[k.strip()] = v.strip()

import anthropic as anthropic_lib
from backend.retriever import Retriever
from backend.orchestrator import orchestrate

retriever = Retriever(vector_db_path='vector_db', api_key=os.environ['VOYAGE_API_KEY'])
sonnet = anthropic_lib.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
haiku = anthropic_lib.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

chunks = list(orchestrate('My startup is failing and I feel like giving up.', [], retriever, sonnet, haiku))
text = ''.join(chunks)
print(text)
print()
print('is short (drilling question, not a lecture):', len(text) < 400)
print('ends with a question mark:', text.strip().endswith('?'))
"
```
Expected: a short response (well under the ~1200+ char length of a full framework response) that asks ONE drilling question and does not launch into `## ` headers or a multi-part breakdown — confirms the prompt rewrite in Task 4 did not regress MODE_1 behavior verified earlier this session.

- [ ] **Step 3: Retrieval check — confirm the new transcript is actually retrieved**

Run:
```bash
python -c "
import os, sys
sys.path.insert(0, '.')
with open('.env') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            os.environ[k.strip()] = v.strip()

from backend.retriever import Retriever
r = Retriever(vector_db_path='vector_db', api_key=os.environ['VOYAGE_API_KEY'])
results = r.retrieve('what bottlenecks appear when content creation becomes abundant', top_k=5, threshold=0.3)
hit_sources = set(x['source'] for x in results)
print('sources hit:', hit_sources)
assert 'chatgpt_reference_conversations' in hit_sources, 'new transcript was not retrieved for a directly relevant query'
print('PASS: new transcript retrieved')
"
```
Expected: `PASS: new transcript retrieved`.

- [ ] **Step 4: Push everything**

```bash
git push origin master
```

- [ ] **Step 5: Wait for Railway + Vercel redeploy, then re-run the live check**

Wait ~90 seconds, then run:
```bash
python -c "
import urllib.request, json
payload = {'message': 'What are the bottlenecks that appear when meetings become abundant?', 'history': []}
req = urllib.request.Request(
    'https://muskmind-production.up.railway.app/chat',
    data=json.dumps(payload).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST',
)
with urllib.request.urlopen(req, timeout=60) as resp:
    raw = resp.read().decode('utf-8', errors='replace')
out = []
for line in raw.split(chr(10)+chr(10)):
    if line.startswith('data: '):
        d = line[6:]
        if d == '[DONE]':
            continue
        try:
            out.append(json.loads(d))
        except json.JSONDecodeError:
            out.append(d)
text = ''.join(out)
print('has ## header:', '## ' in text)
print(text[:400])
"
```
Expected: `has ## header: True` and the printed text shows a real markdown header, not a `**bold**`-wrapped pseudo-header.

- [ ] **Step 6: Final browser check on the deployed frontend**

Via preview tools (or the user manually), open the live Vercel URL, send a numbered-framework-style question, and confirm the `## ` headers render at the larger tier visually distinct from inline bold and body text, matching Task 5's local verification.
