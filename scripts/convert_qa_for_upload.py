import json
from pathlib import Path

p = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\conversation_style\elon_qa_pairs.jsonl")
out = []
for line in p.read_text(encoding="utf-8").strip().splitlines():
    if not line.strip():
        continue
    pair = json.loads(line)
    q = pair["instruction"]
    a = pair["response"]
    out.append(f"Q: {q}\n\nA: {a}\n\n---")

result = "\n\n".join(out)
dest = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\conversation_style\elon_qa_pairs.md")
dest.write_text(result, encoding="utf-8")
print(f"Done — {len(out)} pairs written to {dest}")
