from __future__ import annotations

import asyncio
from types import SimpleNamespace
import yaml
import pytest

from core.runner import Runner
from core.output_contract import GAIA_OUTPUT_CONTRACT, output_contract_from_name
from core.reflection_persistence import persist_reflection_to_source
from tools.primitives import REFLECTION_TOOL_NAMES, rebuild_primitive_schemas


def _pool(tmp_path, *, with_answer_agent=False):
    names = ["chairman", "worker_a", "worker_b"]
    if with_answer_agent:
        names.append("answer_agent")
    for name in names:
        agent_dir = tmp_path / name
        agent_dir.mkdir()
        (agent_dir / "config.yaml").write_text(
            yaml.safe_dump(
                {
                    "name": name,
                    "role": "worker",
                    "description": name,
                    "model": "test",
                    "tools": [],
                }
            ),
            encoding="utf-8",
        )
        (agent_dir / "prompt.md").write_text("test", encoding="utf-8")
    return tmp_path


def test_selected_team_is_the_only_recruitable_pool_view(tmp_path):
    pool = _pool(tmp_path)
    runner = Runner(
        pool_dir=pool,
        chairman_name="chairman",
        allowed_agent_ids={"worker_a"},
    )
    assert [row["name"] for row in runner.list_pool_agents()] == ["worker_a"]
    with pytest.raises(PermissionError):
        runner.load_agent_from_pool("worker_b")


def test_chairman_profile_is_scoped_to_selected_family(tmp_path):
    pool = _pool(tmp_path)
    profile_dir = pool / "chairman" / "evolution"
    profile_dir.mkdir()
    (profile_dir / "teammate_profiles.yaml").write_text(
        "worker_a:\n  strengths:\n    - selected\n"
        "worker_b:\n  strengths:\n    - outside-family\n",
        encoding="utf-8",
    )
    runner = Runner(
        pool_dir=pool,
        chairman_name="chairman",
        allowed_agent_ids={"worker_a"},
        teammate_profiles_enabled=True,
    )

    chairman = runner.load_agent_from_pool("chairman")

    assert "worker_a" in chairman.teammate_profiles
    assert "selected" in chairman.teammate_profiles
    assert "worker_b" not in chairman.teammate_profiles
    assert "outside-family" not in chairman.teammate_profiles
    assert [row["name"] for row in runner.list_pool_agents()] == ["worker_a"]
    assert runner.allowed_agent_ids == frozenset({"worker_a"})


def test_recruited_agent_gets_peer_but_not_own_family_profile(tmp_path):
    pool = _pool(tmp_path)
    (pool / "chairman" / "evolution").mkdir()
    (pool / "worker_b" / "evolution").mkdir()
    (pool / "chairman" / "evolution" / "teammate_profiles.yaml").write_text(
        "worker_a:\n"
        "  reliability: high\n"
        "  strengths:\n"
        "    - chairman-observed\n"
        "worker_b:\n"
        "  strengths:\n"
        "    - peer-b\n",
        encoding="utf-8",
    )
    (pool / "worker_b" / "evolution" / "teammate_profiles.yaml").write_text(
        "worker_a:\n"
        "  weaknesses:\n"
        "    - peer-observed\n",
        encoding="utf-8",
    )
    runner = Runner(
        pool_dir=pool,
        chairman_name="chairman",
        allowed_agent_ids={"worker_a", "worker_b"},
        teammate_profiles_enabled=True,
    )

    worker = runner.load_agent_from_pool("worker_a")

    assert "Your current family profile" not in worker.teammate_profiles
    assert "chairman-observed" not in worker.teammate_profiles
    assert "peer-observed" not in worker.teammate_profiles
    assert "Relevant profiles for other selected family members" in worker.teammate_profiles
    assert "worker_b" in worker.teammate_profiles
    assert "peer-b" in worker.teammate_profiles
    assert runner.allowed_agent_ids == frozenset({"worker_a", "worker_b"})


def test_chairman_only_profiles_hide_all_profiles_from_execution_members(tmp_path):
    pool = _pool(tmp_path)
    (pool / "chairman" / "evolution").mkdir()
    (pool / "worker_a" / "evolution").mkdir()
    (pool / "chairman" / "evolution" / "teammate_profiles.yaml").write_text(
        "worker_a:\n  strengths:\n    - strong evidence synthesis\n",
        encoding="utf-8",
    )
    (pool / "worker_a" / "evolution" / "teammate_profiles.yaml").write_text(
        "worker_b:\n  strengths:\n    - legacy worker observation\n",
        encoding="utf-8",
    )
    runner = Runner(
        pool_dir=pool,
        chairman_name="chairman",
        allowed_agent_ids={"worker_a", "worker_b"},
        chairman_teammate_profiles_enabled=True,
        member_teammate_profiles_enabled=False,
    )

    chairman = runner.load_agent_from_pool("chairman")
    worker = runner.load_agent_from_pool("worker_a")

    assert "strong evidence synthesis" in chairman.teammate_profiles
    assert worker.teammate_profiles == ""
    assert "## Teammate Profiles" not in worker.build_system_prompt()


def test_chairman_only_policy_does_not_load_worker_profile_file(tmp_path, monkeypatch):
    pool = _pool(tmp_path)
    profile_dir = pool / "worker_a" / "evolution"
    profile_dir.mkdir()
    (profile_dir / "teammate_profiles.yaml").write_text(
        "chairman:\n  strengths:\n    - stale worker memory\n",
        encoding="utf-8",
    )

    import core.agent as agent_module

    original_loader = agent_module.load_teammate_profiles
    loaded_dirs: list[str] = []

    def tracked_loader(agent_dir: str) -> str:
        loaded_dirs.append(agent_dir)
        return original_loader(agent_dir)

    monkeypatch.setattr(agent_module, "load_teammate_profiles", tracked_loader)
    runner = Runner(
        pool_dir=pool,
        chairman_name="chairman",
        chairman_teammate_profiles_enabled=True,
        member_teammate_profiles_enabled=False,
    )

    worker = runner.load_agent_from_pool("worker_a")

    assert worker.teammate_profiles == ""
    assert str(pool / "worker_a") not in loaded_dirs


def test_chairman_receives_and_can_select_its_outgoing_handoff_rules(tmp_path):
    rule = {
        "rule_id": "research_handoff",
        "from_agent": "chairman",
        "to_agent": "worker_a",
        "trigger_description": "Use when cited web research is needed.",
        "instruction": "Return source-backed findings.",
    }
    runner = Runner(
        pool_dir=_pool(tmp_path),
        chairman_name="chairman",
        team_selection_metadata={"handoff_rules": [rule]},
    )
    chairman = runner.load_agent_from_pool("chairman")
    worker = runner.load_agent_from_pool("worker_a")
    runner.agents = {"chairman": chairman, "worker_a": worker}
    chairman.bind_message_store(runner.message_store)
    worker.bind_message_store(runner.message_store)
    chairman._runner_ref = runner
    worker._runner_ref = runner

    send_schema = next(
        item["function"] for item in chairman._build_messaging_schemas()
        if item["function"]["name"] == "send_message"
    )
    rule_ids = send_schema["parameters"]["properties"]["handoff_rule_id"]["enum"]

    assert rule_ids == ["research_handoff", "NONE"]
    assert "research_handoff" in runner._build_chairman_context()
    assert "worker_a" in runner._build_chairman_context()


def test_chairman_only_l2_exposes_profile_tools_only_to_chairman(tmp_path):
    runner = Runner(
        pool_dir=_pool(tmp_path),
        chairman_name="chairman",
        enable_reflection=True,
        chairman_teammate_profiles_enabled=True,
        member_teammate_profiles_enabled=False,
    )
    chairman = runner.load_agent_from_pool("chairman")
    worker = runner.load_agent_from_pool("worker_a")
    runner.agents = {"chairman": chairman, "worker_a": worker}
    runner._recruited_agent_ids = ["worker_a"]
    runner._l2_reflection_agents = runner.l2_reflection_agents()
    runner._phase = "l2_reflection"

    chairman_schemas = rebuild_primitive_schemas(
        runner, agent_name="chairman",
    )
    worker_schemas = rebuild_primitive_schemas(
        runner, include_chairman_tools=False, agent_name="worker_a",
    )
    chairman_profile_schema = next(
        item["function"] for item in chairman_schemas
        if item["function"]["name"] == "update_teammate_profile"
    )

    assert chairman_profile_schema["parameters"]["properties"]["teammate_name"]["enum"] == [
        "worker_a"
    ]
    assert "update_teammate_profile" not in {
        item["function"]["name"] for item in worker_schemas
    }


def test_chairman_only_profile_persistence_ignores_worker_profile_artifacts(tmp_path):
    session = tmp_path / "session"
    source = tmp_path / "source"
    for root in (session, source):
        for name in ("chairman", "worker_a"):
            agent_dir = root / name
            agent_dir.mkdir(parents=True)
            (agent_dir / "config.yaml").write_text(f"name: {name}\n", encoding="utf-8")
    for name, strength in (("chairman", "new-chairman-observation"), ("worker_a", "worker-write")):
        evolution = session / name / "evolution"
        evolution.mkdir()
        (evolution / "teammate_profiles.yaml").write_text(
            f"worker_a:\n  strengths:\n    - {strength}\n", encoding="utf-8",
        )

    modified = persist_reflection_to_source(
        session,
        source,
        include_teammate_profiles=True,
        teammate_profile_agent_ids={"chairman"},
    )

    chairman_profile = (
        source / "chairman" / "evolution" / "teammate_profiles.yaml"
    )
    assert chairman_profile.exists()
    assert "new-chairman-observation" in chairman_profile.read_text(encoding="utf-8")
    assert not (source / "worker_a" / "evolution" / "teammate_profiles.yaml").exists()
    assert modified == ["chairman/evolution/teammate_profiles.yaml"]


def test_chairman_only_persistence_clears_legacy_worker_profile(tmp_path):
    session = tmp_path / "session"
    source = tmp_path / "source"
    for root in (session, source):
        for name in ("chairman", "worker_a"):
            agent_dir = root / name
            agent_dir.mkdir(parents=True)
            (agent_dir / "config.yaml").write_text(f"name: {name}\n", encoding="utf-8")
    stale_profile = source / "worker_a" / "evolution" / "teammate_profiles.yaml"
    stale_profile.parent.mkdir()
    stale_profile.write_text("chairman:\n  notes:\n    - legacy\n", encoding="utf-8")

    modified = persist_reflection_to_source(
        session,
        source,
        include_teammate_profiles=True,
        teammate_profile_agent_ids={"chairman"},
    )

    assert not stale_profile.exists()
    assert modified == ["worker_a/evolution/teammate_profiles.yaml (cleared)"]


def test_unrestricted_runner_preserves_legacy_pool_visibility(tmp_path):
    runner = Runner(pool_dir=_pool(tmp_path), chairman_name="chairman")
    assert [row["name"] for row in runner.list_pool_agents()] == [
        "worker_a",
        "worker_b",
    ]


def test_stopped_agent_remains_in_append_only_usage_history(tmp_path):
    runner = Runner(pool_dir=_pool(tmp_path), chairman_name="chairman")

    async def exercise():
        chairman = runner.load_agent_from_pool("chairman")
        runner.agents["chairman"] = chairman
        runner._record_agent_participation("chairman", recruited=False)

        worker = runner.load_agent_from_pool("worker_a")
        runner.start_agent(worker, cwd=str(tmp_path))
        assert runner.stop_agent("worker_a") is True
        await asyncio.sleep(0)

    asyncio.run(exercise())
    usage = runner._agent_usage_snapshot()
    assert usage == {
        "agents_used": ["chairman", "worker_a"],
        "recruited_agent_ids": ["worker_a"],
        "active_agent_ids": ["chairman"],
        "stopped_agent_ids": ["worker_a"],
    }


def test_global_answer_service_is_not_counted_as_recruited_member(tmp_path):
    runner = Runner(
        pool_dir=_pool(tmp_path, with_answer_agent=True),
        chairman_name="chairman",
        output_contract=GAIA_OUTPUT_CONTRACT,
    )

    async def exercise():
        answer_agent = runner.load_agent_from_pool("answer_agent")
        runner.start_agent(answer_agent, cwd=str(tmp_path), global_service=True)
        await asyncio.sleep(0)

    asyncio.run(exercise())
    usage = runner._agent_usage_snapshot()
    assert usage["agents_used"] == ["answer_agent"]
    assert usage["recruited_agent_ids"] == []
    assert usage["active_agent_ids"] == ["answer_agent"]


def test_final_output_is_locked_before_reflection(tmp_path):
    runner = Runner(pool_dir=_pool(tmp_path), chairman_name="chairman")

    async def exercise():
        assert await runner.set_final_output("FINAL ANSWER: 17") == "Output recorded successfully."
        runner._phase = "l1_reflection"
        message = await runner.set_final_output("reflection prose")
        assert "locked" in message

    asyncio.run(exercise())
    assert runner._result == "FINAL ANSWER: 17"


def test_chairman_context_has_one_mode_specific_submission_protocol(tmp_path):
    pool = _pool(tmp_path)
    eval_context = Runner(
        pool_dir=pool, chairman_name="chairman", enable_reflection=False,
        output_contract=GAIA_OUTPUT_CONTRACT,
    )._build_chairman_context()
    evolve_context = Runner(
        pool_dir=pool, chairman_name="chairman", enable_reflection=True,
        output_contract=GAIA_OUTPUT_CONTRACT,
    )._build_chairman_context()

    assert "Call exactly `set_final_output(output=<final output>)`" in eval_context
    assert "Do not call `finalize_task` in this run." in eval_context
    assert "Call exactly `finalize_task(output=<final output>)`" in evolve_context
    assert "Do not call `set_final_output` or `terminate` during task execution." in evolve_context


def test_worker_context_does_not_duplicate_l2_profiles(tmp_path):
    pool = _pool(tmp_path)
    profile_dir = pool / "worker_a" / "evolution"
    profile_dir.mkdir()
    (profile_dir / "teammate_profiles.yaml").write_text(
        "chairman:\n  reliability: high\n",
        encoding="utf-8",
    )
    runner = Runner(
        pool_dir=pool,
        chairman_name="chairman",
        teammate_profiles_enabled=True,
    )
    worker = runner.load_agent_from_pool("worker_a")

    assert worker.build_system_prompt().count("## Teammate Profiles") == 1
    assert "reliability: high" not in runner._build_agent_context(worker)


def test_teammate_profile_ablation_removes_prompt_and_skips_l2(tmp_path):
    pool = _pool(tmp_path)
    profile_dir = pool / "worker_a" / "evolution"
    profile_dir.mkdir()
    (profile_dir / "teammate_profiles.yaml").write_text(
        "chairman:\n  reliability: high\n",
        encoding="utf-8",
    )
    runner = Runner(
        pool_dir=pool,
        chairman_name="chairman",
        teammate_profiles_enabled=False,
    )

    worker = runner.load_agent_from_pool("worker_a")
    assert "## Teammate Profiles" not in worker.build_system_prompt()

    runner._phase = "l1_reflection"
    message = runner._auto_advance_phase("L1")
    assert runner._phase == "terminated"
    assert runner._done.is_set()
    assert "L2 teammate profiles are disabled" in message


def test_teammate_profiles_are_disabled_by_default(tmp_path):
    pool = _pool(tmp_path)
    profile_dir = pool / "worker_a" / "evolution"
    profile_dir.mkdir()
    (profile_dir / "teammate_profiles.yaml").write_text(
        "chairman:\n  reliability: high\n",
        encoding="utf-8",
    )

    runner = Runner(pool_dir=pool, chairman_name="chairman")
    worker = runner.load_agent_from_pool("worker_a")

    assert runner.teammate_profiles_enabled is False
    assert "## Teammate Profiles" not in worker.build_system_prompt()


def test_legacy_l3_tools_are_not_registered():
    assert REFLECTION_TOOL_NAMES.isdisjoint({
        "propose_reflection",
        "view_reflection",
        "view_current_config",
        "apply_reflection",
        "skip_reflection",
        "suggest_team_improvement",
        "skip_l3_reflection",
    })


def test_teammate_profile_ablation_does_not_persist_l2_artifact(tmp_path):
    session = tmp_path / "session"
    source = tmp_path / "source"
    for root in (session, source):
        agent_dir = root / "worker_a"
        agent_dir.mkdir(parents=True)
        (agent_dir / "config.yaml").write_text("name: worker_a\n", encoding="utf-8")

    evolution = session / "worker_a" / "evolution"
    evolution.mkdir()
    (evolution / "prompt_patches.md").write_text("keep L1\n", encoding="utf-8")
    (evolution / "teammate_profiles.yaml").write_text(
        "chairman:\n  reliability: high\n",
        encoding="utf-8",
    )

    modified = persist_reflection_to_source(
        session,
        source,
        include_teammate_profiles=False,
    )

    assert (source / "worker_a" / "evolution" / "prompt_patches.md").exists()
    assert not (source / "worker_a" / "evolution" / "teammate_profiles.yaml").exists()
    assert all("teammate_profiles" not in path for path in modified)


def test_emergency_finalization_uses_plain_completion_and_locks_output(tmp_path, monkeypatch):
    runner = Runner(
        pool_dir=_pool(tmp_path), chairman_name="chairman",
        output_contract=GAIA_OUTPUT_CONTRACT,
    )
    runner._forced_termination = "timeout"
    chairman = SimpleNamespace(
        config=SimpleNamespace(name="chairman", model="test", temperature=0, max_tokens=32),
        messages=[{"role": "system", "content": "system"}, {"role": "user", "content": "task"}],
    )
    runner.agents["chairman"] = chairman
    answer_agent = SimpleNamespace(
        config=SimpleNamespace(name="answer_agent", model="test", temperature=0, max_tokens=32),
        messages=[],
        build_system_prompt=lambda: "AnswerAgent system",
    )
    runner.agents["answer_agent"] = answer_agent
    captured = {}

    async def fake_complete(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="FINAL ANSWER: 17"))])

    monkeypatch.setattr("core.llm.complete", fake_complete)
    asyncio.run(runner._emergency_finalize_after_forced_termination())

    assert "tools" not in captured
    assert captured["messages"][0]["content"] == "AnswerAgent system"
    assert runner._result == "17"
    assert runner._final_output_locked is True
    assert runner._finalization_mode == "emergency"


def test_emergency_finalization_strips_tool_protocol_from_history(tmp_path, monkeypatch):
    runner = Runner(
        pool_dir=_pool(tmp_path), chairman_name="chairman",
        output_contract=GAIA_OUTPUT_CONTRACT,
    )
    runner._forced_termination = "timeout"
    chairman = SimpleNamespace(
        config=SimpleNamespace(name="chairman", model="test", temperature=0, max_tokens=32),
        messages=[
            {"role": "system", "content": "system"},
            {"role": "user", "content": "task"},
            {
                "role": "assistant",
                "content": "I will inspect the source.",
                "tool_calls": [{"id": "call_1", "function": {"name": "web", "arguments": "{}"}}],
            },
            {"role": "tool", "tool_call_id": "call_1", "content": "The answer is 17."},
        ],
    )
    runner.agents["chairman"] = chairman
    answer_agent = SimpleNamespace(
        config=SimpleNamespace(name="answer_agent", model="test", temperature=0, max_tokens=32),
        messages=[],
        build_system_prompt=lambda: "AnswerAgent system",
    )
    runner.agents["answer_agent"] = answer_agent
    captured = {}

    async def fake_complete(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="FINAL ANSWER: 17"))])

    monkeypatch.setattr("core.llm.complete", fake_complete)
    asyncio.run(runner._emergency_finalize_after_forced_termination())

    assert "tools" not in captured
    assert all(message["role"] != "tool" for message in captured["messages"])
    assert all("tool_calls" not in message for message in captured["messages"])
    assert any("Previously gathered tool result" in message["content"] for message in captured["messages"])
    assert runner._result == "17"


def test_emergency_finalization_rejects_explanatory_text(tmp_path, monkeypatch):
    runner = Runner(
        pool_dir=_pool(tmp_path), chairman_name="chairman",
        output_contract=GAIA_OUTPUT_CONTRACT,
    )
    runner._forced_termination = "timeout"
    chairman = SimpleNamespace(
        config=SimpleNamespace(name="chairman", model="test", temperature=0, max_tokens=32),
        messages=[{"role": "system", "content": "system"}, {"role": "user", "content": "task"}],
    )
    runner.agents["chairman"] = chairman
    answer_agent = SimpleNamespace(
        config=SimpleNamespace(name="answer_agent", model="test", temperature=0, max_tokens=32),
        messages=[],
        build_system_prompt=lambda: "AnswerAgent system",
    )
    runner.agents["answer_agent"] = answer_agent

    async def fake_complete(**kwargs):
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(
            content="Based on the evidence, the answer is 17.",
        ))])

    monkeypatch.setattr("core.llm.complete", fake_complete)
    asyncio.run(runner._emergency_finalize_after_forced_termination())

    assert runner._result is None
    assert runner._final_output_locked is False
    assert runner._finalization_mode == "none"


def test_non_gaia_emergency_finalization_accepts_tagged_multiline_output(tmp_path, monkeypatch):
    runner = Runner(
        pool_dir=_pool(tmp_path), chairman_name="chairman",
        output_contract=output_contract_from_name("deep_research_report"),
    )
    runner._forced_termination = "timeout"
    runner._task = "Write a report"
    runner.agents["chairman"] = SimpleNamespace(
        config=SimpleNamespace(name="chairman", model="test", temperature=0, max_tokens=32),
        messages=[{"role": "system", "content": "system"}, {"role": "user", "content": "task"}],
    )
    runner.agents["answer_agent"] = SimpleNamespace(
        config=SimpleNamespace(name="answer_agent", model="test", temperature=0, max_tokens=32),
        messages=[],
        build_system_prompt=lambda: "Research AnswerAgent system",
    )

    async def fake_complete(**kwargs):
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(
            content="FINAL OUTPUT:\n# Report\n\nConclusion.\nConfidence: 90%",
        ))])

    monkeypatch.setattr("core.llm.complete", fake_complete)
    asyncio.run(runner._emergency_finalize_after_forced_termination())

    assert runner._result == "# Report\n\nConclusion.\nConfidence: 90%"
    assert runner._finalization_mode == "emergency"


def test_global_answer_agent_is_not_recruitable_but_gates_normal_submission(tmp_path):
    runner = Runner(
        pool_dir=_pool(tmp_path, with_answer_agent=True),
        chairman_name="chairman",
        allowed_agent_ids={"worker_a"},
        output_contract=GAIA_OUTPUT_CONTRACT,
    )
    assert [row["name"] for row in runner.list_pool_agents()] == ["worker_a"]
    assert "AnswerAgent has not returned" in runner.validate_answer_agent_submission("17")
    runner.message_store.register("chairman")
    runner.message_store.send(
        sender="answer_agent", receiver="chairman", content="FINAL ANSWER: 17",
    )
    assert runner.validate_answer_agent_submission("17") is None
    assert "must equal AnswerAgent" in runner.validate_answer_agent_submission("FINAL ANSWER: 17")


def test_global_answer_agent_receives_a_task_length_idle_budget(tmp_path, monkeypatch):
    runner = Runner(
        pool_dir=_pool(tmp_path, with_answer_agent=True),
        chairman_name="chairman",
        max_seconds=900,
        idle_timeout=120,
        allowed_agent_ids={"worker_a"},
        output_contract=GAIA_OUTPUT_CONTRACT,
    )
    answer_agent = runner.load_agent_from_pool("answer_agent")
    captured = {}

    async def fake_run_loop(**kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(answer_agent, "run_loop", fake_run_loop)
    async def exercise():
        runner.start_agent(answer_agent, global_service=True)
        await asyncio.sleep(0)

    asyncio.run(exercise())
    assert captured["max_idle_rounds"] == 9


def test_generic_contract_neither_requires_answer_agent_nor_emergency_text(tmp_path, monkeypatch):
    runner = Runner(pool_dir=_pool(tmp_path), chairman_name="chairman")
    runner._forced_termination = "timeout"
    chairman = SimpleNamespace(
        config=SimpleNamespace(name="chairman", model="test", temperature=0, max_tokens=32),
        messages=[{"role": "system", "content": "system"}, {"role": "user", "content": "task"}],
    )
    runner.agents["chairman"] = chairman

    async def fail_if_called(**kwargs):
        raise AssertionError("generic benchmarks must not emergency-finalize text")

    monkeypatch.setattr("core.llm.complete", fail_if_called)
    asyncio.run(runner._emergency_finalize_after_forced_termination())

    assert runner.validate_answer_agent_submission("a complete report") is None
    assert runner._result is None
