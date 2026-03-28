#!/usr/bin/env python3
"""
Basic tests for the VIDS validator.
Run: python -m pytest tests/ -v
"""

import sys
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
VALIDATOR = REPO_ROOT / "validators" / "validate_vids.py"
FIXTURES = Path(__file__).parent / "fixtures"


def setup_module():
    """Generate fixtures if they don't exist."""
    if not FIXTURES.exists():
        subprocess.run(
            [sys.executable, str(Path(__file__).parent / "generate_test_fixtures.py")],
            check=True
        )


def run_validator(dataset_path, profile="auto"):
    """Run validator and return parsed JSON report."""
    cmd = [sys.executable, str(VALIDATOR), str(dataset_path), "--json"]
    if profile != "auto":
        cmd.extend(["--profile", profile])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout), result.returncode


class TestPOCProfile:
    def test_poc_passes(self):
        report, code = run_validator(FIXTURES / "example-poc")
        assert report["Summary"]["Status"] == "PASS"
        assert code == 0

    def test_poc_has_15_pass(self):
        report, _ = run_validator(FIXTURES / "example-poc")
        passed = report["Summary"]["Passed"]
        skipped = report["Summary"]["Skipped"]
        assert passed >= 15
        assert skipped >= 5  # Q001-Q003, M001-M002

    def test_poc_zero_fail(self):
        report, _ = run_validator(FIXTURES / "example-poc")
        assert report["Summary"]["Failed"] == 0


class TestFullProfile:
    def test_full_passes(self):
        report, code = run_validator(FIXTURES / "example-full", profile="full")
        assert report["Summary"]["Status"] == "PASS"
        assert code == 0

    def test_full_21_rules(self):
        report, _ = run_validator(FIXTURES / "example-full", profile="full")
        assert report["Summary"]["TotalRules"] == 21

    def test_full_zero_fail(self):
        report, _ = run_validator(FIXTURES / "example-full", profile="full")
        assert report["Summary"]["Failed"] == 0
