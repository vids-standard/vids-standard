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
SCAFFOLD = REPO_ROOT / "tools" / "vids_init.py"
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


class TestClassificationProfile:
    def test_classification_passes(self):
        report, code = run_validator(FIXTURES / "example-classification")
        assert report["Summary"]["Status"] == "PASS"
        assert code == 0

    def test_classification_zero_fail(self):
        report, _ = run_validator(FIXTURES / "example-classification")
        assert report["Summary"]["Failed"] == 0


class TestDetectionProfile:
    def test_detection_passes(self):
        report, code = run_validator(FIXTURES / "example-detection")
        assert report["Summary"]["Status"] == "PASS"
        assert code == 0

    def test_detection_zero_fail(self):
        report, _ = run_validator(FIXTURES / "example-detection")
        assert report["Summary"]["Failed"] == 0


class TestLandmarkProfile:
    def test_landmark_passes(self):
        report, code = run_validator(FIXTURES / "example-landmark")
        assert report["Summary"]["Status"] == "PASS"
        assert code == 0

    def test_landmark_zero_fail(self):
        report, _ = run_validator(FIXTURES / "example-landmark")
        assert report["Summary"]["Failed"] == 0


class TestROIProfile:
    def test_roi_passes(self):
        report, code = run_validator(FIXTURES / "example-roi")
        assert report["Summary"]["Status"] == "PASS"
        assert code == 0

    def test_roi_zero_fail(self):
        report, _ = run_validator(FIXTURES / "example-roi")
        assert report["Summary"]["Failed"] == 0


def run_scaffold(tmp_path, name, *extra_args):
    """Run vids_init.py in tmp_path and return CompletedProcess."""
    cmd = [sys.executable, str(SCAFFOLD), name,
           "--subjects", "3", "--profile", "poc"] + list(extra_args)
    return subprocess.run(cmd, cwd=tmp_path, capture_output=True, text=True)


class TestScaffolding:
    def test_scaffold_seg_passes(self, tmp_path):
        result = run_scaffold(tmp_path, "test-seg",
                              "--modality", "ct", "--annotation-type", "seg")
        assert result.returncode == 0, result.stderr
        report, _ = run_validator(tmp_path / "test-seg")
        assert report["Summary"]["Status"] == "PASS"

    def test_scaffold_cls_passes(self, tmp_path):
        result = run_scaffold(tmp_path, "test-cls",
                              "--modality", "fundus", "--annotation-type", "cls")
        assert result.returncode == 0, result.stderr
        report, _ = run_validator(tmp_path / "test-cls")
        assert report["Summary"]["Status"] == "PASS"

    def test_scaffold_bbox_passes(self, tmp_path):
        result = run_scaffold(tmp_path, "test-bbox",
                              "--modality", "xr", "--annotation-type", "bbox")
        assert result.returncode == 0, result.stderr
        report, _ = run_validator(tmp_path / "test-bbox")
        assert report["Summary"]["Status"] == "PASS"

    def test_scaffold_lm_passes(self, tmp_path):
        result = run_scaffold(tmp_path, "test-lm",
                              "--modality", "mr", "--annotation-type", "lm")
        assert result.returncode == 0, result.stderr
        report, _ = run_validator(tmp_path / "test-lm")
        assert report["Summary"]["Status"] == "PASS"

    def test_scaffold_roi_passes(self, tmp_path):
        result = run_scaffold(tmp_path, "test-roi",
                              "--modality", "ct", "--annotation-type", "roi")
        assert result.returncode == 0, result.stderr
        report, _ = run_validator(tmp_path / "test-roi")
        assert report["Summary"]["Status"] == "PASS"

    def test_scaffold_default_is_seg(self, tmp_path):
        result = run_scaffold(tmp_path, "test-default", "--modality", "ct")
        assert result.returncode == 0, result.stderr
        # Default (no --annotation-type) must produce _seg files for backward compat
        ann_root = tmp_path / "test-default" / "derivatives" / "annotations"
        assert list(ann_root.rglob("*_seg.nii.gz")), "default scaffold should produce _seg files"
        report, _ = run_validator(tmp_path / "test-default")
        assert report["Summary"]["Status"] == "PASS"

    def test_scaffold_invalid_annotation_type_rejected(self, tmp_path):
        result = run_scaffold(tmp_path, "test-bad",
                              "--modality", "ct", "--annotation-type", "invalid")
        assert result.returncode != 0
        assert "invalid choice" in result.stderr
        assert not (tmp_path / "test-bad").exists()
