#!/usr/bin/env python3
"""
Generate minimal VIDS test fixture datasets for CI validation.
Creates example-poc and example-full datasets with NIfTI stubs.
"""

import json
import gzip
import struct
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def create_nifti_stub(path: Path):
    """Create a minimal valid NIfTI-1 .nii.gz file (2x2x2 voxels)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # Minimal NIfTI-1 header (348 bytes) + 8 voxels of float32
    header = bytearray(348)
    # sizeof_hdr = 348
    struct.pack_into('<i', header, 0, 348)
    # dim: ndim=3, 2x2x2
    struct.pack_into('<8h', header, 40, 3, 2, 2, 2, 1, 1, 1, 1)
    # datatype = 16 (float32), bitpix = 32
    struct.pack_into('<h', header, 70, 16)
    struct.pack_into('<h', header, 72, 32)
    # pixdim
    struct.pack_into('<8f', header, 76, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    # vox_offset = 352.0
    struct.pack_into('<f', header, 108, 352.0)
    # magic = "n+1\0"
    header[344:348] = b'n+1\x00'
    # 4 bytes extension pad + 8 float32 voxels
    data = header + b'\x00' * 4 + struct.pack('<8f', *([0.0] * 8))
    with gzip.open(str(path), 'wb') as f:
        f.write(data)


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def create_poc(root: Path):
    """Create a minimal POC-profile dataset."""
    root.mkdir(parents=True, exist_ok=True)

    # .vids
    write_text(root / '.vids', 'profile: poc\nvids_version: 1.0\n')

    # dataset_description.json
    write_json(root / 'dataset_description.json', {
        "Name": "Example POC Dataset",
        "VIDSVersion": "1.0",
        "DatasetVersion": "1.0.0",
        "License": "CC BY 4.0",
        "Description": "Minimal single-subject POC dataset for CI testing.",
        "Authors": ["VIDS Examples Working Group"]
    })

    # participants.json
    write_json(root / 'participants.json', {
        "VIDSVersion": "1.0",
        "Participants": [
            {"SubjectID": "sub-001", "Age": 62, "Sex": "F",
             "DataSource": "Synthetic example"}
        ]
    })

    # README.md
    write_text(root / 'README.md',
        '# Example POC Dataset\n\n'
        'Minimal VIDS-compliant dataset for CI validation.\n\n'
        '## Contents\n\n'
        '- 1 subject, 1 session, CT modality\n'
        '- Segmentation annotation with provenance\n\n'
        '## Contact\n\nstandards@vidsstandard.org\n')

    # Imaging
    img_dir = root / 'sub-001' / 'ses-baseline' / 'ct'
    create_nifti_stub(img_dir / 'sub-001_ses-baseline_ct_img.nii.gz')
    write_json(img_dir / 'sub-001_ses-baseline_ct_img.json', {
        "VIDSVersion": "1.0",
        "SourceFormat": "DICOM",
        "ConversionTool": "dcm2niix v1.0.20240202",
        "ConversionDate": "2026-02-10"
    })

    # Annotations
    ann_dir = root / 'derivatives' / 'annotations' / 'sub-001' / 'ses-baseline' / 'ct'
    create_nifti_stub(ann_dir / 'sub-001_ses-baseline_ct_seg.nii.gz')
    write_json(ann_dir / 'sub-001_ses-baseline_ct_seg.json', {
        "VIDSVersion": "1.0",
        "AnnotationType": "segmentation",
        "SourceImage": "sub-001_ses-baseline_ct_img.nii.gz",
        "LabelMap": {"0": "background", "1": "nodule"},
        "Provenance": {
            "Annotator": {
                "ID": "radiologist_001",
                "Name": "Dr. Jane Smith",
                "Credentials": "MD, Board-certified radiologist"
            },
            "AnnotationProcess": {
                "Tool": "3D Slicer",
                "ToolVersion": "5.6.2",
                "Date": "2026-02-12",
                "Method": "Manual segmentation"
            },
            "QualityControl": {
                "ReviewedBy": "senior_radiologist_001",
                "ReviewDate": "2026-02-13",
                "ReviewOutcome": "approved"
            }
        }
    })


def create_full(root: Path):
    """Create a minimal Full-profile dataset (extends POC)."""
    # Start with POC
    create_poc(root)

    # Override .vids to full
    write_text(root / '.vids', 'profile: full\nvids_version: 1.0\n')

    # Update dataset_description
    write_json(root / 'dataset_description.json', {
        "Name": "Example Full Dataset",
        "VIDSVersion": "1.0",
        "DatasetVersion": "1.0.0",
        "License": "CC BY 4.0",
        "Description": "Minimal single-subject Full profile dataset for CI testing.",
        "Authors": ["VIDS Examples Working Group"]
    })

    # CHANGES.md
    write_text(root / 'CHANGES.md',
        '# Changes\n\n'
        '## [1.0.0] - 2026-02-16\n'
        '- Initial release\n'
        '- 1 subject with lung nodule segmentation\n')

    # quality/
    write_json(root / 'quality' / 'quality_summary.json', {
        "VIDSVersion": "1.0",
        "Profile": "full",
        "DatasetName": "Example Full Dataset",
        "DatasetVersion": "1.0.0",
        "QualityAssessmentDate": "2026-02-15",
        "AnnotationStatistics": {
            "TotalSubjects": 1,
            "TotalAnnotations": 1
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
        }
    })

    write_json(root / 'quality' / 'annotation_agreement.json', {
        "VIDSVersion": "1.0",
        "Methodology": {
            "Method": "Dice Coefficient",
            "SamplingStrategy": "All subjects (100%)"
        },
        "AggregateStatistics": {
            "Mean": 0.91,
            "StandardDeviation": 0.0,
            "Min": 0.91,
            "Max": 0.91
        },
        "PerSubjectResults": [
            {"SubjectID": "sub-001", "DiceCoefficient": 0.91, "Quality": "excellent"}
        ]
    })

    # ml/
    write_json(root / 'ml' / 'splits.json', {
        "VIDSVersion": "1.0",
        "SplitStrategy": "single-subject-example",
        "SplitRatio": "100/0/0",
        "RandomSeed": 42,
        "Splits": {
            "train": ["sub-001"],
            "val": [],
            "test": []
        },
        "Notes": "Minimal example. Real datasets should use 70/15/15 or similar."
    })


if __name__ == '__main__':
    import shutil
    # Clean previous fixtures
    if FIXTURES_DIR.exists():
        shutil.rmtree(FIXTURES_DIR)

    create_poc(FIXTURES_DIR / 'example-poc')
    create_full(FIXTURES_DIR / 'example-full')

    print(f"✅ Test fixtures generated in {FIXTURES_DIR}")
    print(f"   example-poc/  — POC profile")
    print(f"   example-full/ — Full profile")
