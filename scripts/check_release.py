#!/usr/bin/env python3
"""Offline release checks that require neither datasets nor API calls."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "benchmarks/MIX-COOP/manifests/mix_coop_official_116_seed20260828.json"
INITIAL_POOLS = (
    "pool_GAIA_pool",
    "pool_LoCoBench",
    "pool_LOCAbench",
    "pool_BeyondSWE",
    "pool_MIX_COOP",
)
FROZEN_POOLS = {
    "pool_GAIA_81pct_20260902": (4, 35),
    "pool_LoCoBench_FI_20260903_v020": (2, 29),
}
SECRET_PATTERNS = (
    re.compile(r"(?<![a-zA-Z0-9_-])sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"apikey\.fun", re.IGNORECASE),
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    manifest = load_json(MANIFEST)
    counts = Counter(task["phase"] for task in manifest["tasks"])
    if counts != Counter({"evolve": 116, "test": 8}):
        failures.append(f"unexpected MIX split counts: {dict(counts)}")
    if manifest["ordering"].get("seed") != 20260828:
        failures.append("unexpected MIX ordering seed")

    for name in INITIAL_POOLS:
        pool = ROOT / "agents" / name
        for required in ("pool.yaml", "constitution.md"):
            if not (pool / required).is_file():
                failures.append(f"{name} is missing {required}")
        templates_path = pool / "templates.json"
        rules_path = pool / "handoff_rules.json"
        templates = load_json(templates_path) if templates_path.exists() else {"families": []}
        rules = load_json(rules_path) if rules_path.exists() else {"rules": []}
        if templates.get("families"):
            failures.append(f"initial pool {name} has non-empty templates")
        if rules.get("rules"):
            failures.append(f"initial pool {name} has non-empty handoff rules")

    for name, expected in FROZEN_POOLS.items():
        pool = ROOT / "agents" / name
        families = len(load_json(pool / "templates.json").get("families", []))
        rules = len(load_json(pool / "handoff_rules.json").get("rules", []))
        if (families, rules) != expected:
            failures.append(
                f"{name} snapshot drift: expected {expected}, got {(families, rules)}"
            )
        if not (pool / "PROVENANCE.zh-CN.md").is_file():
            failures.append(f"{name} is missing provenance")

    ignored_names = {".git", ".venv", ".pytest_cache", "__pycache__"}
    for path in ROOT.rglob("*"):
        if any(part in ignored_names for part in path.parts) or not path.is_file():
            continue
        if path.name not in {".env.example"} and (path.name == ".env" or path.suffix == ".env"):
            failures.append(f"private env file present: {path.relative_to(ROOT)}")
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            failures.append(f"possible credential/endpoint leak: {path.relative_to(ROOT)}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("release check: OK")
    print("MIX-COOP: 116 evolve + 8 test; seed=20260828")
    print("initial pools: 4 benchmark pools + 1 shared MIX pool")
    print("frozen snapshots: GAIA 4 families/35 rules; FI 2 families/29 rules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
