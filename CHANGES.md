# Changes

## Errata

### 2026-07-09 — re: [v1.2], A004 / A005

The v1.2 entry below describes the A004 and A005 changes as "generalized." That
wording understates their effect and is corrected here.

Prior to v1.2, A004 and A005 inspected only `*_seg.json`. From v1.2 they inspect
every annotation sidecar across all five spec-defined suffixes. SPEC §10.1 has
marked `VIDSVersion` and `Provenance` **REQUIRED** on every annotation sidecar
since VIDS 1.0, so v1.2 brought the validator into conformance with the
specification. It was a **validator conformance correction for previously
under-enforced REQUIRED annotation-sidecar fields**, and it is ratified as the
intended architecture.

It also produced **new FAIL outcomes**, which the original entry did not state.
A dataset carrying a `_bbox`, `_cls`, `_lm`, or `_roi` sidecar without
`VIDSVersion` or a conformant `Provenance` block passes under validator 1.1.x
and fails under 1.2.x.

No published VIDS dataset is affected. LIDC-Hybrid-100 is segmentation-only and
validates 21/21 under 1.2.1. The IDRiD fundus reference implementation validates
15/21 PASS under 1.2.1.

See SPEC.md §15.3 and the Backward Compatibility Guarantee in CONTRIBUTING.md.

---

## [v1.2] — 2026-05-20

Validator and scaffolding tool both extended to cover all five spec-defined
annotation suffixes (`_seg`, `_cls`, `_bbox`, `_lm`, `_roi`) uniformly.

### Validator (`validators/validate_vids.py`)

- A002 generalized: detects any spec-defined annotation file across all five
  suffixes. Pass message reports per-type counts (e.g.,
  `Annotations found (40 seg, 80 cls)`).
- A003 generalized: pairs `_seg.nii.gz`/`_seg.nii` binaries with their
  `_seg.json` sidecars. JSON-only annotations (`_cls`, `_bbox`, `_lm`, `_roi`)
  are self-sidecared and satisfy the rule trivially.
- A004 generalized: JSON validity and `VIDSVersion` presence checked across
  all annotation sidecars.
- A005 generalized: provenance completeness checked across all annotation
  sidecars (Provenance schema is shape-identical across types per spec §10.2).
- `ValidatorVersion` bumped from `1.1` to `1.2`.

### Scaffolding (`tools/vids_init.py`)

- New `--annotation-type {seg|cls|bbox|lm|roi}` CLI flag, default `seg`.
- For `seg`: existing behavior preserved byte-for-byte — NIfTI mask stub
  plus the v1.1 rich JSON sidecar (`Annotator.Specialty`,
  `AnnotationProcess.TimeSpent_minutes`, `QualityControl` block all retained).
- For `cls`, `bbox`, `lm`, `roi`: a single JSON sidecar is generated with
  the type-specific payload key (`Classifications`, `BoundingBoxes`,
  `Landmarks`, `Regions`) and populated placeholder provenance; no NIfTI
  annotation stub since the file is the annotation.
- Scaffold output (README, CHANGES.md, "Next steps" guidance) reflects the
  chosen paradigm.

### Test infrastructure (`tests/`)

- `generate_test_fixtures.py` produces four new POC fixtures
  (`example-classification`, `example-detection`, `example-landmark`,
  `example-roi`) plus a `negative/` suite of five intentionally-malformed
  fixtures covering A002–A005 failure modes.
- `test_validator.py` adds `TestClassificationProfile`,
  `TestDetectionProfile`, `TestLandmarkProfile`, `TestROIProfile`,
  `TestScaffolding` (end-to-end `vids_init` → validator), and
  `TestNegativeFixtures`. 26 tests total, all passing.

### What did not change

- The v1.0 specification (`SPEC.md`) is unchanged. Appendix B already
  defined all five annotation suffixes; this release is enforcement parity,
  not spec extension.
- File layout, directory structure, and sidecar schemas are unchanged.
- All non-annotation rules (S, I, Q, M, D) are unchanged.

### Backward compatibility

- Datasets that validated under v1.1 continue to validate under v1.2 with
  `Status: PASS`.
- The default `vids-init` invocation (`--annotation-type seg` implicit)
  produces a scaffold that is byte-identical to v1.1.
- Existing v1.0-compliant datasets do not require migration.

### Forward compatibility

- Datasets using only non-segmentation annotation suffixes
  (`_cls` / `_bbox` / `_lm` / `_roi`) — which previously failed A002
  silently — now validate when otherwise well-formed.
