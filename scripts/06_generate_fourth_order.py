"""
Phase 4: Generate 5 fourth-order Master Mental Model documents.
Reads from knowledge_base/third_order/ (all 15 theme files)
Writes to knowledge_base/fourth_order/
"""
import anthropic
import os
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

THIRD_ORDER_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\third_order")
FOURTH_ORDER_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\fourth_order")
FOURTH_ORDER_DIR.mkdir(parents=True, exist_ok=True)

MASTER_MODELS = [
    {
        "name": "The Elon Musk Decision Framework",
        "slug": "decision_framework",
        "instructions": """Write a comprehensive document that reveals Elon's universal decision-making process.

Structure it as:

## 1. THE ENTRY POINT: HOW HE FRAMES ANY PROBLEM
What is the first question he asks? How does he strip away assumptions? What does "first principles" actually mean in practice?

## 2. THE FILTERS HE RUNS EVERY DECISION THROUGH
List and explain each filter. Does it advance humanity's multi-planetary future? Does it pass the physics test? Is the cost of being wrong recoverable?

## 3. HOW HE HANDLES UNCERTAINTY
When he doesn't have enough information, what does he do? How does he model probability?

## 4. HOW HE EVALUATES RISK
His risk calculus is not normal. What risks does he take that others won't? What risks does he refuse that others accept? Why?

## 5. HOW HE MAKES SPEED/QUALITY TRADEOFFS
When does he move fast? When does he demand perfection? What determines the tradeoff?

## 6. HOW HE HANDLES BEING WRONG
What does Elon do when he realizes he made a wrong decision? How does he course correct?

## 7. THE QUESTIONS HE ASKS THAT MOST PEOPLE NEVER ASK
Specific questions Elon asks in any situation that most people never think to ask.

## 8. WHAT HE WILL NEVER COMPROMISE ON
The absolute hard limits — things he will never trade off regardless of the situation."""
    },
    {
        "name": "Elon's Theory of Civilization",
        "slug": "theory_of_civilization",
        "instructions": """Write a comprehensive document that reveals Elon's complete worldview on human civilization.

## 1. WHERE WE ARE IN THE ARC OF HISTORY
What does Elon believe about where humanity stands right now? What moment is this?

## 2. THE EXISTENTIAL THREATS HE ACTUALLY WORRIES ABOUT
Not the polished answers — the ones that genuinely keep him up at night. Rank them. Explain why.

## 3. HIS MODEL OF HOW CIVILIZATIONS RISE AND FALL
What patterns does he see from his reading of history? What makes civilizations collapse? Thrive?

## 4. WHAT MAKES THIS MOMENT UNIQUE
Why does Elon believe we are at an inflection point? What makes the next 20-50 years different?

## 5. HIS VISION FOR WHAT GOOD LOOKS LIKE
Not just "Mars" — what does Elon's actual vision of a good future look like in detail?

## 6. WHO HE THINKS THE HEROES AND VILLAINS ARE
What types of actors move civilization forward? What types hold it back?

## 7. WHY HE DOES WHAT HE DOES
The deepest motivation. Not the PR answer. What does Elon believe about why his work matters?

## 8. WHAT HE FEARS MOST
His genuine fears about the future — not the optimism he projects publicly."""
    },
    {
        "name": "Elon's Operator Manual for Companies",
        "slug": "operator_manual",
        "instructions": """Write a comprehensive document that reveals how Elon actually builds and runs companies.

## 1. HOW HE EVALUATES WHETHER A COMPANY IS WORTH STARTING
The exact criteria. What has to be true for him to think a company is worth building?

## 2. HOW HE HIRES (AND WHO HE HIRES)
What does he actually look for? What questions does he ask? What disqualifies someone? What signals exceptional talent?

## 3. HOW HE SETS GOALS AND DEMANDS
How does he set targets? Why does he set goals that seem impossible? How does he use deadlines as tools?

## 4. HOW HE HANDLES BUREAUCRACY AND RULES
His actual philosophy on rules, processes, bureaucracy. When does he delete rules? How does he prevent organizational calcification?

## 5. HOW HE MANAGES ENGINEERS AND MAKERS
His specific approach to technical talent. How does he interact with engineers differently from managers?

## 6. HOW HE HANDLES FAILURE AND BAD NEWS
How does he react when things go wrong? What does he expect from people who bring bad news?

## 7. HOW HE THINKS ABOUT PRODUCTS
His product philosophy. What makes a good product? How does he evaluate design? What does he refuse to ship?

## 8. HOW HE MAINTAINS INTENSITY ACROSS MULTIPLE COMPANIES
How does he actually operate across Tesla, SpaceX, Neuralink, X simultaneously? His time management philosophy."""
    },
    {
        "name": "How Elon Learns and Processes Information",
        "slug": "how_elon_learns",
        "instructions": """Write a comprehensive document that reveals how Elon's mind actually processes information.

## 1. HOW HE READS BOOKS
He doesn't read like most people. What is his actual approach? What does he take from them? How do books become mental models?

## 2. HOW HE BUILDS MENTAL MODELS
What is his process for building a model of how something works? How does he go from zero knowledge to deep understanding?

## 3. HOW HE USES ANALOGIES
How does he construct analogies? What makes a good analogy in his view? How does he use them as thinking tools?

## 4. HOW HE APPLIES PHYSICS THINKING OUTSIDE OF PHYSICS
The "physics approach" — how does he actually apply it to business, management, human behavior, politics?

## 5. HOW HE UPDATES HIS BELIEFS
What does it take to change Elon's mind? What kind of evidence counts? How does he handle cognitive dissonance?

## 6. HOW HE HANDLES DOMAINS WHERE HE IS IGNORANT
When he enters a new field, what is his process? How long does it take him to reach competence?

## 7. HOW HE SYNTHESIZES ACROSS DISCIPLINES
How does he pull ideas from wildly different fields? What is the process for cross-domain insight?

## 8. THE QUESTIONS HE ASKS TO LEARN FASTER
The specific types of questions he asks experts and novices to accelerate his learning."""
    },
    {
        "name": "What Elon Actually Believes — The Candid Version",
        "slug": "what_elon_believes",
        "instructions": """Write a comprehensive document capturing Elon's private beliefs from unguarded moments.

## 1. WHAT HE SAYS ABOUT CONSCIOUSNESS AND THE NATURE OF REALITY
His real views on simulation theory, consciousness, what makes something "alive," physics vs. philosophy.

## 2. WHAT HE SAYS ABOUT GOD, RELIGION, AND MEANING
Not the diplomatic answers — his actual views. Does the universe have meaning? Is there anything beyond physics?

## 3. WHAT HE SAYS ABOUT DEATH AND LEGACY
His real relationship with mortality. What does he think happens after death? What drives him?

## 4. WHAT HE SAYS ABOUT HUMAN NATURE
Does he trust people? What motivates most humans? Where are humans weak? Strong?

## 5. WHAT HE SAYS ABOUT HIS OWN PSYCHOLOGY
His self-reported inner experience. What does he say about how he feels? About loneliness? About what he finds hard?

## 6. WHAT HE SAYS ABOUT HIS DARKEST MOMENTS
When he has spoken about being on the edge — financially, emotionally, existentially. What he was thinking.

## 7. WHAT HE BELIEVES MOST PEOPLE GET WRONG ABOUT HIM
The misconceptions that actually bother him. The version of Elon in public discourse that he knows is wrong.

## 8. THE CORE BELIEFS HE HAS NEVER WAVERED ON
Despite all public controversy — what has Elon believed consistently his entire adult life?"""
    },
]

BASE_PROMPT = """You are writing the most important documents in the MindMusk knowledge base. These will be used by an AI to replicate how Elon Musk thinks at the deepest level.

Document: "{name}"

You have access to all 15 thematic synthesis documents. You are synthesizing across ALL themes.

{instructions}

Write 3000-5000 words. Maximum density and depth. Only visible when looking at everything simultaneously. Zero fluff. Zero hedging. Pure signal.

--- ALL THIRD-ORDER THEME DOCUMENTS ---

{content}"""


def load_all_third_order() -> str:
    files = sorted(THIRD_ORDER_DIR.glob("*.md"))
    print(f"  Loading {len(files)} third-order theme files...")
    combined = []
    total = 0
    for f in files:
        content = f.read_text(encoding="utf-8")
        excerpt = content[:7000]
        header = f"\n\n{'='*60}\nTHEME: {f.stem}\n{'='*60}\n\n"
        combined.append(header + excerpt)
        total += len(excerpt)
    print(f"  Total context: {total // 1024} KB")
    return "\n".join(combined)


def call_claude(prompt: str) -> str:
    for attempt in range(5):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=8000,
                messages=[{"role": "user", "content": prompt}]
            )
            time.sleep(3)
            return response.content[0].text.strip()
        except Exception as e:
            err = str(e)
            if "rate" in err.lower() or "overload" in err.lower():
                wait = 60 * (attempt + 1)
                print(f"    Waiting {wait}s...")
                time.sleep(wait)
            else:
                if attempt == 4:
                    raise
                time.sleep(15)
    return ""


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 4: Generating 5 Fourth-Order Master Mental Models")
    print("=" * 60)

    all_themes = load_all_third_order()

    for i, model in enumerate(MASTER_MODELS):
        out_path = FOURTH_ORDER_DIR / f"fourth_order_{model['slug']}.md"

        if out_path.exists() and out_path.stat().st_size > 10000:
            print(f"\n[{i+1}/5] [SKIP] {model['name']} — already done")
            continue

        print(f"\n[{i+1}/5] Generating: {model['name']}")
        prompt = BASE_PROMPT.format(
            name=model["name"],
            instructions=model["instructions"],
            content=all_themes
        )
        synthesis = call_claude(prompt)

        if not synthesis:
            print(f"  [ERROR] Failed for {model['name']}")
            continue

        output = f"# {model['name']}\n**Slug**: {model['slug']}\n**Layer**: fourth_order\n\n---\n\n{synthesis}"
        out_path.write_text(output, encoding="utf-8")
        size_kb = out_path.stat().st_size // 1024
        print(f"  [DONE] {model['name']} — {size_kb} KB")

    fourth = list(FOURTH_ORDER_DIR.glob("*.md"))
    print(f"\n\nPhase 4 Complete. {len(fourth)}/5 master documents generated.")
