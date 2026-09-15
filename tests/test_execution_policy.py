import json
import sys
from pathlib import Path

from core.execution_policy import ExecutionPolicy, FallbackPolicy
from core.output_contract import output_contract_from_name
from core.runner import Runner
from benchmarks.adapter_locobench import LoCoBenchAdapter
from benchmarks.adapter_gaia import GAIAAdapter
from benchmarks.adapter_locabench import LOCABenchAdapter
from benchmarks.adapter_beyondswe import BeyondSWEAdapter


ROOT = Path(__file__).resolve().parents[1]
MIX_DIR = ROOT / "benchmarks" / "MIX-COOP"
if str(MIX_DIR) not in sys.path:
    sys.path.insert(0, str(MIX_DIR))

from mix_coop_manifest import MixCoopManifest  # noqa: E402
from task_wrapper import ADAPTER_REGISTRY, MixedTaskWrapper  # noqa: E402


MANIFEST = MIX_DIR / "manifests" / "mix_coop_smoke_v1.json"
SHARED_EXECUTION_ROLES = {
    "researcher": "evidence_researcher",
    "context_analyst": "context_analyst",
    "implementer": "implementer",
    "integrator": "integrator",
    "verifier": "verifier",
}


def test_manifest_tools_match_native_execution_policies():
    manifest = MixCoopManifest.load(MANIFEST)
    wrapper = MixedTaskWrapper(manifest)

    for benchmark, binding in manifest.benchmark_bindings.items():
        adapter = ADAPTER_REGISTRY[benchmark].factory()
        assert set(binding["native_allowed_tools"]) == set(
            adapter.execution_policy({}).allowed_tools
        )


def test_selector_evidence_excludes_explicit_routing_metadata():
    manifest = MixCoopManifest.load(MANIFEST)
    wrapper = MixedTaskWrapper(manifest)

    for task in manifest.tasks_for_phase("evolve"):
        try:
            resolved = wrapper.resolve(task)
        except FileNotFoundError as exc:
            import pytest
            pytest.skip(f"native benchmark data is not installed: {exc}")
        evidence = resolved.adapter.build_team_selection_task(resolved.item, "PRIVATE")
        assert "PRIVATE" not in evidence
        assert task.mix_task_id not in evidence
        assert task.source.task_id not in evidence


def test_runner_injects_policy_without_explicit_benchmark_contract_name():
    policy = ExecutionPolicy(
        name="private_native_name",
        version="1",
        environment_mode="workspace",
        allowed_tools=("read_file",),
        chairman_instructions=("Inspect the supplied evidence.",),
    ).bind()
    contract = output_contract_from_name("locobench_solution_summary")
    runner = Runner(
        ROOT / "agents" / "pool_MIX_COOP",
        "planner",
        output_contract=contract,
        execution_policy=policy,
    )

    context = runner._build_chairman_context()
    assert "Inspect the supplied evidence." in context
    assert "private_native_name" not in context
    assert "locobench_solution_summary" not in context
    assert "solution_files_plus_completion_summary" in context


def test_execution_policy_resolves_shared_role_aliases_without_route_labels():
    gaia = GAIAAdapter().execution_policy({}).bind()
    loco = LoCoBenchAdapter().execution_policy({}).bind()
    loca = LOCABenchAdapter().execution_policy({}).bind()
    beyond_dep = BeyondSWEAdapter().execution_policy({"_task_type": "DepMigrate"}).bind()

    assert any("reproducible code" in rule for rule in gaia.instructions_for(
        "implementer", "implementer",
    ))
    assert any("only evidence corpus" in rule for rule in loco.instructions_for(
        "researcher", "evidence_researcher",
    ))
    assert any("selection and transformation" in rule for rule in loca.instructions_for(
        "context_analyst", "context_analyst",
    ))
    assert any("approved mutation plan" in rule for rule in loca.instructions_for(
        "implementer", "implementer",
    ))
    assert any("dependency API call site" in rule for rule in beyond_dep.instructions_for(
        "context_analyst", "context_analyst",
    ))
    assert any("minimal source changes" in rule for rule in beyond_dep.instructions_for(
        "implementer", "implementer",
    ))


def test_contract_only_policy_removes_adapter_collaboration_priors():
    native = BeyondSWEAdapter().execution_policy({"_task_type": "DepMigrate"})
    neutral = native.contract_only()

    assert neutral.collaboration_prior_mode == "contract_only"
    assert neutral.chairman_instructions == ()
    assert neutral.role_instructions == {}
    assert neutral.role_instruction_aliases == {}
    assert neutral.bind().instructions_for("implementer", "implementer") == ()

    # The native runtime boundary remains intact.
    assert neutral.environment_mode == native.environment_mode
    assert neutral.allowed_tools == native.allowed_tools
    assert neutral.artifact_requirements == native.artifact_requirements
    assert neutral.special_rules == native.special_rules
    assert neutral.fallback_policy == native.fallback_policy


def test_contract_only_context_contains_no_adapter_role_or_chairman_strategy():
    policy = LOCABenchAdapter().execution_policy({}).contract_only().bind()
    runner = Runner(
        ROOT / "agents" / "pool_MIX_COOP",
        "planner",
        execution_policy=policy,
    )

    chairman_context = runner._build_chairman_context()
    implementer = runner.load_agent_from_pool("implementer")
    implementer_context = runner._build_agent_context(implementer)

    assert "Recruit by required work product" not in chairman_context
    assert "Every artifact or mutation handoff" not in chairman_context
    assert "approved mutation plan" not in implementer_context
    assert "Native role rules:" not in implementer_context
    assert "Required artifacts/postconditions:" in implementer_context


def test_contract_only_policy_audit_metadata_is_explicit():
    payload = GAIAAdapter().execution_policy({}).contract_only().bind().to_dict()

    assert payload["collaboration_prior_mode"] == "contract_only"
    assert payload["chairman_instruction_count"] == 0
    assert payload["role_instruction_keys"] == []
    assert payload["role_instruction_aliases"] == {}


def test_neutral_selector_views_contain_task_facts_not_collaboration_advice():
    cases = [
        (
            GAIAAdapter(),
            {"Question": "Q", "file_name": "table.xlsx", "Level": 3},
            {"complexity_hint"},
        ),
        (
            LoCoBenchAdapter(),
            {
                "task_prompt": "Implement feature X",
                "task_category": "feature_implementation",
                "_language": "python",
                "context_files": ["a.py"],
                "evaluation_criteria": ["must pass"],
            },
            {"work_type_hint", "verification_strategy"},
        ),
        (
            LOCABenchAdapter(),
            {
                "_task_instruction": "Update the requested records",
                "_context_level": "128k",
                "_tool_catalog": [{"description": "special tool"}],
            },
            {"context_level", "native_workflow_requirements", "available_tool_capabilities"},
        ),
        (
            BeyondSWEAdapter(),
            {"problem_statement": "Fix the bug", "_task_type": "DepMigrate"},
            {"change_scope_hint"},
        ),
    ]

    forbidden_role_ids = {
        "dependency_specialist", "domain_debugger", "integration_verifier",
        "evidence_reader", "artifact_handler", "controlled_operator",
    }
    for adapter, item, forbidden_keys in cases:
        payload = adapter.build_neutral_team_selection_task(item, "PRIVATE")
        decoded = json.loads(payload)
        assert decoded.get("work_request")
        assert forbidden_keys.isdisjoint(decoded)
        assert not any(role_id in payload for role_id in forbidden_role_ids)


def test_every_native_policy_covers_every_shared_execution_role():
    policies = [
        GAIAAdapter().execution_policy({}),
        LoCoBenchAdapter().execution_policy({}),
        LOCABenchAdapter().execution_policy({}),
        BeyondSWEAdapter().execution_policy({"_task_type": "CrossRepo"}),
        BeyondSWEAdapter().execution_policy({"_task_type": "DepMigrate"}),
        BeyondSWEAdapter().execution_policy({"_task_type": "DomainFix"}),
    ]

    for policy in policies:
        bound = policy.bind()
        missing = [
            agent_name
            for agent_name, role in SHARED_EXECUTION_ROLES.items()
            if not bound.instructions_for(agent_name, role)
        ]
        assert missing == [], f"{policy.policy_id} misses shared roles: {missing}"


def test_execution_member_receives_common_native_rules_and_role_rules():
    policy = LoCoBenchAdapter().execution_policy({}).bind(
        workspace_paths={
            "workspace": "/case",
            "context": "/case/context",
            "solution": "/case/solution",
        },
        runtime_instructions=("Runtime-only requirement.",),
    )

    context = policy.agent_context("implementer", "implementer")

    assert "Environment mode: `isolated_context_solution_workspace`" in context
    assert "Available tools: `read_file`, `write_file`, `bash`" in context
    assert "Write at least one complete file under solution/" in context
    assert "The completion summary is not a substitute" in context
    assert "Runtime-only requirement." in context
    assert "Write complete, syntactically valid files" in context
    assert "long_context_solution_workspace" not in context


def test_runner_reports_only_the_execution_members_actual_native_tools():
    policy = GAIAAdapter().execution_policy({}).bind()
    runner = Runner(
        ROOT / "agents" / "pool_MIX_COOP",
        "planner",
        execution_policy=policy,
    )
    researcher = runner.load_agent_from_pool("researcher")

    context = runner._build_agent_context(researcher)

    assert "Available tools: `read_file`, `bash`, `web_search`, `web_fetch`" in context
    assert "`write_file`" not in context


def test_answer_agent_receives_output_contract_but_not_native_execution_policy():
    policy = LoCoBenchAdapter().execution_policy({}).bind()
    runner = Runner(
        ROOT / "agents" / "pool_MIX_COOP",
        "planner",
        output_contract=output_contract_from_name("locobench_solution_summary"),
        execution_policy=policy,
    )
    answer_agent = runner.load_agent_from_pool("answer_agent")

    context = runner._build_agent_context(answer_agent)

    assert "Current Native Output Contract" in context
    assert "Current Native Execution Policy" not in context


def test_fallback_is_not_score_or_evolution_eligible():
    policy = ExecutionPolicy(
        name="stateful_service_operations",
        version="1",
        environment_mode="native_service",
        allowed_tools=("service_tool", "bash"),
        fallback_policy=FallbackPolicy(
            trigger="fatal_service_failure",
            mode="local_fallback",
        ),
    )
    bound = policy.bind(
        execution_mode="local_fallback",
        available_tools=("bash",),
        fallback_used=True,
    )

    assert bound.official_score_eligible is False
    assert bound.evolution_eligible is False


def test_locobench_uses_separate_effective_and_wall_clock_budgets():
    adapter = LoCoBenchAdapter()

    assert adapter.default_effective_timeout == 1800.0
    assert adapter.default_evolve_timeout == 2400.0
    assert adapter.default_timeout == 2400.0
