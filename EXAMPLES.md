# VIDS Example Datasets (v1.0)

This document contains complete, minimal example datasets for both VIDS profiles. Every file shown here passes the reference validator (`validate_vids.py`). NIfTI files (`.nii.gz`) are binary and cannot be inlined — placeholder stubs are noted where they belong.

---

## POC Profile Example

### Directory structure

```text
example-poc/
├── .vids
├── dataset_description.json
├── participants.json
├── README.md
├── sub-001/
│   └── ses-baseline/
│       └── ct/
│           ├── sub-001_ses-baseline_ct_img.nii.gz   ← binary stub
│           └── sub-001_ses-baseline_ct_img.json
└── derivatives/
    └── annotations/
        └── sub-001/
            └── ses-baseline/
                └── ct/
                    ├── sub-001_ses-baseline_ct_seg.nii.gz   ← binary stub
                    └── sub-001_ses-baseline_ct_seg.json
```

### `.vids`

```text
profile: poc
vids_version: 1.0
```

### `dataset_description.json`

```json
{
  "Name": "Example POC Dataset",
  "VIDSVersion": "1.0",
  "DatasetVersion": "1.0.0",
  "License": "CC BY 4.0",
  "Description": "Minimal single-subject POC dataset for VIDS validation testing.",
  "Authors": ["VIDS Examples Working Group"]
}
```

### `participants.json`

```json
{
  "VIDSVersion": "1.0",
  "Participants": [
    {
      "SubjectID": "sub-001",
      "Age": 62,
      "Sex": "F",
      "InclusionCriteria": "Non-contrast chest CT, slice thickness ≤2.5mm",
      "DataSource": "Synthetic example"
    }
  ]
}
```

### `README.md`

```markdown
# Example POC Dataset

Minimal VIDS-compliant dataset with one subject, one session, and one CT modality.

## Contents

- 1 subject (sub-001), 1 session (ses-baseline), CT modality
- Segmentation annotation with full provenance

## Purpose

Validator test fixture and reference for VIDS POC profile compliance.

## Contact

standards@vidsstandard.org
```

### `sub-001/ses-baseline/ct/sub-001_ses-baseline_ct_img.json`

```json
{
  "VIDSVersion": "1.0",
  "SourceFormat": "DICOM",
  "ConversionTool": "dcm2niix v1.0.20240202",
  "ConversionDate": "2026-02-10",
  "AcquisitionParameters": {
    "SliceThickness_mm": 1.25,
    "PixelSpacing_mm": [0.7, 0.7],
    "ImageDimensions": [512, 512, 300],
    "KVP": 120,
    "ContrastEnhanced": false,
    "ReconstructionKernel": "standard",
    "Manufacturer": "Siemens",
    "ManufacturerModel": "SOMATOM Force",
    "MagneticFieldStrength_T": null
  },
  "QualityAssessment": {
    "ImageQuality": "good",
    "Artifacts": "none",
    "DiagnosticQuality": true
  },
  "DeIdentification": {
    "Method": "HIPAA Safe Harbor",
    "Tool": "dcm2niix",
    "Date": "2026-02-10",
    "VerifiedBy": "data_curator_001"
  }
}
```

### `derivatives/annotations/sub-001/ses-baseline/ct/sub-001_ses-baseline_ct_seg.json`

```json
{
  "VIDSVersion": "1.0",
  "AnnotationType": "segmentation",
  "Description": "Lung nodule segmentation for sub-001 baseline CT.",
  "SourceImage": "sub-001_ses-baseline_ct_img.nii.gz",
  "LabelMap": {
    "0": "background",
    "1": "nodule"
  },
  "Provenance": {
    "Annotator": {
      "ID": "radiologist_001",
      "Name": "Dr. Jane Smith",
      "Credentials": "MD, Board-certified radiologist, 10 years experience",
      "Specialty": "Chest Radiology"
    },
    "AnnotationProcess": {
      "Tool": "3D Slicer",
      "ToolVersion": "5.6.2",
      "Date": "2026-02-12",
      "TimeSpent_minutes": 15,
      "Method": "Manual segmentation"
    },
    "QualityControl": {
      "ReviewedBy": "senior_radiologist_001",
      "ReviewDate": "2026-02-13",
      "ReviewOutcome": "approved",
      "Confidence": 0.93
    }
  },
  "Annotations": [
    {
      "ID": "nodule_001",
      "Type": "nodule",
      "Location": {
        "Lobe": "RUL",
        "Segment": "apical"
      },
      "Characteristics": {
        "Size_mm": {
          "max_diameter": 11.2,
          "volume_mm3": 540.3
        },
        "Morphology": {
          "Shape": "round",
          "Margin": "smooth",
          "Density": "solid"
        }
      }
    }
  ]
}
```

### Validation rules covered (POC)

| Rule | Status |
|------|--------|
| S001 `.vids` marker | PASS |
| S002 `dataset_description.json` | PASS |
| S003 `participants.json` | PASS |
| S004 `README.md` | PASS |
| S005 Subject directories | PASS |
| S006 Session directories | PASS |
| I001 Imaging NIfTI | PASS |
| I002 Imaging sidecar | PASS |
| I003 Imaging JSON valid | PASS |
| I004 Naming convention | PASS |
| A001 `derivatives/annotations/` | PASS |
| A002 Segmentation files | PASS |
| A003 Annotation sidecars | PASS |
| A004 Annotation JSON valid + `VIDSVersion` | PASS |
| A005 Provenance complete | PASS |
| Q001–Q003 | SKIP (POC) |
| M001–M002 | SKIP (POC) |
| D001 `CHANGES.md` | WARN (recommended) |

---

## Full Profile Example

The Full profile extends POC by adding `quality/` and `ml/` directories.

### Additional directory structure

```text
example-full/
├── .vids
├── dataset_description.json
├── participants.json
├── README.md
├── CHANGES.md
├── sub-001/
│   └── ses-baseline/
│       └── ct/
│           ├── sub-001_ses-baseline_ct_img.nii.gz   ← binary stub
│           └── sub-001_ses-baseline_ct_img.json
├── derivatives/
│   └── annotations/
│       └── sub-001/
│           └── ses-baseline/
│               └── ct/
│                   ├── sub-001_ses-baseline_ct_seg.nii.gz   ← binary stub
│                   └── sub-001_ses-baseline_ct_seg.json
├── quality/
│   ├── quality_summary.json
│   └── annotation_agreement.json
└── ml/
    └── splits.json
```

### `.vids`

```text
profile: full
vids_version: 1.0
```

### `dataset_description.json`

Same as POC, with `"Description"` updated:

```json
{
  "Name": "Example Full Dataset",
  "VIDSVersion": "1.0",
  "DatasetVersion": "1.0.0",
  "License": "CC BY 4.0",
  "Description": "Minimal single-subject Full profile dataset for VIDS validation testing.",
  "Authors": ["VIDS Examples Working Group"]
}
```

### `participants.json`

Same as POC example above.

### `README.md`

Same structure as POC, updated to reference Full profile.

### `CHANGES.md`

```markdown
# Changes

## [1.0.0] - 2026-02-16
- Initial release
- 1 subject with lung nodule segmentation
- Quality documentation and ML splits included
```

### Imaging sidecar and annotation sidecar

Same as POC examples above.

### `quality/quality_summary.json`

```json
{
  "VIDSVersion": "1.0",
  "Profile": "full",
  "DatasetName": "Example Full Dataset",
  "DatasetVersion": "1.0.0",
  "QualityAssessmentDate": "2026-02-15",
  "AnnotationStatistics": {
    "TotalSubjects": 1,
    "TotalAnnotations": 1,
    "SubjectsWithAnnotations": 1,
    "SubjectsWithoutAnnotations": 0,
    "AnnotationsPerSubject": {
      "Mean": 1.0,
      "StandardDeviation": 0.0,
      "Min": 1,
      "Max": 1,
      "Median": 1
    }
  },
  "QualityControlMetrics": {
    "QCReviewer": {
      "Name": "Dr. Senior Reviewer",
      "Credentials": "MD, 15 years experience",
      "Specialty": "Chest Radiology"
    },
    "QCProcess": {
      "ReviewPercentage": 100,
      "DoubleAnnotationPercentage": 100,
      "ReviewMethod": "Visual inspection + measurement verification"
    },
    "PassRates": {
      "FirstSubmissionPassRate": 1.0,
      "AfterRevisionPassRate": 1.0,
      "TotalRevisionsRequired": 0
    }
  },
  "InterAnnotatorAgreement": {
    "Method": "Dice Coefficient",
    "SampleSize": 1,
    "DiceStatistics": {
      "Mean": 0.91,
      "StandardDeviation": 0.0,
      "Min": 0.91,
      "Max": 0.91
    },
    "QualityThresholds": {
      "Target": 0.85,
      "Acceptable": 0.75
    }
  },
  "ValidationResults": {
    "VIDSValidator": {
      "Version": "1.1",
      "Profile": "full",
      "TotalRules": 21,
      "RulesPassed": 21,
      "RulesFailed": 0,
      "ValidationStatus": "PASS"
    }
  },
  "CertificationStatement": "This dataset meets VIDS Full profile requirements.",
  "CertifiedBy": {
    "Name": "Data Quality Lead",
    "Role": "QC Manager",
    "Date": "2026-02-16"
  }
}
```

### `quality/annotation_agreement.json`

```json
{
  "VIDSVersion": "1.0",
  "Methodology": {
    "Method": "Dice Coefficient",
    "SamplingStrategy": "All subjects (100%)",
    "Tool": "Custom Python script using SimpleITK"
  },
  "Annotators": [
    {
      "ID": "radiologist_001",
      "Role": "Primary annotator",
      "Credentials": "MD, Board-certified radiologist"
    },
    {
      "ID": "senior_radiologist_001",
      "Role": "Reviewer / second annotator",
      "Credentials": "MD, 15 years thoracic radiology"
    }
  ],
  "SampleSelection": {
    "TotalSubjects": 1,
    "DoubleAnnotatedSubjects": 1,
    "SelectionMethod": "All subjects double-annotated"
  },
  "AggregateStatistics": {
    "Mean": 0.91,
    "StandardDeviation": 0.0,
    "Min": 0.91,
    "Max": 0.91
  },
  "PerSubjectResults": [
    {
      "SubjectID": "sub-001",
      "SessionID": "ses-baseline",
      "DiceCoefficient": 0.91,
      "Quality": "excellent"
    }
  ],
  "QualityThresholds": {
    "Excellent": 0.90,
    "Good": 0.85,
    "Acceptable": 0.75,
    "Poor_below": 0.75
  }
}
```

### `ml/splits.json`

```json
{
  "VIDSVersion": "1.0",
  "SplitStrategy": "single-subject-example",
  "SplitRatio": "100/0/0",
  "RandomSeed": 42,
  "Splits": {
    "train": ["sub-001"],
    "val": [],
    "test": []
  },
  "Notes": "Minimal example with one subject. Real datasets should use 70/15/15 or similar splits."
}
```

### Validation rules covered (Full)

| Rule | Status |
|------|--------|
| S001–S006 | PASS |
| I001–I004 | PASS |
| A001–A005 | PASS |
| Q001 `quality/` | PASS |
| Q002 `quality_summary.json` | PASS |
| Q003 `annotation_agreement.json` | PASS |
| M001 `ml/` | PASS |
| M002 `ml/splits.json` | PASS |
| D001 `CHANGES.md` | PASS |

---

## Notes

- **Binary stubs:** The `.nii.gz` files are not represented here. When generating a testable dataset, create minimal NIfTI files (e.g., a 2×2×2 voxel volume using nibabel or similar).
- **Reuse:** POC and Full share the same imaging sidecar, annotation sidecar, and participants file. The Full profile adds `quality/`, `ml/`, and `CHANGES.md`.
- **Validator command:** `python validate_vids.py example-poc` and `python validate_vids.py example-full --profile full`.
