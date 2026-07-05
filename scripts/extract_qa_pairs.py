"""
5th Layer: Extract Q&A pairs from all Elon sources for fine-tuning dataset.

Sources:
  1. The Book of Elon PDF (Q: ... answer format + topic quotes)
  2. Book_of_Elon_Transcripts.docx (26 YouTube transcripts)
  3. ELON transcribe.docx (raw timestamped transcripts)
  4. Musky musk.docx (raw timestamped transcripts)
  5. 91 raw podcast transcripts (knowledge_base/podcasts/raw/)

Output: knowledge_base/conversation_style/elon_qa_pairs.jsonl
"""
import os
import re
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from pypdf import PdfReader
from docx import Document
from cerebras.cloud.sdk import Cerebras

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))

OUT_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\conversation_style")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "elon_qa_pairs.jsonl"

RAW_PODCASTS = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\podcasts\raw")

BOOK_PDF     = Path(r"C:\Users\Akshay\OneDrive\Desktop\The+Book+of+Elon+Free+PDF (1).pdf")
DOCX_1       = Path(r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON PODCAST\Book_of_Elon_Transcripts.docx")
DOCX_2       = Path(r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON PODCAST\ELON transcribe.docx")
DOCX_3       = Path(r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON PODCAST\Musky musk.docx")

# ─── HELPERS ────────────────────────────────────────────────────────────────

def strip_timestamps(text: str) -> str:
    """Remove YouTube timestamp patterns like '0:13', '13 seconds', '1 minute, 9 seconds'"""
    text = re.sub(r'\d+:\d+\s*\d*\s*(seconds?|minutes?|hours?)?,?\s*\d*\s*(seconds?|minutes?)?', ' ', text)
    text = re.sub(r'\b\d+:\d+(:\d+)?\b', ' ', text)
    text = re.sub(r'\b\d+\s+seconds?\b', ' ', text)
    text = re.sub(r'\b\d+\s+minutes?\b', ' ', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


def save_pair(question: str, answer: str, source: str, pairs: list):
    q = question.strip()
    a = answer.strip()
    if len(q) < 10 or len(a) < 50:
        return
    # Remove generic filler
    if a.lower().startswith(("um ", "uh ", "yeah, ", "so, ")):
        pass  # keep — these are authentic Elon speech patterns
    pairs.append({"instruction": q, "response": a, "source": source})


def call_cerebras(prompt: str) -> str:
    for attempt in range(5):
        try:
            response = client.chat.completions.create(
                model="gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.2
            )
            time.sleep(35)
            return response.choices[0].message.content.strip()
        except Exception as e:
            err = str(e).lower()
            if "rate" in err or "429" in err:
                wait = 60 * (attempt + 1)
                print(f"      Rate limit, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                time.sleep(15)
    return ""


EXTRACT_PROMPT = """You are extracting Q&A pairs from an Elon Musk interview/transcript for a fine-tuning dataset.

Rules:
1. Extract EVERY exchange where someone asks Elon a question and he gives a substantive answer (40+ words)
2. Clean up the question — make it a clear, natural question someone would ask Elon
3. Keep Elon's answer VERBATIM — do not paraphrase, do not clean up his speech patterns ("yeah", "um", "I mean" — keep them all)
4. Skip exchanges where Elon gives a one-word or one-sentence answer
5. Skip exchanges where the "question" is actually Elon talking

Return ONLY valid JSON array, no other text:
[
  {{"question": "...", "answer": "..."}},
  ...
]

If there are no valid Q&A pairs, return: []

TRANSCRIPT CHUNK:
{chunk}"""


# ─── SOURCE 1: THE BOOK OF ELON PDF ─────────────────────────────────────────

def extract_from_book_pdf() -> list:
    print("\n[SOURCE 1] The Book of Elon PDF")
    pairs = []

    reader = PdfReader(str(BOOK_PDF))
    full_text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            full_text += t + "\n"

    # Method A: Find explicit Q: ... Answer patterns
    # Pattern: "Q: [question]\n[answer until next Q: or chapter heading]"
    qa_pattern = re.compile(
        r'Q:\s*(.+?)\n((?:(?!Q:|^[A-Z\s]{5,}$).)+)',
        re.MULTILINE | re.DOTALL
    )

    matches = qa_pattern.findall(full_text)
    print(f"  Found {len(matches)} explicit Q: patterns")

    for q_text, a_text in matches:
        q_clean = q_text.strip().replace('\n', ' ')
        a_clean = re.sub(r'\s+', ' ', a_text).strip()
        # Remove footnote numbers (superscript numbers at end of sentences)
        a_clean = re.sub(r'\d{1,3}\s*$', '', a_clean).strip()
        a_clean = re.sub(r'(\w)\d{1,3}(\s)', r'\1\2', a_clean)
        save_pair(q_clean, a_clean, "book_of_elon_pdf", pairs)

    # Method B: Chapter-header quotes as synthetic Q&A
    # Find chapter headers (ALL CAPS lines) followed by quotes
    lines = full_text.split('\n')
    current_topic = ""
    topic_quotes = []

    SECTION_HEADERS = {
        "BE USEFUL": "What does it mean to be useful?",
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

    for header, question in SECTION_HEADERS.items():
        # Find text after this header
        idx = full_text.upper().find(header)
        if idx == -1:
            continue
        section_text = full_text[idx + len(header): idx + len(header) + 3000]
        # Take first 800 chars as the "answer block" (Elon's quotes on this topic)
        answer_block = re.sub(r'\s+', ' ', section_text[:800]).strip()
        answer_block = re.sub(r'\d{1,3}\s', ' ', answer_block)  # remove footnote numbers
        if len(answer_block) > 100:
            save_pair(question, answer_block, "book_of_elon_topics", pairs)

    print(f"  Total pairs from PDF: {len(pairs)}")
    return pairs


# ─── SOURCE 2: DOCX FILES ────────────────────────────────────────────────────

MAX_DOCX_CHUNKS = 25  # Sample at most 25 chunks per DOCX (~14 min per file)

def extract_from_docx(path: Path, source_name: str) -> list:
    print(f"\n[SOURCE] {path.name}", flush=True)
    pairs = []

    doc = Document(str(path))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    full_text = strip_timestamps('\n'.join(paragraphs))

    chunk_size = 6000
    all_chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
    total = len(all_chunks)

    # Sample evenly if too many chunks
    if total > MAX_DOCX_CHUNKS:
        step = total // MAX_DOCX_CHUNKS
        chunks = [all_chunks[i * step] for i in range(MAX_DOCX_CHUNKS)]
        print(f"  {total} chunks total, sampling {len(chunks)} evenly spaced...", flush=True)
    else:
        chunks = all_chunks
        print(f"  {len(chunks)} chunks to process...", flush=True)

    for i, chunk in enumerate(chunks):
        result = call_cerebras(EXTRACT_PROMPT.format(chunk=chunk))
        if not result:
            print(f"  {i+1}", end=" ", flush=True)
            continue
        try:
            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            if json_match:
                qa_list = json.loads(json_match.group())
                for item in qa_list:
                    if isinstance(item, dict) and 'question' in item and 'answer' in item:
                        save_pair(item['question'], item['answer'], source_name, pairs)
        except json.JSONDecodeError:
            pass
        print(f"{i+1}", end=" ", flush=True)

    print(f"\n  Pairs extracted: {len(pairs)}", flush=True)
    return pairs


# ─── SOURCE 3: RAW PODCAST TRANSCRIPTS ───────────────────────────────────────

def extract_from_podcasts() -> list:
    print(f"\n[SOURCE] Raw Podcast Transcripts", flush=True)
    pairs = []

    raw_files = sorted(RAW_PODCASTS.glob("*.md"))
    print(f"  Found {len(raw_files)} transcripts", flush=True)

    for i, f in enumerate(raw_files):
        raw = f.read_text(encoding="utf-8")
        cleaned = strip_timestamps(raw)

        # Only process if file has enough content
        if len(cleaned) < 500:
            continue

        # Take first 6000 chars of each transcript (enough for main Q&A)
        chunk = cleaned[:6000]
        result = call_cerebras(EXTRACT_PROMPT.format(chunk=chunk))
        if not result:
            print(f"  {i+1}", end=" ", flush=True)
            continue
        try:
            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            if json_match:
                qa_list = json.loads(json_match.group())
                for item in qa_list:
                    if isinstance(item, dict) and 'question' in item and 'answer' in item:
                        save_pair(item['question'], item['answer'], f"podcast_{f.stem}", pairs)
        except json.JSONDecodeError:
            pass
        print(f"{i+1}", end=" ", flush=True)

    print(f"\n  Pairs extracted: {len(pairs)}")
    return pairs


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def append_pairs(pairs: list):
    """Append pairs to JSONL immediately — no data loss if script crashes later."""
    with open(OUT_FILE, 'a', encoding='utf-8') as f:
        for pair in pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    print("=" * 60, flush=True)
    print("5th Layer: Extracting Elon Q&A Pairs for Fine-Tuning", flush=True)
    print("=" * 60, flush=True)

    # Clear output file at start
    OUT_FILE.write_text("", encoding="utf-8")

    # Source 1: Book PDF (no LLM needed — direct regex)
    pairs1 = extract_from_book_pdf()
    append_pairs(pairs1)
    print(f"  [SAVED] {len(pairs1)} pairs from Book PDF", flush=True)

    # Source 2: Book of Elon Transcripts DOCX
    pairs2 = extract_from_docx(DOCX_1, "book_of_elon_transcripts")
    append_pairs(pairs2)
    print(f"  [SAVED] {len(pairs2)} pairs from DOCX 1", flush=True)

    # Source 3: ELON transcribe DOCX
    pairs3 = extract_from_docx(DOCX_2, "elon_transcribe")
    append_pairs(pairs3)
    print(f"  [SAVED] {len(pairs3)} pairs from DOCX 2", flush=True)

    # Source 4: Musky musk DOCX
    pairs4 = extract_from_docx(DOCX_3, "musky_musk")
    append_pairs(pairs4)
    print(f"  [SAVED] {len(pairs4)} pairs from DOCX 3", flush=True)

    # Source 5: Raw podcasts
    pairs5 = extract_from_podcasts()
    append_pairs(pairs5)
    print(f"  [SAVED] {len(pairs5)} pairs from podcasts", flush=True)

    # Deduplicate the full file
    all_pairs = []
    seen = set()
    with open(OUT_FILE, 'r', encoding='utf-8') as f:
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

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        for pair in all_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')

    print(f"\n{'='*60}", flush=True)
    print(f"DONE. {len(all_pairs)} unique Q&A pairs saved to:", flush=True)
    print(f"  {OUT_FILE}", flush=True)
    print(f"\nBreakdown by source:", flush=True)
    from collections import Counter
    counts = Counter(p['source'].split('_podcast_')[0] if 'podcast_' in p['source'] else p['source'] for p in all_pairs)
    for src, count in counts.most_common():
        print(f"  {src}: {count}", flush=True)
