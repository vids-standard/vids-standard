# VIDS — Verified Imaging Dataset Standard

[![VIDS Version](https://img.shields.io/badge/VIDS-v1.0-blue)](SPEC.md)
[![PyPI](https://img.shields.io/pypi/v/vids-validator)](https://pypi.org/project/vids-validator/)
[![License: CC BY 4.0](https://img.shields.io/badge/Spec-CC%20BY%204.0-lightgrey)](LICENSE)
[![License: Apache 2.0](https://img.shields.io/badge/Tools-Apache%202.0-green)](LICENSE-TOOLS)
[![Validator](https://img.shields.io/badge/validator-21%20rules-orange)](validators/validate_vids.py)
[![CI](https://github.com/vids-standard/vids-standard/actions/workflows/ci.yml/badge.svg)](https://github.com/vids-standard/vids-standard/actions/workflows/ci.yml)

**The compliance layer for medical imaging AI datasets.**

VIDS enforces dataset structure, annotation provenance, and quality documentation with 21 machine-verifiable rules. Run the validator, get PASS or FAIL. No ambiguity, no checklists, no trust required.

```bash
pip install vids-validator
vids-validate my-dataset/ --profile full
```

```
  ✅ S001–S006: Structure rules           PASS
  ✅ I001–I004: Imaging rules              PASS
  ✅ A001–A005: Annotation + provenance    PASS
  ✅ Q001–Q003: Quality documentation      PASS
  ✅ M001–M002: ML readiness               PASS

  ✅ VALIDATION PASSED (21/21 rules)
```

**Validate before you train. Validate before you pay. Validate before you submit.**

---

## Paper

**VIDS: A Verified Imaging Dataset Standard for Medical AI**
Dr. Joan S. Muthu, John Shalen — Princeton Medical Systems
[arXiv:2604.17525](https://arxiv.org/abs/2604.17525)

Four major public datasets (LIDC-IDRI, BraTS, CheXpert, Medical Segmentation Decathlon) scored against 22 VIDS compliance dimensions. Average: 29%. Provenance: 8%. The paper presents the full spec design, the compliance analysis, and LIDC-Hybrid-100 — a 100-subject VIDS-compliant reference CT dataset published on [Zenodo](https://doi.org/10.5281/zenodo.19582717).

---

## Why VIDS?

Medical imaging AI teams waste weeks untangling datasets that arrive as ZIP files full of unnamed NIfTIs and undocumented annotations. Nobody knows who annotated what, when, or whether anyone reviewed it. VIDS eliminates this:

- **Mandatory provenance** — every annotation records annotator identity, credentials, tool, date, and QC status
- **Automated validation** — one command, 21 rules, PASS or FAIL
- **Two profiles** — POC (15 rules) for pilots, Full (21 rules) for production and regulatory
- **Format-agnostic export** — curate once in VIDS, export to nnU-Net, MONAI, COCO, or flat NIfTI without losing provenance

VIDS sits above DICOM and BIDS. DICOM handles image storage. BIDS handles neuroimaging research organization. VIDS handles the layer neither covers: annotated datasets with documented provenance and enforced compliance.

## Quick Start

### Option 1: Scaffold a new dataset (recommended)

```bash
pip install vids-validator
git clone https://github.com/vids-standard/vids-standard.git

# Create a VIDS dataset skeleton — passes validation immediately
python vids-standard/tools/vids_init.py my-dataset --subjects 10 --modality ct --profile poc

# Validate
vids-validate my-dataset/
# ✅ VALIDATION PASSED (16/21 rules)
```

Replace the NIfTI stubs with your real imaging data, fill in the JSON templates, validate again. See [QUICKSTART.md](QUICKSTART.md) for the full walkthrough.

### Option 2: Validate an existing dataset

```bash
pip install vids-validator
vids-validate /path/to/your/dataset
vids-validate /path/to/your/dataset --profile full --json
```

### Python API

```python
from vids_validator import VIDSValidator

validator = VIDSValidator("/path/to/dataset", profile="auto")
report = validator.validate()
assert report["Summary"]["Status"] == "PASS"
```

## How It Works

Every VIDS dataset follows this structure:

```
my-dataset/
├── .vids                              # Profile: poc or full
├── dataset_description.json           # Name, version, license, authors
├── participants.json                  # Subject registry
├── README.md                          # Human-readable description
├── sub-001/
│   └── ses-baseline/
│       └── ct/
│           ├── sub-001_ses-baseline_ct_img.nii.gz      # Imaging volume
│           └── sub-001_ses-baseline_ct_img.json         # Acquisition metadata
└── derivatives/
    └── annotations/
        └── sub-001/
            └── ses-baseline/
                └── ct/
                    ├── sub-001_ses-baseline_ct_seg.nii.gz   # Segmentation mask
                    └── sub-001_ses-baseline_ct_seg.json      # Provenance sidecar
```

Every annotation sidecar documents **who** annotated, **when**, **with what tool**, and **what QC was performed**:

```json
{
  "Provenance": {
    "Annotator": { "ID": "radiologist_001", "Credentials": "MD, Board-certified" },
    "AnnotationProcess": { "Tool": "3D Slicer", "Date": "2026-03-25" },
    "QualityControl": { "ReviewedBy": "senior_rad_001", "ReviewOutcome": "approved" }
  }
}
```

This is not optional metadata. This is a first-class requirement. If the provenance is missing, the validator fails.

## Specification

| Document | What's in it |
|----------|-------------|
| [SPEC.md](SPEC.md) | Full specification (v1.0) — the canonical reference |
| [VALIDATION_RULES.md](VALIDATION_RULES.md) | All 21 rules in one page |
| [PROFILES.md](PROFILES.md) | POC vs Full profile comparison |
| [FILE_NAMING.md](FILE_NAMING.md) | Naming conventions and modality codes |
| [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) | Required directory layout |
| [EXAMPLES.md](EXAMPLES.md) | Complete copy-pasteable JSON for every file |
| [QUICKSTART.md](QUICKSTART.md) | From zero to PASS in 15 minutes |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute, governance, versioning |

## Validator

Available as a [PyPI package](https://pypi.org/project/vids-validator/) and as a single-file script. Zero dependencies beyond Python 3.8.

| Category | Rules | Scope |
|----------|-------|-------|
| Structure (S001–S006) | 6 | All profiles |
| Imaging (I001–I004) | 4 | All profiles |
| Annotation (A001–A005) | 5 | All profiles |
| Quality (Q001–Q003) | 3 | Full only |
| ML (M001–M002) | 2 | Full only |
| Metadata (D001) | 1 | All (WARN) |

**Compliant** = zero FAIL rules. That's the only test.

## Relationship to Other Standards

| Standard | What it handles | What it doesn't handle |
|----------|----------------|----------------------|
| **DICOM** | Image acquisition and storage | Annotation structure, provenance, quality docs |
| **BIDS** | Neuroimaging research organization | Multi-modality annotation, automated validation |
| **NIfTI** | Volumetric image file format | Dataset structure, metadata, provenance |
| **COCO / VOC** | Detection annotation format | Medical imaging specifics, provenance, quality |
| **VIDS** | All of the above for annotated medical imaging datasets | Model training, inference, deployment |

VIDS complements these standards. It doesn't replace any of them.

## Tools

| Tool | What it does | How to get it |
|------|-------------|--------------|
| **vids-validator** | 21-rule compliance check | `pip install vids-validator` |
| **vids-init** | Scaffold a VIDS dataset in seconds | `python tools/vids_init.py my-dataset` |

## Contributing

We welcome contributions — spec clarifications, validator improvements, new modality support, and framework integrations. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and governance details.

## License

- **Specification and documentation:** [CC BY 4.0](LICENSE)
- **Tools and reference implementations:** [Apache 2.0](LICENSE-TOOLS)

## Citation

```bibtex
@misc{muthu2026vids,
  title   = {VIDS: A Verified Imaging Dataset Standard for Medical AI},
  author  = {Muthu, Joan S. and Shalen, John},
  year    = {2026},
  eprint  = {2604.17525},
  archivePrefix = {arXiv},
  primaryClass  = {eess.IV},
  url     = {https://arxiv.org/abs/2604.17525}
}
```

---

**VIDS was created by [Princeton Medical Systems](https://princetonmed.systems) and is maintained as an open community standard.**

**Contact:** standards@vidsstandard.org
