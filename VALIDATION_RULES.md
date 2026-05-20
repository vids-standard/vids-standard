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
- A002: at least one annotation file exists across the five spec-defined suffixes — `*_seg.nii.gz`, `*_seg.nii`, `*_cls.json`, `*_bbox.json`, `*_lm.json`, or `*_roi.json`.
- A003: every binary annotation file (`*_seg.nii.gz`, `*_seg.nii`) has its paired sidecar JSON. JSON-only annotation files (`*_cls.json`, `*_bbox.json`, `*_lm.json`, `*_roi.json`) are sidecars themselves and satisfy this rule trivially.
- A004: all annotation sidecars (across all five suffixes) parse as valid JSON and contain the `VIDSVersion` field.
- A005: all annotation sidecars have populated provenance fields: `Annotator.ID` or `Annotator.Name`, and `AnnotationProcess.Date` or `AnnotationProcess.Tool`. Provenance schema is identical across all annotation types (spec §10.2).

## Quality rules (Q\*) — Full only

- Q001: `quality/` exists.
- Q002: `quality/quality_summary.json` exists.
- Q003: `quality/annotation_agreement.json` exists.

## ML rules (M\*) — Full only

- M001: `ml/` exists.
- M002: `ml/splits.json` exists.

## Metadata rule (D\*)

- D001: `CHANGES.md` exists; missing is WARN (recommended).
