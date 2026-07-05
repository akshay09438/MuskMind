"""
Final Verification: Check all 4 phases are complete.
"""
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
    else:
        sizes = [f.stat().st_size // 1024 for f in files]
        if sizes:
            print(f"  Sizes: min={min(sizes)} KB, max={max(sizes)} KB, avg={sum(sizes)//len(sizes)} KB")

print("\n" + "=" * 60)
if all_ok:
    print("ALL PHASES COMPLETE. Knowledge base is ready for embedding.")
else:
    print("INCOMPLETE. Re-run the script for the failing phase.")
print("=" * 60)
