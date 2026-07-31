# Contributing to VIDS

Thank you for your interest in improving the Verified Imaging Dataset Standard. This document explains how to contribute and how the project is governed.

## How to Contribute

### Reporting Issues

Open a GitHub issue for:

- **Spec ambiguities** - wording that could be interpreted in conflicting ways
- **Validator bugs** - cases where the validator produces incorrect PASS/FAIL/WARN results
- **Missing modality support** - imaging modalities not covered by the current spec
- **Documentation gaps** - missing examples, unclear instructions, broken links

Use descriptive titles and include enough context to reproduce the issue.

### Proposing Changes

**Spec changes** (normative requirements, validation rules, JSON schemas):

1. Open a GitHub issue describing the proposed change and its rationale.
2. Label it `spec-change`. The maintainers will assess impact and assign a milestone.
3. If approved, submit a pull request against `SPEC.md` (and supporting docs if needed).
4. All spec changes require at least one maintainer review before merge.

**Validator changes** (bug fixes, new checks, performance improvements):

1. Fork the repository and create a branch from `main`.
2. Make your changes to `validators/validate_vids.py`.
3. Regenerate the fixtures with `python tests/generate_test_fixtures.py`, then verify both still pass: `python validators/validate_vids.py tests/fixtures/example-poc` and `python validators/validate_vids.py tests/fixtures/example-full --profile full`. Run the unit tests with `python -m pytest tests/`.
4. Submit a pull request with a clear description of the change.

**Documentation changes** (typos, clarifications, new examples):

- Small fixes: submit a pull request directly.
- Larger additions: open an issue first to discuss scope.

### Adding Modality Support

To propose a new modality code:

1. Open an issue titled `[Modality] <modality name>`.
2. Include: proposed code (e.g., `oct`), full modality name, any domain-specific `Characteristics` fields, and an example annotation sidecar JSON.
3. If accepted, the code is added to Appendix A and FILE_NAMING.md.

Custom modality codes can always be used immediately by documenting them in `dataset_description.json` under `CustomModalities` - formal addition to the spec just makes them standard.

### Adding Framework Integrations

We welcome export/loader contributions for ML frameworks (nnU-Net, MONAI, TorchIO, Hugging Face datasets, etc.). These belong in a separate `vids-tools` package - not in this spec repository. Contact the maintainers to coordinate.

## Pull Request Guidelines

- One logical change per pull request.
- Keep diffs minimal - don't reformat unrelated lines.
- If your PR modifies `SPEC.md`, explain whether the change is normative (affects conformance) or editorial (clarification only).
- If your PR modifies the validator, include before/after validation output for both example datasets.
- All PRs require at least one maintainer approval.

## Governance

The full governance model, including the artifact taxonomy (SPEC, MD, CN, SOP, REG) and the Normative Principle that only the Core Specification creates conformance requirements, is defined in GOVERNANCE.md. Governance decisions are recorded as Maintainer Decisions (MDs); adopter-facing impact of changes is recorded in Change Notes (CNs).

### Project Roles

**Steering Committee** - Responsible for reviewing and merging pull requests, deciding on spec changes and version increments, and managing releases and the canonical URL (vidsstandard.org). Current composition is recorded in GOVERNANCE.md Section 7 and established by Maintainer Decision; it is not restated here, so there is one place to read it and one place to change it. All members hold governance signatory authority. As the community grows, additional seats will be added to ensure representation from academic, clinical, and industry stakeholders.

**Maintainers** - Individuals with merge access to the repository. All current Steering Committee members are maintainers. External contributors can become maintainers (see below).

**Contributors** - Anyone who submits an accepted issue or pull request. Listed in `CONTRIBUTORS.md` (created after the first external contribution).

**Advisory Council** - Independent experts advising on strategy, clinical relevance, and adoption. The Council holds no normative vote and its members serve as individuals, not as representatives of their employers.

**Community** - Anyone using VIDS, providing feedback, or building tools around it.

### Path to Maintainership

Active contributors who demonstrate sustained, high-quality contributions may be nominated as maintainers by any existing Steering Committee member. Criteria include: multiple accepted PRs across spec or tools, constructive participation in spec-change discussions, and demonstrated understanding of the VIDS design principles. Nominations are decided by Steering Committee consensus.

### Decision Process

- **Editorial changes** (typos, clarifications, example improvements): merged by any maintainer.
- **Minor spec changes** (new optional fields, new modality codes, new annotation suffixes): discussed in a GitHub issue, decided by Steering Committee consensus.
- **Major spec changes** (new required fields, new validation rules, breaking changes): discussed in a GitHub issue with a minimum 30-day comment period, decided by Steering Committee consensus with consideration of community feedback.

The long-term governance model is a VIDS Consortium with formal representation from academic institutions, clinical organizations, and industry adopters. The transition to consortium governance will be initiated once VIDS has active external maintainers and multiple independent implementations.

## Versioning

VIDS follows semantic versioning for both the specification and the validator:

### Specification

| Change Type | Version Increment | Examples |
|------------|-------------------|---------|
| **Major** (X.0.0) | Breaking changes | New required fields, removed rules, restructured directories |
| **Minor** (1.X.0) | Backward-compatible additions | New optional fields, new modality codes, new annotation types |
| **Patch** (1.0.X) | Editorial only | Typo fixes, clarifications, example corrections |

### Backward Compatibility Guarantee

Datasets valid under VIDS 1.0 will remain valid under all VIDS 1.x validators. Breaking changes require a major version increment, a documented migration path, and a 90-day deprecation notice.

**Erratum (2026-07-09).** "Valid" means conformant to the specification, not merely passing under a given validator build. A dataset that passed only because a prior validator under-enforced a REQUIRED annotation-sidecar field is not protected by this guarantee. See SPEC.md Section 15.3.

### Validator Versioning

The validator tracks its own version independently from the spec. The validator version is reported in its JSON output (`ValidatorVersion` field). Validator updates that don't change rule behavior are patch increments; new rules or changed pass/fail logic are minor or major increments.

## Code of Conduct

Be professional and constructive. We're building a standard for medical AI - the stakes are real. Assume good intent, provide evidence for claims, and focus on improving the standard rather than winning arguments.

## Contact

- **GitHub Issues** - Preferred for all technical discussions
- **Email** - standards@vidsstandard.org (for partnership or governance inquiries)

---

## Change log

| Date | Change |
|------|--------|
| 2026-07-31 | Steering Committee composition removed from Project Roles and cross-referenced to GOVERNANCE.md Section 7, per MD-0005. Two regressions against `main` corrected before merge: the contributor verification step had been changed to `examples/poc` and `examples/full`, which do not exist in the repository, and the 2026-07-09 backward-compatibility erratum had been dropped. Both restored, and the unit-test run added to the verification step. No change to the contribution process, decision thresholds, or versioning rules. |
| 2026-07-26 | Canonical URL corrected to vidsstandard.org (retired domain removed); contact email updated to standards@vidsstandard.org; conformance vocabulary applied; governance section cross-referenced to GOVERNANCE.md and the artifact taxonomy; Advisory Council added to project roles; punctuation normalized. No change to the contribution process, decision thresholds, or versioning rules. |

---

**VIDS was created by Princeton Medical Systems and is maintained as an open community standard.**
