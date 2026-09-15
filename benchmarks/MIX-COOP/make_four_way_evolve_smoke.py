#!/usr/bin/env python3
"""Build the four-way MIX-COOP smoke manifest with two evolve items each."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THIS_DIR = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from randomize_manifest import materialize_payload  # noqa: E402
from task_wrapper import ADAPTER_REGISTRY  # noqa: E402


SOURCE = THIS_DIR / "manifests" / "mix_coop_smoke_v1.json"
TARGET = THIS_DIR / "manifests" / "mix_coop_four_way_evolve_smoke_v1_seed20260822.json"


SPLITS = {
    "locobench": ("python", {"category": "feature_implementation"}),
    "locabench": ("evolve_96k", {}),
    "gaia": ("train_20", {}),
    "beyondswe": ("crossrepo", {}),
}


def _native_row(benchmark: str, source_index: int) -> dict:
    split, adapter_args = SPLITS[benchmark]
    adapter = ADAPTER_REGISTRY[benchmark].factory()
    args = adapter.build_parser().parse_args([])
    args.split = split
    for key, value in adapter_args.items():
        setattr(args, key, value)
    items = adapter.load_dataset(args)
    item = items[source_index]
    return {
        "benchmark": benchmark,
        "split": split,
        "task_id": adapter.get_item_id(item),
        "source_index": source_index,
        "adapter_args": dict(adapter_args),
    }


def build() -> dict:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    evolve = [row for row in payload["tasks"] if row["phase"] == "evolve"]
    existing = {row["source"]["benchmark"] for row in evolve}
    if existing != set(SPLITS):
        raise RuntimeError(f"unexpected base smoke evolve benchmarks: {sorted(existing)}")

    for benchmark in sorted(SPLITS):
        template = next(row for row in evolve if row["source"]["benchmark"] == benchmark)
        extra = copy.deepcopy(template)
        extra["mix_task_id"] = f"mix-evolve-extra-{benchmark}"
        extra["source"] = _native_row(benchmark, 1)
        extra["hidden_annotations"] = copy.deepcopy(template.get("hidden_annotations", {}))
        payload["tasks"].append(extra)

    payload["suite_id"] = "mix-coop-four-way-evolve-smoke-v1-seed20260822"
    payload["description"] = (
        "Four-way MIX-COOP smoke: two evolve tasks per benchmark and one "
        "native holdout reference per benchmark."
    )
    return materialize_payload(payload, seed=20260822)


if __name__ == "__main__":
    TARGET.write_text(
        json.dumps(build(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(TARGET)
