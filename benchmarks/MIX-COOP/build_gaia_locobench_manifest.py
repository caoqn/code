#!/usr/bin/env python3
"""Materialize the first GAIA + LoCoBench mixed experiment manifest.

The split follows the native paper partitions: GAIA train_20/test_100 and
LoCoBench Python category indices 0--19/20--99. The generated JSON locks task
IDs, source indices, and the round-robin order for reproducibility.
"""

from __future__ import annotations

import json
import sys
from argparse import Namespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THIS_DIR = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from benchmarks.adapter_gaia import GAIAAdapter  # noqa: E402
from benchmarks.adapter_locobench import LoCoBenchAdapter  # noqa: E402


def _pick_by_level(items: list[dict], counts: dict[int, int]) -> list[int]:
    selected: list[int] = []
    for level, count in sorted(counts.items()):
        candidates = [
            index for index, item in enumerate(items)
            if int(item.get("_level", item.get("Level", 0))) == level
        ]
        if len(candidates) < count:
            raise RuntimeError(f"GAIA level {level} has only {len(candidates)} candidates")
        selected.extend(candidates[:count])
    return sorted(selected)


def _gaia_tasks(phase: str) -> list[dict]:
    adapter = GAIAAdapter()
    split = "train_20" if phase == "evolve" else "test_100"
    items = adapter.load_dataset(Namespace(split=split, max_items=None, level=None))
    counts = {1: 3, 2: 4, 3: 3} if phase == "evolve" else {1: 15, 2: 20, 3: 5}
    rows = []
    for source_index in _pick_by_level(items, counts):
        item = items[source_index]
        rows.append({
            "benchmark": "gaia",
            "split": split,
            "task_id": adapter.get_item_id(item),
            "source_index": source_index,
            "adapter_args": {},
            "hidden_annotations": {
                "collaboration_profile": [
                    "evidence_retrieval",
                    "independent_verification",
                    "global_synthesis",
                ],
                "difficulty": f"level_{item.get('_level', item.get('Level', 'unknown'))}",
                "notes": "Analysis-only annotation; never passed to Selector.",
            },
        })
    return rows


def _loco_tasks(phase: str) -> list[dict]:
    adapter = LoCoBenchAdapter()
    rows = []
    categories = ["feature_implementation", "cross_file_refactoring"]
    # Five evolve items per category; twenty holdout items per category.
    indices = range(0, 5) if phase == "evolve" else range(20, 40)
    for category in categories:
        items = adapter.load_dataset(Namespace(
            split="python",
            max_items=None,
            category=category,
            language=None,
        ))
        for source_index in indices:
            item = items[source_index]
            profile = (
                ["repository_understanding", "implementation", "test_verification"]
                if category == "feature_implementation"
                else ["cross_file_consistency", "implementation", "test_verification"]
            )
            rows.append({
                "benchmark": "locobench",
                "split": "python",
                "task_id": adapter.get_item_id(item),
                "source_index": source_index,
                "adapter_args": {"category": category},
                "hidden_annotations": {
                    "collaboration_profile": profile,
                    "difficulty": str(item.get("difficulty", "")),
                    "notes": "Analysis-only annotation; native category is not selector input.",
                },
            })
    # Keep category alternation stable within each benchmark's sequence.
    interleaved = []
    halves = [rows[: len(rows) // 2], rows[len(rows) // 2 :]]
    for left, right in zip(*halves):
        interleaved.extend([left, right])
    return interleaved


def build() -> dict:
    smoke_path = THIS_DIR / "manifests" / "mix_coop_smoke_v1.json"
    payload = json.loads(smoke_path.read_text(encoding="utf-8"))
    payload["suite_id"] = "mix-coop-gaia-locobench-v1"
    payload["description"] = (
        "GAIA + LoCoBench mixed evolution: 10 evolve and 40 holdout tasks per benchmark."
    )
    payload["active_benchmarks"] = ["gaia", "locobench"]
    payload["benchmark_bindings"] = {
        key: payload["benchmark_bindings"][key]
        for key in payload["active_benchmarks"]
    }
    payload["ordering"].update({
        "seed": 20260822,
        "round_unit": "one GAIA task plus one LoCoBench task",
        "shuffle_within_round": False,
    })

    evolve_gaia = _gaia_tasks("evolve")
    evolve_loco = _loco_tasks("evolve")
    test_gaia = _gaia_tasks("test")
    test_loco = _loco_tasks("test")

    task_rows = []
    for phase, gaia_rows, loco_rows in (
        ("evolve", evolve_gaia, evolve_loco),
        ("test", test_gaia, test_loco),
    ):
        if len(gaia_rows) != len(loco_rows):
            raise RuntimeError(f"unbalanced {phase}: GAIA={len(gaia_rows)}, LoCoBench={len(loco_rows)}")
        for round_index, (gaia_row, loco_row) in enumerate(zip(gaia_rows, loco_rows)):
            for benchmark_row in (gaia_row, loco_row):
                task_rows.append({
                    "mix_task_id": f"mix-{phase}-{len(task_rows):03d}-{benchmark_row['benchmark']}",
                    "phase": phase,
                    "order": len(task_rows) if phase == "evolve" else len(task_rows) - len(evolve_gaia) - len(evolve_loco),
                    "source": {
                        key: benchmark_row[key]
                        for key in ("benchmark", "split", "task_id", "source_index", "adapter_args")
                    },
                    "hidden_annotations": benchmark_row["hidden_annotations"],
                })
    # The order field is per phase, not the global list position.
    for phase in ("evolve", "test"):
        phase_rows = [row for row in task_rows if row["phase"] == phase]
        for order, row in enumerate(phase_rows):
            row["order"] = order
    payload["tasks"] = task_rows
    return payload


if __name__ == "__main__":
    target = THIS_DIR / "manifests" / "mix_coop_gaia_locobench_v1.json"
    target.write_text(
        json.dumps(build(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(target)
