"""
Phase 2: Generate per-source Elon synthesis for every book and podcast.
Uses Cerebras llama3.3-70b (generous free tier, fast inference).
Reads from knowledge_base/first_order/
Writes to knowledge_base/second_order/
Skips files that already exist.

Strategy: one call per file. For large files, sample evenly across the full book
(beginning + middle + end) up to MAX_SAMPLE chars. No map-reduce = no rate cascade.
"""
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))

FIRST_ORDER  = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\first_order")
SECOND_ORDER = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\second_order")
SECOND_ORDER.mkdir(parents=True, exist_ok=True)

MAX_SAMPLE  = 40000   # 40K chars ≈ 10K tokens — safe for single call
N_SAMPLES   = 5
SAMPLE_SIZE = MAX_SAMPLE // N_SAMPLES  # 8K chars per sample position

BOOK_PROMPT = """You are building the knowledge base for MindMusk — an AI that replicates Elon Musk's mind.

Book: "{title}"
Category: {category}

Read the extracted text below and write a deep synthesis titled "Elon's Synthesis: {title}".

Include ALL of these sections:

## 1. WHY ELON READ THIS
One paragraph. What problem was Elon trying to solve? What drew him to it? What made it stick?

## 2. THE IDEAS THAT CHANGED HIM
The 8-12 most important concepts, each written as Elon would interpret them — not what the author intended, what Elon extracted. Each concept: 3-6 sentences. Use Elon's lens: physics, first principles, practical application, scale, civilization impact.

## 3. HOW THIS SHOWS UP IN HIS COMPANIES
Specific, concrete connections to decisions/quotes/behaviors at Tesla, SpaceX, Neuralink, X, or Boring. Minimum 5 specific examples.

## 4. QUOTES FROM ELON THAT CONNECT HERE
5-8 things Elon has actually said that echo ideas from this book. Format: "[Quote]" — connects to [idea].

## 5. FIRST PRINCIPLES ELON EXTRACTED
What fundamental truths did Elon pull from this book? List 5-8.

## 6. WHERE ELON WOULD PUSH BACK
Where would Elon argue with the author? What does he think is wrong, naive, or too slow?

## 7. THE ONE-LINE ELON TAKEAWAY
If Elon summarized what he got from this book in one sentence, what would it be?

Write densely. No fluff. No "This book explores..." sentences. Pure signal.

--- BOOK CONTENT (sampled from throughout) ---
{content}"""

PODCAST_PROMPT = """You are building the knowledge base for MindMusk — an AI that replicates Elon Musk's mind.

Interview/Talk: "{title}"

Below is the filtered transcript — ONLY Elon's words. Write a synthesis titled "Elon's Voice: {title}".

## 1. CONTEXT AND SETTING
When was this? Who was the interviewer? What was happening at his companies at the time?

## 2. THE POSITIONS ELON TOOK
The 8-12 most important things Elon stated or argued. For each: his position, confidence level, any uncertainty.

## 3. DIRECT QUOTES (THE BEST ONES)
The 10-15 most powerful, revealing things Elon said. Keep them verbatim.

## 4. HOW HE REASONED
His thinking process: analogies, physics, historical examples, numbers, how he handled pushback.

## 5. WHAT THIS REVEALS ABOUT HOW HE THINKS
What does this interview reveal about his values, fears, ambitions, or mental models?

## 6. CONNECTIONS TO HIS COMPANIES AND DECISIONS
What connects to actual decisions at Tesla/SpaceX/Neuralink/X?

## 7. THE MOST ELON MOMENT
One specific exchange most characteristic of how Elon operates. Describe it and say why.

Write densely. Verbatim quotes where possible.

--- ELON'S WORDS ---
{content}"""


def sample_content(text: str) -> str:
    """Take N evenly-spaced samples across the full text for large files."""
    if len(text) <= MAX_SAMPLE:
        return text
    step = len(text) // N_SAMPLES
    parts = [text[i * step: i * step + SAMPLE_SIZE] for i in range(N_SAMPLES)]
    return "\n\n[...]\n\n".join(parts)


def call_cerebras(prompt: str) -> str:
    for attempt in range(6):
        try:
            response = client.chat.completions.create(
                model="gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.3
            )
            time.sleep(35)
            return response.choices[0].message.content.strip()
        except Exception as e:
            err = str(e).lower()
            if "rate" in err or "429" in err or "quota" in err:
                wait = 60 * (attempt + 1)
                print(f"\n      Rate limit, waiting {wait}s...", flush=True)
                time.sleep(wait)
            elif "connection" in err or "timeout" in err or "getaddr" in err:
                wait = 30 * (attempt + 1)
                print(f"\n      Network error, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                if attempt == 5:
                    raise
                print(f"\n      Error: {e}, retrying...", flush=True)
                time.sleep(15)
    return ""


def synthesize(source_path: Path) -> None:
    slug = source_path.stem.replace("_first_order", "").replace("_elon_only", "")
    is_podcast = source_path.name.startswith("podcast_")
    out_name = f"podcast_{slug}_synthesis.md" if is_podcast else f"{slug}_elon_synthesis.md"
    out_path = SECOND_ORDER / out_name

    if out_path.exists() and out_path.stat().st_size > 3000:
        print(f"  [SKIP] {slug}")
        return

    print(f"  [SYNTHESIZING] {slug}...", end=" ", flush=True)
    raw = source_path.read_text(encoding="utf-8")
    lines = raw.split('\n')
    title = lines[0].replace('# ', '').strip()
    category = next((l.split(":", 1)[1].strip().strip("*") for l in lines[:10] if "**Category**" in l), "")

    content = sample_content(raw)
    if len(raw) > MAX_SAMPLE:
        print(f"(sampled {len(content)//1024}KB from {len(raw)//1024}KB)", end=" ", flush=True)

    if is_podcast:
        prompt = PODCAST_PROMPT.format(title=title, content=content)
    else:
        prompt = BOOK_PROMPT.format(title=title, category=category, content=content)

    synthesis = call_cerebras(prompt)

    if not synthesis:
        print("FAILED")
        return

    output = f"# Elon's Synthesis: {title}\n**Slug**: {slug}\n**Layer**: second_order\n\n---\n\n{synthesis}"
    out_path.write_text(output, encoding="utf-8")
    print(f"OK ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 2: Second-Order Synthesis (Cerebras llama3.3-70b)")
    print("=" * 60)

    files = sorted(FIRST_ORDER.glob("*.md"))
    print(f"Found {len(files)} first-order files\n")

    for f in files:
        synthesize(f)

    done = list(SECOND_ORDER.glob("*.md"))
    print(f"\nPhase 2 complete. {len(done)} second-order files.")
