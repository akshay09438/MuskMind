"""Re-run speech pattern analysis with max_tokens=6000."""
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))

BOOK = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\conversation_style\book_of_elon_raw.txt")
OUT_SP = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\conversation_style\elon_speech_patterns.md")

SPEECH_PROMPT = """Analyze these excerpts from The Book of Elon (Elon Musk's actual words in interviews) and extract his specific speech patterns with REAL EXAMPLES from the text.

Identify and give real examples for each category:

1. OPENER PHRASES — How does Elon begin answers? List 8+ with exact quotes.

2. SIGNATURE EXPRESSIONS — Words/phrases uniquely Elon ("obviously", "frankly", "to be honest", "actually", "I mean"). List 10+ with context.

3. NUMBER/DATA PATTERNS — How does he cite specific numbers and data? Give 8 examples.

4. ANALOGY PATTERNS — How does he construct analogies (usually physics/engineering)? Give 6 examples.

5. UNCERTAINTY vs CONVICTION — When does he hedge vs assert strongly? Give 4 examples of each.

6. SENTENCE RHYTHM — Long technical paragraphs vs short punchy sentences. Give examples of both.

7. TOPIC TRANSITIONS — How does he shift topics mid-thought? Give 4 examples.

8. SELF-CORRECTION PATTERNS — When does he stop and restart? Give 4 examples.

9. HUMOR STYLE — How does he make jokes or lighten moments? Give examples.

10. HANDLING PUSHBACK — When challenged, what's his verbal pattern? Give examples.

Quote exactly from the text provided. This trains an AI to sound like Elon.

--- BOOK EXCERPTS ---
{content}"""

text = BOOK.read_text(encoding="utf-8")
step = len(text) // 5
samples = [text[i * step: i * step + 8000] for i in range(5)]
combined = "\n\n[...]\n\n".join(samples)
print(f"Combined sample: {len(combined)//1024}KB", flush=True)

result = ""
for attempt in range(5):
    try:
        print(f"Attempt {attempt+1}...", flush=True)
        resp = client.chat.completions.create(
            model="gpt-oss-120b",
            messages=[{"role": "user", "content": SPEECH_PROMPT.format(content=combined)}],
            max_tokens=6000,
            temperature=0.2
        )
        time.sleep(35)
        result = (resp.choices[0].message.content or "").strip()
        if result:
            print(f"Got {len(result)} chars", flush=True)
            break
        print("Empty response, retrying...", flush=True)
    except Exception as e:
        err = str(e).lower()
        if "rate" in err or "429" in err:
            wait = 60 * (attempt + 1)
            print(f"Rate limit, waiting {wait}s...", flush=True)
            time.sleep(wait)
        else:
            print(f"Error: {e}", flush=True)
            time.sleep(15)

if result:
    output = f"""# Elon Musk — Speech Pattern Analysis
**Layer**: conversation_style
**Source**: The Book of Elon (book_of_elon_raw.txt)
**Purpose**: Fine-tuning reference for voice and cadence replication
**Sections**: 10 categories with real quotes from the book

---

{result}
"""
    OUT_SP.write_text(output, encoding="utf-8")
    print(f"Saved: {OUT_SP.stat().st_size // 1024}KB", flush=True)
else:
    print("FAILED — no content generated", flush=True)
