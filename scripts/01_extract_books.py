"""
Phase 1A: Extract text from all 41 book PDFs.
Saves cleaned text to knowledge_base/first_order/{slug}_first_order.md
"""
from pypdf import PdfReader
from pathlib import Path
import re

OUTPUT_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\first_order")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
    text = text.replace('\x00', '')
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'^\s*\d{1,4}\s*$', '', text, flags=re.MULTILINE)
    text = text.strip()
    return text


def extract_book(pdf_path: str, slug: str, title: str, category: str) -> None:
    out_path = OUTPUT_DIR / f"{slug}_first_order.md"

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

    files = list(OUTPUT_DIR.glob("*_first_order.md"))
    print(f"\nDone. {len(files)} book files in knowledge_base/first_order/")
