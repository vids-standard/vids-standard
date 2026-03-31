#!/usr/bin/env python3
"""
vids-init — Scaffold a VIDS-compliant dataset in seconds.

Creates the complete directory structure, template JSON files, and placeholder
NIfTI stubs so you can fill in your data and pass the validator immediately.

Usage:
    vids-init my-dataset --subjects 10 --modality ct --profile poc
    vids-init my-dataset --subjects 50 --modality mr --profile full
    vids-init my-dataset --subjects 5 --modality ct --session baseline followup
    vids-init my-dataset --subjects 3 --modality ct mr --profile full

Zero dependencies beyond Python 3.8+ standard library.
"""

import json
import sys
import gzip
import struct
import argparse
from pathlib import Path
from datetime import datetime, timezone


def create_nifti_stub(path):
    """Create a minimal valid NIfTI-1 .nii.gz file (2x2x2 voxels).

    This is a placeholder. Replace with your actual imaging/segmentation data.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    header = bytearray(348)
    struct.pack_into('<i', header, 0, 348)
    struct.pack_into('<8h', header, 40, 3, 2, 2, 2, 1, 1, 1, 1)
    struct.pack_into('<h', header, 70, 16)
    struct.pack_into('<h', header, 72, 32)
    struct.pack_into('<8f', header, 76, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    struct.pack_into('<f', header, 108, 352.0)
    header[344:348] = b'n+1\x00'
    data = header + b'\x00' * 4 + struct.pack('<8f', *([0.0] * 8))
    with gzip.open(str(path), 'wb') as f:
        f.write(data)


def write_json(path, data):
    """Write JSON with consistent formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def write_text(path, text):
    """Write text file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def zero_pad(n, total):
    """Generate zero-padded subject ID."""
    width = max(3, len(str(total)))
    return str(n).zfill(width)


def scaffold_dataset(args):
    """Create the complete VIDS dataset scaffold."""
    root = Path(args.name).resolve()
    if root.exists() and any(root.iterdir()):
        print(f"Error: {root} already exists and is not empty.", file=sys.stderr)
        print(f"Remove it first or choose a different name.", file=sys.stderr)
        sys.exit(1)

    root.mkdir(parents=True, exist_ok=True)

    profile = args.profile
    n_subjects = args.subjects
    modalities = args.modality
    sessions = args.session
    dataset_name = args.dataset_name or args.name
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print(f"\nScaffolding VIDS dataset: {root.name}")
    print(f"  Profile:    {profile}")
    print(f"  Subjects:   {n_subjects}")
    print(f"  Sessions:   {', '.join(sessions)}")
    print(f"  Modalities: {', '.join(modalities)}")
    print()

    # ── .vids marker ────────────────────────────────────────
    write_text(root / ".vids", f"profile: {profile}\nvids_version: 1.0\n")
    print(f"  ✅ .vids")

    # ── dataset_description.json ────────────────────────────
    write_json(root / "dataset_description.json", {
        "Name": dataset_name,
        "VIDSVersion": "1.0",
        "DatasetVersion": "1.0.0",
        "License": "CC BY 4.0",
        "Description": f"TODO: Describe your dataset here. "
                       f"{n_subjects} subjects, "
                       f"{', '.join(m.upper() for m in modalities)} modality.",
        "Authors": ["TODO: Your organization or author names"],
        "Created": today,
        "LastModified": today
    })
    print(f"  ✅ dataset_description.json")

    # ── participants.json ───────────────────────────────────
    participants = {
        "VIDSVersion": "1.0",
        "Participants": [
            {
                "SubjectID": f"sub-{zero_pad(i, n_subjects)}",
                "Age": "TODO",
                "Sex": "TODO",
                "InclusionCriteria": "TODO",
                "DataSource": "TODO"
            }
            for i in range(1, n_subjects + 1)
        ]
    }
    write_json(root / "participants.json", participants)
    print(f"  ✅ participants.json ({n_subjects} entries)")

    # ── README.md ───────────────────────────────────────────
    readme = f"""# {dataset_name}

TODO: Describe your dataset in detail.

## Contents

- {n_subjects} subjects
- Sessions: {', '.join(sessions)}
- Modalities: {', '.join(m.upper() for m in modalities)}
- Annotation type: segmentation

## VIDS Compliance

This dataset follows the [VIDS v1.0 specification](https://github.com/vids-standard/vids-standard).

Profile: **{profile.upper()}**

Validate with:
```bash
pip install vids-validator
vids-validate {root.name}/ --profile {profile}
```

## Contact

TODO: Add contact information

## Citation

TODO: Add citation guidance
"""
    write_text(root / "README.md", readme)
    print(f"  ✅ README.md")

    # ── CHANGES.md ──────────────────────────────────────────
    write_text(root / "CHANGES.md", f"""# Changes

## [1.0.0] - {today}
- Initial release
- {n_subjects} subjects with segmentation annotations
""")
    print(f"  ✅ CHANGES.md")

    # ── Subject/session/modality structure ──────────────────
    file_count = 0
    for i in range(1, n_subjects + 1):
        sub_id = f"sub-{zero_pad(i, n_subjects)}"

        for ses in sessions:
            ses_id = f"ses-{ses}"

            for mod in modalities:
                stem = f"{sub_id}_{ses_id}_{mod}"

                # Imaging files
                img_dir = root / sub_id / ses_id / mod
                create_nifti_stub(img_dir / f"{stem}_img.nii.gz")

                write_json(img_dir / f"{stem}_img.json", {
                    "VIDSVersion": "1.0",
                    "SourceFormat": "TODO: DICOM | NIfTI | NRRD | Other",
                    "ConversionTool": "TODO: e.g., dcm2niix v1.0.20240202",
                    "ConversionDate": today,
                    "AcquisitionParameters": {
                        "SliceThickness_mm": "TODO",
                        "PixelSpacing_mm": "TODO: [x, y]",
                        "ImageDimensions": "TODO: [w, h, d]",
                        "Manufacturer": "TODO",
                        "ManufacturerModel": "TODO"
                    },
                    "DeIdentification": {
                        "Method": "TODO: HIPAA Safe Harbor | Expert Determination",
                        "Tool": "TODO",
                        "Date": today,
                        "VerifiedBy": "TODO"
                    }
                })

                # Annotation files
                ann_dir = root / "derivatives" / "annotations" / sub_id / ses_id / mod
                create_nifti_stub(ann_dir / f"{stem}_seg.nii.gz")

                write_json(ann_dir / f"{stem}_seg.json", {
                    "VIDSVersion": "1.0",
                    "AnnotationType": "segmentation",
                    "Description": "TODO: What was annotated",
                    "SourceImage": f"{stem}_img.nii.gz",
                    "LabelMap": {
                        "0": "background",
                        "1": "TODO: class name (e.g., tumor, nodule, organ)"
                    },
                    "Provenance": {
                        "Annotator": {
                            "ID": "TODO: annotator_001",
                            "Name": "TODO: Dr. Name",
                            "Credentials": "TODO: e.g., MD, Board-certified radiologist",
                            "Specialty": "TODO"
                        },
                        "AnnotationProcess": {
                            "Tool": "TODO: e.g., 3D Slicer",
                            "ToolVersion": "TODO: e.g., 5.6.2",
                            "Date": today,
                            "TimeSpent_minutes": "TODO",
                            "Method": "TODO: Manual segmentation | Semi-automated | Automated with review"
                        },
                        "QualityControl": {
                            "ReviewedBy": "TODO: reviewer_001",
                            "ReviewDate": "TODO",
                            "ReviewOutcome": "TODO: approved | revisions_requested | rejected"
                        }
                    }
                })

                file_count += 4  # 2 NIfTI + 2 JSON per subject/session/modality

    print(f"  ✅ {n_subjects} subjects x {len(sessions)} sessions x "
          f"{len(modalities)} modalities = {file_count} files")

    # ── Quality directory (Full profile) ────────────────────
    if profile == "full":
        quality_dir = root / "quality"

        write_json(quality_dir / "quality_summary.json", {
            "VIDSVersion": "1.0",
            "Profile": "full",
            "DatasetName": dataset_name,
            "DatasetVersion": "1.0.0",
            "QualityAssessmentDate": today,
            "AnnotationStatistics": {
                "TotalSubjects": n_subjects,
                "TotalAnnotations": "TODO",
                "SubjectsWithAnnotations": n_subjects,
                "SubjectsWithoutAnnotations": 0,
                "AnnotationsPerSubject": {
                    "Mean": "TODO", "StandardDeviation": "TODO",
                    "Min": "TODO", "Max": "TODO", "Median": "TODO"
                }
            },
            "QualityControlMetrics": {
                "QCProcess": {
                    "ReviewPercentage": "TODO: e.g., 100",
                    "DoubleAnnotationPercentage": "TODO: e.g., 10",
                    "ReviewMethod": "TODO"
                }
            },
            "CertificationStatement": "TODO",
            "CertifiedBy": {"Name": "TODO", "Role": "TODO", "Date": today}
        })
        print(f"  ✅ quality/quality_summary.json")

        write_json(quality_dir / "annotation_agreement.json", {
            "VIDSVersion": "1.0",
            "Methodology": {
                "Method": "TODO: e.g., Dice Coefficient",
                "SamplingStrategy": "TODO",
                "Tool": "TODO"
            },
            "Annotators": [
                {"ID": "TODO: annotator_001", "Role": "Primary", "Credentials": "TODO"},
                {"ID": "TODO: annotator_002", "Role": "Reviewer", "Credentials": "TODO"}
            ],
            "AggregateStatistics": {
                "Mean": "TODO", "StandardDeviation": "TODO",
                "Min": "TODO", "Max": "TODO"
            },
            "QualityThresholds": {
                "Excellent": 0.90, "Good": 0.85,
                "Acceptable": 0.75, "Poor_below": 0.75
            }
        })
        print(f"  ✅ quality/annotation_agreement.json")

    # ── ML directory (Full profile) ─────────────────────────
    if profile == "full":
        ml_dir = root / "ml"
        subject_ids = [f"sub-{zero_pad(i, n_subjects)}"
                       for i in range(1, n_subjects + 1)]

        import random
        rng = random.Random(42)
        shuffled = list(subject_ids)
        rng.shuffle(shuffled)

        n_train = int(n_subjects * 0.7)
        n_val = int(n_subjects * 0.15)

        write_json(ml_dir / "splits.json", {
            "VIDSVersion": "1.0",
            "SplitStrategy": "random",
            "SplitRatio": "70/15/15",
            "RandomSeed": 42,
            "Splits": {
                "train": sorted(shuffled[:n_train]),
                "val": sorted(shuffled[n_train:n_train + n_val]),
                "test": sorted(shuffled[n_train + n_val:])
            },
            "Notes": "Subject-level split. No data leakage between splits."
        })
        print(f"  ✅ ml/splits.json (train={n_train}, "
              f"val={n_val}, test={n_subjects - n_train - n_val})")

    # ── Summary ─────────────────────────────────────────────
    total_files = sum(1 for _ in root.rglob("*") if _.is_file())
    print(f"\n{'=' * 50}")
    print(f"Dataset scaffolded: {root}")
    print(f"Total files: {total_files}")
    print(f"Profile: {profile.upper()}")
    print(f"{'=' * 50}")
    print(f"\nNext steps:")
    print(f"  1. Replace NIfTI stubs with your actual imaging and segmentation data")
    print(f"  2. Fill in TODO fields in all JSON files")
    print(f"  3. Validate: vids-validate {root.name}/ --profile {profile}")
    print(f"\nEvery JSON file contains TODO markers for fields you need to fill in.")
    print(f"Search for 'TODO' across the dataset to find all placeholders.")
    print()


def main():
    parser = argparse.ArgumentParser(
        prog="vids-init",
        description="Scaffold a VIDS-compliant dataset structure with "
                    "template files ready to fill in.")
    parser.add_argument("name", help="Dataset directory name to create")
    parser.add_argument("--subjects", type=int, default=10,
                        help="Number of subjects (default: 10)")
    parser.add_argument("--modality", nargs="+", default=["ct"],
                        help="Modality codes, e.g., ct mr xr (default: ct)")
    parser.add_argument("--session", nargs="+", default=["baseline"],
                        help="Session names, e.g., baseline followup (default: baseline)")
    parser.add_argument("--profile", choices=["poc", "full"], default="poc",
                        help="VIDS profile (default: poc)")
    parser.add_argument("--dataset-name",
                        help="Human-readable dataset name (default: directory name)")
    args = parser.parse_args()

    scaffold_dataset(args)


if __name__ == "__main__":
    main()
