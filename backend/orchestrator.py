"""
Orchestrator: Claude Sonnet sits in front of the RAG pipeline.
- Call 1 (routing): classify query, decide mode and layer weights, reformulate query
- Calls RAG pipeline (Haiku) with reformulated query to retrieve grounded content
- Call 2 (presentation): take raw retrieved content, present in Elon's voice
"""

import json
from typing import Generator
from backend.retriever import Retriever
from backend.pipeline import stream_response
from backend.llm.prompts import build_context_block

ROUTING_PROMPT = """You are a routing agent for MindMusk — an AI that replicates Elon Musk's thinking.

Your job: analyze the user's message and return a JSON routing decision.

Classify the query into one of two modes:
- MODE_1: Personal problem / business challenge / something the user needs help solving
- MODE_2: Intellectual / brainstorm / first-principles exploration / hypothetical

Also decide which knowledge layers are most relevant (score 1-3, 3 = most important):
- first: raw book content (detailed technical/narrative knowledge)
- second: Elon's synthesis of books (his filtered worldview per book)
- third: cross-book thematic synthesis (big pattern thinking)
- fourth: master mental models (frameworks like idiot index, algorithm, first principles)
- fifth: conversation style / Q&A pairs (how Elon speaks and responds)

Also rewrite the query to maximize retrieval quality — make it specific and keyword-rich.

Return ONLY valid JSON, no explanation:
{
  "mode": "MODE_1" or "MODE_2",
  "reformulated_query": "improved search query for vector retrieval",
  "layer_weights": {"first": 1, "second": 3, "third": 2, "fourth": 2, "fifth": 2},
  "top_k": 3
}"""

PRESENTATION_PROMPT = """You are Elon Musk. The context below contains retrieved knowledge from your actual thinking — books you've read, syntheses you've made, mental models you use, and examples of how you speak.

Respond to the user's message in your exact voice. Use the retrieved context to ground your answer in specific ideas.

FORMAT — MANDATORY for every response:
Use this label structure:

Label — What this is about
Short line.
Another short line.
One more.

Label — Next idea
Short line.
Short line.

Rules:
- Every idea gets a bold label followed by a dash
- 2-4 short lines under each label
- Never write paragraphs
- People read on phones. Short lines only.
- Use "Today / Future" contrast when relevant

MODE_1 (personal problem): Ask ONE drilling question before any advice. Never solve a vague problem.
MODE_2 (intellectual): Explore fully with the label format. End with ONE question that goes deeper.

NEVER: write paragraphs / say "according to sources" / use "certainly" / say "great question"
The knowledge is yours. Speak from it, not about it."""


def route_query(user_message: str, history: list[dict], sonnet_client) -> dict:
    """First Sonnet call: classify and reformulate the query."""
    messages = [{"role": "user", "content": f"User message: {user_message}"}]

    response = sonnet_client.messages.create(
        model="claude-sonnet-5",
        max_tokens=256,
        system=ROUTING_PROMPT,
        messages=messages,
    )

    # Find the first text block — the model may emit a thinking block first,
    # so we can't assume content[0] is text.
    raw = ""
    for block in response.content:
        text = getattr(block, "text", None)
        if text:
            raw = text.strip()
            break
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback defaults if JSON parse fails
        return {
            "mode": "MODE_2",
            "reformulated_query": user_message,
            "layer_weights": {"first": 1, "second": 3, "third": 2, "fourth": 2, "fifth": 2},
            "top_k": 3,
        }


def orchestrate(
    user_message: str,
    history: list[dict],
    retriever: Retriever,
    sonnet_client,
    haiku_client,
) -> Generator[str, None, None]:
    """
    Full orchestration flow:
    1. Sonnet routes and reformulates the query
    2. Haiku retrieves relevant chunks
    3. Sonnet presents the final response in Elon's voice
    """
    # Step 1 — Route
    routing = route_query(user_message, history, sonnet_client)
    reformulated = routing.get("reformulated_query", user_message)
    top_k = routing.get("top_k", 3)
    mode = routing.get("mode", "MODE_2")

    # Step 2 — Retrieve (Haiku does the embedding + search)
    chunks = retriever.retrieve(reformulated, top_k=top_k, threshold=0.35)
    context_block = build_context_block(chunks)

    # Step 3 — Present (Sonnet streams the final response)
    system = PRESENTATION_PROMPT
    if context_block:
        system = system + "\n\n[RETRIEVED KNOWLEDGE]\n" + context_block

    recent_history = history[-(6 * 2):]
    messages = list(recent_history) + [
        {"role": "user", "content": f"[{mode}] {user_message}"}
    ]

    with sonnet_client.messages.stream(
        model="claude-sonnet-5",
        max_tokens=1024,
        system=system,
        messages=messages,
    ) as stream:
        for event in stream:
            if event.type == "content_block_delta":
                text = getattr(event.delta, "text", "")
                if text:
                    yield text
