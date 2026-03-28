# Contributing to VIDS

Thank you for your interest in improving the Verified Imaging Dataset Standard. This document explains how to contribute and how the project is governed.

## How to Contribute

### Reporting Issues

Open a GitHub issue for:

- **Spec ambiguities** — wording that could be interpreted in conflicting ways
- **Validator bugs** — cases where the validator produces incorrect PASS/FAIL/WARN results
- **Missing modality support** — imaging modalities not covered by the current spec
- **Documentation gaps** — missing examples, unclear instructions, broken links

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
3. Verify both example datasets still pass: `python validators/validate_vids.py examples/poc` and `python validators/validate_vids.py examples/full --profile full`.
4. Submit a pull request with a clear description of the change.

**Documentation changes** (typos, clarifications, new examples):

- Small fixes: submit a pull request directly.
- Larger additions: open an issue first to discuss scope.

### Adding Modality Support

To propose a new modality code:

1. Open an issue titled `[Modality] <modality name>`.
2. Include: proposed code (e.g., `oct`), full modality name, any domain-specific `Characteristics` fields, and an example annotation sidecar JSON.
3. If accepted, the code is added to Appendix A and FILE_NAMING.md.

Custom modality codes can always be used immediately by documenting them in `dataset_description.json` under `CustomModalities` — formal addition to the spec just makes them standard.

### Adding Framework Integrations

We welcome export/loader contributions for ML frameworks (nnU-Net, MONAI, TorchIO, Hugging Face datasets, etc.). These belong in a separate `vids-tools` package — not in this spec repository. Contact the maintainers to coordinate.

## Pull Request Guidelines

- One logical change per pull request.
- Keep diffs minimal — don't reformat unrelated lines.
- If your PR modifies `SPEC.md`, explain whether the change is normative (affects compliance) or editorial (clarification only).
- If your PR modifies the validator, include before/after validation output for both example datasets.
- All PRs require at least one maintainer approval.

## Governance

### Project Roles

**Steering Committee** — Responsible for reviewing and merging pull requests, deciding on spec changes and version increments, and managing releases and the canonical URL (vids.ai). The Steering Committee currently consists of Princeton Medical Systems, the original authors of VIDS. As the community grows, additional seats will be added to ensure representation from academic, clinical, and industry stakeholders.

**Maintainers** — Individuals with merge access to the repository. All current Steering Committee members are maintainers. External contributors can become maintainers (see below).

**Contributors** — Anyone who submits an accepted issue or pull request. Listed in `CONTRIBUTORS.md` (created after the first external contribution).

**Community** — Anyone using VIDS, providing feedback, or building tools around it.

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

### Validator Versioning

The validator tracks its own version independently from the spec. The validator version is reported in its JSON output (`ValidatorVersion` field). Validator updates that don't change rule behavior are patch increments; new rules or changed pass/fail logic are minor or major increments.

## Code of Conduct

Be professional and constructive. We're building a standard for medical AI — the stakes are real. Assume good intent, provide evidence for claims, and focus on improving the standard rather than winning arguments.

## Contact

- **GitHub Issues** — Preferred for all technical discussions
- **Email** — info@princetonmed.systems (for partnership or governance inquiries)

---

**VIDS was created by Princeton Medical Systems and is maintained as an open community standard.**
