#!/usr/bin/env python3
"""
Enforcement tests for SOP Section 7.3 (no unreviewable artifacts in a
reviewed path).

The rule: any file that cannot be read as a diff in review must not sit in a
path where review is the control. Either it is generated at distribution time,
or CI regenerates it and fails on divergence.

The rule further states that CI must not push commits back to a protected
branch to satisfy it. These tests therefore fail the build; they do not
regenerate or delete anything.

The rule also names a specific hazard: a repository PDF sitting beside a
record whose sign-off cites `MD-NNNN-ApprovalEvidence-YYYY-MM-DD.pdf` is a
file a reader could mistake for the executed signature copy. The executed
instrument is held outside this repository and cited by filename only.

Without these tests the rule is a statement of intent. Eight rendered PDFs
accumulated in `main` before it was applied, and the divergence they caused
was invisible to review precisely because a binary artifact is opaque to a
diff.

Run: python -m pytest tests/test_repo_hygiene.py -v
"""

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent

RENDERED_DOCUMENT_SUFFIXES = {
    ".pdf",
    ".doc", ".docx",
    ".ppt", ".pptx",
    ".xls", ".xlsx",
    ".odt", ".odp", ".ods",
    ".rtf",
    ".pages", ".key", ".numbers",
}

EXCLUDED_COMPONENTS = {
    ".git", "__pycache__", ".pytest_cache", ".mypy_cache",
    "fixtures", ".venv", "venv", "env", "node_modules", "dist", "build",
}

PERMITTED_BINARIES: set = set()

GOVERNANCE_DIR = "governance"
GOVERNANCE_PERMITTED_SUFFIXES = {".md"}

APPROVAL_EVIDENCE_PATTERN = re.compile(r"ApprovalEvidence", re.IGNORECASE)


def _tracked_files():
    """Return repo-relative paths of files under review."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        )
        paths = [Path(p) for p in result.stdout.split("\0") if p]
        if paths:
            return paths
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return [
        p.relative_to(REPO_ROOT)
        for p in REPO_ROOT.rglob("*")
        if p.is_file()
        and not EXCLUDED_COMPONENTS.intersection(p.relative_to(REPO_ROOT).parts)
    ]


@pytest.fixture(scope="module")
def tracked():
    paths = _tracked_files()
    assert paths, "no files discovered; the fixture is wrong, not the repository"
    return paths


def test_no_rendered_documents_in_repository(tracked):
    """No rendered document format sits anywhere in the reviewed tree."""
    offences = [
        str(p) for p in tracked
        if p.suffix.lower() in RENDERED_DOCUMENT_SUFFIXES
        and str(p) not in PERMITTED_BINARIES
    ]
    assert not offences, (
        "SOP Section 7.3: rendered documents cannot be read as a diff and must "
        "not sit in a reviewed path. Generate them at distribution time "
        "instead:\n  " + "\n  ".join(sorted(offences))
    )


def test_governance_records_are_markdown_only(tracked):
    """The governance path holds records, and records are Markdown."""
    offences = [
        str(p) for p in tracked
        if p.parts and p.parts[0] == GOVERNANCE_DIR
        and p.suffix.lower() not in GOVERNANCE_PERMITTED_SUFFIXES
    ]
    assert not offences, (
        "Governance records are Markdown; renderings are generated at "
        "distribution time and executed approval evidence is held outside "
        "this repository (REG-DOC Notes):\n  " + "\n  ".join(sorted(offences))
    )


def test_no_signature_copy_lookalike(tracked):
    """No file in the repository can be mistaken for executed evidence."""
    offences = [
        str(p) for p in tracked
        if APPROVAL_EVIDENCE_PATTERN.search(p.name)
    ]
    assert not offences, (
        "SOP Section 7.3: a repository file a reader could mistake for the "
        "executed signature copy. Executed evidence is held outside this "
        "repository and cited by filename only:\n  "
        + "\n  ".join(sorted(offences))
    )


def test_no_undiffable_binaries_tracked(tracked):
    """Catch-all: every reviewed file is decodable as UTF-8 text."""
    offences = []
    for p in tracked:
        if str(p) in PERMITTED_BINARIES:
            continue
        full = REPO_ROOT / p
        if not full.is_file():
            continue
        try:
            full.read_text(encoding="utf-8")
        except (UnicodeDecodeError, ValueError):
            offences.append(str(p))
    assert not offences, (
        "SOP Section 7.3: file is not reviewable as a diff. Either generate "
        "it at distribution time, or add it to PERMITTED_BINARIES with a "
        "reason:\n  " + "\n  ".join(sorted(offences))
    )
