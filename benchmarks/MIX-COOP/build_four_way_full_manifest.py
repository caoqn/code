#!/usr/bin/env python3
"""Build the Meta-Team official-protocol 116-task MIX-COOP manifest."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THIS_DIR = Path(__file__).resolve().parent
for path in (str(ROOT), str(THIS_DIR)):
    if path not in sys.path:
        sys.path.insert(0, path)

from randomize_manifest import materialize_payload  # noqa: E402
from task_wrapper import ADAPTER_REGISTRY  # noqa: E402


BASE = THIS_DIR / "manifests" / "mix_coop_four_way_evolve_test2_v1_seed20260827.json"

# These are the exact native selections used by the official Meta-Team runs:
# GAIA/FI/CR/CrossRepo/DepMigrate cases 0..19 and all 16 evolve_96k cases.
OFFICIAL_GROUPS = (
    ("gaia", "train_20", {}, tuple(range(20))),
    ("locobench", "python", {"category": "feature_implementation"}, tuple(range(20))),
    ("locobench", "python", {"category": "cross_file_refactoring"}, tuple(range(20))),
    ("locabench", "evolve_96k", {}, tuple(range(16))),
    ("beyondswe", "crossrepo", {}, tuple(range(20))),
    ("beyondswe", "depmigrate", {}, tuple(range(20))),
)


def build(seed: int) -> dict:
    payload = json.loads(BASE.read_text(encoding="utf-8"))
    test_rows = [copy.deepcopy(row) for row in payload["tasks"] if row["phase"] == "test"]
    templates = {row["source"]["benchmark"]: row for row in test_rows}
    evolve_rows: list[dict] = []

    for benchmark, split, adapter_args, indices in OFFICIAL_GROUPS:
        adapter = ADAPTER_REGISTRY[benchmark].factory()
        args = adapter.build_parser().parse_args([])
        args.split = split
        for key, value in adapter_args.items():
            setattr(args, key, value)
        items = adapter.load_dataset(args)
        if len(items) <= max(indices):
            raise RuntimeError(
                f"{benchmark}/{split} returned {len(items)} items; "
                f"official index {max(indices)} is unavailable"
            )
        ids = [adapter.get_item_id(items[index]) for index in indices]
        if len(ids) != len(set(ids)):
            raise RuntimeError(f"duplicate official task IDs in {benchmark}/{split}")
        for source_index, task_id in zip(indices, ids):
            serial = len(evolve_rows)
            row = copy.deepcopy(templates[benchmark])
            row["mix_task_id"] = f"mix-evolve-{serial:03d}"
            row["phase"] = "evolve"
            row["order"] = serial
            row["source"] = {
                "benchmark": benchmark,
                "split": split,
                "task_id": task_id,
                "source_index": source_index,
                "adapter_args": dict(adapter_args),
            }
            evolve_rows.append(row)

    if len(evolve_rows) != 116:
        raise RuntimeError(f"built {len(evolve_rows)} evolve tasks; expected 116")
    payload["tasks"] = evolve_rows + test_rows
    payload["suite_id"] = "mix-coop-official-116"
    payload["description"] = (
        "Meta-Team official-aligned 116-task MIX-COOP evolution set with "
        "one fixed-seed global shuffle."
    )
    return materialize_payload(
        payload,
        seed=seed,
        strategy="global_shuffle",
        shuffle_phases=("evolve",),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or (
        THIS_DIR / "manifests" / f"mix_coop_official_116_seed{args.seed}.json"
    )
    result = build(args.seed)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)
    print(f"seed={args.seed} order_hash={result['ordering']['order_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
