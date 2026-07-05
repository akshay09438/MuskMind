"""
Layer 5: Generate Q&A fine-tuning pairs + speech pattern analysis
from The Book of Elon PDF (already extracted to book_of_elon_raw.txt).

Sources: regex Q: patterns + chapter themes + 20 sampled chunks
API calls: 21 Cerebras calls (~13 minutes total)
"""
import os
import re
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))

BOOK = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\conversation_style\book_of_elon_raw.txt")
OUT_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\conversation_style")
OUT_QA = OUT_DIR / "elon_qa_pairs.jsonl"
OUT_SP = OUT_DIR / "elon_speech_patterns.md"


def clean(text: str) -> str:
    text = re.sub(r'\[PAGE \d+\]', '', text)
    text = re.sub(r'(\w)\d{1,3}(\s|$)', r'\1\2', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def is_valid_pair(q: str, a: str) -> bool:
    return len(q) >= 10 and len(a) >= 50


def append_pairs(pairs: list) -> None:
    with open(OUT_QA, 'a', encoding='utf-8') as f:
        for p in pairs:
            f.write(json.dumps(p, ensure_ascii=False) + '\n')


def extract_regex_qa(text: str) -> list:
    """Find all explicit Q: ... answer blocks in the book."""
    pairs = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('Q:'):
            q_parts = [line[2:].strip()]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('Q:'):
                next_line = lines[i].strip()
                if len(next_line) > 80 and next_line[0].islower():
                    break
                if re.match(r'^\[PAGE', next_line):
                    i += 1
                    continue
                q_parts.append(next_line)
                i += 1
                if len(' '.join(q_parts)) > 300:
                    break
            question = clean(' '.join(q_parts))

            a_parts = []
            while i < len(lines):
                l = lines[i].strip()
                if l.startswith('Q:'):
                    break
                if re.match(r'^[A-Z\s]{10,}$', l) and len(l) > 8:
                    break
                if not re.match(r'^\[PAGE', l):
                    a_parts.append(l)
                i += 1
            answer = clean(' '.join(a_parts))

            if is_valid_pair(question, answer):
                pairs.append({
                    "instruction": question,
                    "response": answer,
                    "source": "book_of_elon_regex"
                })
        else:
            i += 1
    return pairs


CHAPTER_THEMES = {
    "BE USEFUL": "What does it mean to be useful in the world?",
    "FIGHT FOR THE FUTURE": "How do you think about fighting for the future?",
    "OBSESS FOR SUCCESS": "What's your philosophy on obsession and success?",
    "WORK LIKE HELL": "How hard do you actually work and why?",
    "FEEL THE FEAR": "How do you handle fear when making big decisions?",
    "FIRST-PRINCIPLES THINKING": "Can you explain first principles thinking?",
    "THINKING IN LIMITS": "How do you think about physical limits in engineering?",
    "ENGINEERING IS MAGIC": "What do you think about engineering?",
    "RECRUIT FOR EXCEPTIONAL ABILITY": "How do you hire people?",
    "THE ALGORITHM": "What is your algorithm for running companies?",
    "MANIACAL URGENCY": "Why do you push teams so hard on speed?",
    "SIMPLE COMMUNICATION": "What's your philosophy on communication in organizations?",
    "INNOVATION NEEDS PERMISSION TO FAIL": "How do you think about failure and innovation?",
    "MISALIGNED ARTIFICIAL SUPERINTELLIGENCE": "What are your concerns about AI?",
    "BECOMING MULTIPLANETARY": "Why does humanity need to become multiplanetary?",
    "POPULATION COLLAPSE": "What do you think about population decline?",
    "SUSTAINABLE ABUNDANCE": "What's your vision for sustainable energy?",
}


def extract_theme_qa(text: str) -> list:
    pairs = []
    upper_text = text.upper()
    for header, question in CHAPTER_THEMES.items():
        idx = upper_text.find(header)
        if idx == -1:
            continue
        section = text[idx + len(header): idx + len(header) + 1200]
        answer = clean(section[:900])
        if is_valid_pair(question, answer):
            pairs.append({
                "instruction": question,
                "response": answer,
                "source": "book_of_elon_themes"
            })
    return pairs


EXTRACT_PROMPT = """Extract Q&A pairs from this Elon Musk book excerpt for a fine-tuning dataset.

Rules:
1. Only extract where someone asks Elon a question and he gives a substantive answer (40+ words)
2. Make the question natural and clear
3. Keep Elon's answer VERBATIM — do not paraphrase. Keep "yeah", "I mean", "well" etc.
4. Skip one-word or one-sentence answers

Return ONLY valid JSON array, no other text:
[
  {{"question": "...", "answer": "..."}},
  ...
]

If no valid pairs found, return: []

EXCERPT:
{chunk}"""


def call_cerebras(prompt: str) -> str:
    for attempt in range(5):
        try:
            response = client.chat.completions.create(
                model="gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,
                temperature=0.2
            )
            time.sleep(35)
            return response.choices[0].message.content.strip()
        except Exception as e:
            err = str(e).lower()
            if "rate" in err or "429" in err:
                wait = 60 * (attempt + 1)
                print(f"  Rate limit, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                print(f"  Error: {e}", flush=True)
                time.sleep(15)
    return ""


N_CHUNKS = 20
CHUNK_SIZE = 6000


def extract_chunk_qa(text: str) -> list:
    pairs = []
    step = len(text) // N_CHUNKS
    print(f"\n  Sampling {N_CHUNKS} chunks ({CHUNK_SIZE} chars each) from {len(text)//1024}KB book...", flush=True)

    for i in range(N_CHUNKS):
        start = i * step
        chunk = text[start: start + CHUNK_SIZE]
        print(f"  Chunk {i+1}/{N_CHUNKS}...", end=" ", flush=True)

        result = call_cerebras(EXTRACT_PROMPT.format(chunk=chunk))
        if not result:
            print("skip", flush=True)
            continue

        try:
            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            if json_match:
                qa_list = json.loads(json_match.group())
                chunk_pairs = []
                for item in qa_list:
                    if isinstance(item, dict) and 'question' in item and 'answer' in item:
                        q = item['question'].strip()
                        a = item['answer'].strip()
                        if is_valid_pair(q, a):
                            chunk_pairs.append({
                                "instruction": q,
                                "response": a,
                                "source": f"book_of_elon_chunk_{i+1}"
                            })
                append_pairs(chunk_pairs)
                pairs.extend(chunk_pairs)
                print(f"{len(chunk_pairs)} pairs", flush=True)
            else:
                print("no JSON", flush=True)
        except json.JSONDecodeError:
            print("JSON error", flush=True)

    return pairs


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

N_SPEECH_SAMPLES = 5
SPEECH_SAMPLE_SIZE = 8000


def generate_speech_patterns(text: str) -> None:
    print("\n[SPEECH PATTERNS] Sampling book for speech analysis...", flush=True)
    step = len(text) // N_SPEECH_SAMPLES
    samples = [text[i * step: i * step + SPEECH_SAMPLE_SIZE] for i in range(N_SPEECH_SAMPLES)]
    combined = "\n\n[...]\n\n".join(samples)
    print(f"  Combined sample: {len(combined)//1024}KB", flush=True)

    # Use 6000 max_tokens — speech analysis needs more space than Q&A extraction
    prompt = SPEECH_PROMPT.format(content=combined)
    result = ""
    for attempt in range(5):
        try:
            response = client.chat.completions.create(
                model="gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=6000,
                temperature=0.2
            )
            time.sleep(35)
            result = (response.choices[0].message.content or "").strip()
            if result:
                break
        except Exception as e:
            err = str(e).lower()
            if "rate" in err or "429" in err:
                wait = 60 * (attempt + 1)
                print(f"  Rate limit, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                print(f"  Error: {e}", flush=True)
                time.sleep(15)
    if not result:
        print("  FAILED — no analysis generated", flush=True)
        return

    output = f"""# Elon Musk — Speech Pattern Analysis
**Layer**: conversation_style
**Source**: The Book of Elon (book_of_elon_raw.txt)
**Purpose**: Fine-tuning reference for voice and cadence replication
**Sections**: 10 categories with real quotes from the book

---

{result}
"""
    OUT_SP.write_text(output, encoding="utf-8")
    print(f"  Saved: {OUT_SP.name} ({OUT_SP.stat().st_size // 1024}KB)", flush=True)


if __name__ == "__main__":
    print("=" * 60, flush=True)
    print("Layer 5: Book of Elon — Q&A + Speech Patterns", flush=True)
    print("=" * 60, flush=True)

    OUT_QA.write_text("", encoding="utf-8")

    text = BOOK.read_text(encoding="utf-8")
    print(f"Book loaded: {len(text)//1024}KB", flush=True)

    print("\n[1/4] Regex Q&A extraction...", flush=True)
    pairs1 = extract_regex_qa(text)
    append_pairs(pairs1)
    print(f"  Found {len(pairs1)} pairs", flush=True)

    print("\n[2/4] Chapter theme Q&A...", flush=True)
    pairs2 = extract_theme_qa(text)
    append_pairs(pairs2)
    print(f"  Found {len(pairs2)} pairs", flush=True)

    print("\n[3/4] Cerebras sampled chunk extraction...", flush=True)
    pairs3 = extract_chunk_qa(text)
    print(f"  Found {len(pairs3)} pairs from chunks", flush=True)

    print("\n[4/4] Speech pattern analysis...", flush=True)
    generate_speech_patterns(text)

    print("\nDeduplicating...", flush=True)
    all_pairs = []
    seen = set()
    with open(OUT_QA, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                p = json.loads(line)
                key = p["instruction"][:80].lower()
                if key not in seen:
                    seen.add(key)
                    all_pairs.append(p)
            except Exception:
                pass

    with open(OUT_QA, 'w', encoding='utf-8') as f:
        for p in all_pairs:
            f.write(json.dumps(p, ensure_ascii=False) + '\n')

    print(f"\n{'='*60}", flush=True)
    print(f"DONE.", flush=True)
    print(f"  Q&A pairs: {len(all_pairs)} unique pairs -> {OUT_QA}", flush=True)
    print(f"  Speech patterns: {OUT_SP}", flush=True)
    from collections import Counter
    counts = Counter(p['source'].split('_chunk_')[0] for p in all_pairs)
    for src, count in counts.most_common():
        print(f"    {src}: {count}", flush=True)
