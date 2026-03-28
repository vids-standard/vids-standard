# VIDS Directory Structure (v1.0)

A VIDS dataset is organized as a dataset root containing required metadata files, subject/session trees, and a derivatives tree for annotations.

## Dataset root (required elements)

A compliant dataset root includes: `.vids`, `dataset_description.json`, `participants.json` or `participants.tsv`, `README.md`, `sub-*` subject directories, and `derivatives/annotations/`.

Full profile additionally requires `quality/` and `ml/`.

## Reference tree

```text
<dataset>/
  .vids
  dataset_description.json
  participants.json (or participants.tsv)
  README.md
  CHANGES.md (recommended)
  sub-001/
    ses-baseline/
      ct/
        sub-001_ses-baseline_ct_img.nii.gz
        sub-001_ses-baseline_ct_img.json
  derivatives/
    annotations/
      sub-001/
        ses-baseline/
          ct/
            sub-001_ses-baseline_ct_seg.nii.gz
            sub-001_ses-baseline_ct_seg.json
  quality/ (Full only)
    quality_summary.json
    annotation_agreement.json
  ml/ (Full only)
    splits.json
```
