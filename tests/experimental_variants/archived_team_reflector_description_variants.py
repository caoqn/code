from __future__ import annotations

from core.team_reflector import LLMTeamReflector as BaselineTeamReflector
from core.team_reflector_test import LLMTeamReflector as ExperimentalTeamReflector


def _system_prompt(reflector_cls) -> str:
    """Capture the static system prompt without making a model request."""
    source = reflector_cls.reflect.__code__.co_consts
    return " ".join(item for item in source if isinstance(item, str))


def test_experimental_description_prompt_removes_member_division_requirement() -> None:
    baseline_prompt = _system_prompt(BaselineTeamReflector)
    experimental_prompt = _system_prompt(ExperimentalTeamReflector)

    assert "how the members complement one another" in baseline_prompt
    assert "complementary member roles" in baseline_prompt
    assert "how the members complement one another" not in experimental_prompt
    assert "complementary member roles" not in experimental_prompt
    assert "without naming members, role divisions" in experimental_prompt
