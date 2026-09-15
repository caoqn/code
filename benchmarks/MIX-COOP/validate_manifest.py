#!/usr/bin/env python3
"""Validate MIX-COOP structure and optionally resolve native task IDs."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = THIS_DIR.parent.parent
for path in (str(THIS_DIR), str(PROJECT_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

from mix_coop_manifest import MixCoopManifest  # noqa: E402
from task_wrapper import MixedTaskWrapper  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--resolve-native",
        action="store_true",
        help="Load native datasets and verify every source index/task ID pair",
    )
    args = parser.parse_args()

    manifest = MixCoopManifest.load(args.manifest)
    wrapper = MixedTaskWrapper(manifest)
    if args.resolve_native:
        for task in manifest.tasks:
            wrapper.resolve(task)

    phase_counts = Counter(task.phase for task in manifest.tasks if task.enabled)
    benchmark_counts = Counter(
        (task.phase, task.source.benchmark)
        for task in manifest.tasks if task.enabled
    )
    print(f"VALID: {manifest.suite_id} (schema v{manifest.schema_version})")
    print(f"  evolve={phase_counts['evolve']} test={phase_counts['test']}")
    for phase in ("evolve", "test"):
        counts = ", ".join(
            f"{benchmark}={benchmark_counts[(phase, benchmark)]}"
            for benchmark in sorted(manifest.benchmark_bindings)
        )
        print(f"  {phase}: {counts}")
    if args.resolve_native:
        print("  native source references resolved successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

