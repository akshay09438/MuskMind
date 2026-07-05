"""
Phase 1B Step 2: Filter podcasts to Elon-only words using Groq (FREE).
Reads from knowledge_base/podcasts/raw/
Writes to knowledge_base/podcasts/filtered/ AND knowledge_base/first_order/
Has checkpoint saving — large transcripts resume from last completed chunk if crashed.
"""
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

RAW_DIR       = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\podcasts\raw")
FILTERED_DIR  = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\podcasts\filtered")
FIRST_ORDER   = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\first_order")
CHECKPOINT_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\podcasts\checkpoints")
FILTERED_DIR.mkdir(parents=True, exist_ok=True)
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 6000

FILTER_PROMPT = """You are processing a raw podcast/interview transcript. Your ONLY job is to extract the words spoken by Elon Musk and output them.

RULES:
1. Output ONLY text that Elon Musk spoke. Remove everything the interviewer/host said.
2. Keep Elon's exact words verbatim — do not paraphrase or summarize.
3. Remove all timestamps (e.g. "4:23", "4 minutes 23 seconds").
4. Remove filler markers like [laughter], [applause], [music], [inaudible].
5. Context clues: Elon speaks in long technical paragraphs about SpaceX, Tesla, AI, Mars, physics, manufacturing, first principles. Interviewers ask short questions, say "right", "yeah", redirect topics.
6. Do NOT add any labels like "Elon:" — just output his raw words.
7. Separate different speech segments with a single blank line.
8. If an entire chunk has NO Elon content, output exactly: [NO ELON CONTENT IN THIS SECTION]

Transcript chunk to process:
---
{chunk}
---

Output Elon's words only:"""


def call_groq(prompt: str) -> str:
    for attempt in range(8):  # 8 retries instead of 5
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.3,
                timeout=60  # explicit 60s timeout
            )
            time.sleep(20)
            return response.choices[0].message.content.strip()
        except Exception as e:
            err = str(e).lower()
            if "rate" in err or "429" in err or "quota" in err:
                wait = 30 * (attempt + 1)
                print(f"Rate limit, waiting {wait}s...", end=" ", flush=True)
                time.sleep(wait)
            elif "connection" in err or "timeout" in err or "getaddr" in err or "network" in err:
                # Network errors — wait longer and retry
                wait = 20 * (attempt + 1)
                print(f"Network error, waiting {wait}s...", end=" ", flush=True)
                time.sleep(wait)
            else:
                if attempt == 7:
                    raise
                print(f"Error ({e}), retrying...", end=" ", flush=True)
                time.sleep(10)
    return ""


def filter_transcript(slug: str, raw_text: str) -> str:
    chunks = [raw_text[i:i + CHUNK_SIZE] for i in range(0, len(raw_text), CHUNK_SIZE)]
    total = len(chunks)
    print(f"    {total} chunks...", end=" ", flush=True)

    # Load checkpoint if it exists (resume from last saved chunk)
    checkpoint_path = CHECKPOINT_DIR / f"{slug}_checkpoint.txt"
    completed_parts = []
    start_chunk = 0

    if checkpoint_path.exists():
        saved = checkpoint_path.read_text(encoding="utf-8").split("\n<<<CHUNK_BREAK>>>\n")
        completed_parts = [p for p in saved if p.strip()]
        start_chunk = len(completed_parts)
        if start_chunk > 0:
            print(f"(resuming from chunk {start_chunk + 1})...", end=" ", flush=True)

    for i in range(start_chunk, total):
        chunk = chunks[i]
        result = call_groq(FILTER_PROMPT.format(chunk=chunk))
        if result and result != "[NO ELON CONTENT IN THIS SECTION]":
            completed_parts.append(result)
        else:
            completed_parts.append("")  # placeholder to keep count correct

        # Save checkpoint after every chunk
        checkpoint_path.write_text(
            "\n<<<CHUNK_BREAK>>>\n".join(completed_parts),
            encoding="utf-8"
        )
        print(f"{i+1}", end=" ", flush=True)

    print()

    # Clean up checkpoint after successful completion
    if checkpoint_path.exists():
        checkpoint_path.unlink()

    return "\n\n".join(p for p in completed_parts if p.strip())


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 1B: Filtering Podcasts to Elon-Only (Groq FREE)")
    print("=" * 60)

    raw_files = sorted(RAW_DIR.glob("*.md"))
    print(f"Found {len(raw_files)} raw transcripts\n")

    for raw_file in raw_files:
        slug = raw_file.stem
        filtered_path  = FILTERED_DIR / f"{slug}_elon_only.md"
        first_order_path = FIRST_ORDER / f"podcast_{slug}_elon_only.md"
        checkpoint_path  = CHECKPOINT_DIR / f"{slug}_checkpoint.txt"

        # Skip if fully done (and no partial checkpoint pending)
        if filtered_path.exists() and filtered_path.stat().st_size > 1000 and not checkpoint_path.exists():
            print(f"[SKIP] {slug}")
            continue

        print(f"\n[FILTERING] {slug}")
        raw_text = raw_file.read_text(encoding="utf-8")
        title = raw_text.split('\n')[0].replace('# ', '').strip()

        elon_text = filter_transcript(slug, raw_text)
        if not elon_text.strip():
            elon_text = "[No Elon content found — transcript may be predominantly interviewer]"

        output = f"# {title}\n## Elon Musk — Filtered Words Only\n**Layer**: first_order\n**Source**: podcast\n\n---\n\n{elon_text}"
        filtered_path.write_text(output, encoding="utf-8")
        first_order_path.write_text(output, encoding="utf-8")
        print(f"  Saved: {filtered_path.stat().st_size // 1024} KB")
        print(f"  Cooling down 60s before next transcript...")
        time.sleep(60)

    print("\nPhase 1B complete.")
