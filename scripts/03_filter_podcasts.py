"""
Phase 1B Step 2: Use Claude API to extract ONLY Elon's words from each transcript.
Reads from knowledge_base/podcasts/raw/
Writes to knowledge_base/podcasts/filtered/ and knowledge_base/first_order/
"""
import anthropic
import os
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

RAW_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\podcasts\raw")
FILTERED_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\podcasts\filtered")
FIRST_ORDER_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\first_order")
FILTERED_DIR.mkdir(parents=True, exist_ok=True)
FIRST_ORDER_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 6000

FILTER_PROMPT = """You are processing a raw podcast/interview transcript. Your ONLY job is to extract the words spoken by Elon Musk and output them.

RULES:
1. Output ONLY text that Elon Musk spoke. Remove everything the interviewer, host, or any other person said.
2. Keep Elon's exact words verbatim — do not paraphrase, summarize, or rewrite anything.
3. Remove all timestamps (e.g., "4:23", "4 minutes 23 seconds").
4. Remove filler markers like [laughter], [applause], [music], [inaudible].
5. When you're not 100% sure who is speaking, use context clues:
   - Elon typically speaks in long technical paragraphs about SpaceX, Tesla, AI, Mars, physics, manufacturing, first principles, energy, civilization
   - Interviewers typically ask short questions, say "right", "yeah", "interesting", "let me ask you about X"
   - When in doubt and the text sounds like a question directed AT Elon — exclude it
   - When in doubt and the text sounds like a technical explanation — include it
6. Do NOT add any labels like "Elon:", "EM:", "[Elon speaking]" — just output his raw words
7. Separate different speech segments with a single blank line
8. If an entire chunk seems to be ONLY the interviewer speaking, output: [NO ELON CONTENT IN THIS SECTION]

Here is the transcript chunk to process:

---
{chunk}
---

Output Elon's words only:"""


def filter_transcript(raw_text: str, title: str) -> str:
    chunks = []
    start = 0
    while start < len(raw_text):
        chunks.append(raw_text[start:start + CHUNK_SIZE])
        start += CHUNK_SIZE

    print(f"    Processing {len(chunks)} chunks...")
    elon_parts = []

    for i, chunk in enumerate(chunks):
        print(f"    Chunk {i+1}/{len(chunks)}...", end=" ", flush=True)
        for attempt in range(4):
            try:
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=4000,
                    messages=[{
                        "role": "user",
                        "content": FILTER_PROMPT.format(chunk=chunk)
                    }]
                )
                result = response.content[0].text.strip()
                if result and result != "[NO ELON CONTENT IN THIS SECTION]":
                    elon_parts.append(result)
                print("OK")
                time.sleep(2)
                break
            except Exception as e:
                err = str(e)
                if "rate" in err.lower() or "529" in err or "overload" in err.lower():
                    wait = 30 * (attempt + 1)
                    print(f"rate limit, waiting {wait}s...", end=" ")
                    time.sleep(wait)
                else:
                    print(f"error: {e}, retrying...")
                    time.sleep(5)

    return "\n\n".join(elon_parts)


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 1B Step 2: Filtering Podcasts to Elon-Only")
    print("=" * 60)

    raw_files = sorted(RAW_DIR.glob("*.md"))
    print(f"Found {len(raw_files)} raw transcript files\n")

    for raw_file in raw_files:
        slug = raw_file.stem
        filtered_path = FILTERED_DIR / f"{slug}_elon_only.md"
        first_order_path = FIRST_ORDER_DIR / f"podcast_{slug}_elon_only.md"

        if filtered_path.exists() and filtered_path.stat().st_size > 1000:
            print(f"[SKIP] {slug} — already filtered")
            continue

        print(f"\n[FILTERING] {slug}")
        raw_text = raw_file.read_text(encoding="utf-8")
        title = raw_text.split('\n')[0].replace('# ', '')

        elon_text = filter_transcript(raw_text, title)

        if not elon_text.strip():
            print(f"  WARNING: No Elon content found in {slug}")
            elon_text = "[No Elon content extracted — transcript may be predominantly interviewer]"

        output = f"# {title}\n## Elon Musk — Filtered Words Only\n**Layer**: first_order\n**Source**: podcast\n\n---\n\n{elon_text}"
        filtered_path.write_text(output, encoding="utf-8")
        first_order_path.write_text(output, encoding="utf-8")

        size_kb = filtered_path.stat().st_size // 1024
        print(f"  [DONE] {slug} — {size_kb} KB of Elon content saved")

    all_files = list(FIRST_ORDER_DIR.glob("podcast_*"))
    print(f"\n\nPhase 1B Complete. {len(all_files)} podcast files in first_order/")
