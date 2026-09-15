import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MIX_DIR = ROOT / "benchmarks" / "MIX-COOP"
if str(MIX_DIR) not in sys.path:
    sys.path.insert(0, str(MIX_DIR))

from mix_coop_manifest import MixCoopManifest  # noqa: E402
from mixed_scheduler import MixedScheduler  # noqa: E402


MANIFEST_PATH = MIX_DIR / "manifests" / "mix_coop_four_way_evolve_smoke_v1_seed20260822.json"


def test_runtime_task_ids_are_opaque_and_stable():
    manifest = MixCoopManifest.load(MANIFEST_PATH)
    scheduler = MixedScheduler.__new__(MixedScheduler)
    scheduler.manifest = manifest
    scheduler._global_indices = {
        task.mix_task_id: index
        for index, task in enumerate(
            manifest.tasks_for_phase("evolve", enabled_only=False)
            + manifest.tasks_for_phase("test", enabled_only=False)
        )
    }

    for task in manifest.tasks:
        runtime_id = scheduler._runtime_task_id(task)
        assert runtime_id.startswith(f"case-{task.phase}-")
        assert task.source.benchmark not in runtime_id
        assert task.mix_task_id not in runtime_id


def test_outer_result_keeps_analysis_mapping_separate():
    payload = {
        "mix_task_id": "mix-evolve-extra-locobench",
        "runtime_task_id": "case-evolve-000",
        "source_benchmark": "locobench",
    }
    assert payload["runtime_task_id"] != payload["mix_task_id"]
    assert payload["source_benchmark"] == "locobench"
