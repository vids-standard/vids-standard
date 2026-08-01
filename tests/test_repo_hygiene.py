#!/usr/bin/env python3
"""
Enforcement tests for the standing operating routine prohibiting unreviewable
artifacts in reviewed paths.

The routine: any file that cannot be read as a diff in review must not sit in a
path where review is the control. Either it is generated at distribution time,
or CI regenerates it and fails on divergence.

The routine further states that CI must not push commits back to a protected
branch to satisfy it. These tests therefore fail the build; they do not
regenerate or delete anything.

The routine also names a specific hazard: a repository PDF sitting beside a
record whose sign-off cites `MD-NNNN-ApprovalEvidence-YYYY-MM-DD.pdf` is a
file a reader could mistake for the executed signature copy. The executed
instrument is held outside this repository and cited by filename only.

The routine is SOP-class operating practice, not a normative rule: no adopted
decision created it, and it creates no dataset conformance requirement. It is
not yet registered as a numbered SOP artifact in REG-DOC, so it is referred to
here by description rather than by an identifier that would not resolve. When
it is registered, replace these references with the SOP ID in one pass.

Without these tests the routine is a statement of intent. Eight rendered PDFs
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

ROUTINE = "no unreviewable artifacts in a reviewed path"

# Rendered document formats. Each duplicates a canonical source, cannot be
# reviewed as a diff, and carries the signature-copy hazard when it lands
# beside a governance record.
RENDERED_DOCUMENT_SUFFIXES = {
    ".pdf",
    ".doc", ".docx",
    ".ppt", ".pptx",
    ".xls", ".xlsx",
    ".odt", ".odp", ".ods",
    ".rtf",
    ".pages", ".key", ".numbers",
}

# Paths that are generated or otherwise outside the reviewed set. Matched
# against any component of a relative path.
EXCLUDED_COMPONENTS = {
    ".git", "__pycache__", ".pytest_cache", ".mypy_cache",
    "fixtures", ".venv", "venv", "env", "node_modules", "dist", "build",
}

# Tracked binaries permitted by explicit exception. Empty by design: the
# repository contains none.
#
# The routine provides no exception path. An entry here therefore admits a
# file the routine excludes, which is a scope call and belongs in a Maintainer
# Decision rather than in a code review. Cite the MD beside any entry added.
PERMITTED_BINARIES: set = set()

# The governance path holds records, and records are Markdown.
#
# Machine-readable derivatives are permitted alongside them. GOVERNANCE.md
# Section 4 anticipates them explicitly ("REG-DOC.json ... script-generated
# derivatives with a divergence-failing verifier"), and that shape is the
# second remedy the routine allows: generated, with CI failing on divergence.
# Rendered documents remain blocked here by the repository-wide rule above.
GOVERNANCE_DIR = "governance"
GOVERNANCE_PERMITTED_SUFFIXES = {".md", ".json", ".yaml", ".yml"}

APPROVAL_EVIDENCE_PATTERN = re.compile(r"ApprovalEvidence", re.IGNORECASE)


def _tracked_files():
    """Return repo-relative paths of files under review.

    Uses `git ls-files` where a work tree is available, which is the accurate
    definition of "in a reviewed path". Falls back to a filtered walk so the
    tests still run against an exported tree.
    """
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
        f"Standing routine ({ROUTINE}): rendered documents cannot be read as a "
        "diff and must not sit in a reviewed path. Generate them at "
        "distribution time instead:\n  " + "\n  ".join(sorted(offences))
    )


def test_governance_records_are_markdown_only(tracked):
    """The governance path holds records, and records are Markdown."""
    offences = [
        str(p) for p in tracked
        if p.parts and p.parts[0] == GOVERNANCE_DIR
        and p.suffix.lower() not in GOVERNANCE_PERMITTED_SUFFIXES
    ]
    assert not offences, (
        "Governance records are Markdown, with machine-readable derivatives "
        "permitted alongside them. Renderings are generated at distribution "
        "time and executed approval evidence is held outside this repository "
        "(REG-DOC Notes):\n  " + "\n  ".join(sorted(offences))
    )


def test_no_signature_copy_lookalike(tracked):
    """No file in the repository can be mistaken for executed evidence.

    Guards the specific hazard the routine names. The executed instrument lives
    outside the repository and is cited by filename only, so a file bearing
    that name here is either a duplicate or a leak.
    """
    offences = [
        str(p) for p in tracked
        if APPROVAL_EVIDENCE_PATTERN.search(p.name)
    ]
    assert not offences, (
        f"Standing routine ({ROUTINE}): a repository file a reader could mistake "
        "for the executed signature copy. Executed evidence is held outside "
        "this repository and cited by filename only:\n  "
        + "\n  ".join(sorted(offences))
    )


def test_no_undiffable_binaries_tracked(tracked):
    """Catch-all: every reviewed file is decodable as UTF-8 text.

    Broader than the suffix list above, so a new undiffable format cannot
    enter the repository without failing here first. Adding a permitted
    binary requires editing PERMITTED_BINARIES, which is itself a reviewable
    diff.
    """
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
        f"Standing routine ({ROUTINE}): file is not reviewable as a diff. Either "
        "generate it at distribution time, or add it to PERMITTED_BINARIES "
        "under a Maintainer Decision:\n  " + "\n  ".join(sorted(offences))
    )
