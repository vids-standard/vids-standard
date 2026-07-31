# VIDS Governance

| Field | Value |
|-------|-------|
| **Document class** | Charter document (Layer 0), see Section 2 |
| **Status** | Active, adopted by Steering Committee (MD-0002) |
| **Drafted** | 2026-07-12 |
| **Adopted** | 2026-07-26 |
| **Maintained by** | Steering Committee (Princeton Medical Systems) |
| **Related** | CONTRIBUTING.md; SPEC.md; MD-0001; MD-0002; MD-0005; SOP-Governance-Decision-Lifecycle |

This document defines how VIDS classifies the documents it produces, which of them may create requirements, and where authority for each lives. It is a charter document: it defines the classification system rather than being classified by it.

---

## 1. The Normative Principle

> **Only the Core Specification (SPEC) creates, modifies, or removes dataset-conformance requirements.**
>
> All other document types are informative. They may explain, justify, record, or govern project operation, but they cannot change the normative requirements of VIDS.

This is the governing principle of the entire model. Everything below exists to make it enforceable and unambiguous. A change note, a decision record, an operating procedure, or a registry can inform, decide, or track - but it can never make a dataset conformant or non-conformant. Only SPEC does that, and only through the ratification path in CONTRIBUTING.md.

## 2. Two categories of document

The repository contains two categories of document.

**1. Charter documents (Layer 0 - repository governance).** These define the governance and operation of the project itself. They are *not* part of the numbered artifact taxonomy - because they define that taxonomy. They are living repository documents, amended by Steering Committee consensus.

- `README.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `LICENSE`, `NOTICE`, `CODE_OF_CONDUCT.md` (if adopted)

**2. Project artifacts (Layer 1 - produced under the governance model).** These are the documents the project produces, classified by the artifact taxonomy in §4.

- SPEC, MD, CN, SOP, REG

The dependency runs one way, which is what avoids any recursion - no Layer 1 artifact has to define itself:

```
Repository Charter (Layer 0)
────────────────────────────
README · GOVERNANCE · CONTRIBUTING · LICENSE · NOTICE
        │
        ▼   defines
Artifact Taxonomy (Layer 1)
────────────────────────────
SPEC · MD · CN · SOP · REG
        │
        ▼   governs
Project outputs
```

And the authority stack, top to bottom:

```
Repository Charter
        │
        ▼
Artifact Taxonomy
        │
        ▼
SPEC  ── the only normative artifact
        │
        ├───────────►  Validator   (enforces SPEC)
        │
        └───────────►  REG         (records & traces; authoritative for identifiers)
```

Both the validator and the registries derive their authority from SPEC, but in different ways: the **validator enforces** the specification, while a **registry records and traces** it - inventorying identifiers and mappings. Keeping enforcement and traceability as separate consequences of the same normative source is deliberate. The validator alone is intentionally **not** a document type; it is an implementation artifact governed by the Core Specification. (REG *is* a Layer 1 document type; it appears in this diagram only to show that its authority, like the validator's, flows from SPEC.) The principle governing what happens when validator behavior and the specification diverge is recorded in MD-0001.

## 3. Artifact taxonomy at a glance

| Code | Name | Purpose | Normative? | Lifecycle | Default visibility |
|------|------|---------|-----------|-----------|--------------------|
| **SPEC** | Specification | The normative standard: requirements, rules, schemas | **Yes** | Versioned; changed only via PR + maintainer ratification | Public |
| **MD** | Maintainer Decision | A standard-governance decision and its rationale | No | Append-only; superseded, never rewritten | Public |
| **CN** | Change Note | Point-in-time record of what changed and its impact | No | Immutable once published; version-tagged | Public |
| **SOP** | Standard Operating Procedure | An operational process the project follows | No | Living: Draft → Active → Retired | Internal |
| **REG** | Registry | Machine-readable inventory maintained by tooling | No (see §4) | Living; tool-maintained; CI-validated where implemented | Public |

## 4. Artifact type definitions

**SPEC - Specification.** The authoritative standard. Changes follow the CONTRIBUTING.md decision process (editorial / minor / major) and require maintainer review to merge. Identified by version (e.g., `v1.0`), not a sequence number. The only normative artifact.

**MD - Maintainer Decision.** Records a standard-governance decision the maintainers have *made*, and why: scope calls, policy, governance. Forward-looking. Append-only - once accepted, an MD is not rewritten to change its meaning; a later decision that reverses or refines it is a new MD marking the earlier one `Superseded by MD-NNNN`. Correcting a factual error in an MD's description of the world is permitted (dated); changing the *decision* requires a new MD.

*MD is standard governance only.* MD means *Maintainer* Decision: public, standard-governance. Internal company/PMS management decisions are **out of scope** of this taxonomy and do not share its numbering - they belong to a separate internal track.

**CN - Change Note.** Records what *changed* and the impact on adopters. Backward-looking. Immutable once published, tagged to the version(s) it describes.

**The MD-vs-CN test.** MD answers *"what did we decide, and why?"* CN answers *"what changed, and what does it mean for adopters?"* A single governance event may produce several artifact types - for example a SPEC amendment (normative), an MD (the governance decision), and a CN (the adopter-facing impact) - each with a distinct purpose and authority.

**Errata are SPEC-internal, not CN.** Corrections to released normative text live inside SPEC (§15.3) and dataset-facing CHANGES.md. CN is the adopter-facing *narrative* around a change, not the errata record itself.

**SOP - Standard Operating Procedure.** How the project operates: release checklists, the pre-tag documentation grep, the identity-discipline routine (confirm the operating account and git identity before any commit/tag/push). Living, ops-owned, freely revised.

**REG - Registry.** A machine-readable inventory maintained by tooling: continuously updated, consumed by CI, and authoritative for **identifiers and traceability**. Examples: `REG-REQ` (requirements inventory / §3.2 traceability, `requirements.yaml`), `REG-RULE` (validator rule inventory), `REG-DOC` (the index of all Layer 1 artifacts).

A REG is authoritative for the *identifiers and mappings it holds*, but it is **not** normative for conformance: per §1, only SPEC creates a requirement. A REG records *which* requirement/rule exists and how they trace to each other; SPEC remains the source of the requirement itself. This boundary is deliberate - it stops a registry from becoming a backdoor normative source.

REG identifiers are **named slugs** (`REG-REQ`, `REG-RULE`, `REG-DOC`), not `TYPE-NNNN` sequences, because registries are singletons-by-domain. Where CI validation exists, a REG that disagrees with the artifact it inventories is treated as a **build failure**, not a stylistic nit (see Section 8). A REG may exist first as a human-maintained document; machine-readable companions (for example REG-DOC.json) are script-generated derivatives with a divergence-failing verifier, added only when tooling consumes them, and never independently maintained.

## 5. Visibility

Every Layer 1 artifact declares a **Visibility**: `Public` or `Internal`.

- SPEC, CN, and public registries are **Public**.
- SOP is **Internal** by default.
- MD is **Public** by definition (it is standard governance). Internal company management decisions are not MDs and are not published into the public standard repository.

Internal-visibility content MUST NOT be published into the public standard repository.

## 6. Identifiers and status

**Format.** `TYPE-NNNN` - type code, hyphen, zero-padded sequence number (`MD-0002`, `CN-0001`), assigned sequentially per type, never reused, immutable once assigned. SPEC is identified by version; REG by named slug.

**Status values.**

- **SPEC** - by version and release status (Draft / Release).
- **MD** - Proposed → Accepted → (Superseded | Rejected). Acceptance follows the Governance Decision Lifecycle SOP: a Signature Copy with blank sign-off blocks collects approvals; the signed PDF files as immutable approval evidence (MD-NNNN-ApprovalEvidence-YYYY-MM-DD.pdf); the document of record then carries a Proposed date, an Accepted date (the later of the required approvals, never backdated), a completed approval table, and the evidence cited by filename only. The published rendering contains no signature lines.
- **CN** - Draft → Published (immutable thereafter).
- **SOP** - Draft → Active → Retired.
- **REG** - Active → Deprecated.

The **`REG-DOC`** index lists every Layer 1 artifact with its ID, title, status, and visibility, so the governing set is discoverable - and so its own drift is machine-checkable.

## 7. Authority

| Type | Authored by | Accepted / gated by |
|------|-------------|---------------------|
| Charter docs | Anyone (PR) | Steering Committee consensus |
| SPEC | Contributors (PR) | Maintainer ratification (per CONTRIBUTING) |
| MD | Anyone (Proposed) | Maintainer / Steering Committee acceptance |
| CN | Ops | Accuracy-gated (a CN that misstates the artifact is a defect) |
| SOP | Ops | Ops owns |
| REG | Tooling | CI validation where implemented; registry drift treated as a build failure |

### Steering Committee membership

The current composition of the Steering Committee is recorded through Maintainer Decisions (MDs). Appointments, resignations, and removals are recorded by subsequent MDs, each applying from its stated effective date.

| Member | Role | Recorded by |
|--------|------|-------------|
| Dr. Joan S. Muthu | Co-Founder and CTO | MD-0005 |
| John Shalen R. | Co-Founder and COO | MD-0005 |
| John Xavier | Co-Founder and Head of US and Global Operations | MD-0005 |

All Steering Committee members hold governance signatory authority. This section is the charter's record of composition; it is descriptive of the MDs that establish it, and is updated when a subsequent MD changes membership.

## 8. Enforcement

This taxonomy is **filing, not enforcement.** Naming a document "SPEC" does not keep it true. What is meant to keep the normative layer honest is an automated tie between SPEC and the validator, and this section states plainly how much of that tie exists today.

**In place.** Continuous integration runs on every push and pull request to `main`, across three Python versions. It generates the test fixtures, runs the validator against the POC and Full example datasets, and runs the validator unit tests.

**Planned, not yet built.** Two checks are intended and do not exist in the repository:

| Check | Intended scope |
|-------|----------------|
| `check_docs.py` | Rule counts and rule descriptions in the documentation must match the validator. |
| `check_requirements.py` | Every enforced requirement names a real FAIL-severity rule; no orphan rules; no unresolved CONFLICT. |

**Known gap.** The unit-test step currently runs with `continue-on-error`, so a failing test does not fail the build. Until that changes, tests in this repository report rather than enforce, including any test written to enforce an adopted governance rule. Registry drift is likewise not yet treated as a build failure.

Consequently: **adding document types must not add drift surface.** Any normative claim is verifiable only to the extent a check can test it against the artifact, and a claim whose check is planned rather than built is not yet verifiable. The taxonomy rides on top of these checks; it does not substitute for them, and it does not substitute for building them. Structurally: *every statement in the project has a defined authority, and every authoritative statement is checkable against the thing it describes.*

## 9. Amending this document

`GOVERNANCE.md` is a charter document. It is amended by Steering Committee consensus, following the same review discipline as a spec change. Adoption of the model it describes is recorded in **MD-0002**. Steering Committee composition and signatory authority are recorded in **MD-0005**, and change only by a subsequent MD taking effect from its stated effective date.

---

## Change log

| Date | Change |
|------|--------|
| 2026-07-12 | Initial draft (charter and taxonomy), submitted for adoption via MD-0002. |
| 2026-07-29 | Section 8 corrected: `check_docs.py` and `check_requirements.py` were described as operational enforcement but do not exist in the repository. They are now listed as planned, the checks actually running in CI are stated, and the non-blocking unit-test step is recorded as a known gap. "Trustworthy" replaced with "verifiable". No change to the Normative Principle or the taxonomy. |
| 2026-07-28 | Steering Committee membership provision added to Section 7, recording composition and the MD-based membership rule per MD-0005 clauses 2, 3 and 4. Section 9 and the Related field reference MD-0005. No change to the two-layer model, the Normative Principle, or any artifact-type definition. |
| 2026-07-26 | Adopted following acceptance of MD-0002 by Joan S. Muthu and John Shalen R. (evidence: MD-0002-ApprovalEvidence-2026-07-26.pdf). |
| 2026-07-26 | Pre-adoption revisions: date-field convention applied (Drafted; Adopted date added on acceptance); MD acceptance-record convention added to Section 6 per the Governance Decision Lifecycle SOP; REG derivative rule added to Section 4; punctuation normalized (em-dashes removed). No change to the two-layer model, the Normative Principle, or any artifact-type definition. |
