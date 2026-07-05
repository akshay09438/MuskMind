"""
5th Layer Part 2: Analyze HOW Elon talks — speech patterns, cadence, vocabulary.
Reads all filtered podcast transcripts (Elon-only words).
Uses Cerebras to extract patterns, then saves elon_speech_patterns.md
"""
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))

FILTERED = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\podcasts\filtered")
OUT_DIR  = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\conversation_style")
OUT_DIR.mkdir(parents=True, exist_ok=True)

PATTERN_PROMPT = """Analyze these transcripts of Elon Musk speaking (his words only) and extract his specific speech patterns.

Identify and give REAL EXAMPLES from the text for each:

1. OPENER PHRASES — How does Elon begin his answers? (e.g. "Well, I think...", "Yeah, so...", "I mean...")
   List 10+ with actual examples from text.

2. SIGNATURE EXPRESSIONS — Words/phrases uniquely Elon (e.g. "obviously", "frankly", "to be honest", "actually")
   List 15+ with context showing how he uses each.

3. NUMBER/DATA PATTERNS — How does he use specific numbers?
   Give 10 examples showing his style of citing data.

4. ANALOGY PATTERNS — How does he construct analogies?
   Give 8 examples showing his analogy style (usually physics/engineering/history).

5. UNCERTAINTY vs CONVICTION language — When does he hedge vs assert?
   Give 5 examples of each.

6. SENTENCE RHYTHM — Describe his sentence structure. When does he use long paragraphs vs short punchy sentences?
   Give examples of both.

7. TOPIC TRANSITIONS — How does he shift topics or redirect mid-thought?
   Give 5 examples.

8. SELF-CORRECTION PATTERNS — When does he stop and restart? What triggers it?
   Give 5 examples.

9. HUMOR STYLE — How does Elon make jokes or lighten moments?
   Give examples.

10. HOW HE HANDLES PUSHBACK — When someone challenges him, what's his verbal pattern?
    Give examples.

Be extremely specific. Quote exact phrases. This will be used to train an AI to sound exactly like Elon.

--- ELON'S WORDS ---
{content}"""


def call_cerebras(prompt: str) -> str:
    for attempt in range(5):
        try:
            response = client.chat.completions.create(
                model="gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=6000,
                temperature=0.2
            )
            time.sleep(35)
            return response.choices[0].message.content.strip()
        except Exception as e:
            err = str(e).lower()
            if "rate" in err or "429" in err:
                wait = 60 * (attempt + 1)
                print(f"\n  Rate limit, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                time.sleep(15)
    return ""


if __name__ == "__main__":
    print("=" * 60)
    print("5th Layer: Elon Speech Pattern Analysis")
    print("=" * 60)

    # Load filtered transcripts — sample 20 diverse ones for analysis
    filtered_files = sorted(FILTERED.glob("*.md"))
    print(f"Found {len(filtered_files)} filtered transcripts")

    # Pick a diverse sample: every 4th file = ~22 transcripts
    sample_files = filtered_files[::4][:20]
    print(f"Sampling {len(sample_files)} transcripts for analysis\n")

    # Combine sampled content
    combined = []
    for f in sample_files:
        text = f.read_text(encoding="utf-8")
        # Take first 3000 chars of each
        combined.append(f"\n\n=== {f.stem} ===\n{text[:3000]}")

    content = "\n".join(combined)
    if len(content) > 60000:
        content = content[:60000]

    print(f"Total content: {len(content)//1024}KB")
    print("Analyzing speech patterns with Cerebras...")

    analysis = call_cerebras(PATTERN_PROMPT.format(content=content))

    if analysis:
        output = f"""# Elon Musk — Speech Pattern Analysis
**Layer**: conversation_style
**Source**: 20 filtered podcast transcripts (Elon-only words)
**Purpose**: Fine-tuning reference for voice/cadence replication

---

{analysis}
"""
        out_path = OUT_DIR / "elon_speech_patterns.md"
        out_path.write_text(output, encoding="utf-8")
        print(f"\nSaved: {out_path} ({out_path.stat().st_size // 1024}KB)")
    else:
        print("FAILED — no analysis generated")

    print("\nDone.")
