# REG-DOC: VIDS Artifact Index

| Field | Value |
|-------|-------|
| **ID** | REG-DOC |
| **Type** | REG, Registry |
| **Status** | Active, per adoption of MD-0002 (accepted 2026-07-26) |
| **Normative?** | No. Authoritative for the *index of artifacts*, not for conformance. |
| **Visibility** | Public |
| **Drafted** | 2026-07-13 |
| **Active since** | 2026-07-26 |
| **Maintained by** | Ops (tooling); CI-validated where implemented |
| **Related** | GOVERNANCE.md Section 6; MD-0002; MD-0005; SOP-Governance-Decision-Lifecycle |

---

This registry lists the governing **Layer 1 project artifacts** of VIDS, so anyone joining the project can see at a glance which documents govern it and what state each is in. It answers one question: *"What are the governing artifacts, and where does each stand?"*

## Artifact index

| ID | Title | Status | Visibility | Location (target ³) |
|----|-------|--------|------------|---------------------|
| SPEC | Core Specification - current normative version **v1.0** | Release ¹ | Public | `/SPEC.md` |
| SPEC-FUNDUS | Fundus Extension Specification - v1.0 (locked) ⁴ | Release | Public | `/extensions/fundus/SPEC-FUNDUS-1.0.md` |
| MD-0001 | Authority of the Specification over the Validator | Accepted (2026-07-26) | Public | `/governance/MD-0001.md` |
| MD-0002 | Adoption of the VIDS Document Taxonomy | Accepted (2026-07-26) | Public | `/governance/MD-0002.md` |
| MD-0003 | Reference-Implementation Publication Policy (Metadata Layer, Not Images) | Accepted (2026-07-26) | Public | `/governance/MD-0003.md` |
| MD-0004 | Adoption of the VIDS Governance Handbook v1.0 | Accepted (2026-07-26) | Public | `/governance/MD-0004.md` |
| MD-0005 | Steering Committee Composition and Signatory Authority | Accepted (2026-07-28) | Public | `/governance/MD-0005.md` |
| MD-0006 | Assertion Discipline for VIDS Artifacts and Generators | Accepted (2026-07-31) | Public | `/governance/MD-0006.md` |
| MD-0007 | DeIdentification Semantics in SPEC Section 8.2 | Accepted (2026-07-31) | Public | `/governance/MD-0007.md` |
| CN-0001 | Validator v1.2.x Annotation-Sidecar Enforcement | Published | Public | `/governance/CN-0001.md` |
| REG-REQ | Requirements Registry (§3.2 traceability) | Planned ² | Public | `/registry/REG-REQ.yaml` |
| REG-DOC | VIDS Artifact Index (this document) | Active | Public | `/governance/REG-DOC.md` |
| SOP-GOV-HANDBOOK | VIDS Governance Handbook v1.0 | Active (adopted per MD-0004) | Members (Handbook Section 12) | internal; member edition distributed on appointment |
| SOP-GOV-LIFECYCLE | Governance Decision Lifecycle | In effect as working practice | Internal | internal |

¹ The released specification is v1.0. The v1.2.x conformance errata were ratified and merged to `main` (commit `8d8f8a7`, 2026-07-12) via PR #3.
² REG-REQ is a planned migration of the existing §3.2 traceability material (`requirements.yaml`, requirements inventory) into the registry form, per MD-0002 Consequences.
³ Locations are **target paths**. The repository layout is provisional pending a dedicated repository-structure definition (a planned Layer 0 addition); these paths record each artifact's intended home so tooling and contributors have one predictable place to look.
⁴ The Fundus extension specification is locked as of 2026-07-13, drafted from the locked `vids-fundus-1.0.schema.json`, with both example sidecars validated against the schema. It is the first published VIDS extension specification.

## Notes

- **Statuses reflect current reality**, not the intended end-state. They advance (Proposed → Accepted, Draft → Published, Planned → Active) as the maintainers act. A registry that claimed acceptance early would be the exact drift this framework exists to prevent.
- **Layer 0 charter documents** (`README`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `LICENSE`, `NOTICE`) are intentionally **not** indexed here. They define the taxonomy rather than being classified by it (GOVERNANCE.md §2).
- The Fundus 1.0 publication checklist (`publication/ZENODO-CHECKLIST-fundus-1.0.md`) is rolling operational material, not a governing Layer 1 artifact, so it is not indexed here (same treatment as the status note).
- The first registered SOP is the Governance Handbook (Active per MD-0004). Further operational material (release checklist, identity-discipline routine) remains candidate for future SOP entries.
- **Proposed MDs are indexed before they are filed.** An MD appears here on proposal so the pending set is discoverable, with its status shown as Proposed. Its target location is recorded, but the file is not committed to `/governance/` until acceptance. A Proposed MD in the repository would imply a status it does not hold.
- A **`Supersedes`** column is planned - to be added when governance history first requires it (e.g., when one MD supersedes another) - so tooling can navigate lineage. It is omitted now because there is no supersession to record.

## Change log

| Date | Change |
|------|--------|
| 2026-07-13 | Initial draft. |
| 2026-07-31 | MD-0006 and MD-0007 advanced to Accepted (2026-07-31) and filed to `/governance/`. |
| 2026-07-29 | MD-0006 and MD-0007 added (Proposed), covering assertion discipline and DeIdentification semantics. |
| 2026-07-28 | MD-0005 added (Accepted 2026-07-28), recording Steering Committee composition and signatory authority. |
| 2026-07-26 | Active per adoption of MD-0002. Statuses advanced: MD-0001, MD-0002, MD-0003 Accepted; MD-0004 added (Accepted); Governance Handbook registered as the first SOP (Active per MD-0004); Governance Decision Lifecycle SOP listed as working practice. Punctuation normalized. |

---

*REG-DOC is a registry. It is authoritative for the set of governing artifacts and their status; it is non-normative with respect to dataset conformance.*
