# VIDS Quickstart: From Zero to PASS in 15 Minutes

This tutorial walks you through creating a VIDS-compliant dataset from scratch. By the end, you'll have a validated dataset that passes all compliance checks.

## What you'll need

- Python 3.8+
- 15 minutes

## Step 1: Install the tools (2 minutes)

```bash
pip install vids-validator
```

Download the scaffolding tool:

```bash
# From the VIDS repo
curl -O https://raw.githubusercontent.com/vids-standard/vids-standard/main/tools/vids_init.py
```

Or clone the repo:

```bash
git clone https://github.com/vids-standard/vids-standard.git
cd vids-standard
```

## Step 2: Scaffold your dataset (1 minute)

```bash
python vids_init.py my-first-dataset --subjects 3 --modality ct --profile poc
```

This creates the complete directory structure with template files:

```
my-first-dataset/
├── .vids                           ← Profile marker (poc)
├── dataset_description.json        ← Dataset metadata (fill in)
├── participants.json               ← Subject registry (fill in)
├── README.md                       ← Documentation (fill in)
├── CHANGES.md                      ← Version history
├── sub-001/
│   └── ses-baseline/
│       └── ct/
│           ├── sub-001_ses-baseline_ct_img.nii.gz    ← Placeholder (replace)
│           └── sub-001_ses-baseline_ct_img.json       ← Template (fill in)
├── sub-002/ ...
├── sub-003/ ...
└── derivatives/
    └── annotations/
        ├── sub-001/
        │   └── ses-baseline/
        │       └── ct/
        │           ├── sub-001_ses-baseline_ct_seg.nii.gz   ← Placeholder (replace)
        │           └── sub-001_ses-baseline_ct_seg.json      ← Template (fill in)
        ├── sub-002/ ...
        └── sub-003/ ...
```

## Step 3: Validate immediately (1 minute)

The scaffold passes validation right out of the box:

```bash
vids-validate my-first-dataset/
```

You should see:

```
  ✅ S001: .vids marker file present
  ✅ S002: dataset_description.json valid
  ✅ S003: Participants file present (json)
  ✅ S004: README.md present
  ✅ S005: 3 subject directories found
  ✅ S006: All subjects have session directories
  ✅ I001: All subjects have imaging files
  ✅ I002: All subjects have imaging sidecar JSONs
  ✅ I003: 3 imaging JSONs valid
  ✅ I004: All files follow VIDS naming convention
  ✅ A001: derivatives/annotations/ exists
  ✅ A002: 3 segmentation files found
  ✅ A003: 3 annotation sidecar JSONs found
  ✅ A004: 3 annotation JSONs valid
  ✅ A005: All annotations have complete provenance

  ✅ VALIDATION PASSED (16/21 rules)
```

16 rules pass, 5 are skipped (those are Full profile only — quality docs and ML splits).

## Step 4: Replace the placeholders with your real data (10 minutes)

Now swap the placeholder files with your actual data. Here's what to replace:

### 4a. Replace NIfTI stubs with your imaging data

Copy your actual NIfTI files over the placeholders:

```bash
# Replace imaging volumes
cp /path/to/your/patient1_ct.nii.gz \
    my-first-dataset/sub-001/ses-baseline/ct/sub-001_ses-baseline_ct_img.nii.gz

# Replace segmentation masks
cp /path/to/your/patient1_seg.nii.gz \
    my-first-dataset/derivatives/annotations/sub-001/ses-baseline/ct/sub-001_ses-baseline_ct_seg.nii.gz
```

The filenames must stay exactly as they are — that's the VIDS naming convention.

### 4b. Fill in the imaging sidecars

Edit `sub-001/ses-baseline/ct/sub-001_ses-baseline_ct_img.json`:

```json
{
  "VIDSVersion": "1.0",
  "SourceFormat": "DICOM",
  "ConversionTool": "dcm2niix v1.0.20240202",
  "ConversionDate": "2026-03-28",
  "AcquisitionParameters": {
    "SliceThickness_mm": 1.25,
    "PixelSpacing_mm": [0.7, 0.7],
    "ImageDimensions": [512, 512, 300],
    "Manufacturer": "Siemens",
    "ManufacturerModel": "SOMATOM Force"
  },
  "DeIdentification": {
    "Method": "HIPAA Safe Harbor",
    "Tool": "dcm2niix",
    "Date": "2026-03-28",
    "VerifiedBy": "data_curator_001"
  }
}
```

### 4c. Fill in the annotation sidecars

Edit `derivatives/annotations/sub-001/ses-baseline/ct/sub-001_ses-baseline_ct_seg.json`:

```json
{
  "VIDSVersion": "1.0",
  "AnnotationType": "segmentation",
  "Description": "Lung nodule segmentation",
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
      "Date": "2026-03-25",
      "TimeSpent_minutes": 15,
      "Method": "Manual segmentation"
    },
    "QualityControl": {
      "ReviewedBy": "senior_radiologist_001",
      "ReviewDate": "2026-03-26",
      "ReviewOutcome": "approved"
    }
  }
}
```

The key provenance fields are: who annotated it (`Annotator.ID` or `Annotator.Name`), and when or with what tool (`AnnotationProcess.Date` or `AnnotationProcess.Tool`). These are the minimum for VIDS compliance.

### 4d. Fill in dataset_description.json

```json
{
  "Name": "Lung Nodule CT Dataset",
  "VIDSVersion": "1.0",
  "DatasetVersion": "1.0.0",
  "License": "CC BY 4.0",
  "Description": "3 chest CT scans with lung nodule segmentation annotations.",
  "Authors": ["Your Organization"]
}
```

### 4e. Fill in participants.json

```json
{
  "VIDSVersion": "1.0",
  "Participants": [
    {"SubjectID": "sub-001", "Age": 67, "Sex": "M", "DataSource": "Hospital A"},
    {"SubjectID": "sub-002", "Age": 54, "Sex": "F", "DataSource": "Hospital A"},
    {"SubjectID": "sub-003", "Age": 72, "Sex": "M", "DataSource": "Hospital B"}
  ]
}
```

## Step 5: Validate again (1 minute)

```bash
vids-validate my-first-dataset/
```

If everything is filled in correctly, you'll see the same PASS result. If anything fails, the validator tells you exactly which rule failed and why.

### JSON output for CI pipelines

```bash
vids-validate my-first-dataset/ --json
```

### Python API

```python
from vids_validator import VIDSValidator

validator = VIDSValidator("my-first-dataset/")
report = validator.validate()
print(report["Summary"]["Status"])  # "PASS"
```

## What's next?

### Upgrade to Full profile

When you need quality documentation and ML splits (for production, publications, or regulatory submissions):

```bash
python vids_init.py my-production-dataset --subjects 100 --modality ct --profile full
```

The Full profile adds `quality/` and `ml/` directories with template files for inter-annotator agreement, quality summaries, and train/val/test splits.

### Export to ML frameworks

VIDS datasets can be exported to any framework:

```bash
# See the VIDS spec for export format details
vids-validate my-first-dataset/ --json  # Confirm compliance first
```

Supported export targets: nnU-Net, MONAI, COCO JSON, flat NIfTI.

### Find TODOs

To find all remaining placeholder fields:

```bash
grep -r "TODO" my-first-dataset/ --include="*.json" --include="*.md"
```

## Common issues

**"dataset_description.json missing fields"** — Make sure all 6 required fields are present: `Name`, `VIDSVersion`, `DatasetVersion`, `License`, `Description`, `Authors`.

**"No segmentation files found"** — Your `_seg.nii.gz` files must be under `derivatives/annotations/`, not in the subject directories.

**"Incomplete provenance"** — Each `_seg.json` needs at minimum: `Provenance.Annotator.ID` (or `.Name`) AND `Provenance.AnnotationProcess.Date` (or `.Tool`).

**"Imaging sidecar JSON invalid"** — Check for trailing commas or syntax errors. Run `python -m json.tool file.json` to validate.

## Links

- [Full Specification](https://github.com/vids-standard/vids-standard/blob/main/SPEC.md)
- [Validation Rules](https://github.com/vids-standard/vids-standard/blob/main/VALIDATION_RULES.md)
- [Complete Examples](https://github.com/vids-standard/vids-standard/blob/main/EXAMPLES.md)
- [Contributing](https://github.com/vids-standard/vids-standard/blob/main/CONTRIBUTING.md)
