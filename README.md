# VIDS — Verified Imaging Dataset Standard

[![VIDS Version](https://img.shields.io/badge/VIDS-v1.0.1-blue)](SPEC.md)
[![PyPI](https://img.shields.io/pypi/v/vids-validator?prefix=v&label=pypi&color=blue)](https://pypi.org/project/vids-validator/)
[![License: CC BY 4.0](https://img.shields.io/badge/Spec-CC%20BY%204.0-lightgrey)](LICENSE)
[![License: Apache 2.0](https://img.shields.io/badge/Tools-Apache%202.0-green)](LICENSE-Apache-2.0.txt)
[![Validator](https://img.shields.io/badge/validator-21%20rules-orange)](validators/validate_vids.py)
[![CI](https://github.com/vids-standard/vids-standard/actions/workflows/ci.yml/badge.svg)](https://github.com/vids-standard/vids-standard/actions/workflows/ci.yml)

**A machine-checkable documentation standard for medical imaging AI datasets.**

VIDS specifies what a dataset should document about its structure, annotation provenance, and quality, in a form a validator can check. The validator evaluates 21 rules, with each rule reporting PASS, FAIL, WARN, or SKIP.

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
  ✅ D001: Metadata documentation          PASS

  ✅ VALIDATION PASSED (21/21 rules)
```

---

## Paper

**VIDS: A Verified Imaging Dataset Standard for Medical AI**
Dr. Joan S. Muthu, John Shalen — Princeton Medical Systems
[arXiv:2604.17525](https://arxiv.org/abs/2604.17525)

Four major public datasets (LIDC-IDRI, BraTS, CheXpert, Medical Segmentation Decathlon) scored against 22 compliance dimensions used in the paper's analysis, which are broader than the 21 rules the validator enforces. Average: 29%. Provenance: 8%. The paper presents the full spec design, the compliance analysis, and LIDC-Hybrid-100, a 100-subject VIDS-compliant reference CT dataset published on [Zenodo](https://doi.org/10.5281/zenodo.19582717).

Compliance analysis data: [vids-benchmarks](https://github.com/vids-standard/vids-benchmarks)
Compliance analysis methodology: [COMPLIANCE_ANALYSIS.md](COMPLIANCE_ANALYSIS.md)

---

## Why VIDS?

Medical imaging AI teams spend weeks untangling datasets that arrive as ZIP files full of unnamed NIfTIs and undocumented annotations. Who annotated what, when, and whether anyone reviewed it is often unrecorded. VIDS asks a dataset to document these things and makes the documentation checkable:

- **Required provenance.** Every annotation sidecar identifies the annotator and records annotation-process provenance; credentials and QC documentation are supported as recommended provenance fields
- **Automated validation.** One command, 21 machine-checkable rules, with PASS, FAIL, WARN, and SKIP outcomes
- **Two profiles.** POC (15 rules) for pilots, Full (21 rules) for production work
- **Interoperable structure.** VIDS preserves dataset-level documentation and provenance in a structured form that can accompany downstream transformations and framework-specific exports

DICOM handles image acquisition and storage. BIDS handles neuroimaging research organization. VIDS addresses a level neither covers: the dataset as a curated artifact, with documented annotation provenance and curation history. It complements both and replaces neither.

## Quick Start

### Option 1: Scaffold a new dataset (recommended)

```bash
pip install vids-validator
git clone https://github.com/vids-standard/vids-standard.git

# Create a VIDS dataset skeleton that passes validation immediately
python vids-standard/tools/vids_init.py my-dataset --subjects 10 --modality ct --profile poc

# Validate
vids-validate my-dataset/
# POC profile: 15 applicable rules pass; 6 Full-only rules are skipped
# ✅ VALIDATION PASSED (15/21 rules)
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

The provenance schema can document **who** annotated, **when**, **with what tool**, and **what QC was performed**:

```json
{
  "Provenance": {
    "Annotator": { "ID": "radiologist_001", "Credentials": "MD, Board-certified" },
    "AnnotationProcess": { "Tool": "3D Slicer", "Date": "2026-03-25" },
    "QualityControl": { "ReviewedBy": "senior_rad_001", "ReviewOutcome": "approved" }
  }
}
```

Required provenance applies to both POC and Full profiles. If the required annotator and annotation-process provenance is missing, the validator fails.

## Specification

| Document | What's in it |
|----------|-------------|
| [SPEC.md](SPEC.md) | Full specification (v1.0.1). The canonical reference for core VIDS conformance requirements |
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
| Metadata (D001) | 1 | Full only (WARN) |

A dataset conforms when no rule fails. Conformance means the documentation the specification asks for is present and correctly structured. It is not a statement about data quality, annotation correctness, or fitness for any particular research, clinical or regulatory purpose.

## Relationship to Other Standards

| Standard | Primary role | VIDS distinction |
|----------|-------------|------------------|
| **DICOM** | Medical image acquisition, exchange and storage, including structured imaging objects | VIDS specifies dataset-level organization, annotation provenance and curation documentation |
| **BIDS** | Standardized organization and validation of primarily research imaging datasets | VIDS focuses on curated medical imaging AI datasets, annotation provenance and associated quality documentation |
| **NIfTI** | Volumetric image file format | VIDS adds dataset structure, metadata and provenance requirements |
| **COCO / VOC** | General-purpose annotation representations | VIDS adds medical-imaging dataset structure, provenance and quality documentation |
| **VIDS** | Dataset-level documentation and machine-checkable conformance | Does not assess model performance, clinical outcomes, bias or fitness for use |

VIDS complements these standards. It doesn't replace any of them.

## Tools

| Tool | What it does | How to get it |
|------|-------------|--------------|
| **vids-validator** | 21-rule conformance check | `pip install vids-validator` |
| **vids-init** | Scaffold a VIDS dataset in seconds | `python tools/vids_init.py my-dataset` |

## Governance

VIDS is maintained by a Steering Committee at Princeton Medical Systems under published governance. How decisions are made, who makes them, and where each decision is recorded is documented at [vidsstandard.org/governance](https://vidsstandard.org/governance/), including the full record of accepted governance decisions.

The VIDS Specification and its normative extensions are the only sources of VIDS conformance requirements. The validator implements machine-checkable requirements from the Specification. Where the two disagree, the Specification governs, and the discrepancy is recorded and corrected.

## Contributing

We welcome contributions: specification clarifications, validator improvements, new modality support, and framework integrations. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and the change process.

## License

- **Specification and documentation:** [CC BY 4.0](LICENSE)
- **Tools and reference implementations:** [Apache 2.0](LICENSE-Apache-2.0.txt)

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

**VIDS was created and is maintained by [Princeton Medical Systems](https://princetonmedicalsystems.com) as an open standard, under the governance published at [vidsstandard.org/governance](https://vidsstandard.org/governance/).**

**Contact:** standards@vidsstandard.org
