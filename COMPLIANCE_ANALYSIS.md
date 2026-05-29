# VIDS Compliance Analysis: Methodology Reference

This document records the methodology used in the compliance analysis presented in Section 5 of the VIDS v1.0 paper (Muthu and Shalen, 2026, arXiv:2604.17525). It addresses the reference in footnote 1 of Section 5.3 ("Per dimension scoring criteria are available at the project repository") and points readers to the published per-dimension scoring data.

## 1. Status

The 22-dimension framework documented here is the framework used in the one-time research analysis published in the paper. It is not the framework used for ongoing operational VIDS Compliance Evaluations, which use the [Scoring Rubric](https://vidsstandard.org/for-buyers/scoring-rubric/) published on the VIDS site.

The two frameworks coexist for different purposes:

| | Research methodology (this document) | Operational rubric ([site](https://vidsstandard.org/for-buyers/scoring-rubric/)) |
|---|---|---|
| Purpose | One-time benchmarking of four major public datasets to characterize the field | Recurring evaluation of buyer-submitted datasets |
| Categories | 6 (Structure, Imaging, Annotation, Provenance, Quality, ML Readiness) | 4 (Structure, Annotation Provenance, Quality, ML Readiness) |
| Dimensions | 22 | 22 |
| Scoring | Satisfied (1.0), partial (0.5), absent (0.0) | Binary (1 or 0); no partial credit |
| Profile thresholds | Not defined (research analysis did not use profile thresholds) | POC 16/22, Full 22/22 |
| Used in | arXiv paper Table 4 | Buyer evaluation reports, compliance attestations |

Both frameworks remain in use. The research methodology is the documented source for the published Table 4 results. The operational rubric is the framework used for any new compliance evaluation going forward. Scores produced by the two frameworks for the same dataset will not be numerically equivalent.

## 2. The framework used in the paper

### 2.1 Categories and dimensions

Section 5.1 of the paper defines 22 dimensions across six categories. Table 3 from the paper, reproduced verbatim:

| Category | Dimensions |
|---|---|
| Structure (6) | Dataset marker, dataset description, participant registry, human readable README, subject hierarchy, session hierarchy |
| Imaging (3) | Standardized format (NIfTI), per image metadata sidecar, consistent file naming |
| Annotation (4) | Structured annotation directory, segmentation masks, per annotation metadata sidecar, machine readable label map |
| Provenance (5) | Annotator identity, annotator credentials, annotation tool, annotation date, QC review documented |
| Quality (2) | Inter annotator agreement, quality summary |
| ML Readiness (2) | Documented splits, split rationale |

### 2.2 Scoring model

From Section 5.1 of the paper, verbatim:

> Each dimension is scored as satisfied (present and machine readable), partial (present but not structured or requiring manual extraction), or absent. Partial scores count as 0.5 and are assigned only when information is present in the dataset but not in a machine readable or standardized form (e.g., provenance described in a companion paper but absent from the dataset files).

Each dimension produces one of three scores:

- **1.0 (Satisfied)**: Information is present in the dataset itself, in a structured machine-readable form, and matches the dimension definition.
- **0.5 (Partial)**: Information is present in the dataset's published material (companion papers, README files, dataset cards) but not in the dataset's structured machine-readable files. A human can extract it; a parser cannot.
- **0.0 (Absent)**: Information is not present in the dataset or its published material.

The category total is the sum of dimension scores within that category. The total score is the sum of category totals.

### 2.3 Per-dimension scoring data

The per-dimension scoring data for all four datasets is published as a structured artifact:

[github.com/vids-standard/vids-benchmarks/blob/main/data/compliance_scores.json](https://github.com/vids-standard/vids-benchmarks/blob/main/data/compliance_scores.json)

That file contains the dimension definitions (with descriptions), the scoring scale, and per-dataset scores for all 22 dimensions across the four datasets in Table 4. The verification script in the same repository (`verify_scores.py`) reproduces the category totals and per-dataset percentages from the JSON.

Each dimension's score for each dataset is determined by applying the dimension definition to the dataset's published artifacts under the scoring model in Section 2.2 above. The published JSON contains the scores; it does not separately document per-cell narrative rationale. A reader can verify or extend any individual cell by applying the dimension definition to the corresponding dataset and arriving at one of {1.0, 0.5, 0.0}.

## 3. Per-dataset results

Table 4 from the paper, reproduced verbatim:

| Category | LIDC-IDRI | BraTS | CheXpert | MSD | VIDS native |
|---|---|---|---|---|---|
| Structure (6) | 1.5 | 2.0 | 1.5 | 1.5 | 6 |
| Imaging (3) | 1.0 | 2.0 | 1.0 | 2.0 | 3 |
| Annotation (4) | 1.5 | 2.0 | 1.0 | 2.0 | 4 |
| Provenance (5) | 1.0 | 0.5 | 0.0 | 0.0 | 5 |
| Quality (2) | 1.0 | 1.0 | 0.0 | 0.0 | 2 |
| ML Readiness (2) | 0.0 | 1.0 | 1.0 | 1.0 | 2 |
| Total (22) | 6.0 | 8.5 | 4.5 | 6.5 | 22 |
| Percentage | 27% | 39% | 20% | 30% | 100% |

The per-dimension breakdown producing these category totals is in `compliance_scores.json` (linked above). The Section 5.4 narrative in the paper describes the key findings at the category level.

## 4. Relationship to the validator rules

The 22-dimension compliance framework and the 21-rule reference validator described in Section 3.4 of the paper are distinct instruments. The paper does not establish a canonical numeric mapping between dimension scores and rule outcomes; readers should not expect them to correspond one-to-one.

The POC and Full profile thresholds (15 rules for POC, 21 rules for Full) referenced elsewhere in the paper apply to the 21-rule validator, not to the 22-dimension compliance analysis. The 22-dimension framework does not define profile thresholds.

## 5. Citation

If citing the research methodology, reference both the paper and this document:

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

@misc{vids2026compliance,
  title   = {VIDS Compliance Analysis: Methodology Reference},
  author  = {{Princeton Medical Systems}},
  year    = {2026},
  url     = {https://github.com/vids-standard/vids-standard/blob/main/COMPLIANCE_ANALYSIS.md}
}
```

## 6. License

This document is published under CC BY 4.0, matching the VIDS specification license.

---

**Version note**: This document addresses the reference in footnote 1 of the paper's Section 5.3. The per-dimension scoring data is in [vids-benchmarks](https://github.com/vids-standard/vids-benchmarks). Operational compliance evaluations use the separate [Scoring Rubric](https://vidsstandard.org/for-buyers/scoring-rubric/) and are out of scope for this document.
