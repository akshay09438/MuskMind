"""
Fix missing books: extract 5 books that failed due to path issues.
Uses glob to find PDFs dynamically to avoid Windows apostrophe path issues.
Skips 'A Woman Makes a Plan' (PDF is corrupt, 1634 bytes).
Also re-extracts Art of War (extracted 0 bytes previously).
"""
from pypdf import PdfReader
from pathlib import Path
import re
import glob as globlib

BOOKS_ROOT = Path(r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS")
OUTPUT_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\first_order")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Map: (glob_pattern, slug, title, category)
MISSING = [
    ("**/The Hitchhiker*", "hitchhikers_guide", "The Hitchhiker's Guide to the Galaxy", "Fiction"),
    ("**/The Skeptics*", "skeptics_guide", "The Skeptics' Guide to the Universe", "Sciences"),
    ("**/Structures*", "structures", "Structures: Or Why Things Don't Fall Down", "Rocket Science and Engineering"),
    ("**/Man*Search*", "mans_search_meaning", "Man's Search for Meaning", "History"),
    ("**/What*Our Problem*", "whats_our_problem", "What's Our Problem", "Business and Economics"),
    ("**/The Art of War*", "art_of_war", "The Art of War", "History"),
]


def clean_text(text: str) -> str:
    text = text.replace('\x00', '')
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'^\s*\d{1,4}\s*$', '', text, flags=re.MULTILINE)
    return text.strip()


def find_pdf(pattern: str) -> Path | None:
    matches = list(BOOKS_ROOT.glob(pattern))
    if matches:
        return matches[0]
    return None


def extract_book(pdf_path: Path, slug: str, title: str, category: str) -> bool:
    out_path = OUTPUT_DIR / f"{slug}_first_order.md"
    print(f"\n[EXTRACTING] {title}")
    print(f"  PDF: {pdf_path.name} ({pdf_path.stat().st_size // 1024} KB)")

    try:
        reader = PdfReader(str(pdf_path))
        total_pages = len(reader.pages)
        all_text = []

        for page_num, page in enumerate(reader.pages):
            try:
                text = page.extract_text()
                if text and len(text.strip()) > 10:
                    all_text.append(text)
            except Exception as e:
                print(f"    Warning: page {page_num} skipped: {e}")
                continue

        full_text = "\n\n".join(all_text)
        full_text = clean_text(full_text)

        if len(full_text) < 100:
            print(f"  [WARN] Very little text extracted ({len(full_text)} chars) — PDF may be image-based")

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
        print(f"  [DONE] {total_pages} pages, {size_kb} KB saved")
        return True

    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Fix Missing Books Extraction")
    print("=" * 60)

    success = 0
    for pattern, slug, title, category in MISSING:
        pdf_path = find_pdf(pattern)
        if not pdf_path:
            print(f"\n[NOT FOUND] {title} — glob: {pattern}")
            continue
        if extract_book(pdf_path, slug, title, category):
            success += 1

    print(f"\n{'='*60}")
    print(f"Done. {success}/{len(MISSING)} books extracted.")
    total = list(OUTPUT_DIR.glob("*_first_order.md"))
    print(f"Total first_order files now: {len(total)}")
