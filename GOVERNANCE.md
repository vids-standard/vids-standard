# VIDS Governance

This document explains how the Verified Imaging Dataset Standard (VIDS) is governed and how decisions are made.

VIDS uses lightweight governance. The goal is to preserve clear authority, technical integrity, openness, and traceability without creating unnecessary administrative process.

## 1. Governing Principles

VIDS follows five principles:

1. **The Specification defines conformance.**
2. **The validator implements the Specification.**
3. **GitHub is the primary record of changes and approvals.**
4. **Routine work should require routine process.**
5. **Additional review is reserved for changes that materially affect adopters or VIDS governance.**

Governance should be no more complicated than necessary to maintain a credible and stable open standard.

## 2. Normative Authority

The VIDS Specification and its normative extensions are the only sources of VIDS conformance requirements.

Guides, examples, websites, validator messages, decision records, checklists, implementation notes, and other project materials may explain or support the Specification, but they do not independently create conformance requirements.

If supporting material conflicts with the Specification, the Specification governs.

## 3. Validator Authority

The VIDS validator implements machine-checkable requirements from the Specification.

The validator does not independently define the standard.

If the validator and the Specification appear to disagree:

1. the Specification governs;
2. the discrepancy should be reviewed; and
3. the validator or Specification should be corrected as appropriate.

A validator defect does not by itself change the meaning of an existing VIDS requirement.

## 4. Steering Committee

VIDS is governed by its Steering Committee.

The Steering Committee is responsible for:

- maintaining the Specification;
- maintaining the validator and related technical infrastructure;
- reviewing substantive changes;
- approving major or breaking changes;
- making governance and policy decisions;
- managing Steering Committee membership; and
- protecting the neutrality and integrity of VIDS.

The current Steering Committee consists of:

- Dr. Joan S. Muthu
- John Xavier
- John Shalen R.

The Steering Committee may update this list as membership changes.

## 5. Routine Decision-Making

VIDS does not require formal votes for routine work.

### Editorial and Routine Changes

A maintainer may merge changes such as:

- typo corrections;
- formatting changes;
- broken-link fixes;
- documentation improvements;
- examples that do not alter requirements; and
- other changes that do not materially affect VIDS conformance.

No separate approval record, vote, signature, or decision document is required.

### Substantive Specification Changes

A backward-compatible change that affects the meaning or implementation of a VIDS requirement requires review by at least one other Steering Committee member before merge.

The approving pull request is the decision record.

A separate Maintainer Decision is not required unless the matter represents a durable governance or policy decision that should be recorded independently.

## 6. Major and Breaking Changes

A major or breaking change is a change that could materially affect existing adopters or previously conformant datasets.

Examples include:

- introducing new REQUIRED information;
- removing an existing requirement;
- materially changing the meaning of an existing requirement;
- making incompatible changes to required file or directory structures; or
- otherwise introducing a breaking conformance change.

Major or breaking changes require:

1. a public proposal or discussion;
2. at least 30 days for public comment;
3. consideration of material feedback; and
4. approval by at least two Steering Committee members who are eligible to participate in the decision.

The change may then be merged through GitHub.

The GitHub discussion, pull request, and repository history serve as the approval record.

No signatures or separate approval certificates are required.

## 7. Steering Committee Decisions

Decisions concerning VIDS governance, Steering Committee membership, or other significant policy matters require approval from at least two eligible Steering Committee members.

Unless a member is recused, each seated Steering Committee member may participate.

Unanimous consent is not required.

For the current three-member Steering Committee, approval by two members is sufficient.

Routine technical and editorial decisions do not need to be escalated to a Steering Committee vote.

## 8. Conflicts and Recusal

A Steering Committee member should not approve a decision where a material conflict of interest makes independent participation inappropriate.

A recused member is excluded from that specific decision.

If a recusal materially affects the ability of the Steering Committee to make a decision, the remaining members should use reasonable judgment and document the resolution in the relevant GitHub discussion or Maintainer Decision.

A separate recusal form or register is not required.

## 9. Maintainer Decisions

A Maintainer Decision, or MD, may be used when it is useful to preserve a durable record of an important governance or policy decision.

Examples may include:

- changing the governance model;
- establishing an important interpretation of authority;
- adopting a major publication policy;
- changing Steering Committee structure; or
- resolving a significant policy question that is likely to matter again.

MDs should be short and focused.

At minimum, an MD should state:

- the decision;
- the reason for the decision; and
- its effective date or implementation point where relevant.

An MD is accepted when the required Steering Committee approval has been recorded and the corresponding pull request is merged.

GitHub is the approval record.

MDs do not require:

- Signature Copies;
- handwritten or electronic signatures;
- separate approval-evidence PDFs;
- individual sign-off tables;
- formal voting forms; or
- separate acceptance certificates.

Consultation, recusals, dissent, or other context should be recorded only when it is materially relevant.

## 10. Public Participation

VIDS welcomes public issues, pull requests, technical feedback, implementation experience, and proposed improvements.

Public comment is particularly important when a proposed change could affect existing adopters.

The Steering Committee should consider substantive feedback but is not required to accept every proposal or resolve all comments by consensus.

The Steering Committee remains responsible for the final decision.

## 11. Extensions

VIDS may support domain-specific or modality-specific normative extensions.

An extension must clearly identify:

- the VIDS version with which it is intended to operate;
- which requirements it adds or modifies; and
- any additional conformance rules it introduces.

Normative extensions have authority only within their stated scope.

New extensions and material extension changes follow the same review principles as the core Specification.

## 12. Requirements and Technical Traceability

VIDS may maintain technical files such as requirement registries, mappings, tests, or machine-readable rule definitions to support implementation and verification.

These artifacts are useful for traceability and automation but do not independently override the Specification.

Where practical, machine-generated or automatically checked records are preferred over manually maintained administrative records.

## 13. Versioning

VIDS uses semantic versioning for the Specification.

- **Major versions** indicate incompatible or breaking changes.
- **Minor versions** introduce backward-compatible additions.
- **Patch versions** contain non-breaking corrections and clarifications.

Specification and validator versions may advance independently.

A change should be classified according to its effect on the standard, not according to the amount of work required to implement it.

## 14. Advisory Council

VIDS may maintain an Advisory Council or other external advisory group.

Advisory members may provide:

- technical feedback;
- domain expertise;
- implementation perspective;
- strategic advice; and
- independent external input.

The Advisory Council is advisory and does not define VIDS conformance or exercise Steering Committee authority unless this governance document is explicitly amended to provide otherwise.

Appointments are approved by the Steering Committee using the normal decision rule in this document.

Written acceptance from the appointee and an appropriate record of the appointment are sufficient.

No signature package or separate governance ceremony is required.

## 15. Project and Commercial Separation

VIDS governance covers the VIDS standard, its normative extensions, related open-source implementation, and associated governance decisions.

It does not govern the ordinary internal operations of Princeton Medical Systems, Voxsyl, or any other company.

Commercial services, contracts, pricing, staffing, partnerships, internal operating procedures, and similar company matters do not become part of VIDS governance merely because they relate to VIDS.

Commercial activity must not independently redefine VIDS conformance.

## 16. Records

GitHub should be used as the primary project record wherever practical.

Relevant records may include:

- commits;
- pull requests;
- reviews;
- issues;
- releases;
- tags;
- CI results; and
- Maintainer Decisions when needed.

The project should avoid duplicating information across manually maintained registers when the same information can be reliably obtained from the repository.

Separate signatures, certificates, approval logs, or status registers should be created only when they serve a specific external, legal, or operational need.

## 17. Governance Changes

This governance document may be amended with approval from at least two eligible Steering Committee members.

A major governance change should be proposed through a pull request that explains the reason for the change.

A separate signature process is not required.

Once merged, the updated GOVERNANCE.md becomes the current governance policy.

## Simple Operating Rule

In practice:

- routine work can be handled by one maintainer;
- substantive specification changes receive review from another Steering Committee member;
- major, breaking, or governance decisions require approval from two Steering Committee members;
- major or breaking specification changes receive at least 30 days of public comment; and
- GitHub records the decision.

No additional process should be added unless it addresses a demonstrated need.

---

**VIDS was created by Princeton Medical Systems and is maintained as an open standard.**
