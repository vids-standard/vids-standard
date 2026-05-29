# VIDS Compliance Analysis: Methodology and Per-Dataset Results

This document records the methodology used in the compliance analysis presented in Section 5 of the VIDS v1.0 paper (Muthu and Shalen, 2026, arXiv:2604.17525). It is the canonical reference for any reader wishing to interpret, reproduce, or extend the published Table 4 scores.

This document fulfills the reference promised in footnote 1 of Section 5.3 of the paper ("Per dimension scoring criteria are available at the project repository").

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

Both frameworks remain in use. The research methodology is the documented source for the published Table 4 results. The operational rubric is the framework used for any new compliance evaluation going forward. The two scores produced by the two frameworks for the same dataset will not be numerically equivalent.

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

Each dimension is defined by the structure it requires in a compliant dataset, derived from the VIDS specification. For example, the Provenance "annotation tool" dimension asks whether the dataset documents, in structured machine-readable form, the software tool used to produce each annotation.

### 2.2 Scoring model

From Section 5.1 of the paper, verbatim:

> Each dimension is scored as satisfied (present and machine readable), partial (present but not structured or requiring manual extraction), or absent. Partial scores count as 0.5 and are assigned only when information is present in the dataset but not in a machine readable or standardized form (e.g., provenance described in a companion paper but absent from the dataset files).

Each dimension produces one of three scores:

- **1.0 (Satisfied)**: Information is present in the dataset itself, in a structured machine-readable form, and matches the dimension definition.
- **0.5 (Partial)**: Information is present in the dataset's published material (companion papers, README files, dataset cards) but not in the dataset's structured machine-readable files. A human can extract it; a parser cannot.
- **0.0 (Absent)**: Information is not present in the dataset or its published material.

The category total is the sum of dimension scores within that category. The total score is the sum of category totals.

### 2.3 Profile thresholds

The 22-dimension framework does not define profile thresholds. The POC and Full profile thresholds referenced elsewhere in the paper (15 rules for POC, 21 rules for Full) apply to the 21-rule reference validator described in Section 3.4, not to the 22-dimension compliance analysis.

The relationship between the 21 validator rules and the 22 dimensions is described in the paper: 21 of the 22 dimensions correspond to machine-enforceable validator rules, with the 22nd dimension (split rationale documentation) being a content-quality dimension that the validator does not check directly. Readers should not expect a one-to-one numeric mapping between rule outcomes and dimension scores.

## 3. Per-dataset results

### 3.1 Table 4 reproduced verbatim

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

### 3.2 Per-category observations

The category-level scoring is constrained by the observations in Section 5.4 of the paper, quoted below for each category. Per-dimension scoring (which specific dimensions within a category received satisfied, partial, or absent scores for each dataset) is not separately published in the paper. The category total constrains the number of partial and full credits awarded within the category, and the Section 5.4 narrative further constrains which dimensions those credits map to, but the full per-dimension breakdown is not documented in the published material.

**Structure (max 6):**

> All four datasets have some directory organization and imaging data in standardized formats, but none use a machine readable dataset marker, structured participant registry, or per image metadata sidecar.

This constrains three of the six Structure dimensions (dataset marker, participant registry, per-image sidecar relevance) to score 0 for all four datasets. The remaining three dimensions (dataset description, README, subject/session hierarchy) account for the partial and full credits visible in the category totals (1.5 to 2.0 across the four datasets). The exact per-dimension assignment within these three is not separately documented.

**Imaging (max 3):**

> All four datasets have ... imaging data in standardized formats.

The Standardized format dimension is satisfied or partially satisfied across all four datasets. Per-image metadata sidecars are not provided in standardized form by any of the four. Score variation across datasets (1.0 to 2.0) reflects differences in the third dimension (consistent file naming). The exact per-dimension assignment is not separately documented.

**Annotation (max 4):**

The paper does not provide an Annotation-specific narrative in Section 5.4. Category totals (LIDC 1.5, BraTS 2.0, CheXpert 1.0, MSD 2.0) reflect varying degrees of annotation directory structure and segmentation file availability. The lower CheXpert score is consistent with CheXpert's NLP-derived classification labels (no segmentation masks present), under the framework's segmentation-mask dimension. The exact per-dimension assignment is not separately documented.

**Provenance (max 5):**

> Provenance is the largest gap. Across all four datasets, the provenance category averaged 0.4/5 (8%). LIDC-IDRI documents its annotation protocol in the original publication but anonymizes individual reader identities and provides no per annotation tool or date metadata in machine readable form. BraTS, CheXpert, and MSD provide no per annotation provenance at all.

LIDC's 1.0 corresponds to partial credit on 2 of 5 dimensions. One partial credit maps to "annotation protocol documented in companion paper" per the Section 5.4 quote. The source of the second partial credit is not specifically identified in the paper and is most consistent with one of: annotator credentials (LIDC's original publication describes the radiologist panel composition), QC review (LIDC's two-phase blinded review is documented in the original publication), or a related dimension. The paper does not single out which.

BraTS's 0.5 reflects partial credit on 1 of 5 dimensions. The specific dimension is not identified in the paper. CheXpert and MSD score 0 across all 5 dimensions.

**Quality (max 2):**

> LIDC-IDRI and BraTS have inter annotator agreement data that is computable from the raw annotations or published in challenge papers, but neither provides it as a structured file within the dataset itself. CheXpert and MSD provide no quality documentation.

LIDC and BraTS each score 1.0 on Quality, corresponding to partial credit (0.5) on both dimensions (Inter-annotator agreement and Quality summary): information is present in published material but not in structured form within the dataset. CheXpert and MSD score 0.

**ML Readiness (max 2):**

> MSD, BraTS, and CheXpert provide predefined splits, though documentation of split rationale and leakage prevention varies. LIDC-IDRI provides no predefined splits.

BraTS, CheXpert, and MSD each score 1.0 on the Documented splits dimension. Split rationale documentation is not credited for any of the four datasets (Score 0 on the second dimension across all). LIDC scores 0 across both dimensions.

## 4. Reproducing or extending the analysis

A reader wishing to verify a specific cell of Table 4 should:

1. Apply the dimension definitions from Section 2.1 to the corresponding dataset's published artifacts (dataset README, official documentation, companion papers, structured metadata files).
2. For each dimension within the category, determine satisfied, partial, or absent using the scoring model in Section 2.2.
3. Sum the dimension scores. The result should match the category total in Table 4.

The constraints from Section 3.2 narrow the within-category dimension assignments substantially. Where per-dimension assignment remains ambiguous within a category total, the paper does not document a single canonical choice. Readers performing independent verification should produce category totals matching Table 4 and report any cells where their per-dimension assignment differs from this document's constraints.

For new datasets not in Table 4, the same procedure produces a comparable score. Note that ongoing operational evaluations use the [Scoring Rubric](https://vidsstandard.org/for-buyers/scoring-rubric/), which has different category structure, dimension counts, and a binary scoring model. Scores from the two frameworks are not directly comparable.

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
  title   = {VIDS Compliance Analysis: Methodology and Per-Dataset Results},
  author  = {{Princeton Medical Systems}},
  year    = {2026},
  url     = {https://github.com/vids-standard/vids-standard/blob/main/COMPLIANCE_ANALYSIS.md}
}
```

## 6. License

This document is published under CC BY 4.0, matching the VIDS specification license.

---

**Version note**: This document was published after the v1.0 paper to fulfill the footnote reference to per-dimension scoring criteria. Any future compliance analysis publications using the 22-dimension research framework should reference this document for methodology. Operational compliance evaluations use the separate [Scoring Rubric](https://vidsstandard.org/for-buyers/scoring-rubric/) and are out of scope for this document.
