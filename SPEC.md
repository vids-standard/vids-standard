# VIDS — Verified Imaging Dataset Standard

## Specification v1.0

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Release |
| **Date** | 2026-02-16 |
| **Authors** | Princeton Medical Systems |
| **License** | CC BY 4.0 (Specification/Docs) / Apache-2.0 (Tools) |
| **Canonical URL** | https://vids.ai/spec/1.0 |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Scope](#2-scope)
3. [Terminology and Conventions](#3-terminology-and-conventions)
4. [Dataset Root Structure](#4-dataset-root-structure)
5. [File Naming Conventions](#5-file-naming-conventions)
6. [Root-Level Required Files](#6-root-level-required-files)
7. [Subject and Session Layout](#7-subject-and-session-layout)
8. [Imaging Files](#8-imaging-files)
9. [Annotation Files](#9-annotation-files)
10. [Annotation Sidecar JSON Schema](#10-annotation-sidecar-json-schema)
11. [Quality Documentation](#11-quality-documentation)
12. [ML Readiness Files](#12-ml-readiness-files)
13. [Compliance Profiles](#13-compliance-profiles)
14. [Validation Rules](#14-validation-rules)
15. [Versioning Policy](#15-versioning-policy)
16. [Extension Mechanism](#16-extension-mechanism)
17. [Export and Interoperability](#17-export-and-interoperability)
18. [Appendix A: Modality Codes](#appendix-a-modality-codes)
19. [Appendix B: Annotation Type Suffixes](#appendix-b-annotation-type-suffixes)
20. [Appendix C: Complete Folder Reference](#appendix-c-complete-folder-reference)
21. [Appendix D: JSON Schema Quick Reference](#appendix-d-json-schema-quick-reference)

---

## 1. Introduction

### 1.1 Purpose

VIDS (Verified Imaging Dataset Standard) defines a complete, enforceable structure for organizing medical imaging datasets intended for AI/ML development. It specifies folder layout, file naming, metadata schemas, annotation provenance, quality documentation, and validation rules.

VIDS addresses a critical gap in the medical imaging AI ecosystem: there is no existing standard that simultaneously covers dataset structure, annotation provenance, quality metrics, and ML readiness. DICOM handles image storage. BIDS handles neuroimaging research organization. Neither handles annotated datasets for AI training with documented provenance and quality assurance.

### 1.2 Design Principles

VIDS is built on five principles:

1. **Provenance is mandatory, not optional.** Every annotation must document who created it, when, with what tool, and under what quality controls. This is not metadata — it is a first-class requirement.

2. **Validation is automated.** Compliance is determined by running a validator, not by reading a checklist. If the validator passes, the dataset is compliant.

3. **The standard is format-agnostic at delivery.** VIDS defines a canonical internal structure. Datasets curated in VIDS can be exported to any downstream format (nnU-Net, MONAI, COCO, flat NIfTI) without loss of provenance.

4. **Profiles enable incremental adoption.** The POC profile requires 15 rules. The Full profile requires all 21. Organizations can start at POC and graduate to Full.

5. **The standard complements, not replaces.** VIDS works with NIfTI (file format), DICOM (source data), BIDS (naming inspiration), and existing ML frameworks. It does not require abandoning any existing tool.

### 1.3 Relationship to Other Standards

| Standard | Relationship |
|----------|-------------|
| **DICOM** | VIDS datasets may originate from DICOM sources. DICOM handles acquisition and storage; VIDS handles annotation and curation. |
| **BIDS** | VIDS adopts BIDS-inspired naming (`sub-`, `ses-`) and sidecar JSON conventions. VIDS extends BIDS concepts to multi-modality annotation with provenance. |
| **NIfTI** | VIDS uses NIfTI (.nii.gz) as the default imaging and segmentation file format. |
| **COCO / VOC** | VIDS can export to COCO-style JSON for detection tasks. These are delivery formats, not storage formats. |
| **nnU-Net / MONAI** | VIDS can export to these framework-specific layouts. The export preserves provenance as a companion package. |

---

## 2. Scope

### 2.1 In Scope

- 2D and 3D medical imaging datasets across all modalities (CT, MRI, X-Ray, Ultrasound, Mammography, PET, Nuclear Medicine, Digital Pathology)
- Annotation types: segmentation masks, bounding boxes, classification labels, anatomical landmarks, regions of interest
- Per-annotation provenance: annotator identity, credentials, tool, date, time spent, QC status
- Quality documentation: inter-annotator agreement, QC pass rates, class distributions
- ML readiness: train/val/test splits, dataset statistics

### 2.2 Out of Scope

- 4D temporal sequences (e.g., cardiac cine MRI) — planned for VIDS v2.0
- Non-imaging clinical data (EHR, genomics, lab values) — use HL7 FHIR
- Real-time annotation during acquisition
- Cell-level tracking in live microscopy
- Model training, inference, or deployment pipelines

---

## 3. Terminology and Conventions

### 3.1 Key Terms

| Term | Definition |
|------|-----------|
| **Dataset** | A complete VIDS-structured collection of imaging data, annotations, and documentation |
| **Subject** | A single patient, phantom, or imaging target, identified by a unique `sub-` prefix |
| **Session** | A single imaging acquisition event for a subject, identified by a `ses-` prefix |
| **Modality** | The imaging technique used (CT, MRI, etc.), represented by a directory code |
| **Annotation** | A human- or machine-generated label applied to imaging data (segmentation, bounding box, classification) |
| **Sidecar JSON** | A JSON file that accompanies an imaging or annotation file, sharing the same filename stem |
| **Provenance** | The documented chain of custody for an annotation: who, when, how, and quality status |
| **Profile** | A validation tier (POC or Full) that determines which rules are enforced |
| **Derivative** | A file generated from source imaging data (annotations, quality metrics) |

### 3.2 Requirement Levels

This specification uses the following terms to indicate requirement levels:

- **MUST / REQUIRED** — Absolute requirement. Validator will fail if absent.
- **SHOULD / RECOMMENDED** — Strong recommendation. Validator will warn if absent.
- **MAY / OPTIONAL** — Truly optional. Validator will not check.

### 3.3 Data Types

| Type | Format | Example |
|------|--------|---------|
| Date | `YYYY-MM-DD` (ISO 8601) | `2026-02-16` |
| DateTime | `YYYY-MM-DDThh:mm:ssZ` (ISO 8601 UTC) | `2026-02-16T14:30:00Z` |
| Subject ID | `sub-` followed by alphanumeric | `sub-001`, `sub-LIDC0042` |
| Session ID | `ses-` followed by alphanumeric | `ses-baseline`, `ses-followup01` |
| Version | Semantic versioning | `1.0.0`, `1.2.3` |

---

## 4. Dataset Root Structure

A VIDS-compliant dataset MUST have the following top-level structure:

```
<dataset-name>/
├── .vids                              # REQUIRED — Profile marker
├── dataset_description.json           # REQUIRED — Dataset metadata
├── participants.json                  # REQUIRED — Subject demographics (or .tsv)
├── README.md                          # REQUIRED — Human-readable description
├── CHANGES.md                         # RECOMMENDED — Version history
├── LICENSE                            # RECOMMENDED — License terms
│
├── sub-001/                           # REQUIRED — Subject directories
│   └── ses-baseline/                  # REQUIRED — Session directories
│       └── <modality>/                # REQUIRED — Modality directory
│           ├── sub-001_ses-baseline_<mod>_img.nii.gz    # Imaging data
│           └── sub-001_ses-baseline_<mod>_img.json      # Imaging sidecar
│
├── derivatives/                       # REQUIRED — Derived data
│   └── annotations/                   # REQUIRED — Annotation outputs
│       └── sub-001/
│           └── ses-baseline/
│               └── <modality>/
│                   ├── sub-001_ses-baseline_<mod>_seg.nii.gz   # Segmentation mask
│                   └── sub-001_ses-baseline_<mod>_seg.json     # Annotation sidecar
│
├── quality/                           # REQUIRED (Full) — Quality metrics
│   ├── quality_summary.json
│   ├── annotation_agreement.json
│   └── class_distribution.json
│
└── ml/                                # REQUIRED (Full) — ML readiness
    └── splits.json
```

### 4.1 Rules

- The dataset root directory name is unrestricted but SHOULD be descriptive (e.g., `lung-nodule-ct-100`).
- All paths are case-sensitive.
- Directory names MUST NOT contain spaces. Use hyphens (`-`) or underscores (`_`).
- The structure MUST be consistent: every subject follows the same nesting pattern.

---

## 5. File Naming Conventions

### 5.1 General Pattern

All VIDS data files follow this naming pattern:

```
sub-<ID>_ses-<ID>_<modality>_<suffix>.<extension>
```

| Component | Required | Pattern | Example |
|-----------|----------|---------|---------|
| Subject | Yes | `sub-` + alphanumeric | `sub-001` |
| Session | Yes | `ses-` + alphanumeric | `ses-baseline` |
| Modality | Yes | See Appendix A | `ct`, `mr`, `xr` |
| Suffix | Yes | See Appendix B | `img`, `seg`, `bbox`, `cls` |
| Extension | Yes | `.nii.gz`, `.json` | — |

### 5.2 Examples

```
sub-001_ses-baseline_ct_img.nii.gz       # CT imaging volume
sub-001_ses-baseline_ct_img.json         # CT imaging sidecar
sub-001_ses-baseline_ct_seg.nii.gz       # Segmentation mask
sub-001_ses-baseline_ct_seg.json         # Annotation sidecar
sub-001_ses-baseline_ct_bbox.json        # Bounding box annotations
sub-001_ses-baseline_ct_cls.json         # Classification labels
sub-001_ses-baseline_mr_img.nii.gz       # MRI imaging volume
sub-042_ses-followup01_mg_img.nii.gz     # Mammography follow-up
```

### 5.3 Rules

- Subject IDs MUST be unique within a dataset.
- Session IDs MUST be unique within a subject.
- The modality code MUST match the parent directory name.
- File stems (everything before the first `.`) MUST start with `sub-`.
- Sidecar JSON files MUST share the same stem as their parent file (e.g., `*_img.nii.gz` paired with `*_img.json`).

---

## 6. Root-Level Required Files

### 6.1 `.vids` — Profile Marker

The `.vids` file is a plain text file that marks a directory as a VIDS dataset root and declares the compliance profile.

**Required:** Yes (all profiles)

**Contents:**

```
profile: poc
vids_version: 1.0
```

or

```
profile: full
vids_version: 1.0
```

The validator reads this file to determine which rule set to apply.

### 6.2 `dataset_description.json` — Dataset Metadata

**Required:** Yes (all profiles)

**Required fields:**

| Field | Type | Description |
|-------|------|-------------|
| `Name` | string | **REQUIRED.** Human-readable dataset name |
| `VIDSVersion` | string | **REQUIRED.** VIDS specification version (e.g., `"1.0"`) |
| `DatasetVersion` | string | **REQUIRED.** Semantic version of this dataset release |
| `License` | string | **REQUIRED.** License identifier or description |
| `Description` | string | **REQUIRED.** Brief description of the dataset |
| `Authors` | array[string] | **REQUIRED.** List of contributing organizations or individuals |

**Recommended fields:**

| Field | Type | Description |
|-------|------|-------------|
| `DatasetDOI` | string | DOI if published (e.g., `"10.5281/zenodo.XXXXXXX"`) |
| `DatasetType` | object | Structured metadata (see below) |
| `SubjectCount` | integer | Total number of subjects |
| `AnnotationCount` | integer | Total number of annotations |
| `AcquisitionParameters` | object | Imaging parameters summary |
| `AnnotationWorkflow` | object | Annotation process description |
| `QualityMetrics` | object | Summary quality metrics |
| `Compliance` | object | De-identification and regulatory info |
| `Contact` | object | Contact information |
| `Created` | string (date) | Dataset creation date |
| `LastModified` | string (date) | Last modification date |

**`DatasetType` object:**

```json
{
  "Modality": "CT",
  "BodyPart": "Chest",
  "AnnotationType": "segmentation",
  "ClinicalDomain": "Lung Nodule Detection"
}
```

**`AnnotationWorkflow` object:**

```json
{
  "PrimaryAnnotator": "Board-certified thoracic radiologist",
  "ReviewProcess": "100% senior radiologist QC, 10% double-annotation",
  "Tool": "3D Slicer 5.6.2",
  "Guidelines": "VIDS Annotation Guide v1.0"
}
```

**`Compliance` object:**

```json
{
  "DeIdentification": "HIPAA Safe Harbor method",
  "IRBApproval": "IRB exemption - retrospective de-identified data",
  "DataUseAgreement": "DUA-2026-001"
}
```

### 6.3 `participants.json` or `participants.tsv` — Subject Registry

**Required:** Yes (all profiles). At least one of `.json` or `.tsv` MUST be present.

**JSON format:**

```json
{
  "VIDSVersion": "1.0",
  "Participants": [
    {
      "SubjectID": "sub-001",
      "Age": 67,
      "Sex": "M",
      "InclusionCriteria": "Non-contrast chest CT, slice thickness ≤2.5mm",
      "DataSource": "Public dataset / Hospital partnership",
      "Notes": ""
    }
  ]
}
```

**TSV format (tab-separated):**

```
subject_id	age	sex	inclusion_criteria	data_source
sub-001	67	M	Non-contrast chest CT	Public dataset
sub-002	54	F	Non-contrast chest CT	Public dataset
```

**Rules:**

- Every subject directory (`sub-*`) in the dataset MUST have a corresponding entry in the participants file.
- Age and Sex are RECOMMENDED but MAY be omitted for privacy compliance.
- For de-identified datasets, age MAY be provided as a range (e.g., `"60-70"`) instead of exact value.

### 6.4 `README.md` — Human-Readable Description

**Required:** Yes (all profiles)

**Minimum contents:**

- Dataset name and purpose
- Summary of contents (subject count, annotation type, modality)
- Brief usage instructions or pointer to quickstart guide
- Contact information
- Citation guidance (if applicable)

### 6.5 `CHANGES.md` — Version History

**Required:** Recommended (all profiles)

**Format:**

```markdown
# Changes

## [1.0.0] - 2026-02-16
- Initial release
- 100 subjects with lung nodule segmentation

## [0.9.0] - 2026-01-30
- QC review complete, 6 subjects revised
- Inter-annotator agreement calculated (Dice 0.87)
```

### 6.6 `LICENSE` — License Terms

**Required:** Recommended

A plain text or Markdown file specifying the terms under which the dataset may be used.

---

## 7. Subject and Session Layout

### 7.1 Subject Directories

Every imaging subject is represented by a directory at the dataset root:

```
sub-<ID>/
```

- `<ID>` MUST be alphanumeric (letters, digits, hyphens allowed). No spaces or underscores.
- Subject IDs SHOULD be zero-padded for consistent sorting (e.g., `sub-001`, not `sub-1`).
- Subject IDs MUST NOT contain protected health information (PHI).

### 7.2 Session Directories

Each subject contains one or more session directories:

```
sub-001/
└── ses-<ID>/
```

- Every subject MUST have at least one session directory.
- For single-timepoint datasets, use `ses-baseline`.
- For longitudinal data, use descriptive IDs: `ses-baseline`, `ses-followup01`, `ses-month06`.

### 7.3 Modality Directories

Each session contains one or more modality directories:

```
sub-001/
└── ses-baseline/
    └── ct/
```

The modality directory name MUST use a recognized modality code (see Appendix A). Custom modality codes are permitted if documented in `dataset_description.json`.

---

## 8. Imaging Files

### 8.1 Imaging Data File

**Path:** `sub-<ID>/ses-<ID>/<modality>/sub-<ID>_ses-<ID>_<mod>_img.nii.gz`

**Required:** Yes, for every subject-session-modality combination

**Format:** NIfTI-1 or NIfTI-2, gzip compressed (`.nii.gz`). Uncompressed `.nii` is permitted but discouraged.

**Rules:**

- One imaging file per modality directory. Multi-sequence acquisitions (e.g., MRI T1 + T2) are handled by using separate modality directories or appending sequence identifiers (e.g., `mr-t1/`, `mr-t2/`, or `mr-flair/`).
- The NIfTI header MUST contain valid affine transformation information (qform or sform) to enable spatial alignment.
- Voxel dimensions, orientation, and coordinate system SHOULD be preserved from the original acquisition.

### 8.2 Imaging Sidecar JSON

**Path:** `sub-<ID>/ses-<ID>/<modality>/sub-<ID>_ses-<ID>_<mod>_img.json`

**Required:** Yes, for every imaging file

The imaging sidecar captures acquisition parameters and image quality assessment.

**Schema:**

```json
{
  "VIDSVersion": "1.0",
  "SourceFormat": "DICOM | NIfTI | NRRD | Other",
  "ConversionTool": "dcm2niix v1.0.20240202 | manual | N/A",
  "ConversionDate": "YYYY-MM-DD",

  "AcquisitionParameters": {
    "SliceThickness_mm": 1.25,
    "PixelSpacing_mm": [0.7, 0.7],
    "ImageDimensions": [512, 512, 300],
    "KVP": 120,
    "ContrastEnhanced": false,
    "ReconstructionKernel": "standard | lung | soft_tissue | bone",
    "Manufacturer": "Siemens | GE | Philips | Canon | Other",
    "ManufacturerModel": "SOMATOM Force",
    "MagneticFieldStrength_T": null
  },

  "QualityAssessment": {
    "ImageQuality": "excellent | good | adequate | poor",
    "Artifacts": "none | motion | beam_hardening | noise | metal | other",
    "DiagnosticQuality": true
  },

  "DeIdentification": {
    "Method": "HIPAA Safe Harbor | Expert Determination | Other",
    "Tool": "dcm2niix | CTP | pydicom | manual",
    "Date": "YYYY-MM-DD",
    "VerifiedBy": "Name or ID"
  }
}
```

**Required fields within sidecar:** `VIDSVersion`. All other fields are RECOMMENDED.

---

## 9. Annotation Files

Annotations are stored under the `derivatives/annotations/` tree, mirroring the subject/session/modality layout of the source data.

### 9.1 Directory Structure

```
derivatives/
└── annotations/
    └── sub-001/
        └── ses-baseline/
            └── ct/
                ├── sub-001_ses-baseline_ct_seg.nii.gz    # Segmentation mask
                ├── sub-001_ses-baseline_ct_seg.json       # Annotation sidecar
                ├── sub-001_ses-baseline_ct_bbox.json      # Bounding boxes (optional)
                └── sub-001_ses-baseline_ct_cls.json       # Classification (optional)
```

### 9.2 Segmentation Mask

**Suffix:** `_seg.nii.gz`

**Format:** NIfTI, same spatial dimensions and affine as the source imaging file.

**Voxel values:**

| Value | Meaning |
|-------|---------|
| 0 | Background |
| 1 | Annotation class 1 (e.g., nodule) |
| 2 | Annotation class 2 (if multi-label) |
| N | Annotation class N |

The mapping of integer values to class names MUST be documented in the annotation sidecar JSON (`LabelMap` field).

### 9.3 Bounding Box File

**Suffix:** `_bbox.json`

**Schema:**

```json
{
  "VIDSVersion": "1.0",
  "AnnotationType": "bbox",
  "SourceImage": "sub-001_ses-baseline_ct_img.nii.gz",
  "CoordinateSystem": "voxels | mm",
  "BoundingBoxes": [
    {
      "ID": "nodule_001",
      "Label": "nodule",
      "min_x": 245, "min_y": 180, "min_z": 102,
      "max_x": 260, "max_y": 198, "max_z": 110
    }
  ],
  "Provenance": { }
}
```

### 9.4 Classification File

**Suffix:** `_cls.json`

**Schema:**

```json
{
  "VIDSVersion": "1.0",
  "AnnotationType": "classification",
  "SourceImage": "sub-001_ses-baseline_ct_img.nii.gz",
  "Classifications": [
    {
      "Label": "nodule_present",
      "Value": true,
      "Confidence": 0.95
    }
  ],
  "Provenance": { }
}
```

### 9.5 Landmark File

**Suffix:** `_lm.json`

**Schema:**

```json
{
  "VIDSVersion": "1.0",
  "AnnotationType": "landmark",
  "SourceImage": "sub-001_ses-baseline_ct_img.nii.gz",
  "CoordinateSystem": "voxels | mm",
  "Landmarks": [
    {
      "ID": "carina",
      "Label": "Carina",
      "x": 256.0, "y": 245.0, "z": 180.0
    }
  ],
  "Provenance": { }
}
```

---

## 10. Annotation Sidecar JSON Schema

The annotation sidecar is the core of VIDS provenance tracking. Every annotation file (segmentation, bounding box, classification, landmark) MUST have an accompanying sidecar JSON.

### 10.1 Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `VIDSVersion` | string | **REQUIRED** | VIDS specification version |
| `AnnotationType` | string | **REQUIRED** | `"segmentation"`, `"bbox"`, `"classification"`, `"landmark"`, `"roi"` |
| `Description` | string | RECOMMENDED | Brief description of what was annotated |
| `SourceImage` | string | **REQUIRED** | Filename of the source imaging file |
| `Provenance` | object | **REQUIRED** | Provenance block (see §10.2) |
| `Annotations` | array | RECOMMENDED | Per-finding annotation details (see §10.4) |
| `ImageMetadata` | object | OPTIONAL | Acquisition parameter summary |
| `LabelMap` | object | RECOMMENDED (segmentation) | Integer-to-class mapping |
| `Notes` | string | OPTIONAL | Free text notes |

### 10.2 Provenance Object

The Provenance object is the distinguishing feature of VIDS. It documents the complete chain of custody for the annotation.

```json
{
  "Provenance": {
    "Annotator": {
      "ID": "radiologist_001",
      "Name": "Dr. [Full Name]",
      "Credentials": "MD, DNB (Radiology), 8 years experience",
      "Specialty": "Chest Radiology",
      "Institution": "[Hospital Name]"
    },
    "AnnotationProcess": {
      "Tool": "3D Slicer",
      "ToolVersion": "5.6.2",
      "Date": "2026-02-10",
      "TimeSpent_minutes": 18,
      "Method": "Manual segmentation"
    },
    "QualityControl": {
      "ReviewedBy": "senior_radiologist_001",
      "ReviewDate": "2026-02-12",
      "ReviewOutcome": "approved",
      "Confidence": 0.92
    }
  }
}
```

#### 10.2.1 `Provenance.Annotator` — Required Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ID` | string | **REQUIRED**¹ | Unique identifier for the annotator |
| `Name` | string | **REQUIRED**¹ | Full name or pseudonym |
| `Credentials` | string | RECOMMENDED | Qualifications and experience |
| `Specialty` | string | RECOMMENDED | Clinical specialty |
| `Institution` | string | OPTIONAL | Affiliated institution |

¹ At least one of `ID` or `Name` MUST be present.

#### 10.2.2 `Provenance.AnnotationProcess` — Required Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `Tool` | string | **REQUIRED**¹ | Annotation software name |
| `ToolVersion` | string | RECOMMENDED | Software version |
| `Date` | string (date) | **REQUIRED**¹ | Date annotation was performed |
| `TimeSpent_minutes` | number | RECOMMENDED | Time spent in minutes |
| `Method` | string | RECOMMENDED | `"Manual segmentation"`, `"Semi-automated with manual correction"`, `"Automated with manual review"` |

¹ At least one of `Date` or `Tool` MUST be present.

#### 10.2.3 `Provenance.QualityControl`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ReviewedBy` | string | RECOMMENDED | Reviewer ID or name |
| `ReviewDate` | string (date) | RECOMMENDED | Date of review |
| `ReviewOutcome` | string | RECOMMENDED | `"approved"`, `"revisions_requested"`, `"rejected"` |
| `Confidence` | number (0–1) | OPTIONAL | Annotator/reviewer confidence score |

### 10.3 LabelMap (for Segmentation)

When the annotation type is `segmentation`, the sidecar SHOULD include a LabelMap that maps integer voxel values to class names:

```json
{
  "LabelMap": {
    "0": "background",
    "1": "nodule"
  }
}
```

For multi-label segmentation:

```json
{
  "LabelMap": {
    "0": "background",
    "1": "tumor_enhancing",
    "2": "tumor_non_enhancing",
    "3": "edema",
    "4": "necrosis"
  }
}
```

### 10.4 Annotations Array

The `Annotations` array provides per-finding details. Each element represents a distinct annotated finding (e.g., one nodule, one lesion).

```json
{
  "Annotations": [
    {
      "ID": "nodule_001",
      "Type": "nodule",
      "Location": {
        "Lobe": "RUL",
        "Segment": "apical",
        "Coordinates_mm": { "x": 125.3, "y": -42.7, "z": 310.8 }
      },
      "Characteristics": {
        "Size_mm": {
          "max_diameter": 12.5,
          "min_diameter": 8.2,
          "volume_mm3": 620.4
        },
        "Morphology": {
          "Shape": "round",
          "Margin": "smooth",
          "Density": "solid",
          "Texture": "homogeneous"
        },
        "LungRADS": "3",
        "Malignancy": {
          "suspicion_level": "moderate",
          "confidence": 0.75,
          "notes": ""
        }
      },
      "BoundingBox": {
        "min_x": 245, "min_y": 180, "min_z": 102,
        "max_x": 260, "max_y": 198, "max_z": 110,
        "units": "voxels"
      }
    }
  ]
}
```

**Important:** The `Location` and `Characteristics` fields are domain-specific and SHOULD be adapted for each clinical use case. The lung CT fields shown above are the reference implementation. See the VIDS Compatibility Analysis for adaptation guidance by modality.

---

## 11. Quality Documentation

Quality documentation files live in the `quality/` directory at the dataset root.

### 11.1 `quality/quality_summary.json`

**Required:** Full profile only (RECOMMENDED for POC)

Summarizes overall dataset quality. Key fields:

```json
{
  "VIDSVersion": "1.0",
  "Profile": "full",
  "DatasetName": "...",
  "DatasetVersion": "1.0.0",
  "QualityAssessmentDate": "YYYY-MM-DD",

  "AnnotationStatistics": {
    "TotalSubjects": 100,
    "TotalAnnotations": 267,
    "SubjectsWithAnnotations": 95,
    "SubjectsWithoutAnnotations": 5,
    "AnnotationsPerSubject": {
      "Mean": 2.81, "StandardDeviation": 1.42,
      "Min": 0, "Max": 8, "Median": 2
    }
  },

  "QualityControlMetrics": {
    "QCReviewer": { "Name": "...", "Credentials": "...", "Specialty": "..." },
    "QCProcess": {
      "ReviewPercentage": 100,
      "DoubleAnnotationPercentage": 10,
      "ReviewMethod": "Visual inspection + measurement verification"
    },
    "PassRates": {
      "FirstSubmissionPassRate": 0.88,
      "AfterRevisionPassRate": 0.98,
      "TotalRevisionsRequired": 12
    }
  },

  "InterAnnotatorAgreement": {
    "Method": "Dice Coefficient",
    "SampleSize": 10,
    "DiceStatistics": {
      "Mean": 0.872, "StandardDeviation": 0.043,
      "Min": 0.79, "Max": 0.94
    },
    "QualityThresholds": { "Target": 0.85, "Acceptable": 0.75 }
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

  "CertificationStatement": "...",
  "CertifiedBy": { "Name": "...", "Role": "...", "Date": "..." }
}
```

### 11.2 `quality/annotation_agreement.json`

**Required:** Full profile only

Documents inter-annotator agreement (IAA) with per-subject Dice coefficients for segmentation tasks, or per-subject agreement metrics for other annotation types.

Key fields:

| Field | Description |
|-------|-------------|
| `Methodology` | IAA method, sampling strategy, and tool used |
| `Annotators` | Credentials and roles of each annotator |
| `SampleSelection` | How subjects were selected for double annotation |
| `AggregateStatistics` | Mean, SD, min, max Dice coefficient |
| `PerSubjectResults` | Array of per-subject agreement scores |
| `QualityThresholds` | Excellent (≥0.90), Good (0.85–0.90), Acceptable (0.75–0.85), Poor (<0.75) |

### 11.3 `quality/class_distribution.json`

**Required:** Recommended for all profiles

Documents the distribution of annotation classes, clinical scores, anatomical locations, and size measurements across the dataset. Includes bias considerations and ML suitability guidance.

---

## 12. ML Readiness Files

### 12.1 `ml/splits.json`

**Required:** Full profile only (RECOMMENDED for POC)

Defines train/validation/test splits:

```json
{
  "VIDSVersion": "1.0",
  "SplitStrategy": "random",
  "SplitRatio": "70/15/15",
  "RandomSeed": 42,
  "Splits": {
    "train": ["sub-001", "sub-002", "sub-003"],
    "val": ["sub-050", "sub-051"],
    "test": ["sub-080", "sub-081"]
  },
  "Notes": "Subject-level split. No data leakage between splits."
}
```

**Rules:**

- Splits MUST be at the subject level (not slice or study level) to prevent data leakage.
- Every subject with annotations SHOULD appear in exactly one split.
- The split SHOULD be reproducible (document the random seed and strategy).

---

## 13. Compliance Profiles

VIDS defines two compliance profiles. The profile is declared in the `.vids` marker file and determines which validation rules are enforced.

### 13.1 POC Profile (Proof of Concept)

**Purpose:** Quick prototypes, internal research, MVP development, pilot deliveries.

**Requirements:**

- 15 validation rules enforced (S001–S006, I001–I004, A001–A005)
- Single annotator acceptable
- Quality documentation optional (but recommended)
- ML splits optional (but recommended)

### 13.2 Full Profile (Production)

**Purpose:** Commercial AI products, FDA submissions, publications, enterprise delivery.

**Requirements:**

- All 21 validation rules enforced
- Multi-annotator consensus required (minimum 10% double annotation)
- Quality documentation required (quality_summary.json, annotation_agreement.json)
- ML splits required (ml/splits.json)
- Dice coefficient ≥0.85 target for inter-annotator agreement

### 13.3 Profile Comparison

| Requirement | POC | Full |
|------------|-----|------|
| `.vids` marker | ✅ Required | ✅ Required |
| `dataset_description.json` | ✅ Required | ✅ Required |
| `participants.json/.tsv` | ✅ Required | ✅ Required |
| `README.md` | ✅ Required | ✅ Required |
| Subject/session directories | ✅ Required | ✅ Required |
| Imaging files + sidecars | ✅ Required | ✅ Required |
| Annotation files + sidecars | ✅ Required | ✅ Required |
| Complete provenance | ✅ Required | ✅ Required |
| `quality/` directory | Optional | ✅ Required |
| `quality_summary.json` | Optional | ✅ Required |
| `annotation_agreement.json` | Optional | ✅ Required |
| `ml/` directory | Optional | ✅ Required |
| `ml/splits.json` | Optional | ✅ Required |
| `CHANGES.md` | Recommended | Recommended |
| Double annotation (≥10%) | Not required | ✅ Required |
| Dice ≥0.85 target | Not required | ✅ Required |

---

## 14. Validation Rules

VIDS compliance is verified by the VIDS Validator (`validate_vids.py`), which enforces 21 rules organized into 6 categories.

### 14.1 Structure Rules (S001–S006) — All Profiles

| Rule | Check | Requirement |
|------|-------|-------------|
| **S001** | `.vids` marker file exists at dataset root | REQUIRED |
| **S002** | `dataset_description.json` exists and contains required fields: `Name`, `VIDSVersion`, `DatasetVersion`, `License`, `Description`, `Authors` | REQUIRED |
| **S003** | `participants.json` or `participants.tsv` exists | REQUIRED |
| **S004** | `README.md` exists | REQUIRED |
| **S005** | At least one subject directory matching `sub-*` pattern exists | REQUIRED |
| **S006** | Every subject directory contains at least one session directory matching `ses-*` | REQUIRED |

### 14.2 Imaging Rules (I001–I004) — All Profiles

| Rule | Check | Requirement |
|------|-------|-------------|
| **I001** | Every subject-session has at least one `*_img.nii.gz` or `*_img.nii` file | REQUIRED |
| **I002** | Every imaging file has a corresponding `*_img.json` sidecar | REQUIRED |
| **I003** | All imaging sidecar JSONs parse as valid JSON | REQUIRED |
| **I004** | All NIfTI filenames start with `sub-` (VIDS naming convention) | WARNING |

### 14.3 Annotation Rules (A001–A005) — All Profiles

| Rule | Check | Requirement |
|------|-------|-------------|
| **A001** | `derivatives/annotations/` directory exists | REQUIRED |
| **A002** | At least one segmentation file (`*_seg.nii.gz`) exists in annotations tree | REQUIRED |
| **A003** | At least one annotation sidecar JSON (`*_seg.json`) exists | REQUIRED |
| **A004** | All annotation sidecar JSONs are valid JSON and contain `VIDSVersion` field | REQUIRED |
| **A005** | Provenance fields populated: `Annotator.ID` or `Annotator.Name`, and `AnnotationProcess.Date` or `AnnotationProcess.Tool` | REQUIRED |

### 14.4 Quality Rules (Q001–Q003) — Full Profile Only

| Rule | Check | Requirement |
|------|-------|-------------|
| **Q001** | `quality/` directory exists | REQUIRED (Full) |
| **Q002** | `quality/quality_summary.json` exists | REQUIRED (Full) |
| **Q003** | `quality/annotation_agreement.json` exists | REQUIRED (Full) |

### 14.5 ML Rules (M001–M002) — Full Profile Only

| Rule | Check | Requirement |
|------|-------|-------------|
| **M001** | `ml/` directory exists | REQUIRED (Full) |
| **M002** | `ml/splits.json` exists | REQUIRED (Full) |

### 14.6 Metadata Rules (D001) — All Profiles

| Rule | Check | Requirement |
|------|-------|-------------|
| **D001** | `CHANGES.md` exists | WARNING |

### 14.7 Validation Outcomes

Each rule produces one of four outcomes:

| Status | Meaning |
|--------|---------|
| **PASS** | Rule satisfied |
| **FAIL** | Rule violated — dataset is non-compliant |
| **WARN** | Recommended practice not followed — does not block compliance |
| **SKIP** | Rule not applicable to the declared profile |

A dataset is **VIDS-compliant** if and only if zero rules have FAIL status after validation.

---

## 15. Versioning Policy

### 15.1 Specification Versioning

The VIDS specification follows semantic versioning:

- **Major** (X.0.0): Breaking changes to folder structure, required fields, or validation rules
- **Minor** (1.X.0): New optional features, new annotation types, new modality codes
- **Patch** (1.0.X): Clarifications, typo fixes, example corrections

### 15.2 Dataset Versioning

Datasets SHOULD use semantic versioning in `dataset_description.json`:

- Increment **major** when subjects are added or removed
- Increment **minor** when annotations are revised or quality metrics updated
- Increment **patch** when only documentation or metadata changes

### 15.3 Backward Compatibility

- Datasets created under VIDS 1.0 MUST remain valid under VIDS 1.x validators.
- Breaking changes require a major version increment and a documented migration path.

---

## 16. Extension Mechanism

VIDS supports domain-specific extensions without modifying the core specification.

### 16.1 Custom Modality Codes

If a modality is not listed in Appendix A, a custom code MAY be used. The custom code MUST be documented in `dataset_description.json` under a `CustomModalities` field:

```json
{
  "CustomModalities": {
    "oct": "Optical Coherence Tomography",
    "endo": "Endoscopy Video Frames"
  }
}
```

### 16.2 Custom Annotation Fields

The `Annotations[].Characteristics` object is explicitly designed for domain-specific extension. New fields MAY be added freely. The VIDS validator does not enforce specific field names within `Characteristics`.

Example — Brain MRI extension:

```json
{
  "Characteristics": {
    "WHO_Grade": "IV",
    "IDH_Status": "wildtype",
    "MGMT_Methylation": "unmethylated",
    "RANO_Response": "stable_disease"
  }
}
```

Example — Mammography extension:

```json
{
  "Characteristics": {
    "BI_RADS": "4C",
    "Breast": "left",
    "Quadrant": "UOQ",
    "ClockFace": "2_oclock"
  }
}
```

### 16.3 Custom Quality Metrics

Additional quality metric files MAY be placed in `quality/` with descriptive filenames. The validator only checks for the presence of `quality_summary.json` and `annotation_agreement.json`; additional files are ignored.

### 16.4 Custom Derivative Types

Additional derivatives MAY be placed under `derivatives/` in new subdirectories:

```
derivatives/
├── annotations/          # Standard VIDS annotations
├── radiomics/            # Custom: radiomics features
└── model-predictions/    # Custom: AI model outputs
```

Custom derivative directories are ignored by the validator.

---

## 17. Export and Interoperability

VIDS is designed as a canonical internal format. Datasets curated in VIDS can be exported to any downstream format for delivery.

### 17.1 Supported Export Formats

| Format | Use Case | Tool |
|--------|----------|------|
| **nnU-Net v2** | Medical image segmentation training | `export_vids.py --format nnunet` |
| **MONAI** | PyTorch medical imaging framework | `export_vids.py --format monai` |
| **Flat NIfTI** | Generic ML pipelines, custom frameworks | `export_vids.py --format flat` |
| **COCO JSON** | Detection tasks, bounding box models | `export_vids.py --format coco` |

### 17.2 Provenance Preservation

All export formats include a `vids-provenance/` companion directory containing the complete provenance documentation, quality metrics, and dataset description from the source VIDS dataset. This ensures that provenance is never lost during format conversion.

### 17.3 Traceability

Export tools generate a mapping file that links exported case identifiers back to original VIDS subject IDs, enabling full traceability from model input back to annotation provenance.

---

## Appendix A: Modality Codes

| Code | Modality | File Suffix Example |
|------|----------|-------------------|
| `ct` | Computed Tomography | `ct_img.nii.gz` |
| `mr` | Magnetic Resonance Imaging | `mr_img.nii.gz` |
| `mr-t1` | MRI T1-weighted | `mr-t1_img.nii.gz` |
| `mr-t2` | MRI T2-weighted | `mr-t2_img.nii.gz` |
| `mr-flair` | MRI FLAIR | `mr-flair_img.nii.gz` |
| `mr-dwi` | MRI Diffusion-Weighted | `mr-dwi_img.nii.gz` |
| `mr-dce` | MRI Dynamic Contrast-Enhanced | `mr-dce_img.nii.gz` |
| `xr` | X-Ray / Radiography | `xr_img.nii.gz` |
| `us` | Ultrasound | `us_img.nii.gz` |
| `mg` | Mammography | `mg_img.nii.gz` |
| `pt` | PET (Positron Emission Tomography) | `pt_img.nii.gz` |
| `nm` | Nuclear Medicine / SPECT | `nm_img.nii.gz` |
| `path` | Digital Pathology (Whole-Slide Imaging) | `path_img.nii.gz` |

Custom codes are permitted per §16.1.

---

## Appendix B: Annotation Type Suffixes

| Suffix | Annotation Type | File Format |
|--------|----------------|-------------|
| `_seg` | Segmentation mask | `.nii.gz` (mask) + `.json` (sidecar) |
| `_bbox` | Bounding boxes | `.json` |
| `_cls` | Classification labels | `.json` |
| `_lm` | Anatomical landmarks | `.json` |
| `_roi` | Region of interest | `.json` |

---

## Appendix C: Complete Folder Reference

```
<dataset-name>/
│
├── .vids                                    # Profile marker (poc or full)
├── dataset_description.json                 # Dataset-level metadata
├── participants.json                        # Subject registry
├── participants.tsv                         # Subject registry (tabular, alternative)
├── README.md                                # Human-readable description
├── CHANGES.md                               # Version changelog
├── LICENSE                                  # License terms
│
├── sub-001/
│   └── ses-baseline/
│       └── ct/
│           ├── sub-001_ses-baseline_ct_img.nii.gz
│           └── sub-001_ses-baseline_ct_img.json
│
├── sub-002/
│   └── ses-baseline/
│       └── ct/
│           ├── sub-002_ses-baseline_ct_img.nii.gz
│           └── sub-002_ses-baseline_ct_img.json
│
├── derivatives/
│   └── annotations/
│       ├── sub-001/
│       │   └── ses-baseline/
│       │       └── ct/
│       │           ├── sub-001_ses-baseline_ct_seg.nii.gz
│       │           ├── sub-001_ses-baseline_ct_seg.json
│       │           ├── sub-001_ses-baseline_ct_bbox.json    (optional)
│       │           └── sub-001_ses-baseline_ct_cls.json     (optional)
│       └── sub-002/
│           └── ses-baseline/
│               └── ct/
│                   ├── sub-002_ses-baseline_ct_seg.nii.gz
│                   └── sub-002_ses-baseline_ct_seg.json
│
├── quality/                                  (Required: Full profile)
│   ├── quality_summary.json
│   ├── annotation_agreement.json
│   └── class_distribution.json
│
└── ml/                                       (Required: Full profile)
    └── splits.json
```

---

## Appendix D: JSON Schema Quick Reference

### Minimum Viable Annotation Sidecar (`_seg.json`)

The absolute minimum required by the validator:

```json
{
  "VIDSVersion": "1.0",
  "AnnotationType": "segmentation",
  "SourceImage": "sub-001_ses-baseline_ct_img.nii.gz",
  "Provenance": {
    "Annotator": {
      "ID": "radiologist_001"
    },
    "AnnotationProcess": {
      "Tool": "3D Slicer",
      "Date": "2026-02-10"
    }
  }
}
```

### Minimum Viable `dataset_description.json`

```json
{
  "Name": "My Dataset",
  "VIDSVersion": "1.0",
  "DatasetVersion": "1.0.0",
  "License": "CC BY 4.0",
  "Description": "Description of the dataset",
  "Authors": ["Organization Name"]
}
```

### Minimum Viable `.vids`

```
profile: poc
vids_version: 1.0
```

---

## Citation

```bibtex
@misc{vids2026,
  title   = {VIDS: Verified Imaging Dataset Standard, Specification v1.0},
  author  = {{Princeton Medical Systems}},
  year    = {2026},
  version = {1.0},
  url     = {https://vids.ai/spec/1.0}
}
```

---

## License

This specification is released under the **Creative Commons Attribution 4.0 International License** (CC BY 4.0). You are free to share and adapt this material for any purpose, provided you give appropriate credit.

VIDS tools and reference implementations are released under the **Apache License 2.0 (Apache-2.0)**.

---

**VIDS — Verified Imaging Dataset Standard**
**Specification v1.0 — February 2026**
**© 2026 Princeton Medical Systems**
