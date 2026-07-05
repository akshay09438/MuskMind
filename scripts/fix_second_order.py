"""
Generate second_order synthesis for the 7 books added/fixed after the main run:
- hitchhikers_guide, skeptics_guide, structures, mans_search_meaning,
  whats_our_problem, woman_makes_plan, art_of_war
"""
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))

FIRST_ORDER = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\first_order")
SECOND_ORDER = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\second_order")
SECOND_ORDER.mkdir(parents=True, exist_ok=True)

TARGET_SLUGS = [
    "hitchhikers_guide",
    "skeptics_guide",
    "structures",
    "mans_search_meaning",
    "whats_our_problem",
    "woman_makes_plan",
    "art_of_war",
]

N_SAMPLES = 5
SAMPLE_SIZE = 8000
MAX_SAMPLE = 40000

SYNTHESIS_PROMPT = """You are analyzing a book that Elon Musk has read. Extract what Elon specifically got from this book — the ideas that shaped how he thinks and operates.

Source: {title}

Content:
{content}

Write a deep synthesis (800-1200 words) covering:

1. CORE IDEAS ELON ABSORBED — The 3-5 most important concepts from this book that would resonate with Elon's worldview
2. MENTAL MODELS EXTRACTED — Specific thinking frameworks or decision-making tools this book gives
3. HOW IT CONNECTS TO ELON'S WORK — Concrete connections to SpaceX, Tesla, xAI, or his broader mission
4. KEY QUOTES OR PASSAGES — Most important lines from the text (or the book's central arguments)
5. INFLUENCE ON ELON'S WORLDVIEW — How this book shaped his thinking on physics, business, humanity, or risk

Be specific. Reference actual content from the text. Write as if you are documenting what a highly intelligent, mission-driven engineer and entrepreneur extracted from this book."""


def sample_content(text: str) -> str:
    if len(text) <= MAX_SAMPLE:
        return text
    step = len(text) // N_SAMPLES
    parts = [text[i * step: i * step + SAMPLE_SIZE] for i in range(N_SAMPLES)]
    return "\n\n[...]\n\n".join(parts)


def call_cerebras(prompt: str) -> str:
    for attempt in range(5):
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
            if "rate" in err or "429" in err:
                wait = 60 * (attempt + 1)
                print(f"  Rate limit, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  Error: {e}")
                time.sleep(15)
    return ""


if __name__ == "__main__":
    print("=" * 60)
    print("Fix Second Order: 7 new book syntheses")
    print("=" * 60)

    success = 0
    for slug in TARGET_SLUGS:
        first_path = FIRST_ORDER / f"{slug}_first_order.md"
        out_path = SECOND_ORDER / f"{slug}_second_order.md"

        if not first_path.exists():
            print(f"\n[SKIP] {slug} — first_order file not found")
            continue

        raw = first_path.read_text(encoding="utf-8")
        # Get title from header
        title = slug.replace("_", " ").title()
        for line in raw.split("\n")[:3]:
            if line.startswith("# "):
                title = line[2:].strip()
                break

        print(f"\n[{success+1}/7] {title}")
        content = sample_content(raw)
        print(f"  Content: {len(content)//1024}KB sampled from {len(raw)//1024}KB")

        synthesis = call_cerebras(SYNTHESIS_PROMPT.format(title=title, content=content))
        if not synthesis:
            print("  FAILED")
            continue

        output = f"""# {title} — Elon Musk Synthesis
**Source**: {slug}_first_order.md
**Layer**: second_order
**Model**: Cerebras gpt-oss-120b

---

{synthesis}
"""
        out_path.write_text(output, encoding="utf-8")
        size_kb = out_path.stat().st_size // 1024
        print(f"  Saved: {size_kb} KB")
        success += 1

    print(f"\n{'='*60}")
    print(f"Done. {success}/7 second_order syntheses generated.")
    total = list(SECOND_ORDER.glob("*.md"))
    print(f"Total second_order files: {len(total)}")
