# VIDS File Naming (v1.0)

VIDS uses BIDS-inspired `sub-` and `ses-` prefixes and sidecar JSON pairing conventions.

## General pattern

`sub-<ID>_ses-<ID>_<modality>_<suffix>.<extension>`

## Required pairs

- `*_img.nii.gz` (or `.nii`) MUST have `*_img.json`.
- `*_seg.nii.gz` (or `.nii`) SHOULD have `*_seg.json` and is REQUIRED for validator compliance where segmentation is used.

## Common suffixes

- `_img` imaging volume.
- `_seg` segmentation mask.
- `_bbox` bounding boxes (JSON).
- `_cls` classification labels (JSON).
- `_lm` landmarks (JSON).

## Modality codes (examples)

- `ct`, `mr`, `xr`, `us`, `mg`, `pt`, `nm`, `path` (custom allowed if documented).
