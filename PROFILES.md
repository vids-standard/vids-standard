# VIDS Profiles (v1.0)

VIDS defines two compliance profiles declared in `.vids`: `poc` and `full`.

## POC profile

POC is intended for quick prototypes and pilot deliveries and enforces structure, imaging, and annotation/provenance rules.

Validator coverage: S001–S006, I001–I004, A001–A005 (15 checks).

## Full profile

Full is intended for production, publications, and regulatory workflows, and adds required quality documentation and ML splits.

Validator coverage: all 21 checks, including Q001–Q003 and M001–M002.

## Comparison

| Requirement | POC | Full |
|---|---:|---:|
| `.vids` marker | Required | Required |
| `dataset_description.json` | Required | Required |
| `participants.json` or `.tsv` | Required | Required |
| `README.md` | Required | Required |
| `sub-*` + `ses-*` structure | Required | Required |
| Imaging + imaging sidecars | Required | Required |
| `derivatives/annotations/` | Required | Required |
| Segmentation files + sidecars | Required | Required |
| Provenance minimums | Required | Required |
| `quality/` + required JSONs | Optional | Required |
| `ml/` + `splits.json` | Optional | Required |
| `CHANGES.md` | Recommended | Recommended |
