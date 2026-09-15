"""Unified task boundary for MIX-COOP's four native benchmark adapters.

This module intentionally does not implement a fifth evaluator or environment.
It resolves a manifest reference and delegates preparation/evaluation to the
native adapter. The executable scheduler enters the base-adapter lifecycle,
which supplies the neutral selector view for MIX-COOP runs.
"""

from __future__ import annotations

import argparse
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from core.output_contract import output_contract_from_name
from mix_coop_manifest import MixCoopManifest, MixedTask


@dataclass(frozen=True)
class AdapterRegistration:
    benchmark: str
    module: str
    class_name: str
    factory: Callable[[], Any]


def _gaia_adapter():
    from benchmarks.adapter_gaia import GAIAAdapter
    return GAIAAdapter()


def _locobench_adapter():
    from benchmarks.adapter_locobench import LoCoBenchAdapter
    return LoCoBenchAdapter()


def _locabench_adapter():
    from benchmarks.adapter_locabench import LOCABenchAdapter
    return LOCABenchAdapter()


def _beyondswe_adapter():
    from benchmarks.adapter_beyondswe import BeyondSWEAdapter
    return BeyondSWEAdapter()


ADAPTER_REGISTRY: dict[str, AdapterRegistration] = {
    "gaia": AdapterRegistration(
        "gaia", "benchmarks.adapter_gaia", "GAIAAdapter", _gaia_adapter,
    ),
    "locobench": AdapterRegistration(
        "locobench", "benchmarks.adapter_locobench", "LoCoBenchAdapter", _locobench_adapter,
    ),
    "locabench": AdapterRegistration(
        "locabench", "benchmarks.adapter_locabench", "LOCABenchAdapter", _locabench_adapter,
    ),
    "beyondswe": AdapterRegistration(
        "beyondswe", "benchmarks.adapter_beyondswe", "BeyondSWEAdapter", _beyondswe_adapter,
    ),
}


@dataclass
class ResolvedNativeTask:
    specification: MixedTask
    adapter: Any
    item: dict[str, Any]


@dataclass
class PreparedMixedTask:
    """Runtime state owned by one native adapter for one MIX-COOP task."""

    resolved: ResolvedNativeTask
    env_context: Any
    execution_task: str
    selector_task: str
    output_contract: Any
    execution_policy: Any

    @property
    def mix_task_id(self) -> str:
        return self.resolved.specification.mix_task_id


class MixedTaskWrapper:
    """Route native tasks while preserving shared-evolution boundaries."""

    def __init__(self, manifest: MixCoopManifest):
        self.manifest = manifest
        self._validate_adapter_bindings()

    @classmethod
    def from_path(cls, path: str | Path) -> "MixedTaskWrapper":
        return cls(MixCoopManifest.load(path))

    def _validate_adapter_bindings(self) -> None:
        for benchmark, binding in self.manifest.benchmark_bindings.items():
            registration = ADAPTER_REGISTRY.get(benchmark)
            if registration is None:
                raise ValueError(f"no native adapter registration for {benchmark!r}")
            if binding["adapter_module"] != registration.module:
                raise ValueError(
                    f"{benchmark} adapter_module must be {registration.module!r}"
                )
            if binding["adapter_class"] != registration.class_name:
                raise ValueError(
                    f"{benchmark} adapter_class must be {registration.class_name!r}"
                )
            adapter = registration.factory()
            execution_policy = adapter.execution_policy({})
            if binding["execution_policy"] != execution_policy.name:
                raise ValueError(
                    f"{benchmark} execution policy mismatch: manifest declares "
                    f"{binding['execution_policy']!r}, but {registration.class_name} "
                    f"provides {execution_policy.name!r}"
                )
            if str(binding["execution_policy_version"]) != execution_policy.version:
                raise ValueError(
                    f"{benchmark} execution policy version mismatch: manifest "
                    f"declares {binding['execution_policy_version']!r}, but "
                    f"{registration.class_name} provides {execution_policy.version!r}"
                )
            declared_contract = output_contract_from_name(
                str(binding["output_contract"])
            )
            native_contract = adapter.output_contract()
            if declared_contract.name != native_contract.name:
                raise ValueError(
                    f"{benchmark} output contract mismatch: manifest declares "
                    f"{binding['output_contract']!r} (canonical "
                    f"{declared_contract.name!r}), but {registration.class_name} "
                    f"provides {native_contract.name!r}"
                )
            declared_tools = set(binding["native_allowed_tools"])
            policy_tools = set(execution_policy.allowed_tools)
            if declared_tools != policy_tools:
                raise ValueError(
                    f"{benchmark} native tool mismatch: manifest declares "
                    f"{sorted(declared_tools)}, but {registration.class_name} "
                    f"execution policy provides {sorted(policy_tools)}"
                )

    @staticmethod
    def _adapter_namespace(adapter: Any, task: MixedTask) -> argparse.Namespace:
        # Parser defaults are the canonical adapter defaults.  Only the
        # manifest's dataset-selection fields are overlaid here; run/team and
        # evolution settings remain suite-owned.
        args = adapter.build_parser().parse_args([])
        args.split = task.source.split
        for key, value in task.source.adapter_args.items():
            if not hasattr(args, key):
                raise ValueError(
                    f"unknown {task.source.benchmark} adapter argument: {key!r}"
                )
            setattr(args, key, value)
        return args

    def resolve(self, task: MixedTask) -> ResolvedNativeTask:
        registration = ADAPTER_REGISTRY[task.source.benchmark]
        adapter = registration.factory()
        args = self._adapter_namespace(adapter, task)
        items = adapter.load_dataset(args)
        index = task.source.source_index
        if index >= len(items):
            raise IndexError(
                f"{task.mix_task_id}: source_index {index} is outside "
                f"{task.source.benchmark}/{task.source.split} ({len(items)} items)"
            )
        item = {**items[index], "_source_index": index}
        actual_id = adapter.get_item_id(item)
        if actual_id != task.source.task_id:
            raise ValueError(
                f"{task.mix_task_id}: manifest task_id {task.source.task_id!r} "
                f"does not match adapter item {actual_id!r} at index {index}; "
                "the native dataset or filtering arguments changed"
            )
        return ResolvedNativeTask(task, adapter, item)

    async def prepare(self, task: MixedTask, session: Any) -> PreparedMixedTask:
        """Create the native environment and task without leaking route metadata."""
        resolved = self.resolve(task)
        env_context = resolved.adapter.setup_environment(resolved.item, session)
        if inspect.isawaitable(env_context):
            env_context = await env_context
        execution_policy = resolved.adapter.bind_execution_policy(
            resolved.adapter.execution_policy(resolved.item),
            resolved.item,
            env_context,
            session,
        )
        workspace_files = [
            path.name for path in Path(session.workspace).iterdir()
            if not path.name.startswith(".")
        ]
        execution_task = resolved.adapter.build_task(
            resolved.item, session, workspace_files,
        )
        normalized = resolved.adapter.build_team_selection_task(
            resolved.item, execution_task,
        )
        selector_task = normalized
        return PreparedMixedTask(
            resolved=resolved,
            env_context=env_context,
            execution_task=execution_task,
            selector_task=selector_task,
            output_contract=resolved.adapter.output_contract(),
            execution_policy=execution_policy,
        )

    @staticmethod
    def evaluate(prepared: PreparedMixedTask, predicted: str, session: Any):
        """Delegate scoring to the native evaluator without score conversion."""
        return prepared.resolved.adapter.evaluate(
            prepared.resolved.item,
            predicted,
            session,
            **prepared.env_context.data,
        )

    @staticmethod
    def build_record(
        prepared: PreparedMixedTask,
        predicted: str,
        eval_result: Any,
        session: Any,
        error: str = "",
    ) -> dict[str, Any]:
        """Wrap a native result with auditable MIX-COOP routing metadata."""
        spec = prepared.resolved.specification
        native = prepared.resolved.adapter.build_record(
            prepared.resolved.item,
            spec.source.source_index,
            predicted,
            eval_result,
            session,
            error,
        )
        return {
            "mix_task_id": spec.mix_task_id,
            "phase": spec.phase,
            "order": spec.order,
            "source_benchmark": spec.source.benchmark,
            "source_split": spec.source.split,
            "source_task_id": spec.source.task_id,
            "native_score": float(eval_result.score),
            "is_correct": bool(eval_result.success),
            "infrastructure_failure": bool(native.get("infrastructure_failure", False)),
            "official_score_eligible": prepared.execution_policy.official_score_eligible,
            "evolution_eligible": prepared.execution_policy.evolution_eligible,
            "execution_policy": prepared.execution_policy.to_dict(),
            "native_record": native,
        }

    @staticmethod
    def teardown(prepared: PreparedMixedTask) -> None:
        prepared.resolved.adapter.teardown_environment(prepared.env_context)
