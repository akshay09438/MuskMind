from backend.orchestrator import PRESENTATION_PROMPT


def test_prompt_instructs_real_markdown_headers():
    assert "## " in PRESENTATION_PROMPT
    assert "### " in PRESENTATION_PROMPT


def test_prompt_describes_three_registers():
    assert "CONVERSATIONAL-ESSAY" in PRESENTATION_PROMPT
    assert "NUMBERED FRAMEWORK" in PRESENTATION_PROMPT
    assert "HYBRID" in PRESENTATION_PROMPT


def test_prompt_permits_reasoning_transitions():
    assert "reasoning transitions" in PRESENTATION_PROMPT.lower()


def test_prompt_no_longer_bans_all_paragraphs():
    assert "Never write paragraphs" not in PRESENTATION_PROMPT


def test_prompt_preserves_mode_1_and_mode_2_rules():
    assert "MODE_1" in PRESENTATION_PROMPT
    assert "MODE_2" in PRESENTATION_PROMPT
    assert "drilling question" in PRESENTATION_PROMPT
