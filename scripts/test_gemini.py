import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: Add GEMINI_API_KEY to your .env file")
    exit(1)

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
payload = {"contents": [{"parts": [{"text": "Say 'API key works' and nothing else."}]}]}

print("Testing Gemini 2.0 Flash...")
r = requests.post(url, json=payload)

if r.status_code == 200:
    text = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    print(f"Response: {text}")
    print("Success.")
else:
    print(f"Error {r.status_code}: {r.text}")
