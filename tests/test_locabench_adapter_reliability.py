import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from benchmarks.adapter import EnvContext, EvalResult
from benchmarks.adapter_locabench import (
    LOCA_NATIVE_CONTRACT_PATH,
    LOCABenchAdapter,
    _ensure_email_accounts,
    _ensure_native_contract_skeleton,
    _native_contract_skeleton,
    _validate_native_contract,
)


def test_native_contract_skeleton_is_empty_and_task_visible_only():
    contract = _native_contract_skeleton(
        task_name="CanvasListTestS2LEnv",
        context_level="96k",
        execution_mode="native_mcp",
        tool_catalog=[{"name": "canvas_list", "description": "List courses"}],
    )

    assert contract["contract_id"] == "loca_native_task_contract_v1"
    assert contract["contract_path"] == LOCA_NATIVE_CONTRACT_PATH
    assert contract["status"] == "draft"
    assert contract["authoritative_sources"] == []
    assert contract["selection"]["target_count"] is None
    assert contract["artifacts"] == []
    assert contract["mutations"] == []
    assert contract["completion_gate"]["ready"] is False
    assert contract["available_service_capabilities"] == [{
        "name": "canvas_list",
        "description": "List courses",
    }]


def test_native_contract_skeleton_does_not_overwrite_progress(tmp_path: Path):
    path = _ensure_native_contract_skeleton(
        tmp_path,
        task_name="TaskA",
        context_level="96k",
        execution_mode="native_mcp",
        tool_catalog=[],
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["status"] = "resolved"
    path.write_text(json.dumps(payload), encoding="utf-8")

    second = _ensure_native_contract_skeleton(
        tmp_path,
        task_name="TaskB",
        context_level="128k",
        execution_mode="local_db_fallback",
        tool_catalog=[],
    )

    assert second == path
    assert json.loads(path.read_text(encoding="utf-8"))["status"] == "resolved"


def test_native_contract_validation_blocks_unverified_mutations(tmp_path: Path):
    path = tmp_path / "native_contract.json"
    payload = _native_contract_skeleton(
        task_name="ApplyPhDEmailS2LEnv",
        context_level="96k",
        execution_mode="native_mcp",
        tool_catalog=[],
    )
    payload["status"] = "resolved"
    payload["selection"]["coverage_status"] = "complete"
    payload["completion_gate"].update({
        "contract_resolved": True,
        "source_coverage_complete": True,
        "selection_reconciled": True,
        "artifacts_verified": True,
        "mutations_read_back": False,
        "no_pending_or_unverified_items": True,
        "ready": True,
    })
    payload["mutations"] = [{"target": "recipient-1"}]
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = _validate_native_contract(path)

    assert result["valid"] is False
    assert any("mutations_read_back" in issue for issue in result["issues"])


def test_native_contract_validation_accepts_completed_read_only_contract(tmp_path: Path):
    path = tmp_path / "native_contract.json"
    payload = _native_contract_skeleton(
        task_name="CanvasListTestS2LEnv",
        context_level="96k",
        execution_mode="native_mcp",
        tool_catalog=[],
    )
    payload["status"] = "completed"
    payload["selection"]["coverage_status"] = "complete"
    payload["completion_gate"].update({
        "contract_resolved": True,
        "source_coverage_complete": True,
        "selection_reconciled": True,
        "no_pending_or_unverified_items": True,
        "ready": True,
    })
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert _validate_native_contract(path)["valid"] is True


def test_locabench_prompt_and_execution_policy_are_contract_first(tmp_path: Path):
    adapter = LOCABenchAdapter()
    item = {
        "_task_name": "TaskA",
        "_context_level": "96k",
        "_task_instruction": "Produce the required native result.",
        "_tool_catalog": [{"name": "service_list", "description": "List records"}],
        "_execution_mode": "native_mcp",
    }
    task = adapter.build_task(
        item,
        SimpleNamespace(workspace=tmp_path),
        [],
    )
    policy = adapter.execution_policy(item)

    assert LOCA_NATIVE_CONTRACT_PATH in task
    assert "authoritative Runtime\nSubmission Protocol" in task
    assert "call `set_final_output`" not in task
    assert "version=\"2\"" not in task
    assert policy.version == "2"
    assert any(LOCA_NATIVE_CONTRACT_PATH in rule for rule in policy.artifact_requirements)
    assert "context_analyst" in policy.role_instructions
    assert "evidence_reader" in policy.role_instructions
    assert "artifact_handler" in policy.role_instructions
    assert "controlled_operator" in policy.role_instructions


def test_ensure_email_accounts_provisions_mcp_and_task_sender(tmp_path: Path):
    task_dir = tmp_path / "task"
    task_dir.mkdir()
    (task_dir / "emails_config.json").write_text(
        json.dumps({
            "email": "sender@example.com",
            "password": "sender-pass",
            "name": "Configured Sender",
        }),
        encoding="utf-8",
    )
    config = {
        "mcp_servers": {
            "email": {
                "enabled": True,
                "params": {
                    "data_dir": "{task_workspace}/local_db/emails",
                    "email": "mcp-login@example.com",
                    "password": "mcp-pass",
                },
            },
        },
    }

    report = _ensure_email_accounts(config, task_dir)

    users_path = task_dir / "local_db" / "emails" / "users.json"
    users = json.loads(users_path.read_text(encoding="utf-8"))
    assert users["mcp-login@example.com"]["password"] == "mcp-pass"
    assert users["sender@example.com"]["password"] == "sender-pass"
    assert {entry["email"] for entry in report} == {
        "mcp-login@example.com",
        "sender@example.com",
    }
    for email in ("mcp-login@example.com", "sender@example.com"):
        mailbox = task_dir / "local_db" / "emails" / "users_data" / email
        assert (mailbox / "emails.json").is_file()
        assert (mailbox / "folders.json").is_file()
        assert (mailbox / "drafts.json").is_file()


def test_fatal_mcp_result_is_recorded_without_overriding_evaluation(tmp_path: Path):
    (tmp_path / "events.jsonl").write_text(
        json.dumps({
            "type": "tool.result",
            "data": {"output": "[FATAL MCP ERROR] session closed unexpectedly"},
        }) + "\n",
        encoding="utf-8",
    )
    item = {
        "_cached_eval": EvalResult(
            success=False,
            score=0.0,
            summary="reward=0.0 (FAIL)",
        ),
    }

    LOCABenchAdapter().post_process(
        item,
        SimpleNamespace(dir=tmp_path),
        EnvContext(data={}),
    )
    assert item["_completion_protocol"] == {
        "set_final_output": False,
        "finalize_task": False,
        "finalization_tool": None,
        "final_output_submitted": False,
        "terminate": False,
        "runner_end": False,
        "complete_handshake": False,
    }


def test_successful_fallback_may_evolve_after_fatal_mcp(tmp_path: Path):
    (tmp_path / "events.jsonl").write_text(
        "[FATAL MCP ERROR] session closed unexpectedly\n",
        encoding="utf-8",
    )
    item = {
        "_cached_eval": EvalResult(
            success=True,
            score=1.0,
            summary="reward=1.0 (PASS)",
        ),
    }

    LOCABenchAdapter().post_process(
        item,
        SimpleNamespace(dir=tmp_path),
        EnvContext(data={}),
    )
