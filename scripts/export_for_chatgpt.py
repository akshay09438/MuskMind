"""
Merges all 4 knowledge base layers into 4 combined files for ChatGPT upload.
Output: exports/chatgpt/layer_1_first_order.md (etc.)
"""
from pathlib import Path

KB = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base")
OUT = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\exports\chatgpt")
OUT.mkdir(parents=True, exist_ok=True)

layers = [
    ("first_order",  "Layer 1 — Raw Source Content (Books + Podcast Transcripts)"),
    ("second_order", "Layer 2 — Per-Source Elon Synthesis"),
    ("third_order",  "Layer 3 — Thematic Cross-Source Synthesis"),
    ("fourth_order", "Layer 4 — Master Mental Models"),
]

for folder, title in layers:
    files = sorted((KB / folder).glob("*.md"))
    parts = [f"# {title}\nTotal files: {len(files)}\n\n{'='*80}\n"]
    total_chars = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        parts.append(f"\n{'='*80}\nFILE: {f.name}\n{'='*80}\n\n{text}\n")
        total_chars += len(text)
    combined = "\n".join(parts)
    out_path = OUT / f"layer_{folder}.md"
    out_path.write_text(combined, encoding="utf-8")
    print(f"  {out_path.name}: {len(files)} files, {total_chars//1024}KB")

print(f"\nDone. Files saved to: {OUT}")
print("Upload all 4 files to your ChatGPT project.")
