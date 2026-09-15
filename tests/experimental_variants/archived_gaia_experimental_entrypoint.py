from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_experimental_gaia_entrypoint_aliases_only_test_variants() -> None:
    root = Path(__file__).resolve().parents[1]
    probe = """
import sys
import benchmarks.adapter_gaia_test
import core.team_reflector_test as reflector_test
import core.team_selector_test as selector_test
assert sys.modules['core.team_reflector'] is reflector_test
assert sys.modules['core.team_selector'] is selector_test
"""
    completed = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
