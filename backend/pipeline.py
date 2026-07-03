"""
RAG Pipeline: retrieves context chunks via Haiku, assembles prompt, streams response.
Called by the orchestrator with a reformulated query and layer weights.
"""

from typing import Generator
from backend.retriever import Retriever
from backend.llm.prompts import SYSTEM_PROMPT, build_context_block

MAX_HISTORY_TURNS = 6


def stream_response(
    user_message: str,
    history: list[dict],
    retriever: Retriever,
    anthropic_client,
    top_k: int = 3,
    threshold: float = 0.35,
) -> Generator[str, None, None]:
    """
    Retrieve relevant chunks, assemble prompt, stream text from claude-haiku-4-5.
    history: list of {role: "user"|"assistant", content: str}
    Yields raw text strings (caller adds SSE formatting).
    """
    chunks = retriever.retrieve(user_message, top_k=top_k, threshold=threshold)
    context_block = build_context_block(chunks)

    system = SYSTEM_PROMPT.rstrip()
    if context_block:
        system = system + "\n" + context_block

    recent_history = history[-(MAX_HISTORY_TURNS * 2):]
    messages = list(recent_history) + [{"role": "user", "content": user_message}]

    with anthropic_client.messages.stream(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=system,
        messages=messages,
    ) as stream:
        for event in stream:
            if event.type == "content_block_delta":
                text = getattr(event.delta, "text", "")
                if text:
                    yield text
