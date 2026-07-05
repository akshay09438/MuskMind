"""
Generate first_order content for 3 books where PDF extraction failed:
- Structures: Or Why Things Don't Fall Down (image-based PDF)
- The Art of War (image-based PDF)
- A Woman Makes a Plan (corrupted PDF, 1634 bytes)

Uses Cerebras to synthesize the full content of each book from its knowledge.
"""
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))

OUTPUT_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\first_order")

BOOKS = [
    {
        "slug": "art_of_war",
        "title": "The Art of War",
        "author": "Sun Tzu",
        "category": "History",
        "prompt": """Write a comprehensive summary of Sun Tzu's "The Art of War" as if it were extracted from the book itself.

Include:
1. All 13 chapters with their key teachings (Laying Plans, Waging War, Attack by Stratagem, Tactical Dispositions, Energy, Weak Points and Strong, Maneuvering, Variation in Tactics, The Army on the March, Terrain, The Nine Situations, The Attack by Fire, The Use of Spies)
2. Core philosophical principles: deception, speed, adaptability, knowing yourself and your enemy
3. Key quotes and maxims from each chapter
4. How Sun Tzu's principles apply to business, engineering, and strategy
5. The concept of winning without fighting
6. Intelligence and information warfare principles

Be exhaustive and faithful to the original text. Include actual quotes where possible. This is for a knowledge base."""
    },
    {
        "slug": "structures",
        "title": "Structures: Or Why Things Don't Fall Down",
        "author": "J.E. Gordon",
        "category": "Rocket Science and Engineering",
        "prompt": """Write a comprehensive summary of J.E. Gordon's "Structures: Or Why Things Don't Fall Down" as if it were extracted from the book itself.

Include:
1. Core concepts: stress, strain, tension, compression, shear, torsion
2. Why materials fail: cracks, fractures, Griffith's theory of fracture
3. The story of how engineers learned about structural safety (historical failures and lessons)
4. Columns and compression: Euler buckling, why tall thin columns fail
5. Beams: how they work, bending moments, neutral axis
6. Arches and domes: how compression structures work
7. Tension structures: suspension bridges, cables, membranes
8. Biological structures: bones, shells, wood — what engineers can learn
9. Ships, aircraft, and how modern materials changed everything
10. The concept of energy storage in structures (springs, resilience)
11. Key insight: structures are about energy, not just strength

This book is on Elon Musk's recommended reading list for SpaceX engineers. Be exhaustive and technical."""
    },
    {
        "slug": "woman_makes_plan",
        "title": "A Woman Makes a Plan",
        "author": "Maye Musk",
        "category": "Business and Economics",
        "prompt": """Write a comprehensive summary of Maye Musk's "A Woman Makes a Plan: Advice for a Lifetime of Adventure, Beauty, and Success" as if it were extracted from the book itself.

Maye Musk is Elon Musk's mother, a model and dietitian who immigrated from Canada to South Africa, then to the US.

Include:
1. Her core life philosophy: making plans and taking action even in uncertainty
2. Her personal story: raising three exceptional children (Elon, Kimbal, Tosca) largely alone after leaving a difficult marriage
3. Advice on reinventing yourself at any age — she became a top model in her 60s and 70s
4. Career advice: multiple careers, resilience, perseverance
5. Health and nutrition wisdom from her dietitian background
6. The Musk family values she instilled: work hard, be curious, don't accept limits
7. Immigration and starting over in new countries
8. Her relationship with Elon: what she observed about his early genius, obsession, and drive
9. Key life lessons and specific advice for women

Be detailed and include her actual advice and observations, especially about Elon's upbringing and character."""
    },
]


def call_cerebras(prompt: str) -> str:
    for attempt in range(5):
        try:
            response = client.chat.completions.create(
                model="gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=6000,
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
    print("Fix Image-Based / Corrupted Books via Cerebras")
    print("=" * 60)

    for book in BOOKS:
        print(f"\n[GENERATING] {book['title']} by {book['author']}")
        content = call_cerebras(book["prompt"])

        if not content:
            print("  FAILED — no content generated")
            continue

        output = f"""# {book['title']}
**Author**: {book['author']}
**Category**: {book['category']}
**Slug**: {book['slug']}
**Layer**: first_order
**Note**: Generated from AI knowledge (original PDF was image-based or corrupted)

---

{content}
"""
        out_path = OUTPUT_DIR / f"{book['slug']}_first_order.md"
        out_path.write_text(output, encoding="utf-8")
        size_kb = out_path.stat().st_size // 1024
        print(f"  [DONE] {size_kb} KB saved to {out_path.name}")

    print("\nDone.")
    total = list(OUTPUT_DIR.glob("*.md"))
    print(f"Total first_order files: {len(total)}")
