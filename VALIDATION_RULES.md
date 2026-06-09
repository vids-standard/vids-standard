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
- A005: all annotation sidecars have populated provenance fields: `Annotator.ID` or `Annotator.Name`, and `AnnotationProcess.Date` or `AnnotationProcess.Tool`. These fields must carry a non-empty value. Empty strings, null values, or missing fields do not satisfy the rule, since the check tests for a populated value rather than mere key presence. Provenance schema is identical across all annotation types (spec §10.2).

## Quality rules (Q\*) — Full only

- Q001: `quality/` exists.
- Q002: `quality/quality_summary.json` exists.
- Q003: `quality/annotation_agreement.json` exists.

## ML rules (M\*) — Full only

- M001: `ml/` exists.
- M002: `ml/splits.json` exists.

## Metadata rule (D\*)

- D001: `CHANGES.md` exists; missing is WARN (recommended). SKIP under the POC profile.

## Conformance Boundary

VIDS validation is a structural and documentation-conformance check. It determines whether a dataset contains the files, fields, metadata, provenance records, and quality artifacts required by the selected VIDS profile. It does not independently verify the clinical, scientific, or statistical truth of the values reported in those artifacts.

This follows the same general validation boundary used in mature imaging standards such as DICOM: validators can check whether required elements are present and syntactically valid, but they do not generally prove that every supplied value is clinically correct or semantically true.

A VIDS PASS therefore asserts that the dataset satisfies the machine-checkable requirements of the selected VIDS profile. It does not assert that:

- image data are clinically correct;
- annotations are clinically accurate;
- annotator credentials are independently verified;
- extension fields are semantically validated beyond their documented structure;
- reported quality metrics, including Dice scores or pass-rate values, are independently recomputed or plausible.

Extension fields may be present and useful for downstream review, procurement, or audit workflows, but their presence in a VIDS-valid dataset should not be interpreted as VIDS validation of their clinical or scientific truth.
