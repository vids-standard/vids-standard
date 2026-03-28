# VIDS Validation Rules (v1.0)

VIDS compliance is determined by running the reference validator.

A dataset is compliant if it has zero FAIL rules.

## Structure rules (S\*)

- S001: `.vids` marker exists.
- S002: `dataset_description.json` exists and includes required fields: `Name`, `VIDSVersion`, `DatasetVersion`, `License`, `Description`, `Authors`.
- S003: `participants.json` or `participants.tsv` exists.
- S004: `README.md` exists.
- S005: at least one `sub-*` directory exists.
- S006: each subject has at least one `ses-*` directory.

## Imaging rules (I\*)

- I001: imaging NIfTI exists per subject (`*_img.nii.gz` or `*_img.nii`).
- I002: imaging sidecar exists (`*_img.json`).
- I003: imaging sidecars are valid JSON.
- I004: naming convention check; non-conforming files are WARN in the validator.

## Annotation rules (A\*)

- A001: `derivatives/annotations/` exists.
- A002: segmentation files exist (`*_seg.nii.gz` or `*_seg.nii`).
- A003: segmentation sidecars exist (`*_seg.json`).
- A004: segmentation sidecars are valid JSON and include `VIDSVersion`.
- A005: provenance completeness: annotator identity and tool/date recorded (minimums).

## Quality rules (Q\*) — Full only

- Q001: `quality/` exists.
- Q002: `quality/quality_summary.json` exists.
- Q003: `quality/annotation_agreement.json` exists.

## ML rules (M\*) — Full only

- M001: `ml/` exists.
- M002: `ml/splits.json` exists.

## Metadata rule (D\*)

- D001: `CHANGES.md` exists; missing is WARN (recommended).
