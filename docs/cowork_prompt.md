# MindMusk — Full Knowledge Base Generation
## Complete Instructions for Claude Co-Work

---

## WHO YOU ARE AND WHAT YOU ARE DOING

You are helping build **MindMusk** — an AI product that replicates how Elon Musk thinks, reasons, and speaks. When a user asks MindMusk a question, it should respond exactly how Elon would: using first principles, physics-based reasoning, Socratic questioning, blunt honesty, and a specific vocabulary.

To make this work, you need to build a **4-layer knowledge base** from two types of source material:
1. **41 books** that Elon Musk has read and that shaped his worldview
2. **~55-60 podcast/interview transcripts** where Elon speaks directly

You will process these sources into 4 layers:
- **1st order** = Raw cleaned content from each source
- **2nd order** = Per-source synthesis: how Elon thinks about THIS specific book/talk
- **3rd order** = Cross-source thematic synthesis: 15 deep theme documents
- **4th order** = Master mental models: 5 ultra-deep documents that capture Elon's complete worldview

**You do these in order. Do not skip ahead. Complete Phase 1 entirely before starting Phase 2. Complete Phase 2 entirely before starting Phase 3. Complete Phase 3 entirely before starting Phase 4.**

---

## TECH STACK — READ THIS CAREFULLY

- **OS**: Windows 11 ARM64. This matters because some Python packages DO NOT work.
- **Python**: 3.11 ARM64 — located at `C:\Users\Akshay\AppData\Local\Programs\Python\Python311-arm64\python.exe`
- **DO NOT try to install**: PyMuPDF, chromadb, grpcio — they require C++ compilation that fails on this machine
- **USE INSTEAD**:
  - `pypdf` — for reading PDF files (pure Python, works fine)
  - `python-docx` — for reading .docx files (pure Python, works fine)
  - `anthropic` — for Claude API calls
  - `voyageai` — for embeddings (Phase 5 only, not your job right now)
  - `numpy` — already installed

**API Keys** are stored in: `C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env`

The file looks like this:
```
ANTHROPIC_API_KEY=sk-ant-api03-...
VOYAGE_API_KEY=pa-...
```

To load them in Python:
```python
from dotenv import load_dotenv
import os
load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
```

---

## DIRECTORY STRUCTURE — WHERE EVERYTHING LIVES

```
C:\Users\Akshay\OneDrive\Desktop\
│
├── ELON LLM\                          ← SOURCE DATA (read only, never modify)
│   ├── ELON BOOKS\
│   │   ├── AI AND MACHINE LEARNING\   ← 5 PDFs (already done for 1st order)
│   │   ├── Fiction\                   ← 10 PDFs
│   │   ├── Sciences\                  ← 4 PDFs
│   │   ├── Rocket Science and Engineering\  ← 2 PDFs
│   │   ├── History\                   ← 12 PDFs
│   │   └── Business and economics\    ← 8 PDFs
│   ├── ELON PODCAST\
│   │   ├── Book_of_Elon_Transcripts.docx   ← 26 transcripts
│   │   ├── ELON transcribe.docx            ← 14 transcripts
│   │   └── Musky musk.docx                 ← 19 transcripts
│   └── The+Book+of+Elon+Free+PDF.pdf       ← Primary Elon biography
│
└── MindMusk\                          ← THE PROJECT (write everything here)
    ├── .env                           ← API keys
    ├── knowledge_base\
    │   ├── first_order\               ← YOU WRITE HERE IN PHASE 1
    │   ├── second_order\              ← YOU WRITE HERE IN PHASE 2
    │   ├── third_order\               ← YOU WRITE HERE IN PHASE 3
    │   ├── fourth_order\              ← YOU WRITE HERE IN PHASE 4
    │   └── podcasts\
    │       ├── raw\                   ← Extracted podcast text per transcript
    │       └── filtered\              ← Elon-only words per transcript
    ├── vector_db\                     ← Already has embeddings for 5 AI books
    └── scripts\
        └── ingest_knowledge_base.py   ← Existing embedding script
```

**Create all missing directories before starting.** Use this Python snippet:
```python
from pathlib import Path
dirs = [
    r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\first_order",
    r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\second_order",
    r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\third_order",
    r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\fourth_order",
    r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\podcasts\raw",
    r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\podcasts\filtered",
]
for d in dirs:
    Path(d).mkdir(parents=True, exist_ok=True)
    print(f"Ready: {d}")
```

---

## ALL SOURCE FILES — COMPLETE LIST

### BOOKS (41 total)

**AI AND MACHINE LEARNING** — `C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\AI AND MACHINE LEARNING\`
1. `Life 3.0 Being Human in the Age of Artificial Intelligence by.pdf` → slug: `life_3_0`
2. `Superintelligence Paths, Dangers, Strategies by Nick Bostrom.pdf` → slug: `superintelligence`
3. `Human Compatible Artificial Intelligence and the Problem of.pdf` → slug: `human_compatible`
4. `Our Final Invention Artificial Intelligence and the End of the.pdf` → slug: `our_final_invention`
5. `Deep Learning by Ian Goodfellow, Yoshua Bengio, and Aaron.pdf` → slug: `deep_learning`

**Fiction** — `C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Fiction\`
6. `The Hitchhiker's Guide to the Galaxy by Douglas Adams.pdf` → slug: `hitchhikers_guide`
7. `The Lord of the Rings by J.R.R. Tolkien.pdf` → slug: `lord_of_the_rings`
8. `Dune series by Frank Herbert.pdf` → slug: `dune`
9. `Stranger in a Strange Land by Robert A. Heinlein.pdf` → slug: `stranger_strange_land`
10. `The Moon Is a Harsh Mistress by Robert A. Heinlein.pdf` → slug: `moon_harsh_mistress`
11. `The Machine Stops by E. M. Forster.pdf` → slug: `machine_stops`
12. `A Game of Thrones by George R. R. Martin.pdf` → slug: `game_of_thrones`
13. `Waiting for Godot by Samuel Becket.pdf` → slug: `waiting_for_godot`
14. `Atlas Shrugged by Ayn Rand.pdf` → slug: `atlas_shrugged`
15. `The Fault in Our Stars by John Green.pdf` → slug: `fault_in_our_stars`

**Sciences** — `C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Sciences\`
16. `If the Universe Is Teeming with Aliens…Where Is Everybody.pdf` → slug: `fermi_paradox`
17. `The Skeptics' Guide to the Universe How to Know What's.pdf` → slug: `skeptics_guide`
18. `The Selfish Gene by Richard Dawkins.pdf` → slug: `selfish_gene`
19. `What We Owe the Future by William MacAskill.pdf` → slug: `what_we_owe_future`

**Rocket Science and Engineering** — `C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Rocket Science and Enginerring\`
20. `Ignition! An Informal History of Liquid Rocket Propellants.pdf` → slug: `ignition`
21. `Structures Or Why Things Don't Fall Down by J. E. Gordon.pdf` → slug: `structures`

**History** — `C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\History\`
22. `The Lessons of History by Will and Ariel Durant1.pdf` → slug: `lessons_of_history`
23. `The Iliad by Homer.pdf` → slug: `iliad`
24. `The History of the Decline and Fall of the Roman Empire by.pdf` → slug: `decline_fall_rome`
25. `Storm of Steel by Ernst Jünger.pdf` → slug: `storm_of_steel`
26. `On War - Carl von Clausewitz.pdf` → slug: `on_war`
27. `The Wages of Destruction The Making and Breaking of the.pdf` → slug: `wages_of_destruction`
28. `The Fifteen Decisive Battles of the World From Marathon to.pdf` → slug: `fifteen_battles`
29. `The Art of War by Sun Tzu.pdf` → slug: `art_of_war`
30. `Steve Jobs by Walter Isaacson.pdf` → slug: `steve_jobs`
31. `ExploreCreate My Life in Pursuit of New Frontiers, Hidden.pdf` → slug: `explore_create`
32. `Benjamin Franklin by Walter Isaacson.pdf` → slug: `benjamin_franklin`
33. `Man's Search for Meaning by Victor E. Frankl.pdf` → slug: `mans_search_meaning`

**Business and Economics** — `C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Business and econimics\`
34. `Screw Business as Usual Turning Capitalism into a Force for.pdf` → slug: `screw_business`
35. `Masters of Doom How Two Guys Created an Empire and.pdf` → slug: `masters_of_doom`
36. `The Wealth of Nations by Adam Smith.pdf` → slug: `wealth_of_nations`
37. `Zero to One Notes on Startups, or How to Build the Future by.pdf` → slug: `zero_to_one`
38. `What's Our Problem A Self-Help Book for Societies by Tim.pdf` → slug: `whats_our_problem`
39. `Lying by Sam Harris.pdf` → slug: `lying`
40. `The Parasitic Mind How Infectious Ideas Are Killing Common.pdf` → slug: `parasitic_mind`
41. `A Woman Makes a Plan Advice for a Lifetime of Adventure,.pdf` → slug: `woman_makes_plan`

### PODCAST FILES (3 .docx files containing ~55-60 transcripts)
- `C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON PODCAST\Book_of_Elon_Transcripts.docx`
- `C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON PODCAST\ELON transcribe.docx`
- `C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON PODCAST\Musky musk.docx`

---

---

# PHASE 1 — FIRST ORDER (RAW CONTENT)

## What Phase 1 Produces

One `.md` file per source saved to `knowledge_base/first_order/`.

- For **books**: Cleaned extracted text from the PDF, organized with headers
- For **podcasts**: Elon's words ONLY, filtered out from the mixed transcript

File naming:
- Books: `{slug}_first_order.md` (e.g., `dune_first_order.md`)
- Podcasts: `podcast_{slug}_elon_only.md` (e.g., `podcast_lex_fridman_438_elon_only.md`)

---

## Phase 1A — Book PDF Extraction

### The Python Script to Write and Run

Write this script and save it as `C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts\extract_books.py`, then run it:

```python
"""
Phase 1A: Extract text from all book PDFs.
Saves cleaned text to knowledge_base/first_order/{slug}_first_order.md
"""
from pypdf import PdfReader
from pathlib import Path
import re

OUTPUT_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\first_order")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Complete book list: (full_pdf_path, slug, book_title, category)
BOOKS = [
    # AI AND MACHINE LEARNING
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\AI AND MACHINE LEARNING\Life 3.0 Being Human in the Age of Artificial Intelligence by.pdf",
     "life_3_0", "Life 3.0", "AI and Machine Learning"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\AI AND MACHINE LEARNING\Superintelligence Paths, Dangers, Strategies by Nick Bostrom.pdf",
     "superintelligence", "Superintelligence", "AI and Machine Learning"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\AI AND MACHINE LEARNING\Human Compatible Artificial Intelligence and the Problem of.pdf",
     "human_compatible", "Human Compatible", "AI and Machine Learning"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\AI AND MACHINE LEARNING\Our Final Invention Artificial Intelligence and the End of the.pdf",
     "our_final_invention", "Our Final Invention", "AI and Machine Learning"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\AI AND MACHINE LEARNING\Deep Learning by Ian Goodfellow, Yoshua Bengio, and Aaron.pdf",
     "deep_learning", "Deep Learning", "AI and Machine Learning"),
    # FICTION
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Fiction\The Hitchhiker's Guide to the Galaxy by Douglas Adams.pdf",
     "hitchhikers_guide", "The Hitchhiker's Guide to the Galaxy", "Fiction"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Fiction\The Lord of the Rings by J.R.R. Tolkien.pdf",
     "lord_of_the_rings", "The Lord of the Rings", "Fiction"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Fiction\Dune series by Frank Herbert.pdf",
     "dune", "Dune", "Fiction"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Fiction\Stranger in a Strange Land by Robert A. Heinlein.pdf",
     "stranger_strange_land", "Stranger in a Strange Land", "Fiction"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Fiction\The Moon Is a Harsh Mistress by Robert A. Heinlein.pdf",
     "moon_harsh_mistress", "The Moon Is a Harsh Mistress", "Fiction"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Fiction\The Machine Stops by E. M. Forster.pdf",
     "machine_stops", "The Machine Stops", "Fiction"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Fiction\A Game of Thrones by George R. R. Martin.pdf",
     "game_of_thrones", "A Game of Thrones", "Fiction"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Fiction\Waiting for Godot by Samuel Becket.pdf",
     "waiting_for_godot", "Waiting for Godot", "Fiction"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Fiction\Atlas Shrugged by Ayn Rand.pdf",
     "atlas_shrugged", "Atlas Shrugged", "Fiction"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Fiction\The Fault in Our Stars by John Green.pdf",
     "fault_in_our_stars", "The Fault in Our Stars", "Fiction"),
    # SCIENCES
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Sciences\If the Universe Is Teeming with Aliens…Where Is Everybody.pdf",
     "fermi_paradox", "If the Universe Is Teeming with Aliens", "Sciences"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Sciences\The Skeptics' Guide to the Universe How to Know What's.pdf",
     "skeptics_guide", "The Skeptics' Guide to the Universe", "Sciences"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Sciences\The Selfish Gene by Richard Dawkins.pdf",
     "selfish_gene", "The Selfish Gene", "Sciences"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Sciences\What We Owe the Future by William MacAskill.pdf",
     "what_we_owe_future", "What We Owe the Future", "Sciences"),
    # ROCKET SCIENCE
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Rocket Science and Enginerring\Ignition! An Informal History of Liquid Rocket Propellants.pdf",
     "ignition", "Ignition!", "Rocket Science and Engineering"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Rocket Science and Enginerring\Structures Or Why Things Don't Fall Down by J. E. Gordon.pdf",
     "structures", "Structures: Or Why Things Don't Fall Down", "Rocket Science and Engineering"),
    # HISTORY
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\History\The Lessons of History by Will and Ariel Durant1.pdf",
     "lessons_of_history", "The Lessons of History", "History"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\History\The Iliad by Homer.pdf",
     "iliad", "The Iliad", "History"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\History\The History of the Decline and Fall of the Roman Empire by.pdf",
     "decline_fall_rome", "The Decline and Fall of the Roman Empire", "History"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\History\Storm of Steel by Ernst Jünger.pdf",
     "storm_of_steel", "Storm of Steel", "History"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\History\On War - Carl von Clausewitz.pdf",
     "on_war", "On War", "History"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\History\The Wages of Destruction The Making and Breaking of the.pdf",
     "wages_of_destruction", "The Wages of Destruction", "History"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\History\The Fifteen Decisive Battles of the World From Marathon to.pdf",
     "fifteen_battles", "The Fifteen Decisive Battles of the World", "History"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\History\The Art of War by Sun Tzu.pdf",
     "art_of_war", "The Art of War", "History"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\History\Steve Jobs by Walter Isaacson.pdf",
     "steve_jobs", "Steve Jobs", "History"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\History\ExploreCreate My Life in Pursuit of New Frontiers, Hidden.pdf",
     "explore_create", "Explore/Create", "History"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\History\Benjamin Franklin by Walter Isaacson.pdf",
     "benjamin_franklin", "Benjamin Franklin", "History"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\History\Man's Search for Meaning by Victor E. Frankl.pdf",
     "mans_search_meaning", "Man's Search for Meaning", "History"),
    # BUSINESS AND ECONOMICS
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Business and econimics\Screw Business as Usual Turning Capitalism into a Force for.pdf",
     "screw_business", "Screw Business as Usual", "Business and Economics"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Business and econimics\Masters of Doom How Two Guys Created an Empire and.pdf",
     "masters_of_doom", "Masters of Doom", "Business and Economics"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Business and econimics\The Wealth of Nations by Adam Smith.pdf",
     "wealth_of_nations", "The Wealth of Nations", "Business and Economics"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Business and econimics\Zero to One Notes on Startups, or How to Build the Future by.pdf",
     "zero_to_one", "Zero to One", "Business and Economics"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Business and econimics\What's Our Problem A Self-Help Book for Societies by Tim.pdf",
     "whats_our_problem", "What's Our Problem", "Business and Economics"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Business and econimics\Lying by Sam Harris.pdf",
     "lying", "Lying", "Business and Economics"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Business and econimics\The Parasitic Mind How Infectious Ideas Are Killing Common.pdf",
     "parasitic_mind", "The Parasitic Mind", "Business and Economics"),
    (r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\Business and econimics\A Woman Makes a Plan Advice for a Lifetime of Adventure,.pdf",
     "woman_makes_plan", "A Woman Makes a Plan", "Business and Economics"),
]


def clean_text(text: str) -> str:
    """Remove garbage characters from PDF extraction."""
    # Remove null bytes
    text = text.replace('\x00', '')
    # Collapse more than 3 newlines into 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove lines that are just page numbers (single number alone on a line)
    text = re.sub(r'^\s*\d{1,4}\s*$', '', text, flags=re.MULTILINE)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text


def extract_book(pdf_path: str, slug: str, title: str, category: str) -> None:
    out_path = OUTPUT_DIR / f"{slug}_first_order.md"

    # Skip if already done
    if out_path.exists() and out_path.stat().st_size > 5000:
        print(f"  [SKIP] {title} — already extracted ({out_path.stat().st_size // 1024} KB)")
        return

    print(f"  [EXTRACTING] {title}...")
    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        all_text = []

        for page_num, page in enumerate(reader.pages):
            try:
                text = page.extract_text()
                if text:
                    all_text.append(text)
            except Exception as e:
                print(f"    Warning: page {page_num} failed: {e}")
                continue

        full_text = "\n\n".join(all_text)
        full_text = clean_text(full_text)

        # Write markdown file with metadata header
        output = f"""# {title}
**Category**: {category}
**Slug**: {slug}
**Pages**: {total_pages}
**Layer**: first_order

---

{full_text}
"""
        out_path.write_text(output, encoding="utf-8")
        size_kb = out_path.stat().st_size // 1024
        print(f"  [DONE] {title} — {total_pages} pages, {size_kb} KB saved")

    except Exception as e:
        print(f"  [ERROR] {title}: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 1A: Book PDF Extraction")
    print("=" * 60)
    for pdf_path, slug, title, category in BOOKS:
        extract_book(pdf_path, slug, title, category)
    print("\nDone. Check knowledge_base/first_order/ for output files.")
```

**Run it with:**
```
python "C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts\extract_books.py"
```

**Verify it worked:** After running, you should see 41 files in `knowledge_base/first_order/` named like `dune_first_order.md`, `atlas_shrugged_first_order.md`, etc. Each file should be at minimum 50 KB. If any file is smaller than 10 KB, that PDF failed — note it and move on.

---

## Phase 1B — Podcast Extraction and Elon-Only Filtering

This is the hardest part. The 3 podcast files contain ~55-60 interviews. The transcripts are raw YouTube auto-transcripts — timestamps every few seconds, NO speaker labels. Your job is to:
1. Parse each docx file and split it into individual transcripts
2. For each transcript, use the Claude API to extract ONLY Elon's words
3. Save each filtered transcript as its own file

### Step 1: Parse the docx files into individual transcripts

Write and run `C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts\parse_podcasts.py`:

```python
"""
Phase 1B Step 1: Parse 3 docx files into individual transcript text files.
Saves to knowledge_base/podcasts/raw/{slug}.md
"""
from docx import Document
from pathlib import Path
import re

RAW_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\podcasts\raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

DOCX_FILES = [
    r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON PODCAST\Book_of_Elon_Transcripts.docx",
    r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON PODCAST\ELON transcribe.docx",
    r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON PODCAST\Musky musk.docx",
]


def make_slug(title: str) -> str:
    """Convert a title to a filename-safe slug."""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s]', '', slug)
    slug = re.sub(r'\s+', '_', slug.strip())
    return slug[:60]


def is_transcript_header(text: str) -> tuple[bool, str | None]:
    """Returns (True, title) if this line looks like a new transcript beginning."""
    # Pattern: number followed by period/space then title text
    m = re.match(r'^#?(\d{1,3})[\.\s]+(.{10,150})$', text)
    if m:
        num = int(m.group(1))
        title = m.group(2).strip()
        # Exclude timestamps disguised as numbered lines
        if num < 200 and not re.match(r'^\d+:\d+', title) and 'second' not in title.lower() and 'minute' not in title.lower():
            return True, f"#{m.group(1)} {title}"
    return False, None


def is_timestamp(text: str) -> bool:
    """True if this line is just a timestamp or time description."""
    if re.match(r'^\d+:\d+', text):
        return True
    if re.match(r'^\d+ (second|minute)', text.lower()):
        return True
    if re.match(r'^(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve) (second|minute)', text.lower()):
        return True
    return False


def parse_docx(docx_path: str) -> dict[str, str]:
    """
    Parse a docx file and return dict of {title: text_content}.
    """
    doc = Document(docx_path)
    transcripts = {}
    current_title = None
    current_lines = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        is_header, title = is_transcript_header(text)
        if is_header:
            # Save previous transcript if we have one
            if current_title and current_lines:
                transcripts[current_title] = "\n".join(current_lines)
            current_title = title
            current_lines = []
        else:
            # Skip pure timestamps — they add no value
            if current_title and not is_timestamp(text):
                current_lines.append(text)

    # Save the last transcript
    if current_title and current_lines:
        transcripts[current_title] = "\n".join(current_lines)

    return transcripts


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 1B Step 1: Parsing Podcast Docx Files")
    print("=" * 60)

    all_transcripts = {}

    for docx_path in DOCX_FILES:
        fname = Path(docx_path).name
        print(f"\nParsing: {fname}")
        transcripts = parse_docx(docx_path)
        print(f"  Found {len(transcripts)} transcripts")
        for title, text in transcripts.items():
            slug = make_slug(title)
            if slug not in all_transcripts:
                all_transcripts[slug] = (title, text)
                print(f"    {title[:70]}")

    print(f"\nTotal unique transcripts: {len(all_transcripts)}")

    # Save each transcript to its own raw file
    for slug, (title, text) in all_transcripts.items():
        out_path = RAW_DIR / f"{slug}.md"
        content = f"# {title}\n\n{text}"
        out_path.write_text(content, encoding="utf-8")

    print(f"\nSaved {len(all_transcripts)} raw transcript files to:")
    print(f"  {RAW_DIR}")
```

### Step 2: Filter each transcript to Elon-only words

This uses the Claude API. For each raw transcript file, you send it to Claude in chunks and get back only Elon's words.

Write and run `C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts\filter_podcasts.py`:

```python
"""
Phase 1B Step 2: Use Claude API to extract ONLY Elon's words from each transcript.
Reads from knowledge_base/podcasts/raw/
Writes to knowledge_base/podcasts/filtered/
Also writes to knowledge_base/first_order/ as podcast_{slug}_elon_only.md
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

CHUNK_SIZE = 6000  # characters per chunk sent to Claude (~1500 tokens)

FILTER_PROMPT = """You are processing a raw podcast/interview transcript. Your ONLY job is to extract the words spoken by Elon Musk and output them.

RULES (follow all of them without exception):
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
8. If an entire chunk seems to be ONLY the interviewer speaking (like an introduction), output: [NO ELON CONTENT IN THIS SECTION]

Here is the transcript chunk to process:

---
{chunk}
---

Output Elon's words only:"""


def filter_transcript(raw_text: str, title: str) -> str:
    """Send transcript in chunks to Claude, get back Elon-only text."""
    # Split into chunks
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
                # Small sleep between chunks to respect rate limits
                time.sleep(2)
                break
            except Exception as e:
                if "rate" in str(e).lower() or "529" in str(e) or "529" in str(e):
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

        # Skip if already filtered
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

        # Save to both locations
        output = f"# {title}\n## Elon Musk — Filtered Words Only\n**Layer**: first_order\n**Source**: podcast\n\n---\n\n{elon_text}"
        filtered_path.write_text(output, encoding="utf-8")
        first_order_path.write_text(output, encoding="utf-8")

        size_kb = filtered_path.stat().st_size // 1024
        print(f"  [DONE] {slug} — {size_kb} KB of Elon content saved")

    print("\n\nPhase 1B Complete.")
    print(f"Filtered files: {FILTERED_DIR}")
    print(f"First-order files: {FIRST_ORDER_DIR}")
```

---

## Phase 1 Completion Check

Before moving to Phase 2, verify:
```python
from pathlib import Path
first_order = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\first_order")
files = list(first_order.glob("*.md"))
print(f"Total first-order files: {len(files)}")
print(f"Books: {len([f for f in files if not f.name.startswith('podcast_')])}")
print(f"Podcasts: {len([f for f in files if f.name.startswith('podcast_')])}")
for f in sorted(files):
    size = f.stat().st_size // 1024
    print(f"  {f.name:60s} {size:>5} KB")
```

You should see ~41 book files + ~55 podcast files = ~96 total first-order files.
**Do not proceed to Phase 2 until you have at least 80 files.**

---

---

# PHASE 2 — SECOND ORDER (PER-SOURCE ELON SYNTHESIS)

## What Phase 2 Produces

One synthesis document per source. This is where you use Claude to write "how does Elon Musk think about THIS specific book or talk?"

Output goes to: `knowledge_base/second_order/`
- Books: `{slug}_elon_synthesis.md`
- Podcasts: `podcast_{slug}_synthesis.md`

The synthesis should be 7-10 pages long (approximately 2500-4000 words). Not a book summary — a deep document about how THIS source lives in Elon's mind.

## The Claude Prompt for Book Synthesis

For each book, you will call Claude with this prompt. Replace `{TITLE}`, `{CATEGORY}`, and `{CONTENT}` with the actual values:

```
SYSTEM: You are building the knowledge base for MindMusk — an AI that replicates Elon Musk's mind. Your job is to generate synthesis documents that help the AI understand how Elon thinks, not to summarize books.

USER:
You are creating a second-order knowledge document for MindMusk.

Book: "{TITLE}"
Category: {CATEGORY}

Below is extracted text from this book. Read it carefully, then write a deep synthesis titled "Elon's Synthesis: {TITLE}".

Your synthesis MUST include ALL of these sections:

## 1. WHY ELON READ THIS
One paragraph. What problem was Elon trying to solve when he picked up this book? What drew him to it? What made it stick?

## 2. THE IDEAS THAT CHANGED HIM
The 8-12 most important concepts from this book, each written as Elon would interpret them. Not what the author intended — what Elon extracted. Each concept should be 3-6 sentences. Use Elon's lens: physics, first principles, practical application, scale, civilization impact.

## 3. HOW THIS SHOWS UP IN HIS COMPANIES
Specific, concrete connections between ideas in this book and decisions/quotes/behaviors at Tesla, SpaceX, Neuralink, X, or Boring Company. Minimum 5 specific examples.

## 4. QUOTES FROM ELON THAT CONNECT HERE
5-8 things Elon has actually said in interviews or tweets that directly echo ideas from this book. Write them as: "[Quote]" — connects to [idea from book].

## 5. FIRST PRINCIPLES ELON EXTRACTED
What fundamental truths — things that are true at the physics or logic level — did Elon pull from this book? These are the building blocks that became part of his operating system. List 5-8 of them.

## 6. WHERE ELON WOULD PUSH BACK
Be honest. Where would Elon argue with the author? What would he think is wrong, naive, incomplete, or too slow? Elon doesn't accept anything uncritically.

## 7. THE ONE-LINE ELON TAKEAWAY
If Elon were to summarize what he got from this book in a single sentence, what would it be?

Write densely. No fluff. No "This book explores..." sentences. Treat the reader as highly intelligent. Write as if you ARE building Elon's mind.

--- BOOK CONTENT BELOW ---

{CONTENT}
```

## The Claude Prompt for Podcast Synthesis

For each podcast/interview, use this prompt:

```
SYSTEM: You are building the knowledge base for MindMusk — an AI that replicates Elon Musk's mind. This document captures what Elon actually said, believed, and revealed about himself in a specific interview.

USER:
You are creating a second-order knowledge document for MindMusk.

Interview/Talk: "{TITLE}"

Below is the filtered transcript — ONLY Elon's words from this interview, with the interviewer's questions removed. Read it carefully and write a synthesis titled "Elon's Voice: {TITLE}".

Your synthesis MUST include ALL of these sections:

## 1. CONTEXT AND SETTING
When was this? Who was the interviewer? What was Elon's headspace at the time? What was happening at his companies that week/month/year?

## 2. THE POSITIONS ELON TOOK
The 8-12 most important things Elon stated, argued, or believed in this interview. For each: state his position clearly, note how confident he was, note if he showed any uncertainty.

## 3. DIRECT QUOTES (THE BEST ONES)
The 10-15 most powerful, revealing, or characteristic things Elon said in this interview. Keep them verbatim. These are the gold — exact words that show how his mind works.

## 4. HOW HE REASONED
What was his thinking process in this interview? Did he use analogies? Physics? Historical examples? Numbers? What rhetorical moves did he make? How did he handle pushback?

## 5. WHAT THIS REVEALS ABOUT HOW HE THINKS
Looking at this interview as a window into his mind: what does it reveal about his values, fears, ambitions, or mental models that isn't obvious from his public persona?

## 6. CONNECTIONS TO HIS COMPANIES AND DECISIONS
What decisions, product choices, or public statements from Tesla/SpaceX/Neuralink/X connect to what he said here?

## 7. THE MOST ELON MOMENT
One specific exchange or monologue from this interview that is the most characteristic of how Elon Musk operates. Describe it and explain why it's so representative.

Write densely. Verbatim quotes where possible. This document will be retrieved by an AI trying to replicate how Elon thinks.

--- ELON'S WORDS BELOW ---

{CONTENT}
```

## The Python Script to Run Phase 2

Large books won't fit in a single Claude call (context limit). For files larger than 80,000 characters, you need to break the book into sections and do a **map-reduce**: synthesize each section, then combine the section syntheses into the final document.

Write and run `C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts\generate_second_order.py`:

```python
"""
Phase 2: Generate second-order Elon synthesis for each source.
Reads from knowledge_base/first_order/
Writes to knowledge_base/second_order/
"""
import anthropic
import os
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

FIRST_ORDER_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\first_order")
SECOND_ORDER_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\second_order")
SECOND_ORDER_DIR.mkdir(parents=True, exist_ok=True)

MAX_CHARS_PER_CALL = 80000  # ~20,000 tokens — safe limit for single call
SECTION_SIZE = 20000        # chunk size for map phase on large books

BOOK_SYNTHESIS_PROMPT = """You are building the knowledge base for MindMusk — an AI that replicates Elon Musk's mind. Your job is to generate synthesis documents that help the AI understand how Elon thinks, not to summarize books.

Book: "{title}"
Category: {category}

Below is extracted text from this book. Read it carefully, then write a deep synthesis titled "Elon's Synthesis: {title}".

Your synthesis MUST include ALL of these sections:

## 1. WHY ELON READ THIS
One paragraph. What problem was Elon trying to solve when he picked up this book? What drew him to it? What made it stick?

## 2. THE IDEAS THAT CHANGED HIM
The 8-12 most important concepts from this book, each written as Elon would interpret them. Not what the author intended — what Elon extracted. Each concept should be 3-6 sentences. Use Elon's lens: physics, first principles, practical application, scale, civilization impact.

## 3. HOW THIS SHOWS UP IN HIS COMPANIES
Specific, concrete connections between ideas in this book and decisions/quotes/behaviors at Tesla, SpaceX, Neuralink, X, or Boring Company. Minimum 5 specific examples.

## 4. QUOTES FROM ELON THAT CONNECT HERE
5-8 things Elon has actually said in interviews or tweets that directly echo ideas from this book.

## 5. FIRST PRINCIPLES ELON EXTRACTED
What fundamental truths did Elon pull from this book? List 5-8 of them.

## 6. WHERE ELON WOULD PUSH BACK
Where would Elon argue with the author? What would he think is wrong, naive, or too slow?

## 7. THE ONE-LINE ELON TAKEAWAY
If Elon summarized what he got from this book in one sentence, what would it be?

Write densely. No fluff. Treat the reader as highly intelligent.

--- BOOK CONTENT BELOW ---

{content}"""

PODCAST_SYNTHESIS_PROMPT = """You are building the knowledge base for MindMusk — an AI that replicates Elon Musk's mind.

Interview/Talk: "{title}"

Below is the filtered transcript — ONLY Elon's words. Write a synthesis titled "Elon's Voice: {title}".

## 1. CONTEXT AND SETTING
When was this? Who was the interviewer? What was happening at his companies at that time?

## 2. THE POSITIONS ELON TOOK
The 8-12 most important things Elon stated or argued. For each: his position, his confidence level, any uncertainty.

## 3. DIRECT QUOTES (THE BEST ONES)
The 10-15 most powerful, revealing things Elon said. Keep them verbatim.

## 4. HOW HE REASONED
His thinking process: analogies, physics, historical examples, numbers, how he handled pushback.

## 5. WHAT THIS REVEALS ABOUT HOW HE THINKS
What does this interview reveal about his values, fears, ambitions, or mental models?

## 6. CONNECTIONS TO HIS COMPANIES AND DECISIONS
What connects to actual decisions at Tesla/SpaceX/Neuralink/X?

## 7. THE MOST ELON MOMENT
One specific exchange that is most characteristic of how Elon operates. Describe it and say why.

Write densely. Verbatim quotes where possible.

--- ELON'S WORDS BELOW ---

{content}"""

MAP_PROMPT = """You are processing a SECTION of the book "{title}" for Elon Musk's knowledge base.

Extract the KEY IDEAS from this section — the passages, arguments, and concepts that would most interest Elon Musk. Focus on:
- Physics and engineering principles
- Civilization-scale thinking
- Counter-intuitive insights
- Analogies that explain complex systems
- Historical lessons applicable today
- Ideas about technology, risk, and the future

Output a compressed but content-rich extraction (not a summary — preserve key ideas verbatim where possible):

--- SECTION CONTENT ---
{content}"""

REDUCE_PROMPT = """You are building the knowledge base for MindMusk — an AI that replicates Elon Musk's mind.

Below are extracted key ideas from all sections of the book "{title}" (Category: {category}).

Now write the complete second-order synthesis. Include ALL of these sections:

## 1. WHY ELON READ THIS
## 2. THE IDEAS THAT CHANGED HIM (8-12 ideas, 3-6 sentences each)
## 3. HOW THIS SHOWS UP IN HIS COMPANIES (5+ specific examples)
## 4. QUOTES FROM ELON THAT CONNECT HERE (5-8 quotes)
## 5. FIRST PRINCIPLES ELON EXTRACTED (5-8 principles)
## 6. WHERE ELON WOULD PUSH BACK
## 7. THE ONE-LINE ELON TAKEAWAY

Write densely. No fluff.

--- EXTRACTED KEY IDEAS ---
{content}"""


def call_claude(prompt: str, max_tokens: int = 6000) -> str:
    """Call Claude with retry logic."""
    for attempt in range(5):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            time.sleep(2)  # Be kind to the API
            return response.content[0].text.strip()
        except Exception as e:
            if "rate" in str(e).lower() or "529" in str(e) or "overload" in str(e).lower():
                wait = 30 * (attempt + 1)
                print(f"      Rate limit/overload, waiting {wait}s...")
                time.sleep(wait)
            else:
                if attempt == 4:
                    raise
                print(f"      Error: {e}, retrying in 10s...")
                time.sleep(10)
    return ""


def generate_synthesis(source_path: Path) -> None:
    slug = source_path.stem.replace("_first_order", "").replace("_elon_only", "")
    is_podcast = source_path.name.startswith("podcast_")

    if is_podcast:
        out_name = f"podcast_{slug}_synthesis.md"
    else:
        out_name = f"{slug}_elon_synthesis.md"

    out_path = SECOND_ORDER_DIR / out_name

    # Skip if already done
    if out_path.exists() and out_path.stat().st_size > 3000:
        print(f"  [SKIP] {slug} — already synthesized")
        return

    print(f"  [SYNTHESIZING] {slug}...")
    content = source_path.read_text(encoding="utf-8")

    # Extract title from first line
    lines = content.split('\n')
    title = lines[0].replace('# ', '').strip()
    category = ""
    for line in lines[:10]:
        if line.startswith("**Category**"):
            category = line.split(":", 1)[1].strip().strip("*")

    if len(content) <= MAX_CHARS_PER_CALL:
        # Small enough for single call
        if is_podcast:
            prompt = PODCAST_SYNTHESIS_PROMPT.format(title=title, content=content)
        else:
            prompt = BOOK_SYNTHESIS_PROMPT.format(title=title, category=category, content=content)

        synthesis = call_claude(prompt, max_tokens=6000)
    else:
        # Too large — use map-reduce
        print(f"    Large source ({len(content)//1024} KB) — using map-reduce...")
        # MAP: Extract key ideas from each section
        sections = []
        for i in range(0, len(content), SECTION_SIZE):
            section = content[i:i + SECTION_SIZE]
            sections.append(section)

        print(f"    Mapping {len(sections)} sections...")
        extractions = []
        for j, section in enumerate(sections):
            print(f"      Section {j+1}/{len(sections)}...", end=" ", flush=True)
            extraction = call_claude(MAP_PROMPT.format(title=title, content=section), max_tokens=2000)
            extractions.append(extraction)
            print("OK")

        # REDUCE: Combine extractions into final synthesis
        print(f"    Reducing to final synthesis...")
        combined = "\n\n---\n\n".join(extractions)
        # Trim if combined is still too large
        if len(combined) > MAX_CHARS_PER_CALL:
            combined = combined[:MAX_CHARS_PER_CALL]

        synthesis = call_claude(
            REDUCE_PROMPT.format(title=title, category=category, content=combined),
            max_tokens=6000
        )

    if not synthesis:
        print(f"  [ERROR] Failed to generate synthesis for {slug}")
        return

    output = f"# Elon's Synthesis: {title}\n**Slug**: {slug}\n**Layer**: second_order\n\n---\n\n{synthesis}"
    out_path.write_text(output, encoding="utf-8")
    size_kb = out_path.stat().st_size // 1024
    print(f"  [DONE] {slug} — {size_kb} KB synthesis saved")


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 2: Generating Second-Order Elon Syntheses")
    print("=" * 60)

    first_order_files = sorted(FIRST_ORDER_DIR.glob("*.md"))
    print(f"Found {len(first_order_files)} first-order files\n")

    for source_file in first_order_files:
        generate_synthesis(source_file)

    print("\n\nPhase 2 Complete.")
    second_order_files = list(SECOND_ORDER_DIR.glob("*.md"))
    print(f"Total second-order files: {len(second_order_files)}")
```

**Run it with:**
```
python "C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts\generate_second_order.py"
```

This will take several hours. It's fine to let it run overnight. It will skip already-completed files if interrupted, so you can restart it safely.

---

## Phase 2 Completion Check

```python
from pathlib import Path
second = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\second_order")
files = list(second.glob("*.md"))
print(f"Total second-order files: {len(files)}")
for f in sorted(files):
    size = f.stat().st_size // 1024
    print(f"  {f.name:65s} {size:>5} KB")
```

You should have ~96 files (41 books + ~55 podcasts). Every file should be at least 5 KB.
**Do not proceed to Phase 3 until you have at least 85 second-order files.**

---

---

# PHASE 3 — THIRD ORDER (15 THEMATIC SYNTHESES)

## What Phase 3 Produces

15 documents, one per theme, each drawing from ALL relevant second-order sources. These are cross-source: they pull ideas from multiple books AND podcasts to show how Elon's thinking on a theme holds together across his whole life.

Output: `knowledge_base/third_order/third_order_{theme_slug}.md`

## The 15 Themes

| # | Theme Name | Slug | Primary Sources |
|---|---|---|---|
| 1 | First Principles and Physics-Based Reasoning | `first_principles` | All books, all podcasts |
| 2 | Multi-Planetary Life and Space Civilization | `multiplanetary` | Dune, Fermi Paradox, SpaceX podcasts, Ignition |
| 3 | Artificial Intelligence and Existential Risk | `ai_risk` | All 5 AI books, Lex Fridman, YC podcasts |
| 4 | Energy, Climate, and Sustainable Civilization | `energy_climate` | Sciences books, Tesla podcasts, TED talks |
| 5 | Manufacturing, Engineering, and Physical Reality | `manufacturing_engineering` | Ignition, Structures, Starship podcasts, Tim Dodd |
| 6 | Company Building and Scaling | `company_building` | Zero to One, Masters of Doom, Steve Jobs, Stanford lectures |
| 7 | Leadership, Teams, and Organizational Design | `leadership_teams` | Steve Jobs, Benjamin Franklin, business podcasts |
| 8 | Motivation, Meaning, and Existential Purpose | `motivation_meaning` | Man's Search for Meaning, Hitchhiker's Guide, commencement speeches |
| 9 | Learning, Mental Models, and How to Think | `learning_mental_models` | All books (Elon as a reader), Foundation Interview, Kevin Rose |
| 10 | History, Civilization Cycles, and Lessons | `history_civilization` | All History books, Lessons of History, Art of War |
| 11 | Fiction and the Books That Shaped Elon's Vision | `fiction_vision` | All Fiction books — Dune, Atlas Shrugged, Moon is a Harsh Mistress, etc. |
| 12 | Risk, Failure, Resilience, and Recovery | `risk_failure` | SpaceX stories, Steve Jobs, Masters of Doom, Starship podcasts |
| 13 | Science, Curiosity, and the Nature of Reality | `science_curiosity` | Selfish Gene, Skeptics Guide, Fermi Paradox, What We Owe the Future |
| 14 | Economics, Wealth, and Capital Allocation | `economics_wealth` | Wealth of Nations, Zero to One, Screw Business as Usual |
| 15 | Truth, Communication, and Fighting Narrative Capture | `truth_communication` | Lying, Parasitic Mind, What's Our Problem, Twitter/X podcasts |

## The Claude Prompt for Third Order

For each theme, you will call Claude with all relevant second-order files as context. Here is the exact prompt template:

```
SYSTEM: You are building the deepest layer of MindMusk's knowledge base. You are synthesizing across multiple sources to reveal how Elon's mind works on a specific theme.

USER:
You are writing a third-order thematic synthesis for MindMusk.

Theme: "{THEME_NAME}"

Below are the second-order synthesis documents for all sources relevant to this theme. These documents already reflect Elon's lens. Your job is to synthesize ACROSS all of them to reveal how this theme runs through Elon's entire thinking — from his reading, to his talking, to his building.

Write a document titled "Elon's Mind on {THEME_NAME}". It must include ALL of these sections:

## 1. THE CORE BELIEF
What does Elon fundamentally believe about this theme? State it in 2-3 paragraphs with no hedging. This is his actual position, derived from everything he has read and said.

## 2. THE INTELLECTUAL LINEAGE
Which books, ideas, and thinkers most shaped Elon's view on this theme? Show the chain: "He read X, which gave him Y, which then showed up in Z decision." Make the connections explicit.

## 3. THE MENTAL FRAMEWORK
What is Elon's actual operating framework for thinking about this theme? When he faces a decision related to this theme, what questions does he ask? What does he optimize for? What does he refuse to trade off?

## 4. HOW IT SHOWS UP IN HIS COMPANIES
At least 8 specific, concrete examples of this theme manifesting in Tesla, SpaceX, Neuralink, X, or Boring Company. Not vague — specific products, decisions, quotes, public statements.

## 5. WHAT ELON HAS SAID (DIRECT QUOTES)
The 10-15 most powerful things Elon has said about this theme across all interviews. Verbatim where possible.

## 6. WHERE HE IS CONTRARIAN
How does Elon's view on this theme differ from the mainstream, conventional, or consensus view? Where do most smart people get it wrong, in his opinion?

## 7. THE SOCRATIC QUESTIONS HE WOULD ASK
If someone came to Elon with a problem in this domain, what are the 5-7 questions he would ask them? These should be the questions that reveal whether someone really understands the first principles.

## 8. THE SYNTHESIS INSIGHT
What insight about this theme only becomes visible when you look at ALL the sources together? Something that you couldn't see from any single book or interview alone.

Write at maximum density. This document will be retrieved by an AI trying to respond as Elon. Every sentence should be signal.

--- RELEVANT SECOND-ORDER DOCUMENTS BELOW ---

{CONTENT}
```

## The Python Script for Phase 3

Write and run `C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts\generate_third_order.py`:

```python
"""
Phase 3: Generate 15 third-order thematic synthesis documents.
Reads from knowledge_base/second_order/
Writes to knowledge_base/third_order/
"""
import anthropic
import os
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SECOND_ORDER_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\second_order")
THIRD_ORDER_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\third_order")
THIRD_ORDER_DIR.mkdir(parents=True, exist_ok=True)

MAX_CONTEXT = 90000  # characters — trim combined sources to this

THEMES = [
    {
        "name": "First Principles and Physics-Based Reasoning",
        "slug": "first_principles",
        "source_keywords": ["superintelligence", "life_3_0", "human_compatible", "our_final_invention",
                            "deep_learning", "structures", "ignition", "selfish_gene", "skeptics_guide",
                            "fermi_paradox", "lex_fridman", "stanford", "foundation", "yc", "ted"],
    },
    {
        "name": "Multi-Planetary Life and Space Civilization",
        "slug": "multiplanetary",
        "source_keywords": ["dune", "fermi_paradox", "ignition", "moon_harsh_mistress", "hitchhikers",
                            "starship", "spacex", "mars", "tim_dodd", "satellite", "boiler_room",
                            "mars_society", "issrdc", "everyday_astronaut"],
    },
    {
        "name": "Artificial Intelligence and Existential Risk",
        "slug": "ai_risk",
        "source_keywords": ["life_3_0", "superintelligence", "human_compatible", "our_final_invention",
                            "deep_learning", "what_we_owe_future", "lex_fridman", "yc", "stanford",
                            "neuralink", "ted", "dealbook", "grok", "xai"],
    },
    {
        "name": "Energy, Climate, and Sustainable Civilization",
        "slug": "energy_climate",
        "source_keywords": ["selfish_gene", "what_we_owe_future", "wealth_of_nations", "screw_business",
                            "ted", "cop21", "solar", "battery", "tesla", "powerwall", "rainn_wilson",
                            "sal_khan", "master_plan"],
    },
    {
        "name": "Manufacturing, Engineering, and Physical Reality",
        "slug": "manufacturing_engineering",
        "source_keywords": ["ignition", "structures", "tim_dodd", "starship", "tesla_factory",
                            "investor_day", "mkbhd", "ai_day", "raptor", "megacast"],
    },
    {
        "name": "Company Building and Scaling",
        "slug": "company_building",
        "source_keywords": ["zero_to_one", "masters_of_doom", "steve_jobs", "screw_business",
                            "stanford", "yc", "motley_fool", "sxsw", "auto_bild", "2003", "paypay",
                            "paypal", "entrepreneur"],
    },
    {
        "name": "Leadership, Teams, and Organizational Design",
        "slug": "leadership_teams",
        "source_keywords": ["steve_jobs", "benjamin_franklin", "masters_of_doom", "on_war", "art_of_war",
                            "investor_day", "pando", "chm", "time_person"],
    },
    {
        "name": "Motivation, Meaning, and Existential Purpose",
        "slug": "motivation_meaning",
        "source_keywords": ["mans_search_meaning", "hitchhikers_guide", "waiting_for_godot",
                            "fault_in_our_stars", "caltech", "usc", "commencement", "rainn",
                            "fox_news", "young_people"],
    },
    {
        "name": "Learning, Mental Models, and How to Think",
        "slug": "learning_mental_models",
        "source_keywords": ["foundation", "kevin_rose", "sxsw", "charlie_rose", "baron", "ted",
                            "skeptics_guide", "lessons_of_history", "selfish_gene", "stanford"],
    },
    {
        "name": "History, Civilization Cycles, and Lessons",
        "slug": "history_civilization",
        "source_keywords": ["lessons_of_history", "iliad", "decline_fall_rome", "storm_of_steel",
                            "on_war", "wages_of_destruction", "fifteen_battles", "art_of_war",
                            "benjamin_franklin", "explore_create", "dan_carlin"],
    },
    {
        "name": "Fiction and the Books That Shaped Elon's Vision",
        "slug": "fiction_vision",
        "source_keywords": ["dune", "hitchhikers_guide", "lord_of_the_rings", "atlas_shrugged",
                            "moon_harsh_mistress", "stranger_strange_land", "machine_stops",
                            "game_of_thrones", "waiting_for_godot", "fault_in_our_stars"],
    },
    {
        "name": "Risk, Failure, Resilience, and Recovery",
        "slug": "risk_failure",
        "source_keywords": ["masters_of_doom", "steve_jobs", "mans_search_meaning", "storm_of_steel",
                            "starship", "spacex", "paypal", "3_flight_failures", "2008", "third_row",
                            "director", "tim_dodd"],
    },
    {
        "name": "Science, Curiosity, and the Nature of Reality",
        "slug": "science_curiosity",
        "source_keywords": ["selfish_gene", "skeptics_guide", "fermi_paradox", "what_we_owe_future",
                            "life_3_0", "deep_learning", "aliens", "smithsonian", "lex_fridman"],
    },
    {
        "name": "Economics, Wealth, and Capital Allocation",
        "slug": "economics_wealth",
        "source_keywords": ["wealth_of_nations", "zero_to_one", "screw_business", "whats_our_problem",
                            "masters_of_doom", "baron", "motley_fool", "robin_li", "bill_gates"],
    },
    {
        "name": "Truth, Communication, and Fighting Narrative Capture",
        "slug": "truth_communication",
        "source_keywords": ["lying", "parasitic_mind", "whats_our_problem", "woman_makes_plan",
                            "dealbook", "bill_maher", "time_person", "twitter", "x_algorithm",
                            "free_speech", "adl"],
    },
]

THIRD_ORDER_PROMPT = """You are building the deepest layer of MindMusk's knowledge base. You are synthesizing across multiple sources to reveal how Elon's mind works on a specific theme.

Theme: "{theme_name}"

Below are the second-order synthesis documents for all sources relevant to this theme. These documents already reflect Elon's lens. Your job is to synthesize ACROSS all of them to reveal how this theme runs through Elon's entire thinking.

Write a document titled "Elon's Mind on {theme_name}". Include ALL of these sections:

## 1. THE CORE BELIEF
What does Elon fundamentally believe about this theme? 2-3 paragraphs, no hedging. His actual position.

## 2. THE INTELLECTUAL LINEAGE
Which books, ideas, and thinkers shaped his view? Show the chain: "He read X, which gave him Y, which showed up in Z decision."

## 3. THE MENTAL FRAMEWORK
What is his operating framework for this theme? When he faces decisions here, what does he ask? What does he optimize for? What won't he trade off?

## 4. HOW IT SHOWS UP IN HIS COMPANIES
At least 8 specific examples — products, decisions, quotes, public statements from Tesla, SpaceX, Neuralink, X.

## 5. WHAT ELON HAS SAID (DIRECT QUOTES)
10-15 most powerful things Elon has said about this theme. Verbatim.

## 6. WHERE HE IS CONTRARIAN
How does his view differ from conventional wisdom? Where do most people get it wrong?

## 7. THE SOCRATIC QUESTIONS HE WOULD ASK
5-7 questions Elon would ask someone who came to him with a problem in this domain.

## 8. THE SYNTHESIS INSIGHT
What insight only becomes visible when you look at ALL sources together?

Write at maximum density. Every sentence should be signal.

--- RELEVANT SECOND-ORDER DOCUMENTS ---

{content}"""


def get_relevant_sources(theme: dict) -> str:
    """Load and combine second-order files relevant to this theme."""
    all_files = list(SECOND_ORDER_DIR.glob("*.md"))
    keywords = [kw.lower() for kw in theme["source_keywords"]]

    matched = []
    for f in all_files:
        fname_lower = f.stem.lower()
        if any(kw in fname_lower for kw in keywords):
            matched.append(f)

    print(f"    Matched {len(matched)} sources for theme '{theme['name']}'")

    # Load and combine, trimming to MAX_CONTEXT
    combined = []
    total_chars = 0
    for f in matched:
        content = f.read_text(encoding="utf-8")
        header = f"\n\n{'='*60}\nSOURCE: {f.stem}\n{'='*60}\n\n"
        addition = header + content[:8000]  # Cap each source at 8000 chars
        if total_chars + len(addition) < MAX_CONTEXT:
            combined.append(addition)
            total_chars += len(addition)
        else:
            # Add abbreviated version
            combined.append(header + content[:3000] + "\n[...truncated for context limit...]")

    return "\n".join(combined)


def call_claude(prompt: str) -> str:
    for attempt in range(5):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=8000,
                messages=[{"role": "user", "content": prompt}]
            )
            time.sleep(3)
            return response.content[0].text.strip()
        except Exception as e:
            if "rate" in str(e).lower() or "overload" in str(e).lower():
                wait = 45 * (attempt + 1)
                print(f"      Waiting {wait}s (rate/overload)...")
                time.sleep(wait)
            else:
                if attempt == 4:
                    raise
                time.sleep(10)
    return ""


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 3: Generating 15 Third-Order Thematic Syntheses")
    print("=" * 60)

    for i, theme in enumerate(THEMES):
        out_path = THIRD_ORDER_DIR / f"third_order_{theme['slug']}.md"

        if out_path.exists() and out_path.stat().st_size > 5000:
            print(f"[{i+1}/15] [SKIP] {theme['name']} — already done")
            continue

        print(f"\n[{i+1}/15] Generating: {theme['name']}")
        sources_content = get_relevant_sources(theme)
        prompt = THIRD_ORDER_PROMPT.format(
            theme_name=theme["name"],
            content=sources_content
        )
        synthesis = call_claude(prompt)

        if not synthesis:
            print(f"  [ERROR] Failed for {theme['name']}")
            continue

        output = f"# Elon's Mind on {theme['name']}\n**Slug**: {theme['slug']}\n**Layer**: third_order\n\n---\n\n{synthesis}"
        out_path.write_text(output, encoding="utf-8")
        size_kb = out_path.stat().st_size // 1024
        print(f"  [DONE] {theme['name']} — {size_kb} KB")

    print("\n\nPhase 3 Complete.")
```

---

## Phase 3 Completion Check

You should have exactly 15 files in `knowledge_base/third_order/`. Every file should be 10-30 KB.
**Do not proceed to Phase 4 until all 15 exist.**

---

---

# PHASE 4 — FOURTH ORDER (MASTER MENTAL MODELS)

## What Phase 4 Produces

5 documents. These are the most important files in the entire knowledge base. They capture Elon's deepest worldview — things that only become visible when you look at EVERYTHING together: all 41 books, all 55+ podcasts, all 15 themes.

Output: `knowledge_base/fourth_order/fourth_order_{slug}.md`

## The 5 Master Mental Models

### Document 1: The Elon Musk Decision Framework
**Slug**: `decision_framework`
This document answers: when Elon faces ANY decision — what process does he use? What questions does he ask? What does he refuse to trade off? How does he handle uncertainty? How does he evaluate risk? This is his universal operating procedure extracted from everything he has ever said and done.

### Document 2: Elon's Theory of Civilization
**Slug**: `theory_of_civilization`
This document answers: what does Elon actually believe about humanity? About history? About where we are headed? About what matters and what doesn't? About the biggest threats and opportunities facing human civilization? This is his big-picture worldview.

### Document 3: Elon's Operator Manual for Companies
**Slug**: `operator_manual`
This document answers: how does Elon actually build and run companies? Not the press-release version — the real philosophy. How does he hire? Fire? Set goals? Handle failure? Deal with bureaucracy? Make product decisions? Motivate people? Structure organizations? This is extracted from all the company-building and leadership content.

### Document 4: How Elon Learns and Processes Information
**Slug**: `how_elon_learns`
This document answers: how does Elon learn? How does he read? How does he think? How does he model reality? How does he update his beliefs? How does he reason from first principles? How does he use analogies? What is his epistemic process? This is his meta-cognition — the operating system behind the operating system.

### Document 5: What Elon Actually Believes (The Candid Version)
**Slug**: `what_elon_believes`
This document answers: what does Elon say in unguarded moments that reveals his real beliefs — not the polished public statements? What does he say when pressed on alien life, simulation theory, consciousness, God, death, fear, regret, love? This draws from his most candid interviews (Joe Rogan, Lex Fridman late-night conversations, Third Row Tesla) to reveal the private Elon.

## The Prompt Template for Fourth Order

```
SYSTEM: You are writing the most important documents in the MindMusk knowledge base. These documents will be used by an AI to genuinely replicate how Elon Musk thinks at the deepest level. Everything you write here becomes part of the AI's core understanding of Elon's mind.

USER:
You are writing a fourth-order Master Mental Model document for MindMusk.

Document: "{DOCUMENT_NAME}"

You have access to all 15 thematic synthesis documents from the third-order layer, which themselves synthesized all 41 books and 55+ podcast transcripts. You are now synthesizing across ALL themes.

{SPECIFIC_INSTRUCTIONS}

Write at absolute maximum density and depth. This document should be 3000-5000 words. It should reveal things about Elon's mind that are only visible when you look at everything simultaneously. Zero fluff. Zero hedging. Pure signal.

--- ALL THIRD-ORDER THEME DOCUMENTS BELOW ---

{CONTENT}
```

## Python Script for Phase 4

Write and run `C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts\generate_fourth_order.py`:

```python
"""
Phase 4: Generate 5 fourth-order Master Mental Model documents.
Reads from knowledge_base/third_order/ (all 15 theme files)
Writes to knowledge_base/fourth_order/
"""
import anthropic
import os
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

THIRD_ORDER_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\third_order")
FOURTH_ORDER_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\fourth_order")
FOURTH_ORDER_DIR.mkdir(parents=True, exist_ok=True)

MASTER_MODELS = [
    {
        "name": "The Elon Musk Decision Framework",
        "slug": "decision_framework",
        "instructions": """Write a comprehensive document that reveals Elon's universal decision-making process.

Structure it as:

## 1. THE ENTRY POINT: HOW HE FRAMES ANY PROBLEM
What is the first question he asks? How does he strip away assumptions? What does "first principles" actually mean in practice, not just as a buzzword?

## 2. THE FILTERS HE RUNS EVERY DECISION THROUGH
List and explain each filter. Does it advance humanity's multi-planetary future? Does it pass the physics test? Is the cost of being wrong recoverable? Is he the right person to do this?

## 3. HOW HE HANDLES UNCERTAINTY
When he doesn't have enough information, what does he do? How does he model probability? How does he think about known unknowns vs unknown unknowns?

## 4. HOW HE EVALUATES RISK
His risk calculus is not normal. Explain his actual approach: what risks does he take that others won't? What risks does he refuse that others accept? Why?

## 5. HOW HE MAKES SPEED/QUALITY TRADEOFFS
When does he move fast and break things? When does he demand perfection? What determines the tradeoff?

## 6. HOW HE HANDLES BEING WRONG
What does Elon do when he realizes he made a wrong decision? How does he course correct? What does he NOT do?

## 7. THE QUESTIONS HE ASKS THAT MOST PEOPLE NEVER ASK
The specific questions that Elon asks in any situation that reveal his decision framework — questions most people never think to ask.

## 8. WHAT HE WILL NEVER COMPROMISE ON
The absolute hard limits — things he will never trade off regardless of the situation."""
    },
    {
        "name": "Elon's Theory of Civilization",
        "slug": "theory_of_civilization",
        "instructions": """Write a comprehensive document that reveals Elon's complete worldview on human civilization.

Structure it as:

## 1. WHERE WE ARE IN THE ARC OF HISTORY
What does Elon believe about where humanity stands right now in the long arc of history? What moment is this?

## 2. THE EXISTENTIAL THREATS HE ACTUALLY WORRIES ABOUT
Not the ones he mentions in polite interviews — the ones that genuinely keep him up at night. Rank them. Explain why he ranks them that way.

## 3. HIS MODEL OF HOW CIVILIZATIONS RISE AND FALL
What patterns does he see from his reading of history? What makes civilizations collapse? What makes them thrive?

## 4. WHAT MAKES THIS MOMENT UNIQUE
Why does Elon believe we are at an inflection point? What makes the next 20-50 years different from any prior period?

## 5. HIS VISION FOR WHAT GOOD LOOKS LIKE
Not just "Mars" — what does Elon's actual vision of a good future look like in detail? What kind of civilization is he trying to build?

## 6. WHO HE THINKS THE HEROES AND VILLAINS ARE
What types of actors does Elon see as moving civilization forward? What types does he see as holding it back?

## 7. WHY HE DOES WHAT HE DOES
The deepest motivation. Not the PR answer. What does Elon actually believe about why his work matters at the civilizational level?

## 8. WHAT HE FEARS MOST
His genuine fears about the future — not the optimism he projects publicly."""
    },
    {
        "name": "Elon's Operator Manual for Companies",
        "slug": "operator_manual",
        "instructions": """Write a comprehensive document that reveals how Elon actually builds and runs companies.

Structure it as:

## 1. HOW HE EVALUATES WHETHER A COMPANY IS WORTH STARTING
The exact criteria. What has to be true for him to think a company is worth building?

## 2. HOW HE HIRES (AND WHO HE HIRES)
What does he actually look for? What questions does he ask? What disqualifies someone? What are the signals of exceptional talent he looks for?

## 3. HOW HE SETS GOALS AND DEMANDS
How does he set targets? Why does he set goals that seem impossible? How does he use deadlines as tools? What happens when targets are missed?

## 4. HOW HE HANDLES BUREAUCRACY AND RULES
His actual philosophy on rules, processes, and bureaucracy. When does he delete rules? How does he prevent organizational calcification?

## 5. HOW HE MANAGES ENGINEERS AND MAKERS
His specific approach to technical talent. How does he interact with engineers differently from managers? What does he think managers are actually for?

## 6. HOW HE HANDLES FAILURE AND BAD NEWS
How does he react when things go wrong? What does he expect from people who bring bad news? What does he do with the information?

## 7. HOW HE THINKS ABOUT PRODUCTS
His product philosophy. What makes a good product? How does he evaluate design? What does he refuse to ship?

## 8. HOW HE MAINTAINS INTENSITY ACROSS MULTIPLE COMPANIES
How does he actually operate across Tesla, SpaceX, Neuralink, X, Boring simultaneously? What is his time management philosophy? What gets his personal attention?"""
    },
    {
        "name": "How Elon Learns and Processes Information",
        "slug": "how_elon_learns",
        "instructions": """Write a comprehensive document that reveals how Elon's mind actually processes information and learns.

Structure it as:

## 1. HOW HE READS BOOKS
He doesn't read like most people. What is his actual approach to books? What does he take from them? How does he remember them? How do books become mental models rather than just information?

## 2. HOW HE BUILDS MENTAL MODELS
What is his process for building a model of how something works? How does he go from zero knowledge to deep understanding in a new domain?

## 3. HOW HE USES ANALOGIES
Elon is famous for his analogies. How does he construct them? What makes a good analogy in his view? How does he use analogies as thinking tools (not just communication tools)?

## 4. HOW HE APPLIES PHYSICS THINKING OUTSIDE OF PHYSICS
The "physics approach" — how does he actually apply it to business, management, human behavior, politics? What does it mean in non-technical domains?

## 5. HOW HE UPDATES HIS BELIEFS
What does it take to change Elon's mind? What kind of evidence counts? How does he handle cognitive dissonance? How does he approach topics where he might be wrong?

## 6. HOW HE HANDLES DOMAINS WHERE HE IS IGNORANT
When he enters a new field, what is his process? How long does it take him to get to competence? What shortcuts does he use?

## 7. HOW HE SYNTHESIZES ACROSS DISCIPLINES
Elon is famous for pulling ideas from wildly different fields. How does he actually do this? What is the process for cross-domain insight?

## 8. THE QUESTIONS HE ASKS TO LEARN FASTER
The specific types of questions he asks experts and novices alike to accelerate his learning."""
    },
    {
        "name": "What Elon Actually Believes — The Candid Version",
        "slug": "what_elon_believes",
        "instructions": """Write a comprehensive document that captures Elon's private beliefs — what he says in unguarded moments that reveals the real person behind the public persona.

Structure it as:

## 1. WHAT HE SAYS ABOUT CONSCIOUSNESS AND THE NATURE OF REALITY
His real views on simulation theory, consciousness, what makes something "alive," his relationship to physics vs. philosophy.

## 2. WHAT HE SAYS ABOUT GOD, RELIGION, AND MEANING
Not the diplomatic answers — his actual views on whether the universe has meaning, whether there is anything beyond physics, what he finds sacred.

## 3. WHAT HE SAYS ABOUT DEATH AND LEGACY
His real relationship with mortality. What does he think happens after death? What drives him — fear of death, love of the mission, or something else?

## 4. WHAT HE SAYS ABOUT HUMAN NATURE
Does he trust people? What does he think motivates most humans? Where does he think humans are weak? Strong? What does he think is fundamental to being human?

## 5. WHAT HE SAYS ABOUT HIS OWN PSYCHOLOGY
His self-reported inner experience. What does he say about how he feels? About loneliness? About relationships? About what he finds hard?

## 6. WHAT HE SAYS ABOUT HIS DARKEST MOMENTS
The times he has spoken about being on the edge — financially, emotionally, existentially. What he was thinking. What kept him going.

## 7. WHAT HE BELIEVES MOST PEOPLE GET WRONG ABOUT HIM
The misconceptions that actually bother him. The version of Elon that exists in public discourse that he knows is wrong.

## 8. THE CORE BELIEFS HE HAS NEVER WAVERED ON
Despite all the public controversy and changing positions on tactics — what are the things Elon has believed consistently his entire adult life?"""
    },
]

BASE_PROMPT = """You are writing the most important documents in the MindMusk knowledge base. These will be used by an AI to replicate how Elon Musk thinks at the deepest level.

Document: "{name}"

You have access to all 15 thematic synthesis documents. You are synthesizing across ALL themes.

{instructions}

Write 3000-5000 words. Maximum density and depth. Only visible when looking at everything simultaneously. Zero fluff. Zero hedging. Pure signal.

--- ALL THIRD-ORDER THEME DOCUMENTS ---

{content}"""


def load_all_third_order() -> str:
    """Load all 15 third-order theme files."""
    files = sorted(THIRD_ORDER_DIR.glob("*.md"))
    print(f"  Loading {len(files)} third-order theme files...")
    combined = []
    total = 0
    for f in files:
        content = f.read_text(encoding="utf-8")
        # Take first 7000 chars per theme file
        excerpt = content[:7000]
        header = f"\n\n{'='*60}\nTHEME: {f.stem}\n{'='*60}\n\n"
        combined.append(header + excerpt)
        total += len(excerpt)
    print(f"  Total context: {total // 1024} KB")
    return "\n".join(combined)


def call_claude(prompt: str) -> str:
    for attempt in range(5):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=8000,
                messages=[{"role": "user", "content": prompt}]
            )
            time.sleep(3)
            return response.content[0].text.strip()
        except Exception as e:
            if "rate" in str(e).lower() or "overload" in str(e).lower():
                wait = 60 * (attempt + 1)
                print(f"    Waiting {wait}s...")
                time.sleep(wait)
            else:
                if attempt == 4:
                    raise
                time.sleep(15)
    return ""


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 4: Generating 5 Fourth-Order Master Mental Models")
    print("=" * 60)

    all_themes = load_all_third_order()

    for i, model in enumerate(MASTER_MODELS):
        out_path = FOURTH_ORDER_DIR / f"fourth_order_{model['slug']}.md"

        if out_path.exists() and out_path.stat().st_size > 10000:
            print(f"\n[{i+1}/5] [SKIP] {model['name']} — already done")
            continue

        print(f"\n[{i+1}/5] Generating: {model['name']}")
        prompt = BASE_PROMPT.format(
            name=model["name"],
            instructions=model["instructions"],
            content=all_themes
        )
        synthesis = call_claude(prompt)

        if not synthesis:
            print(f"  [ERROR] Failed for {model['name']}")
            continue

        output = f"# {model['name']}\n**Slug**: {model['slug']}\n**Layer**: fourth_order\n\n---\n\n{synthesis}"
        out_path.write_text(output, encoding="utf-8")
        size_kb = out_path.stat().st_size // 1024
        print(f"  [DONE] {model['name']} — {size_kb} KB")

    print("\n\nPhase 4 Complete.")
    fourth = list(FOURTH_ORDER_DIR.glob("*.md"))
    print(f"Total fourth-order files: {len(fourth)}")
```

---

---

# FINAL VERIFICATION — EVERYTHING DONE

Run this check after all 4 phases:

```python
from pathlib import Path

BASE = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base")

layers = {
    "first_order":  (BASE / "first_order",  80,  5),
    "second_order": (BASE / "second_order", 80,  3),
    "third_order":  (BASE / "third_order",  15, 10),
    "fourth_order": (BASE / "fourth_order",  5, 15),
}

print("=" * 60)
print("MindMusk Knowledge Base — Final Verification")
print("=" * 60)
all_ok = True
for layer, (path, min_files, min_kb) in layers.items():
    files = list(path.glob("*.md"))
    too_small = [f for f in files if f.stat().st_size // 1024 < min_kb]
    status = "OK" if len(files) >= min_files and not too_small else "INCOMPLETE"
    if status != "OK":
        all_ok = False
    print(f"\n{layer}: {len(files)} files [{status}]")
    if too_small:
        print(f"  WARNING: {len(too_small)} files below {min_kb} KB minimum:")
        for f in too_small:
            print(f"    {f.name} ({f.stat().st_size // 1024} KB)")

print("\n" + "=" * 60)
if all_ok:
    print("ALL PHASES COMPLETE. Knowledge base is ready for embedding.")
    print("Next step: Tell the main session that all 4 phases are done.")
else:
    print("INCOMPLETE. Re-run the script for the failing phase.")
print("=" * 60)
```

---

# WHAT TO DO IF SOMETHING GOES WRONG

**If you get a rate limit error (429 or "overload"):**
The scripts already handle this automatically with retry + wait. If a script keeps failing, wait 5 minutes and restart it — it will skip already-completed files.

**If a PDF extraction produces an empty file:**
Some PDFs have copy protection. Note the book name and skip it — do not delete the empty file.

**If a podcast transcript produces no Elon content:**
Mark it `[NO_ELON_CONTENT]` at the top of the file and continue. Do not delete it.

**If a synthesis sounds wrong or low quality:**
Delete the output file and re-run the script — it will regenerate that file.

**If you get a Python import error for any package:**
Run: `pip install anthropic python-docx pypdf python-dotenv`
Do NOT run: `pip install chromadb` or `pip install pymupdf` — these will fail.

**When you are done:**
Report back: "All 4 phases complete. X first-order files, Y second-order files, 15 third-order files, 5 fourth-order files."
