"""
Phase 3: Generate 15 third-order thematic synthesis documents.
Reads from knowledge_base/second_order/
Writes to knowledge_base/third_order/
"""
import anthropic
import os
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\.env")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SECOND_ORDER_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\second_order")
THIRD_ORDER_DIR = Path(r"C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\third_order")
THIRD_ORDER_DIR.mkdir(parents=True, exist_ok=True)

MAX_CONTEXT = 90000

THEMES = [
    {
        "name": "First Principles and Physics-Based Reasoning",
        "slug": "first_principles",
        "source_keywords": ["superintelligence", "life_3_0", "human_compatible", "our_final_invention",
                            "deep_learning", "structures", "ignition", "selfish_gene", "skeptics_guide",
                            "fermi_paradox", "lex_fridman", "stanford", "foundation", "yc", "ted"],
    },
    {
        "name": "Multi-Planetary Life and Space Civilization",
        "slug": "multiplanetary",
        "source_keywords": ["dune", "fermi_paradox", "ignition", "moon_harsh_mistress", "hitchhikers",
                            "starship", "spacex", "mars", "tim_dodd", "satellite", "boiler_room",
                            "mars_society", "issrdc", "everyday_astronaut"],
    },
    {
        "name": "Artificial Intelligence and Existential Risk",
        "slug": "ai_risk",
        "source_keywords": ["life_3_0", "superintelligence", "human_compatible", "our_final_invention",
                            "deep_learning", "what_we_owe_future", "lex_fridman", "yc", "stanford",
                            "neuralink", "ted", "dealbook", "grok", "xai"],
    },
    {
        "name": "Energy, Climate, and Sustainable Civilization",
        "slug": "energy_climate",
        "source_keywords": ["selfish_gene", "what_we_owe_future", "wealth_of_nations", "screw_business",
                            "ted", "cop21", "solar", "battery", "tesla", "powerwall", "rainn_wilson",
                            "sal_khan", "master_plan"],
    },
    {
        "name": "Manufacturing, Engineering, and Physical Reality",
        "slug": "manufacturing_engineering",
        "source_keywords": ["ignition", "structures", "tim_dodd", "starship", "tesla_factory",
                            "investor_day", "mkbhd", "ai_day", "raptor", "megacast"],
    },
    {
        "name": "Company Building and Scaling",
        "slug": "company_building",
        "source_keywords": ["zero_to_one", "masters_of_doom", "steve_jobs", "screw_business",
                            "stanford", "yc", "motley_fool", "sxsw", "auto_bild", "2003", "paypal",
                            "entrepreneur"],
    },
    {
        "name": "Leadership, Teams, and Organizational Design",
        "slug": "leadership_teams",
        "source_keywords": ["steve_jobs", "benjamin_franklin", "masters_of_doom", "on_war", "art_of_war",
                            "investor_day", "pando", "chm", "time_person"],
    },
    {
        "name": "Motivation, Meaning, and Existential Purpose",
        "slug": "motivation_meaning",
        "source_keywords": ["mans_search_meaning", "hitchhikers_guide", "waiting_for_godot",
                            "fault_in_our_stars", "caltech", "usc", "commencement", "rainn",
                            "fox_news", "young_people"],
    },
    {
        "name": "Learning, Mental Models, and How to Think",
        "slug": "learning_mental_models",
        "source_keywords": ["foundation", "kevin_rose", "sxsw", "charlie_rose", "baron", "ted",
                            "skeptics_guide", "lessons_of_history", "selfish_gene", "stanford"],
    },
    {
        "name": "History, Civilization Cycles, and Lessons",
        "slug": "history_civilization",
        "source_keywords": ["lessons_of_history", "iliad", "decline_fall_rome", "storm_of_steel",
                            "on_war", "wages_of_destruction", "fifteen_battles", "art_of_war",
                            "benjamin_franklin", "explore_create", "dan_carlin"],
    },
    {
        "name": "Fiction and the Books That Shaped Elon's Vision",
        "slug": "fiction_vision",
        "source_keywords": ["dune", "hitchhikers_guide", "lord_of_the_rings", "atlas_shrugged",
                            "moon_harsh_mistress", "stranger_strange_land", "machine_stops",
                            "game_of_thrones", "waiting_for_godot", "fault_in_our_stars"],
    },
    {
        "name": "Risk, Failure, Resilience, and Recovery",
        "slug": "risk_failure",
        "source_keywords": ["masters_of_doom", "steve_jobs", "mans_search_meaning", "storm_of_steel",
                            "starship", "spacex", "paypal", "third_row", "director", "tim_dodd"],
    },
    {
        "name": "Science, Curiosity, and the Nature of Reality",
        "slug": "science_curiosity",
        "source_keywords": ["selfish_gene", "skeptics_guide", "fermi_paradox", "what_we_owe_future",
                            "life_3_0", "deep_learning", "aliens", "smithsonian", "lex_fridman"],
    },
    {
        "name": "Economics, Wealth, and Capital Allocation",
        "slug": "economics_wealth",
        "source_keywords": ["wealth_of_nations", "zero_to_one", "screw_business", "whats_our_problem",
                            "masters_of_doom", "baron", "motley_fool", "robin_li", "bill_gates"],
    },
    {
        "name": "Truth, Communication, and Fighting Narrative Capture",
        "slug": "truth_communication",
        "source_keywords": ["lying", "parasitic_mind", "whats_our_problem", "woman_makes_plan",
                            "dealbook", "bill_maher", "time_person", "twitter", "x_algorithm",
                            "free_speech", "adl"],
    },
]

THIRD_ORDER_PROMPT = """You are building the deepest layer of MindMusk's knowledge base. You are synthesizing across multiple sources to reveal how Elon's mind works on a specific theme.

Theme: "{theme_name}"

Below are the second-order synthesis documents for all sources relevant to this theme. Your job is to synthesize ACROSS all of them to reveal how this theme runs through Elon's entire thinking.

Write a document titled "Elon's Mind on {theme_name}". Include ALL of these sections:

## 1. THE CORE BELIEF
What does Elon fundamentally believe about this theme? 2-3 paragraphs, no hedging. His actual position.

## 2. THE INTELLECTUAL LINEAGE
Which books, ideas, and thinkers shaped his view? Show the chain: "He read X, which gave him Y, which showed up in Z decision."

## 3. THE MENTAL FRAMEWORK
What is his operating framework for this theme? When he faces decisions here, what does he ask? What does he optimize for? What won't he trade off?

## 4. HOW IT SHOWS UP IN HIS COMPANIES
At least 8 specific examples — products, decisions, quotes, public statements from Tesla, SpaceX, Neuralink, X.

## 5. WHAT ELON HAS SAID (DIRECT QUOTES)
10-15 most powerful things Elon has said about this theme. Verbatim.

## 6. WHERE HE IS CONTRARIAN
How does his view differ from conventional wisdom? Where do most people get it wrong?

## 7. THE SOCRATIC QUESTIONS HE WOULD ASK
5-7 questions Elon would ask someone who came to him with a problem in this domain.

## 8. THE SYNTHESIS INSIGHT
What insight only becomes visible when you look at ALL sources together?

Write at maximum density. Every sentence should be signal.

--- RELEVANT SECOND-ORDER DOCUMENTS ---

{content}"""


def get_relevant_sources(theme: dict) -> str:
    all_files = list(SECOND_ORDER_DIR.glob("*.md"))
    keywords = [kw.lower() for kw in theme["source_keywords"]]

    matched = []
    for f in all_files:
        fname_lower = f.stem.lower()
        if any(kw in fname_lower for kw in keywords):
            matched.append(f)

    # If fewer than 5 matches, include all files (fallback)
    if len(matched) < 5:
        matched = all_files[:20]

    print(f"    Matched {len(matched)} sources")

    combined = []
    total_chars = 0
    for f in matched:
        content = f.read_text(encoding="utf-8")
        header = f"\n\n{'='*60}\nSOURCE: {f.stem}\n{'='*60}\n\n"
        addition = header + content[:8000]
        if total_chars + len(addition) < MAX_CONTEXT:
            combined.append(addition)
            total_chars += len(addition)
        else:
            combined.append(header + content[:3000] + "\n[...truncated...]")

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
                wait = 45 * (attempt + 1)
                print(f"      Waiting {wait}s...")
                time.sleep(wait)
            else:
                if attempt == 4:
                    raise
                time.sleep(10)
    return ""


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 3: Generating 15 Third-Order Thematic Syntheses")
    print("=" * 60)

    for i, theme in enumerate(THEMES):
        out_path = THIRD_ORDER_DIR / f"third_order_{theme['slug']}.md"

        if out_path.exists() and out_path.stat().st_size > 5000:
            print(f"[{i+1}/15] [SKIP] {theme['name']} — already done")
            continue

        print(f"\n[{i+1}/15] Generating: {theme['name']}")
        sources_content = get_relevant_sources(theme)
        prompt = THIRD_ORDER_PROMPT.format(
            theme_name=theme["name"],
            content=sources_content
        )
        synthesis = call_claude(prompt)

        if not synthesis:
            print(f"  [ERROR] Failed for {theme['name']}")
            continue

        output = f"# Elon's Mind on {theme['name']}\n**Slug**: {theme['slug']}\n**Layer**: third_order\n\n---\n\n{synthesis}"
        out_path.write_text(output, encoding="utf-8")
        size_kb = out_path.stat().st_size // 1024
        print(f"  [DONE] {theme['name']} — {size_kb} KB")

    third_files = list(THIRD_ORDER_DIR.glob("*.md"))
    print(f"\n\nPhase 3 Complete. {len(third_files)}/15 theme documents generated.")
