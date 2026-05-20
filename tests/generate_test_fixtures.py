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


def create_classification(root: Path):
    """Create a POC-profile dataset with a _cls.json (classification) annotation."""
    root.mkdir(parents=True, exist_ok=True)

    write_text(root / '.vids', 'profile: poc\nvids_version: 1.0\n')

    write_json(root / 'dataset_description.json', {
        "Name": "Example Classification Dataset",
        "VIDSVersion": "1.0",
        "DatasetVersion": "1.0.0",
        "License": "CC BY 4.0",
        "Description": "Minimal single-subject POC dataset with image-level classification.",
        "Authors": ["VIDS Examples Working Group"]
    })

    write_json(root / 'participants.json', {
        "VIDSVersion": "1.0",
        "Participants": [
            {"SubjectID": "sub-001", "Age": 55, "Sex": "F",
             "DataSource": "Synthetic example"}
        ]
    })

    write_text(root / 'README.md',
        '# Example Classification Dataset\n\n'
        'Minimal VIDS-compliant dataset for CI validation.\n\n'
        '## Contents\n\n'
        '- 1 subject, 1 session, fundus modality\n'
        '- Classification annotation with provenance\n\n'
        '## Contact\n\nstandards@vidsstandard.org\n')

    img_dir = root / 'sub-001' / 'ses-baseline' / 'fundus'
    create_nifti_stub(img_dir / 'sub-001_ses-baseline_fundus_img.nii.gz')
    write_json(img_dir / 'sub-001_ses-baseline_fundus_img.json', {
        "VIDSVersion": "1.0",
        "SourceFormat": "DICOM",
        "ConversionTool": "dcm2niix v1.0.20240202",
        "ConversionDate": "2026-02-10"
    })

    ann_dir = root / 'derivatives' / 'annotations' / 'sub-001' / 'ses-baseline' / 'fundus'
    write_json(ann_dir / 'sub-001_ses-baseline_fundus_cls.json', {
        "VIDSVersion": "1.0",
        "AnnotationType": "classification",
        "SourceImage": "sub-001_ses-baseline_fundus_img.nii.gz",
        "Classifications": [
            {"SubjectID": "sub-001", "Label": "no_dr", "Confidence": 0.92}
        ],
        "Provenance": {
            "Annotator": {
                "ID": "rater_001",
                "Name": "Dr. Jane Smith",
                "Credentials": "MD, Board-certified ophthalmologist"
            },
            "AnnotationProcess": {
                "Tool": "VIDS-CLS-Tool",
                "ToolVersion": "0.1.0",
                "Date": "2026-02-12",
                "Method": "Manual classification"
            }
        }
    })


def create_detection(root: Path):
    """Create a POC-profile dataset with a _bbox.json (detection) annotation."""
    root.mkdir(parents=True, exist_ok=True)

    write_text(root / '.vids', 'profile: poc\nvids_version: 1.0\n')

    write_json(root / 'dataset_description.json', {
        "Name": "Example Detection Dataset",
        "VIDSVersion": "1.0",
        "DatasetVersion": "1.0.0",
        "License": "CC BY 4.0",
        "Description": "Minimal single-subject POC dataset with bounding-box detection annotations.",
        "Authors": ["VIDS Examples Working Group"]
    })

    write_json(root / 'participants.json', {
        "VIDSVersion": "1.0",
        "Participants": [
            {"SubjectID": "sub-001", "Age": 48, "Sex": "M",
             "DataSource": "Synthetic example"}
        ]
    })

    write_text(root / 'README.md',
        '# Example Detection Dataset\n\n'
        'Minimal VIDS-compliant dataset for CI validation.\n\n'
        '## Contents\n\n'
        '- 1 subject, 1 session, xr modality\n'
        '- Bounding-box detection annotation with provenance\n\n'
        '## Contact\n\nstandards@vidsstandard.org\n')

    img_dir = root / 'sub-001' / 'ses-baseline' / 'xr'
    create_nifti_stub(img_dir / 'sub-001_ses-baseline_xr_img.nii.gz')
    write_json(img_dir / 'sub-001_ses-baseline_xr_img.json', {
        "VIDSVersion": "1.0",
        "SourceFormat": "DICOM",
        "ConversionTool": "dcm2niix v1.0.20240202",
        "ConversionDate": "2026-02-10"
    })

    ann_dir = root / 'derivatives' / 'annotations' / 'sub-001' / 'ses-baseline' / 'xr'
    write_json(ann_dir / 'sub-001_ses-baseline_xr_bbox.json', {
        "VIDSVersion": "1.0",
        "AnnotationType": "bbox",
        "SourceImage": "sub-001_ses-baseline_xr_img.nii.gz",
        "CoordinateSystem": "voxels",
        "BoundingBoxes": [
            {"SubjectID": "sub-001", "Label": "lesion",
             "Coords": {"x": 5, "y": 5, "z": 0, "w": 10, "h": 10, "d": 1}}
        ],
        "Provenance": {
            "Annotator": {
                "ID": "rater_001",
                "Name": "Dr. Alex Lee",
                "Credentials": "MD, Board-certified radiologist"
            },
            "AnnotationProcess": {
                "Tool": "VIDS-BBox-Tool",
                "ToolVersion": "0.1.0",
                "Date": "2026-02-12",
                "Method": "Manual bounding-box annotation"
            }
        }
    })


def create_landmark(root: Path):
    """Create a POC-profile dataset with a _lm.json (landmark) annotation."""
    root.mkdir(parents=True, exist_ok=True)

    write_text(root / '.vids', 'profile: poc\nvids_version: 1.0\n')

    write_json(root / 'dataset_description.json', {
        "Name": "Example Landmark Dataset",
        "VIDSVersion": "1.0",
        "DatasetVersion": "1.0.0",
        "License": "CC BY 4.0",
        "Description": "Minimal single-subject POC dataset with anatomical landmark annotations.",
        "Authors": ["VIDS Examples Working Group"]
    })

    write_json(root / 'participants.json', {
        "VIDSVersion": "1.0",
        "Participants": [
            {"SubjectID": "sub-001", "Age": 35, "Sex": "F",
             "DataSource": "Synthetic example"}
        ]
    })

    write_text(root / 'README.md',
        '# Example Landmark Dataset\n\n'
        'Minimal VIDS-compliant dataset for CI validation.\n\n'
        '## Contents\n\n'
        '- 1 subject, 1 session, mr modality\n'
        '- Landmark annotation with provenance\n\n'
        '## Contact\n\nstandards@vidsstandard.org\n')

    img_dir = root / 'sub-001' / 'ses-baseline' / 'mr'
    create_nifti_stub(img_dir / 'sub-001_ses-baseline_mr_img.nii.gz')
    write_json(img_dir / 'sub-001_ses-baseline_mr_img.json', {
        "VIDSVersion": "1.0",
        "SourceFormat": "DICOM",
        "ConversionTool": "dcm2niix v1.0.20240202",
        "ConversionDate": "2026-02-10"
    })

    ann_dir = root / 'derivatives' / 'annotations' / 'sub-001' / 'ses-baseline' / 'mr'
    write_json(ann_dir / 'sub-001_ses-baseline_mr_lm.json', {
        "VIDSVersion": "1.0",
        "AnnotationType": "landmark",
        "SourceImage": "sub-001_ses-baseline_mr_img.nii.gz",
        "CoordinateSystem": "voxels",
        "Landmarks": [
            {"Name": "anterior_commissure", "Coords": {"x": 12, "y": 8, "z": 0}}
        ],
        "Provenance": {
            "Annotator": {
                "ID": "rater_001",
                "Name": "Dr. Morgan Rivera",
                "Credentials": "MD, Board-certified neuroradiologist"
            },
            "AnnotationProcess": {
                "Tool": "VIDS-LM-Tool",
                "ToolVersion": "0.1.0",
                "Date": "2026-02-12",
                "Method": "Manual landmark placement"
            }
        }
    })


def create_roi(root: Path):
    """Create a POC-profile dataset with a _roi.json (region-of-interest) annotation."""
    root.mkdir(parents=True, exist_ok=True)

    write_text(root / '.vids', 'profile: poc\nvids_version: 1.0\n')

    write_json(root / 'dataset_description.json', {
        "Name": "Example ROI Dataset",
        "VIDSVersion": "1.0",
        "DatasetVersion": "1.0.0",
        "License": "CC BY 4.0",
        "Description": "Minimal single-subject POC dataset with polygon ROI annotations.",
        "Authors": ["VIDS Examples Working Group"]
    })

    write_json(root / 'participants.json', {
        "VIDSVersion": "1.0",
        "Participants": [
            {"SubjectID": "sub-001", "Age": 70, "Sex": "M",
             "DataSource": "Synthetic example"}
        ]
    })

    write_text(root / 'README.md',
        '# Example ROI Dataset\n\n'
        'Minimal VIDS-compliant dataset for CI validation.\n\n'
        '## Contents\n\n'
        '- 1 subject, 1 session, ct modality\n'
        '- ROI polygon annotation with provenance\n\n'
        '## Contact\n\nstandards@vidsstandard.org\n')

    img_dir = root / 'sub-001' / 'ses-baseline' / 'ct'
    create_nifti_stub(img_dir / 'sub-001_ses-baseline_ct_img.nii.gz')
    write_json(img_dir / 'sub-001_ses-baseline_ct_img.json', {
        "VIDSVersion": "1.0",
        "SourceFormat": "DICOM",
        "ConversionTool": "dcm2niix v1.0.20240202",
        "ConversionDate": "2026-02-10"
    })

    ann_dir = root / 'derivatives' / 'annotations' / 'sub-001' / 'ses-baseline' / 'ct'
    write_json(ann_dir / 'sub-001_ses-baseline_ct_roi.json', {
        "VIDSVersion": "1.0",
        "AnnotationType": "roi",
        "SourceImage": "sub-001_ses-baseline_ct_img.nii.gz",
        "CoordinateSystem": "voxels",
        "Regions": [
            {"Name": "liver_segment_7",
             "Polygon": [[5, 5, 0], [15, 5, 0], [15, 15, 0], [5, 15, 0]]}
        ],
        "Provenance": {
            "Annotator": {
                "ID": "rater_001",
                "Name": "Dr. Casey Park",
                "Credentials": "MD, Board-certified abdominal radiologist"
            },
            "AnnotationProcess": {
                "Tool": "VIDS-ROI-Tool",
                "ToolVersion": "0.1.0",
                "Date": "2026-02-12",
                "Method": "Manual polygon ROI"
            }
        }
    })


def _create_negative_base(root: Path) -> Path:
    """Create a valid POC scaffold (subject, session, imaging, empty annotations dir).

    Returns the annotation directory so the caller can plant its intentional
    defect (a missing pair, a malformed JSON, etc.) without re-emitting the rest.
    """
    root.mkdir(parents=True, exist_ok=True)
    write_text(root / '.vids', 'profile: poc\nvids_version: 1.0\n')
    write_json(root / 'dataset_description.json', {
        "Name": "Negative Test Fixture",
        "VIDSVersion": "1.0",
        "DatasetVersion": "1.0.0",
        "License": "CC BY 4.0",
        "Description": "Intentionally malformed for validator negative tests.",
        "Authors": ["VIDS Examples Working Group"]
    })
    write_json(root / 'participants.json', {
        "VIDSVersion": "1.0",
        "Participants": [
            {"SubjectID": "sub-001", "Age": 40, "Sex": "F",
             "DataSource": "Synthetic example"}
        ]
    })
    write_text(root / 'README.md',
        '# Negative Test Fixture\n\nIntentionally malformed for validator negative tests.\n')
    img_dir = root / 'sub-001' / 'ses-baseline' / 'ct'
    create_nifti_stub(img_dir / 'sub-001_ses-baseline_ct_img.nii.gz')
    write_json(img_dir / 'sub-001_ses-baseline_ct_img.json', {
        "VIDSVersion": "1.0",
        "SourceFormat": "DICOM",
        "ConversionTool": "dcm2niix v1.0.20240202",
        "ConversionDate": "2026-02-10"
    })
    ann_dir = root / 'derivatives' / 'annotations' / 'sub-001' / 'ses-baseline' / 'ct'
    ann_dir.mkdir(parents=True, exist_ok=True)
    return ann_dir


def _good_provenance() -> dict:
    """Realistic populated provenance block reused across negative fixtures
    that need a valid Provenance to isolate the intended failure rule."""
    return {
        "Annotator": {
            "ID": "rater_001",
            "Name": "Dr. Jane Smith",
            "Credentials": "MD"
        },
        "AnnotationProcess": {
            "Tool": "VIDS-CLS-Tool",
            "ToolVersion": "0.1.0",
            "Date": "2026-02-12",
            "Method": "Manual classification"
        }
    }


def create_negative_fixtures(parent_root: Path):
    """Create the negative-test fixture set under parent_root.

    Each subdirectory is a valid POC structure with exactly one intentional
    defect that targets a specific A-rule failure:
      empty-annotations/   → A002 FAIL (annotations dir exists but empty)
      unpaired-seg/        → A003 FAIL (_seg.nii.gz without paired _seg.json)
      malformed-cls/       → A004 FAIL (_cls.json contains invalid JSON)
      missing-version/     → A004 FAIL (_cls.json missing VIDSVersion)
      missing-provenance/  → A005 FAIL (_cls.json missing populated Provenance)
    """
    # empty-annotations: annotations dir created by the helper, no files added
    _create_negative_base(parent_root / 'empty-annotations')

    # unpaired-seg: seg binary present, no paired sidecar
    ann_dir = _create_negative_base(parent_root / 'unpaired-seg')
    create_nifti_stub(ann_dir / 'sub-001_ses-baseline_ct_seg.nii.gz')

    # malformed-cls: not valid JSON
    ann_dir = _create_negative_base(parent_root / 'malformed-cls')
    write_text(ann_dir / 'sub-001_ses-baseline_ct_cls.json',
               '{ this is not valid JSON ::: \n')

    # missing-version: valid JSON, populated Provenance, no VIDSVersion field
    ann_dir = _create_negative_base(parent_root / 'missing-version')
    write_json(ann_dir / 'sub-001_ses-baseline_ct_cls.json', {
        "AnnotationType": "classification",
        "SourceImage": "sub-001_ses-baseline_ct_img.nii.gz",
        "Classifications": [
            {"SubjectID": "sub-001", "Label": "no_dr", "Confidence": 0.92}
        ],
        "Provenance": _good_provenance()
    })

    # missing-provenance: valid JSON, has VIDSVersion, Annotator and
    # AnnotationProcess both empty (neither ID/Name nor Tool/Date populated)
    ann_dir = _create_negative_base(parent_root / 'missing-provenance')
    write_json(ann_dir / 'sub-001_ses-baseline_ct_cls.json', {
        "VIDSVersion": "1.0",
        "AnnotationType": "classification",
        "SourceImage": "sub-001_ses-baseline_ct_img.nii.gz",
        "Classifications": [],
        "Provenance": {
            "Annotator": {},
            "AnnotationProcess": {}
        }
    })


if __name__ == '__main__':
    import shutil
    # Clean previous fixtures
    if FIXTURES_DIR.exists():
        shutil.rmtree(FIXTURES_DIR)

    create_poc(FIXTURES_DIR / 'example-poc')
    create_full(FIXTURES_DIR / 'example-full')
    create_classification(FIXTURES_DIR / 'example-classification')
    create_detection(FIXTURES_DIR / 'example-detection')
    create_landmark(FIXTURES_DIR / 'example-landmark')
    create_roi(FIXTURES_DIR / 'example-roi')
    create_negative_fixtures(FIXTURES_DIR / 'negative')

    print(f"✅ Test fixtures generated in {FIXTURES_DIR}")
    print(f"   example-poc/            — POC profile (seg)")
    print(f"   example-full/           — Full profile (seg)")
    print(f"   example-classification/ — POC profile (cls)")
    print(f"   example-detection/      — POC profile (bbox)")
    print(f"   example-landmark/       — POC profile (lm)")
    print(f"   example-roi/            — POC profile (roi)")
    print(f"   negative/               — 5 intentionally malformed fixtures")
