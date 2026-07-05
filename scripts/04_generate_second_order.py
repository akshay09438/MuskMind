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

MAX_CHARS_PER_CALL = 80000
SECTION_SIZE = 20000

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
    for attempt in range(5):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            time.sleep(2)
            return response.content[0].text.strip()
        except Exception as e:
            err = str(e)
            if "rate" in err.lower() or "529" in err or "overload" in err.lower():
                wait = 30 * (attempt + 1)
                print(f"      Rate limit, waiting {wait}s...")
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
        out_name = f"podcast_{slug.replace('podcast_', '')}_synthesis.md"
    else:
        out_name = f"{slug}_elon_synthesis.md"

    out_path = SECOND_ORDER_DIR / out_name

    if out_path.exists() and out_path.stat().st_size > 3000:
        print(f"  [SKIP] {slug} — already synthesized")
        return

    print(f"  [SYNTHESIZING] {slug}...")
    content = source_path.read_text(encoding="utf-8")

    lines = content.split('\n')
    title = lines[0].replace('# ', '').strip()
    category = ""
    for line in lines[:10]:
        if line.startswith("**Category**"):
            category = line.split(":", 1)[1].strip().strip("*")

    if len(content) <= MAX_CHARS_PER_CALL:
        if is_podcast:
            prompt = PODCAST_SYNTHESIS_PROMPT.format(title=title, content=content)
        else:
            prompt = BOOK_SYNTHESIS_PROMPT.format(title=title, category=category, content=content)

        synthesis = call_claude(prompt, max_tokens=6000)
    else:
        print(f"    Large source ({len(content)//1024} KB) — using map-reduce...")
        sections = []
        for i in range(0, len(content), SECTION_SIZE):
            sections.append(content[i:i + SECTION_SIZE])

        print(f"    Mapping {len(sections)} sections...")
        extractions = []
        for j, section in enumerate(sections):
            print(f"      Section {j+1}/{len(sections)}...", end=" ", flush=True)
            extraction = call_claude(MAP_PROMPT.format(title=title, content=section), max_tokens=2000)
            extractions.append(extraction)
            print("OK")

        print(f"    Reducing to final synthesis...")
        combined = "\n\n---\n\n".join(extractions)
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

    second_order_files = list(SECOND_ORDER_DIR.glob("*.md"))
    print(f"\n\nPhase 2 Complete. {len(second_order_files)} second-order files generated.")
