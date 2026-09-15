from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from core.handoff_registry import HandoffRegistry
from core.evolution_models import HandoffDecision
from core.handoff_reflector import HandoffReflectionContext, LLMHandoffReflector
from core.handoff_registry import HandoffRegistry
from benchmarks.adapter import _handoff_participant_ids, _handoff_trace_batches


KNOWN = {"reader", "developer", "answer_agent"}


def test_chairman_handoffs_are_eligible_for_family_rule_reflection() -> None:
    pool = SimpleNamespace(chairman_name="chairman")
    result = SimpleNamespace(metadata={
        "recruited_agent_ids": ["context_analyst", "verifier"],
        "global_service_agent_ids": ["answer_agent"],
    })
    trace = [
        {"message_id": "m1", "from_agent": "chairman", "to_agent": "context_analyst"},
        {"message_id": "m2", "from_agent": "verifier", "to_agent": "chairman"},
        {"message_id": "m3", "from_agent": "answer_agent", "to_agent": "chairman"},
    ]

    participants = _handoff_participant_ids(pool, result)
    batches = _handoff_trace_batches(trace, participants)

    assert participants == ["chairman", "context_analyst", "verifier"]
    assert [[item["message_id"] for item in batch] for batch in batches] == [
        ["m1"], ["m2"],
    ]


def _decision(action: str, handoff_family_id: str, instruction: str) -> HandoffDecision:
    return HandoffDecision(
        action=action,
        handoff_family_id=handoff_family_id,
        from_agent="reader",
        to_agent="developer",
        reason="Evidence supports a reusable handoff contract",
        instruction=instruction,
        trigger_description="Use when evidence requires independent verification.",
        payload_schema={"summary": "string"},
        required_evidence=["source_context"],
        verification="Developer confirms the summary is actionable.",
        fallback="Request the missing source context once.",
        rule_id=(
            "rule_research" if handoff_family_id == "hf_research"
            else "rule_code"
        ),
    )


def test_same_agent_pair_can_have_rules_in_different_handoff_families() -> None:
    registry = HandoffRegistry()
    registry.apply_decision(
        _decision("create", "hf_research", "Send cited research evidence."),
        task_id="task_research",
        known_agent_ids=KNOWN,
        team_family_id="family_research",
    )
    registry.apply_decision(
        _decision("create", "hf_code_review", "Send a reproducible code diagnosis."),
        task_id="task_code",
        known_agent_ids=KNOWN,
        team_family_id="family_code",
    )

    assert registry.rules_for_team_family("family_research")[0].instruction == (
        "Send cited research evidence."
    )
    assert registry.rules_for_team_family("family_code")[0].instruction == (
        "Send a reproducible code diagnosis."
    )


def test_refine_preserves_handoff_version_history_and_round_trips(tmp_path) -> None:
    registry = HandoffRegistry()
    created = registry.apply_decision(
        _decision("create", "hf_research", "Send cited research evidence."),
        task_id="task_1",
        known_agent_ids=KNOWN,
        team_family_id="family_research",
    )
    assert created is not None

    refined = registry.apply_decision(
        _decision("refine", "hf_research", "Send cited evidence and unresolved ambiguity."),
        task_id="task_2",
        known_agent_ids=KNOWN,
        team_family_id="family_research",
    )
    assert refined is created
    assert refined.version == 2
    assert refined.version_history[0]["version"] == 1
    assert refined.version_history[0]["trigger_description"] == created.trigger_description
    assert refined.evidence_task_ids == ["task_1", "task_2"]

    path = tmp_path / "handoff_rules.json"
    registry.save(path)
    restored = HandoffRegistry.load(path)
    assert restored.handoff_family_for("family_research") == "hf_research"
    assert restored.list_rules()[0].version == 2
    assert restored.list_rules()[0].trigger_description == created.trigger_description


def test_normal_failure_evidence_is_persisted_with_the_affected_rule(tmp_path) -> None:
    registry = HandoffRegistry()
    created = _decision("create", "hf_research", "Send cited research evidence.")
    created.evidence["failure_evidence"] = {
        "task_id": "task_failed_1",
        "message_id": "msg_1",
        "from_agent": "reader",
        "to_agent": "developer",
        "score": 0.0,
        "evaluation_summary": "The final answer did not satisfy the task.",
    }
    rule = registry.apply_decision(
        created,
        task_id="task_failed_1",
        known_agent_ids=KNOWN,
        team_family_id="family_research",
    )
    assert rule is not None
    assert rule.failure_evidence[0]["message_id"] == "msg_1"
    assert rule.failure_evidence[0]["score"] == 0.0
    assert rule.failure_evidence[0]["recorded_at"]

    retained = _decision("retain", "hf_research", "")
    retained.evidence["failure_evidence"] = {
        "task_id": "task_failed_2",
        "message_id": "msg_2",
        "from_agent": "reader",
        "to_agent": "developer",
        "score": 0.5,
        "evaluation_summary": "Partial but insufficient result.",
    }
    registry.apply_decision(
        retained,
        task_id="task_failed_2",
        known_agent_ids=KNOWN,
        team_family_id="family_research",
    )
    assert [item["message_id"] for item in rule.failure_evidence] == ["msg_1", "msg_2"]

    path = tmp_path / "handoff_rules.json"
    registry.save(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 3
    restored = HandoffRegistry.load(path).list_rules()[0]
    assert [item["task_id"] for item in restored.failure_evidence] == [
        "task_failed_1",
        "task_failed_2",
    ]


def test_legacy_rule_load_gets_compatible_trigger_description(tmp_path) -> None:
    path = tmp_path / "legacy_handoff_rules.json"
    path.write_text(json.dumps({
        "schema_version": 2,
        "bindings": {"family_research": "hf_research"},
        "rules": [{
            "handoff_family_id": "hf_research",
            "from_agent": "reader",
            "to_agent": "developer",
            "version": 1,
            "instruction": "Send cited evidence.",
            "rule_id": "rule_research",
            "status": "active",
        }],
    }), encoding="utf-8")

    rule = HandoffRegistry.load(path).list_rules()[0]
    assert rule.trigger_description == "Use when this handoff is needed: Send cited evidence."


def test_create_does_not_fallback_to_random_rule_id() -> None:
    registry = HandoffRegistry()
    with pytest.raises(ValueError, match="handoff_rule_id"):
        registry.apply_decision(
            HandoffDecision(
                action="create",
                handoff_family_id="hf_research",
                from_agent="reader",
                to_agent="developer",
                reason="A reusable contract is needed",
                instruction="Send cited evidence.",
                trigger_description="Use when evidence requires verification.",
                rule_id="",
            ),
            task_id="task_missing_id",
            known_agent_ids=KNOWN,
            team_family_id="family_research",
        )


@pytest.mark.asyncio
async def test_handoff_reflector_receives_trace_and_allows_free_context_notes() -> None:
    seen = []

    async def completion(**kwargs):
        seen.append(kwargs["messages"])
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(
            tool_calls=[{
                "id": "call_1",
                "function": {
                    "name": "record_handoff_decision",
                    "arguments": {
                        "action": "create",
                        "rule_id": "rule_trace_notes",
                        "from_agent": "reader",
                        "to_agent": "developer",
                        "reason": "Keep ambiguity labels in the evidence packet",
                        "instruction": "Send confirmed evidence before open hypotheses.",
                        "trigger_description": "Use when multiple interpretations remain plausible.",
                        "payload_schema": {"confirmed": "array"},
                        "required_evidence": ["source_context"],
                        "verification": "Developer confirms the packet is actionable.",
                        "fallback": "Request the missing context.",
                        "context_notes": "Preserve alternative interpretations when wording is ambiguous.",
                    },
                },
            }]
        ))])

    reflector = LLMHandoffReflector(model="test", completion=completion)
    decision = await reflector.reflect(HandoffReflectionContext(
        task_id="task_1",
        team_family_id="family_research",
        handoff_family_id="hf_research",
        task="Research task",
        actual_agent_ids=["reader", "developer"],
        handoff_trace=[{
            "from_agent": "reader",
            "to_agent": "developer",
            "content": "Confirmed source and unresolved ambiguity",
        }],
    ))

    payload = json.loads(seen[0][1]["content"])
    assert payload["handoff_trace"][0]["from_agent"] == "reader"
    assert decision.context_notes.startswith("Preserve alternative")
    assert decision.trigger_description.startswith("Use when multiple")


@pytest.mark.asyncio
async def test_handoff_reflector_allows_no_update_without_invented_agent_pair() -> None:
    async def completion(**kwargs):
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(
            tool_calls=[{
                "id": "call_1",
                "function": {
                    "name": "record_handoff_decision",
                    "arguments": {
                        "action": "no_update",
                        "from_agent": "",
                        "to_agent": "",
                        "reason": "No meaningful inter-agent handoff occurred.",
                    },
                },
            }]
        ))])

    reflector = LLMHandoffReflector(model="test", completion=completion)
    decision = await reflector.reflect(HandoffReflectionContext(
        task_id="task_without_handoff",
        team_family_id="family_research",
        handoff_family_id="hf_research",
        task="Independent task",
        actual_agent_ids=["reader"],
    ))

    assert decision.action == "no_update"
    assert decision.from_agent == ""
    assert decision.to_agent == ""


def test_same_agent_pair_can_have_multiple_rules_and_retire_one() -> None:
    registry = HandoffRegistry()
    first = _decision("create", "hf_research", "Send source evidence.")
    second = HandoffDecision(
        action="create",
        handoff_family_id="hf_research",
        from_agent="reader",
        to_agent="developer",
        rule_id="rule_research_alt",
            reason="A separate evidence contract is useful for a different exchange.",
            instruction="Send competing interpretations and verification status.",
            trigger_description="Use when competing interpretations must be reconciled.",
        )
    registry.apply_decision(first, task_id="task_1", known_agent_ids=KNOWN,
                            team_family_id="family_research")
    registry.apply_decision(second, task_id="task_2", known_agent_ids=KNOWN,
                            team_family_id="family_research")

    assert len(registry.rules_for_team_family("family_research")) == 2
    retired = registry.apply_decision(
        HandoffDecision(
            action="retire",
            handoff_family_id="hf_research",
            from_agent="reader",
            to_agent="developer",
            rule_id="rule_research_alt",
            reason="The alternative contract is obsolete after a stable replacement.",
        ),
        task_id="task_3",
        known_agent_ids=KNOWN,
        team_family_id="family_research",
    )
    assert retired is not None and retired.status == "retired"
    assert [r.rule_id for r in registry.rules_for_team_family("family_research")] == [
        "rule_research"
    ]
