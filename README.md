# VIDS — Verified Imaging Dataset Standard

[![VIDS Version](https://img.shields.io/badge/VIDS-v1.0-blue)](SPEC.md)
[![License: CC BY 4.0](https://img.shields.io/badge/Spec-CC%20BY%204.0-lightgrey)](LICENSE)
[![License: Apache 2.0](https://img.shields.io/badge/Tools-Apache%202.0-green)](LICENSE-TOOLS)
[![Validator](https://img.shields.io/badge/validator-21%20rules-orange)](validators/validate_vids.py)
[![CI](https://github.com/vids-standard/vids-standard/actions/workflows/ci.yml/badge.svg)](https://github.com/vids-standard/vids-standard/actions/workflows/ci.yml)

**An open standard for structuring, validating, and delivering annotated medical imaging datasets for AI/ML development.**

VIDS sits above DICOM and BIDS. It defines folder layout, file naming, annotation provenance, quality documentation, and machine-verifiable compliance — so every dataset ships with proof of who annotated what, when, how, and to what quality standard.

---

## Why VIDS?

Medical imaging AI teams waste weeks untangling datasets that arrive as ZIP files full of unnamed NIfTIs and undocumented annotations. VIDS fixes this with:

- **Mandatory provenance** — every annotation records annotator identity, credentials, tool, date, and QC status
- **Automated validation** — run one command, get a pass/fail compliance report with 21 enforceable rules
- **Two profiles** — start with POC (15 rules) for pilots, graduate to Full (21 rules) for production and regulatory
- **Format-agnostic export** — curate once in VIDS, export to nnU-Net, MONAI, COCO, or flat NIfTI without losing provenance

## Quick Start

### Validate an existing dataset

```bash
# Clone the repo
git clone https://github.com/vids-standard/vids-standard.git
cd vids-standard

# Run the validator (zero dependencies — just Python 3.8+)
python validators/validate_vids.py /path/to/your/dataset

# Full profile validation
python validators/validate_vids.py /path/to/your/dataset --profile full

# JSON output for CI pipelines
python validators/validate_vids.py /path/to/your/dataset --json
```

### Minimum viable dataset (POC profile)

```
my-dataset/
├── .vids                          # "profile: poc\nvids_version: 1.0"
├── dataset_description.json       # Name, version, license, authors
├── participants.json              # Subject registry
├── README.md                      # Human-readable description
├── sub-001/
│   └── ses-baseline/
│       └── ct/
│           ├── sub-001_ses-baseline_ct_img.nii.gz
│           └── sub-001_ses-baseline_ct_img.json
└── derivatives/
    └── annotations/
        └── sub-001/
            └── ses-baseline/
                └── ct/
                    ├── sub-001_ses-baseline_ct_seg.nii.gz
                    └── sub-001_ses-baseline_ct_seg.json
```

See [EXAMPLES.md](EXAMPLES.md) for complete, copy-pasteable JSON for every file.

## Specification

| Document | Description |
|----------|-------------|
| [SPEC.md](SPEC.md) | Full specification (v1.0) |
| [VALIDATION_RULES.md](VALIDATION_RULES.md) | All 21 validation rules |
| [PROFILES.md](PROFILES.md) | POC vs Full profile comparison |
| [FILE_NAMING.md](FILE_NAMING.md) | Naming conventions and modality codes |
| [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) | Required directory layout |
| [EXAMPLES.md](EXAMPLES.md) | Complete example datasets for both profiles |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute, governance, versioning |

## Validator

The reference validator (`validators/validate_vids.py`) is a single-file, zero-dependency Python script that checks all 21 rules:

| Category | Rules | Scope |
|----------|-------|-------|
| Structure (S001–S006) | 6 | All profiles |
| Imaging (I001–I004) | 4 | All profiles |
| Annotation (A001–A005) | 5 | All profiles |
| Quality (Q001–Q003) | 3 | Full only |
| ML (M001–M002) | 2 | Full only |
| Metadata (D001) | 1 | All (WARN) |

A dataset is **compliant** if and only if zero rules have FAIL status.

## Relationship to Other Standards

| Standard | Relationship |
|----------|-------------|
| **DICOM** | Source data format — VIDS handles what comes after conversion |
| **BIDS** | Naming inspiration (`sub-`, `ses-`) — VIDS extends to multi-modality annotation with provenance |
| **NIfTI** | Default file format for imaging and segmentation volumes |
| **nnU-Net / MONAI** | Export targets — VIDS datasets can be converted to these framework layouts |
| **COCO / VOC** | Export targets for detection tasks |

## Contributing

We welcome contributions — spec clarifications, validator improvements, new modality support, and framework integrations. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and governance details.

## License

- **Specification and documentation:** [CC BY 4.0](LICENSE)
- **Tools and reference implementations:** [Apache 2.0](LICENSE-TOOLS)

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

**VIDS was created by [Princeton Medical Systems](https://princetonmed.systems) and is maintained as an open community standard.**
