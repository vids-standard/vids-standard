#!/usr/bin/env python3
"""
Enforcement tests for MD-0006 (assertion discipline).

Rule 1: VIDS artifacts and tools must not emit certification, attestation,
approval or assurance claims about a dataset without governance authorization.

Rule 2: A generator may populate a provenance field only when the act that
field denotes is the act the generator just performed.

Without these tests MD-0006 Rule 2 is a statement of intent. The defect it
corrects passed human review in four separate locations.

Run: python -m pytest tests/test_assertion_discipline.py -v
"""

import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SCAFFOLD = REPO_ROOT / "tools" / "vids_init.py"

# Rule 1 vocabulary. Substring match, case-insensitive.
# "certified" is deliberately absent: annotator credentials such as
# "Board-certified radiologist" describe a person, not a dataset, and are
# outside Rule 1 (MD-0006 do-not-touch list).
FORBIDDEN_KEY_SUBSTRINGS = [
    "certification",
    "certifiedby",
    "attestation",
    "attestedby",
    "assurance",
    "approvedby",
]

# Fields naming an act the generator does not perform. Populating any of these
# with a real date is a Rule 2 violation.
FOREIGN_ACT_DATE_PATHS = [
    ("DeIdentification", "Date"),
    ("ConversionDate",),
    ("AnnotationProcess", "Date"),
    ("QualityAssessmentDate",),
]

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@pytest.fixture(scope="module")
def scaffold():
    """Generate a fresh Full-profile scaffold and return its root."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "vids-test-dataset"
        result = subprocess.run(
            [sys.executable, str(SCAFFOLD), str(root),
             "--profile", "full", "--subjects", "2"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            pytest.fail(f"scaffold generation failed:\n{result.stderr}")
        yield root


def _all_json(root):
    for path in sorted(root.rglob("*.json")):
        with open(path) as fh:
            yield path, json.load(fh)


def _walk(node, trail=()):
    """Yield (path_tuple, value) for every key in a nested structure."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield trail + (key,), value
            yield from _walk(value, trail + (key,))
    elif isinstance(node, list):
        for item in node:
            yield from _walk(item, trail)


# --------------------------------------------------------------------------
# Rule 1
# --------------------------------------------------------------------------

def test_no_certification_fields_anywhere(scaffold):
    """No scaffolded JSON emits an outcome claim about the dataset."""
    offences = []
    for path, doc in _all_json(scaffold):
        for trail, _ in _walk(doc):
            key = trail[-1].lower().replace("_", "")
            for banned in FORBIDDEN_KEY_SUBSTRINGS:
                if banned in key:
                    offences.append(f"{path.name}: {'.'.join(trail)}")
    assert not offences, (
        "MD-0006 Rule 1: generator emitted outcome-claim fields:\n  "
        + "\n  ".join(offences)
    )


def test_annotator_credentials_survive(scaffold):
    """Rule 1 must not be implemented by deleting annotator credentials.

    Guards the MD-0006 do-not-touch list. Credentials describe a person and
    are the provenance the standard exists to capture.
    """
    found = any(
        trail[-1] == "Credentials"
        for _, doc in _all_json(scaffold)
        for trail, _ in _walk(doc)
    )
    assert found, (
        "Annotator Credentials absent from the scaffold. Rule 1 targets claims "
        "about datasets, not the recorded credentials of a person."
    )


# --------------------------------------------------------------------------
# Rule 2
# --------------------------------------------------------------------------

def test_no_auto_populated_foreign_act_dates(scaffold):
    """No field denoting an act the generator did not perform carries a date."""
    offences = []
    for path, doc in _all_json(scaffold):
        for trail, value in _walk(doc):
            if not isinstance(value, str) or not ISO_DATE.match(value):
                continue
            for target in FOREIGN_ACT_DATE_PATHS:
                if trail[-len(target):] == target:
                    offences.append(f"{path.name}: {'.'.join(trail)} = {value}")
    assert not offences, (
        "MD-0006 Rule 2: generator populated a date for an act it did not "
        "perform:\n  " + "\n  ".join(offences)
    )


def test_no_todays_date_outside_generator_acts(scaffold):
    """Catch-all: today's date may appear only where the generator acted.

    Broader than the path list above, so a newly added field cannot
    reintroduce the defect without failing here first.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    permitted = {("Created",), ("LastModified",)}
    offences = []
    for path, doc in _all_json(scaffold):
        for trail, value in _walk(doc):
            if value == today and trail[-1:] not in permitted:
                offences.append(f"{path.name}: {'.'.join(trail)} = {value}")
    assert not offences, (
        "MD-0006 Rule 2: today's date written to a field the generator does "
        "not own:\n  " + "\n  ".join(offences)
    )


def test_placeholders_remain_present_for_a005(scaffold):
    """Rule 2 is satisfied by placeholders, not by omitting the field.

    Annotation sidecars must still carry Provenance so A005 passes. Hollow
    structure is by design: VIDS verifies documentation is present and
    structured, not that it is true.
    """
    sidecars = [
        (p, d) for p, d in _all_json(scaffold)
        if re.search(r"_(seg|cls|bbox|lm|roi)\.json$", p.name)
    ]
    assert sidecars, "no annotation sidecars generated; fixture is wrong"
    for path, doc in sidecars:
        assert "VIDSVersion" in doc, f"{path.name}: VIDSVersion missing (A004)"
        assert "Provenance" in doc, f"{path.name}: Provenance missing (A005)"
        date = doc["Provenance"].get("AnnotationProcess", {}).get("Date")
        assert date, f"{path.name}: Provenance date field absent, not placeheld"
        assert not ISO_DATE.match(date), (
            f"{path.name}: Provenance date is a real date, expected placeholder"
        )
