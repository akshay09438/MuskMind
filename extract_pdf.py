import subprocess
import sys

# Install pypdf if not present
try:
    import pypdf
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
    import pypdf

pdf_path = r"C:\Users\Akshay\OneDrive\Desktop\ELON LLM\ELON BOOKS\AI AND MACHINE LEARNING\Our Final Invention Artificial Intelligence and the End of the.pdf"
output_path = r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\our_final_invention_raw.txt"

reader = pypdf.PdfReader(pdf_path)
total_pages = len(reader.pages)
print(f"Total pages: {total_pages}")

with open(output_path, "w", encoding="utf-8") as f:
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        f.write(f"\n\n===PAGE {i+1}===\n\n")
        f.write(text or "")
        if (i+1) % 20 == 0:
            print(f"Processed page {i+1}/{total_pages}")

print(f"Done! Text saved to {output_path}")
