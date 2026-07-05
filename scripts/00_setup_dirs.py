"""
MindMusk Setup: Create all required directories.
Run this first before any other script.
"""
from pathlib import Path

dirs = [
    r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\first_order",
    r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\second_order",
    r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\third_order",
    r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\fourth_order",
    r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\podcasts\raw",
    r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\podcasts\filtered",
    r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts",
]
for d in dirs:
    Path(d).mkdir(parents=True, exist_ok=True)
    print(f"OK: {d}")

print("\nAll directories ready.")
