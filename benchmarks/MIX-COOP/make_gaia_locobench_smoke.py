#!/usr/bin/env python3
"""Derive a small GAIA–LoCoBench protocol smoke manifest from the pilot.

The smoke set preserves the pilot's task order and source references. It is
intended to validate adapter boundaries and shared-team bookkeeping before any
model/API calls are made on the full 20+80 pilot.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PILOT = ROOT / "manifests" / "mix_coop_gaia_locobench_v1.json"
TARGET = ROOT / "manifests" / "mix_coop_gaia_locobench_smoke_v1.json"


def _take_rounds(tasks: list[dict], rounds: int) -> list[dict]:
    selected = []
    for task in tasks:
        if len(selected) >= rounds * 2:
            break
        selected.append(copy.deepcopy(task))
    if len(selected) != rounds * 2:
        raise ValueError(
            f"expected {rounds * 2} tasks in a balanced prefix, got {len(selected)}"
        )
    return selected


def build() -> dict:
    payload = json.loads(PILOT.read_text(encoding="utf-8"))
    evolve = _take_rounds(
        [row for row in payload["tasks"] if row["phase"] == "evolve"],
        rounds=2,
    )
    test = _take_rounds(
        [row for row in payload["tasks"] if row["phase"] == "test"],
        rounds=4,
    )
    for phase_rows in (evolve, test):
        for order, row in enumerate(phase_rows):
            row["order"] = order
            row["mix_task_id"] = f"smoke-{row['phase']}-{order:02d}-{row['source']['benchmark']}"

    payload["suite_id"] = "mix-coop-gaia-locobench-smoke-v1"
    payload["description"] = (
        "Protocol smoke: 2 evolve and 4 test tasks per benchmark, preserving "
        "the GAIA-first round-robin order from the pilot."
    )
    payload["tasks"] = evolve + test
    payload["smoke_policy"] = {
        "purpose": "adapter_and_shared_lineage_validation",
        "model_calls": "allowed_only_when_explicitly_launched",
        "expected_evolve_per_benchmark": 2,
        "expected_test_per_benchmark": 4,
    }
    return payload


if __name__ == "__main__":
    TARGET.write_text(
        json.dumps(build(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(TARGET)

