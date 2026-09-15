from __future__ import annotations

from types import SimpleNamespace

import pytest

from core.evolution_models import TeamReflectionDecision, TemplateMember
from core.team_selector import TeamSelectionContext
from core.team_selector_test import LLMTeamSelector
from core.template_registry import TemplateRegistry


def _registry() -> TemplateRegistry:
    registry = TemplateRegistry()
    registry.apply_reflection(
        TeamReflectionDecision(
            action="create",
            family_id="research",
            family_description="External evidence tasks",
            reason="seed",
            members=[TemplateMember("web", "researcher")],
        ),
        task_id="seed",
        known_agent_ids={"chairman", "web"},
    )
    return registry


@pytest.mark.asyncio
async def test_experimental_selector_treats_members_as_an_eligible_roster():
    captured = []

    async def completion(**kwargs):
        captured.append(kwargs["messages"])
        return SimpleNamespace(choices=[SimpleNamespace(
            message=SimpleNamespace(tool_calls=[{
                "id": "call_1",
                "function": {
                    "name": "select_template_family",
                    "arguments": {
                        "family_action": "reuse",
                        "family_id": "research",
                    },
                },
            }]),
        )])

    selector = LLMTeamSelector(
        model="test", registry=_registry(), completion=completion,
    )
    await selector.select(TeamSelectionContext(
        raw_task="Find a fact with a source.",
        chairman_id="chairman",
        template_catalog=selector.registry.catalog(),
    ))

    system_prompt = captured[0][0]["content"]
    user_prompt = captured[0][1]["content"]
    assert "evidence or reasoning requirements" in system_prompt
    assert "eligible capability roster, not a required workflow" in system_prompt
    assert "any subset of them" in system_prompt
    assert "specialist roles" not in system_prompt
    assert "Otherwise choose cold_start" in user_prompt
