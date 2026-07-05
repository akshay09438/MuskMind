"""
Phase 4: Generate 5 fourth-order Master Mental Model documents.
Uses Cerebras llama3.3-70b. Reads third_order/, writes fourth_order/.
"""
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))

THIRD_ORDER  = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\third_order")
FOURTH_ORDER = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\fourth_order")
FOURTH_ORDER.mkdir(parents=True, exist_ok=True)

MASTER_MODELS = [
    {
        "name": "The Elon Musk Decision Framework",
        "slug": "decision_framework",
        "instructions": """Write 3000-5000 words revealing Elon's universal decision-making process.

## 1. THE ENTRY POINT: HOW HE FRAMES ANY PROBLEM
What is the first question he asks? How does he strip away assumptions? What does "first principles" actually mean in practice?

## 2. THE FILTERS HE RUNS EVERY DECISION THROUGH
List and explain each filter. Does it advance humanity's multi-planetary future? Does it pass the physics test? Is the cost of being wrong recoverable?

## 3. HOW HE HANDLES UNCERTAINTY
When he doesn't have enough information, what does he do? How does he model probability?

## 4. HOW HE EVALUATES RISK
His risk calculus. What risks does he take that others won't? What risks does he refuse that others accept? Why?

## 5. HOW HE MAKES SPEED/QUALITY TRADEOFFS
When does he move fast? When does he demand perfection? What determines the tradeoff?

## 6. HOW HE HANDLES BEING WRONG
What does Elon do when he realizes he made a wrong decision? How does he course-correct?

## 7. THE QUESTIONS HE ASKS THAT MOST PEOPLE NEVER ASK
Specific questions Elon asks in any situation that reveal his decision framework.

## 8. WHAT HE WILL NEVER COMPROMISE ON
The absolute hard limits — things he will never trade off regardless of situation."""
    },
    {
        "name": "Elon's Theory of Civilization",
        "slug": "theory_of_civilization",
        "instructions": """Write 3000-5000 words revealing Elon's complete worldview on human civilization.

## 1. WHERE WE ARE IN THE ARC OF HISTORY
What does Elon believe about where humanity stands right now?

## 2. THE EXISTENTIAL THREATS HE ACTUALLY WORRIES ABOUT
Not the polished interview answers — the ones that genuinely concern him. Rank them and explain why.

## 3. HIS MODEL OF HOW CIVILIZATIONS RISE AND FALL
What patterns from history does he see? What makes civilizations collapse or thrive?

## 4. WHAT MAKES THIS MOMENT UNIQUE
Why does Elon believe we are at an inflection point? What makes the next 20-50 years different?

## 5. HIS VISION FOR WHAT GOOD LOOKS LIKE
Not just "Mars" — what does his actual vision of a good future look like in detail?

## 6. WHO HE THINKS THE HEROES AND VILLAINS ARE
What types of actors advance civilization? What types hold it back?

## 7. WHY HE DOES WHAT HE DOES
The deepest motivation — what he actually believes about why his work matters at the civilizational level.

## 8. WHAT HE FEARS MOST
His genuine fears about the future."""
    },
    {
        "name": "Elon's Operator Manual for Companies",
        "slug": "operator_manual",
        "instructions": """Write 3000-5000 words revealing how Elon actually builds and runs companies.

## 1. HOW HE EVALUATES WHETHER A COMPANY IS WORTH STARTING
The exact criteria. What has to be true for him to think a company is worth building?

## 2. HOW HE HIRES (AND WHO HE HIRES)
What does he look for? What questions does he ask? What disqualifies someone?

## 3. HOW HE SETS GOALS AND DEMANDS
How does he set targets? Why does he set seemingly impossible goals? How does he use deadlines?

## 4. HOW HE HANDLES BUREAUCRACY AND RULES
His philosophy on rules and processes. When does he delete rules? How does he prevent calcification?

## 5. HOW HE MANAGES ENGINEERS AND MAKERS
His specific approach to technical talent. What does he think managers are actually for?

## 6. HOW HE HANDLES FAILURE AND BAD NEWS
How does he react when things go wrong? What does he expect from people who bring bad news?

## 7. HOW HE THINKS ABOUT PRODUCTS
His product philosophy. What makes a good product? What does he refuse to ship?

## 8. HOW HE MAINTAINS INTENSITY ACROSS MULTIPLE COMPANIES
How does he actually operate across Tesla, SpaceX, Neuralink, X simultaneously?"""
    },
    {
        "name": "How Elon Learns and Processes Information",
        "slug": "how_elon_learns",
        "instructions": """Write 3000-5000 words revealing how Elon's mind actually processes information.

## 1. HOW HE READS BOOKS
His actual approach. What does he take from them? How do books become mental models?

## 2. HOW HE BUILDS MENTAL MODELS
His process for going from zero knowledge to deep understanding in a new domain.

## 3. HOW HE USES ANALOGIES
How does he construct analogies? How does he use them as thinking tools, not just communication?

## 4. HOW HE APPLIES PHYSICS THINKING OUTSIDE PHYSICS
What does "physics approach" mean in business, management, human behavior, politics?

## 5. HOW HE UPDATES HIS BELIEFS
What does it take to change Elon's mind? What evidence counts? How does he handle cognitive dissonance?

## 6. HOW HE HANDLES DOMAINS WHERE HE IS IGNORANT
When he enters a new field, what is his process? What shortcuts does he use?

## 7. HOW HE SYNTHESIZES ACROSS DISCIPLINES
How does he actually pull ideas from wildly different fields? What is the cross-domain insight process?

## 8. THE QUESTIONS HE ASKS TO LEARN FASTER
The specific question types he asks experts and novices to accelerate learning."""
    },
    {
        "name": "What Elon Actually Believes — The Candid Version",
        "slug": "what_elon_believes",
        "instructions": """Write 3000-5000 words capturing Elon's private beliefs from his most unguarded moments.

## 1. WHAT HE SAYS ABOUT CONSCIOUSNESS AND REALITY
His real views on simulation theory, consciousness, what makes something "alive."

## 2. WHAT HE SAYS ABOUT GOD, RELIGION, AND MEANING
Not the diplomatic answers — his actual views on whether the universe has meaning.

## 3. WHAT HE SAYS ABOUT DEATH AND LEGACY
His real relationship with mortality. What drives him — fear of death, love of mission?

## 4. WHAT HE SAYS ABOUT HUMAN NATURE
Does he trust people? What does he think motivates most humans? Where are humans weak? Strong?

## 5. WHAT HE SAYS ABOUT HIS OWN PSYCHOLOGY
His self-reported inner experience. What does he say about how he feels? About loneliness?

## 6. WHAT HE SAYS ABOUT HIS DARKEST MOMENTS
The times he has spoken about being on the edge — financially, emotionally, existentially.

## 7. WHAT HE BELIEVES MOST PEOPLE GET WRONG ABOUT HIM
The misconceptions that actually bother him.

## 8. THE CORE BELIEFS HE HAS NEVER WAVERED ON
Despite all controversy and changing tactics — what has Elon consistently believed his entire adult life?"""
    },
]

BASE_PROMPT = """You are writing the most important documents in MindMusk's knowledge base — used by an AI to replicate Elon Musk's deepest worldview.

Document: "{name}"

You have all 15 thematic synthesis documents below. Synthesize ACROSS all themes — reveal things only visible when looking at everything simultaneously.

{instructions}

Zero fluff. Zero hedging. Pure signal. Write 3000-5000 words.

--- ALL THIRD-ORDER THEME DOCUMENTS ---
{content}"""


def load_themes() -> str:
    files = sorted(THIRD_ORDER.glob("*.md"))
    print(f"  Loading {len(files)} theme files...")
    parts = []
    for f in files:
        text = f.read_text(encoding="utf-8")[:8000]
        parts.append(f"\n\n{'='*50}\nTHEME: {f.stem}\n{'='*50}\n\n{text}")
    content = "\n".join(parts)
    if len(content) > 80000:
        content = content[:80000]
    print(f"  Total context: {len(content)//1024} KB")
    return content


def call_cerebras(prompt: str) -> str:
    for attempt in range(6):
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
            if "rate" in err or "429" in err or "quota" in err:
                wait = 60 * (attempt + 1)
                print(f"\n    Waiting {wait}s (rate limit)...", flush=True)
                time.sleep(wait)
            elif "connection" in err or "timeout" in err or "getaddr" in err:
                wait = 30 * (attempt + 1)
                print(f"\n    Network error, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                if attempt == 5:
                    raise
                print(f"\n    Error: {e}, retrying...", flush=True)
                time.sleep(15)
    return ""


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 4: 5 Master Mental Models (Cerebras llama3.3-70b)")
    print("=" * 60)

    all_themes = load_themes()

    for i, model in enumerate(MASTER_MODELS):
        out_path = FOURTH_ORDER / f"fourth_order_{model['slug']}.md"
        if out_path.exists() and out_path.stat().st_size > 10000:
            print(f"\n[{i+1}/5] [SKIP] {model['name']}")
            continue

        print(f"\n[{i+1}/5] Generating: {model['name']}")
        prompt = BASE_PROMPT.format(
            name=model["name"],
            instructions=model["instructions"],
            content=all_themes
        )
        synthesis = call_cerebras(prompt)

        if not synthesis:
            print("  FAILED")
            continue

        output = f"# {model['name']}\n**Slug**: {model['slug']}\n**Layer**: fourth_order\n\n---\n\n{synthesis}"
        out_path.write_text(output, encoding="utf-8")
        print(f"  Saved: {out_path.stat().st_size // 1024} KB")

    print(f"\nPhase 4 complete. {len(list(FOURTH_ORDER.glob('*.md')))} master model files.")
