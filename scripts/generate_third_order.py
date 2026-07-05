"""
Phase 3: Generate 15 third-order thematic synthesis documents.
Uses Cerebras llama3.3-70b. Reads second_order/, writes third_order/.
"""
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))

SECOND_ORDER = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\second_order")
THIRD_ORDER  = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\third_order")
THIRD_ORDER.mkdir(parents=True, exist_ok=True)

PER_SOURCE = 8000  # chars taken from each second-order doc

THEMES = [
    {"name": "First Principles and Physics-Based Reasoning", "slug": "first_principles",
     "keywords": ["superintelligence","life_3_0","human_compatible","our_final_invention","deep_learning",
                  "structures","ignition","selfish_gene","skeptics_guide","fermi_paradox",
                  "lex_fridman","stanford","foundation","yc","ted"]},
    {"name": "Multi-Planetary Life and Space Civilization", "slug": "multiplanetary",
     "keywords": ["dune","fermi_paradox","ignition","moon_harsh_mistress","hitchhikers",
                  "starship","spacex","mars","tim_dodd","satellite","boiler_room",
                  "mars_society","issrdc","everyday_astronaut"]},
    {"name": "Artificial Intelligence and Existential Risk", "slug": "ai_risk",
     "keywords": ["life_3_0","superintelligence","human_compatible","our_final_invention",
                  "deep_learning","what_we_owe_future","lex_fridman","yc","stanford",
                  "neuralink","ted","dealbook","grok","xai"]},
    {"name": "Energy, Climate, and Sustainable Civilization", "slug": "energy_climate",
     "keywords": ["selfish_gene","what_we_owe_future","wealth_of_nations","screw_business",
                  "ted","cop21","solar","battery","tesla","powerwall","rainn_wilson",
                  "sal_khan","master_plan"]},
    {"name": "Manufacturing, Engineering, and Physical Reality", "slug": "manufacturing_engineering",
     "keywords": ["ignition","structures","tim_dodd","starship","tesla_factory",
                  "investor_day","mkbhd","ai_day","raptor","megacast"]},
    {"name": "Company Building and Scaling", "slug": "company_building",
     "keywords": ["zero_to_one","masters_of_doom","steve_jobs","screw_business",
                  "stanford","yc","motley_fool","sxsw","auto_bild","2003","entrepreneur"]},
    {"name": "Leadership, Teams, and Organizational Design", "slug": "leadership_teams",
     "keywords": ["steve_jobs","benjamin_franklin","masters_of_doom","on_war","art_of_war",
                  "investor_day","pando","chm","time_person"]},
    {"name": "Motivation, Meaning, and Existential Purpose", "slug": "motivation_meaning",
     "keywords": ["mans_search_meaning","hitchhikers_guide","waiting_for_godot",
                  "fault_in_our_stars","caltech","usc","commencement","rainn","fox_news"]},
    {"name": "Learning, Mental Models, and How to Think", "slug": "learning_mental_models",
     "keywords": ["foundation","kevin_rose","sxsw","charlie_rose","baron","ted",
                  "skeptics_guide","lessons_of_history","selfish_gene","stanford"]},
    {"name": "History, Civilization Cycles, and Lessons", "slug": "history_civilization",
     "keywords": ["lessons_of_history","iliad","decline_fall_rome","storm_of_steel",
                  "on_war","wages_of_destruction","fifteen_battles","art_of_war",
                  "benjamin_franklin","explore_create","dan_carlin"]},
    {"name": "Fiction and the Books That Shaped Elon's Vision", "slug": "fiction_vision",
     "keywords": ["dune","hitchhikers_guide","lord_of_the_rings","atlas_shrugged",
                  "moon_harsh_mistress","stranger_strange_land","machine_stops",
                  "game_of_thrones","waiting_for_godot","fault_in_our_stars"]},
    {"name": "Risk, Failure, Resilience, and Recovery", "slug": "risk_failure",
     "keywords": ["masters_of_doom","steve_jobs","mans_search_meaning","storm_of_steel",
                  "starship","spacex","paypal","third_row","tim_dodd"]},
    {"name": "Science, Curiosity, and the Nature of Reality", "slug": "science_curiosity",
     "keywords": ["selfish_gene","skeptics_guide","fermi_paradox","what_we_owe_future",
                  "life_3_0","deep_learning","aliens","smithsonian","lex_fridman"]},
    {"name": "Economics, Wealth, and Capital Allocation", "slug": "economics_wealth",
     "keywords": ["wealth_of_nations","zero_to_one","screw_business","whats_our_problem",
                  "masters_of_doom","baron","motley_fool","robin_li","bill_gates"]},
    {"name": "Truth, Communication, and Fighting Narrative Capture", "slug": "truth_communication",
     "keywords": ["lying","parasitic_mind","whats_our_problem","woman_makes_plan",
                  "dealbook","bill_maher","time_person","twitter","free_speech","adl"]},
]

PROMPT = """You are building the knowledge base for MindMusk — an AI that replicates Elon Musk's mind.

Theme: "{theme}"

Below are second-order synthesis documents for all sources relevant to this theme. Your job is to synthesize ACROSS all of them — reveal how this theme runs through Elon's entire thinking.

Write "Elon's Mind on {theme}" with ALL of these sections:

## 1. THE CORE BELIEF
What does Elon fundamentally believe here? 2-3 paragraphs, no hedging. His actual position.

## 2. THE INTELLECTUAL LINEAGE
Which books, thinkers, ideas shaped his view? Show the chain: "He read X → got Y → showed up in Z decision."

## 3. THE MENTAL FRAMEWORK
His operating framework for this theme. What does he ask? What does he optimize for? What won't he trade off?

## 4. HOW IT SHOWS UP IN HIS COMPANIES
At least 8 specific examples — products, decisions, quotes from Tesla, SpaceX, Neuralink, X.

## 5. WHAT ELON HAS SAID (DIRECT QUOTES)
10-15 of the most powerful things Elon has said about this theme. Verbatim.

## 6. WHERE HE IS CONTRARIAN
How does his view differ from conventional wisdom? Where do most smart people get it wrong?

## 7. THE SOCRATIC QUESTIONS HE WOULD ASK
5-7 questions Elon would ask someone who came to him with a problem in this domain.

## 8. THE SYNTHESIS INSIGHT
What insight only becomes visible when you look at ALL sources together?

Maximum density. Every sentence = signal.

--- RELEVANT SECOND-ORDER DOCUMENTS ---
{content}"""


def get_sources(theme: dict) -> str:
    all_files = list(SECOND_ORDER.glob("*.md"))
    kws = [k.lower() for k in theme["keywords"]]
    matched = [f for f in all_files if any(k in f.stem.lower() for k in kws)]
    print(f"    {len(matched)} sources matched", end=" ", flush=True)
    combined = []
    for f in matched:
        text = f.read_text(encoding="utf-8")
        excerpt = f"\n\n{'='*50}\nSOURCE: {f.stem}\n{'='*50}\n\n{text[:PER_SOURCE]}"
        combined.append(excerpt)
    content = "\n".join(combined)
    if len(content) > 80000:
        content = content[:80000]
    print(f"({len(content)//1024}KB)", end=" ", flush=True)
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
                print(f"\n      Waiting {wait}s (rate limit)...", flush=True)
                time.sleep(wait)
            elif "connection" in err or "timeout" in err or "getaddr" in err:
                wait = 30 * (attempt + 1)
                print(f"\n      Network error, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                if attempt == 5:
                    raise
                print(f"\n      Error: {e}, retrying...", flush=True)
                time.sleep(15)
    return ""


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 3: 15 Third-Order Themes (Cerebras llama3.3-70b)")
    print("=" * 60)

    for i, theme in enumerate(THEMES):
        out_path = THIRD_ORDER / f"third_order_{theme['slug']}.md"
        if out_path.exists() and out_path.stat().st_size > 5000:
            print(f"[{i+1}/15] [SKIP] {theme['name']}")
            continue

        print(f"\n[{i+1}/15] {theme['name']}")
        sources = get_sources(theme)
        synthesis = call_cerebras(PROMPT.format(theme=theme["name"], content=sources))

        if not synthesis:
            print("\n  FAILED")
            continue

        output = f"# Elon's Mind on {theme['name']}\n**Slug**: {theme['slug']}\n**Layer**: third_order\n\n---\n\n{synthesis}"
        out_path.write_text(output, encoding="utf-8")
        print(f"\n  Saved: {out_path.stat().st_size // 1024} KB")

    print(f"\nPhase 3 complete. {len(list(THIRD_ORDER.glob('*.md')))} theme files.")
