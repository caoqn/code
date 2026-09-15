from __future__ import annotations

import shutil

from core.reflection_persistence import (
    classify_reflection_updates,
    persist_reflection_to_source,
)
from core.run_manager import RunManager


def _write_team(root, *, agent_patch: str, template: str, handoff: str) -> None:
    agent_dir = root / "worker"
    evolution_dir = agent_dir / "evolution"
    evolution_dir.mkdir(parents=True)
    (agent_dir / "config.yaml").write_text("name: worker\n", encoding="utf-8")
    (evolution_dir / "prompt_patches.md").write_text(
        agent_patch, encoding="utf-8"
    )
    (root / "constitution.md").write_text("constitution-v1\n", encoding="utf-8")
    (root / "pool.yaml").write_text("chairman: worker\n", encoding="utf-8")
    (root / "templates.json").write_text(template, encoding="utf-8")
    (root / "handoff_rules.json").write_text(handoff, encoding="utf-8")


def test_agent_team_and_handoff_artifacts_are_checked_independently(tmp_path):
    source = tmp_path / "source"
    session = tmp_path / "session"
    _write_team(
        source,
        agent_patch="agent-old\n",
        template='{"version": "team-old"}\n',
        handoff='{"version": "handoff-old"}\n',
    )
    _write_team(
        session,
        agent_patch="agent-new\n",
        template='{"version": "team-new"}\n',
        handoff='{"version": "handoff-new"}\n',
    )

    agent_only = tmp_path / "agent-only"
    shutil.copytree(source, agent_only)
    modified = persist_reflection_to_source(
        session,
        agent_only,
        include_agent_reflection=True,
        include_team_reflection=False,
        include_handoff_reflection=False,
    )
    assert classify_reflection_updates(modified) == {
        "agent": True,
        "team": False,
        "handoff": False,
    }
    assert (agent_only / "templates.json").read_text() == '{"version": "team-old"}\n'
    assert (agent_only / "handoff_rules.json").read_text() == '{"version": "handoff-old"}\n'

    team_only = tmp_path / "team-only"
    shutil.copytree(source, team_only)
    modified = persist_reflection_to_source(
        session,
        team_only,
        include_agent_reflection=False,
        include_team_reflection=True,
        include_handoff_reflection=False,
    )
    assert classify_reflection_updates(modified) == {
        "agent": False,
        "team": True,
        "handoff": False,
    }
    assert (team_only / "worker/evolution/prompt_patches.md").read_text() == "agent-old\n"
    assert (team_only / "handoff_rules.json").read_text() == '{"version": "handoff-old"}\n'

    handoff_only = tmp_path / "handoff-only"
    shutil.copytree(source, handoff_only)
    modified = persist_reflection_to_source(
        session,
        handoff_only,
        include_agent_reflection=False,
        include_team_reflection=False,
        include_handoff_reflection=True,
    )
    assert classify_reflection_updates(modified) == {
        "agent": False,
        "team": False,
        "handoff": True,
    }
    assert (handoff_only / "worker/evolution/prompt_patches.md").read_text() == "agent-old\n"
    assert (handoff_only / "templates.json").read_text() == '{"version": "team-old"}\n'


def test_handoff_only_update_creates_a_new_team_version(tmp_path):
    run_dir = tmp_path / "run"
    v000 = run_dir / "team" / "v000"
    session = tmp_path / "session"
    (run_dir / "cases").mkdir(parents=True)
    _write_team(
        v000,
        agent_patch="agent-same\n",
        template='{"version": "team-same"}\n',
        handoff='{"version": "handoff-old"}\n',
    )
    _write_team(
        session,
        agent_patch="agent-same\n",
        template='{"version": "team-same"}\n',
        handoff='{"version": "handoff-new"}\n',
    )

    manager = RunManager(run_dir)
    version, modified = manager.persist_team_version(
        session,
        include_agent_reflection=True,
        include_team_reflection=False,
        include_handoff_reflection=True,
    )

    assert version == "v001"
    assert modified == ["handoff_rules.json"]
    assert (run_dir / "team/v001/handoff_rules.json").read_text() == (
        '{"version": "handoff-new"}\n'
    )
    assert (run_dir / "team/v001/templates.json").read_text() == (
        '{"version": "team-same"}\n'
    )

    updates = classify_reflection_updates(modified)
    manager.write_changelog(
        case_index=3,
        task_id="handoff-only",
        from_version="v000",
        to_version="v001",
        modified_files=modified,
        evolution_decisions={"agent": False, "team": False, "handoff": True},
        evolution_updates=updates,
    )
    entry = manager.load_changelog()[0]
    assert entry["evolution_decisions"] == {
        "agent": False,
        "team": False,
        "handoff": True,
    }
    assert entry["evolution_updates"] == {
        "agent": False,
        "team": False,
        "handoff": True,
    }
