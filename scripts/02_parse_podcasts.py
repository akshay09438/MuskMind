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
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s]', '', slug)
    slug = re.sub(r'\s+', '_', slug.strip())
    return slug[:60]


def is_transcript_header(text: str):
    m = re.match(r'^#?(\d{1,3})[\.\s]+(.{10,150})$', text)
    if m:
        num = int(m.group(1))
        title = m.group(2).strip()
        if num < 200 and not re.match(r'^\d+:\d+', title) and 'second' not in title.lower() and 'minute' not in title.lower():
            return True, f"#{m.group(1)} {title}"
    return False, None


def is_timestamp(text: str) -> bool:
    if re.match(r'^\d+:\d+', text):
        return True
    if re.match(r'^\d+ (second|minute)', text.lower()):
        return True
    if re.match(r'^(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve) (second|minute)', text.lower()):
        return True
    return False


def parse_docx(docx_path: str) -> dict:
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
            if current_title and current_lines:
                transcripts[current_title] = "\n".join(current_lines)
            current_title = title
            current_lines = []
        else:
            if current_title and not is_timestamp(text):
                current_lines.append(text)

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

    for slug, (title, text) in all_transcripts.items():
        out_path = RAW_DIR / f"{slug}.md"
        content = f"# {title}\n\n{text}"
        out_path.write_text(content, encoding="utf-8")

    print(f"\nSaved {len(all_transcripts)} raw transcript files to:")
    print(f"  {RAW_DIR}")
