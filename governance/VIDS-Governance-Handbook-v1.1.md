# VIDS Governance Handbook

*A guide for Steering Committee and Advisory Council members. Member Edition, version 1.1. Supersedes Governance Handbook v1.0 (MD-0004).*

| Field | Value |
|-------|-------|
| Document class | Member handbook. Informative: it explains how VIDS governance operates and creates no conformance requirement |
| Status | Active from the merge of the pull request that records its approval. Supersedes v1.0 (MD-0004) |
| Version · Date | 1.1 · date of merge (see the approving pull request) |
| Maintained by | The Steering Committee. Changes follow the governance policy in GOVERNANCE.md |
| Related | GOVERNANCE.md · SPEC v1.0.1 · MD-0001 · MD-0003 · MD-0004 · MD-0008 |
| Distribution | Steering Committee and Advisory Council members, after appointment |

This handbook explains how VIDS governance operates: decisions, records, releases, meetings, and member responsibilities. It does not define the standard itself. That remains the responsibility of the Specification. Where this handbook and GOVERNANCE.md differ, GOVERNANCE.md governs.

## One-page quick reference · How VIDS governance works

Fifteen minutes with this handbook is enough to work here. Sixty seconds with this page is enough to start.

**Steering Committee** (decides: reviews and approves changes, makes governance decisions) → **Maintainers** (implement: run the repository, validator, and releases) → **Validator** (checks: implements the machine-checkable requirements of the Specification) → **Datasets** (conform: the visible result)

**Advisory Council** advises alongside: strategy, clinical relevance, adoption.

**Five facts to remember.**

- Only the **Specification** defines conformance.
- Changes are **graded**, and the grade sets the process.
- Major changes and governance decisions need approval from **at least two eligible** Steering Committee members.
- **GitHub is the primary record** of changes and approvals, and it is public.
- Deliberation is private; **outcomes never are**.

**Your commitment (Advisory Council).**

- Quarterly virtual sessions, or written input in advance
- About 2–4 hours per quarter
- Review requests within the stated window
- Declare conflicts; respect confidentiality

**What's in this handbook**

1 · About this handbook · 2 · Governance philosophy · 3 · Governance structure · 4 · Responsibilities · 5 · Membership terms · 6 · Meetings & cadence · 7 · How decisions are made · 8 · Approval and eligibility · 9 · Decision records · 10 · Release process · 11 · Conflict of interest · 12 · Confidentiality · 13 · Member onboarding · 14 · Member checklist & acknowledgment · A/B · Appendices

**Remember.** The Advisory Council advises. The Steering Committee decides. The maintainers implement. Only the Specification binds.

## Section 1 · About this handbook

**Purpose.** Explain how the VIDS governance bodies operate, and what is expected of you personally.

**Key points.**

- Covers decisions, records, releases, meetings, and member responsibilities
- Does **not** define the standard: that is the Specification's job
- Provided to members after their appointment is approved

### Who this is for

Members of the two VIDS governance bodies: the **Steering Committee** (the body that maintains and governs the standard) and the **Advisory Council** (the independent advisory body). You do not need to be a governance expert. A 15-minute read is enough to understand how VIDS operates.

### How this handbook relates to the governance policy

The governance policy of record is **GOVERNANCE.md** in the vids-standard repository. This handbook summarises it for members and adds the practical detail members need: meetings, membership terms, conflict of interest, confidentiality, and onboarding. If the two ever appear to differ, GOVERNANCE.md governs and the handbook is corrected.

Changes to this handbook follow the same graded process as everything else (Section 7). Editorial changes (clarity, formatting, contact details) are merged by a maintainer. Changes to operating rules (membership terms, meetings, conflict of interest, confidentiality, onboarding) require approval from at least two eligible Steering Committee members, recorded on GitHub.

**Remember.** This handbook governs how we work, never what the standard requires.

## Section 2 · Governance philosophy

**Purpose.** A small set of published principles from which everything else in this handbook derives.

**Key points.**

- Only the Specification defines conformance
- Routine work gets routine process; additional review is reserved for changes that matter
- Decisions are append-only: they are never rewritten

**Normative authority.** The VIDS Specification and its normative extensions are the only sources of VIDS conformance requirements. Guides, examples, the website, validator messages, decision records, and other project materials may explain or support the Specification, but they do not independently create conformance requirements. If supporting material conflicts with the Specification, the Specification governs.

### The five principles

1. The Specification defines conformance.
2. The validator implements the Specification.
3. GitHub is the primary record of changes and approvals.
4. Routine work requires routine process.
5. Additional review is reserved for changes that materially affect adopters or VIDS governance.

### Supporting principles

- **Openness.** The Specification and documentation are CC BY 4.0; the tools are Apache 2.0. Everything normative and every governance decision is public.
- **Neutrality.** No rule may privilege a vendor, tool, or platform. The steward's own products conform on the same terms as anyone else's, and commercial activity does not redefine VIDS conformance.
- **Backward compatibility.** Existing VIDS 1.x datasets remain conformant under later VIDS 1.x specifications, unless the earlier result depended on a validator defect or under-enforcement of an existing requirement. Breaking specification changes require a major version and an appropriate migration path.
- **Append-only history.** Reversing or refining a decision means recording a new one, and marking the earlier one superseded.

**Remember.** If a situation arises that this handbook doesn't cover, decide in the spirit of these principles.

## Section 3 · Governance structure

**Purpose.** Four roles, one direction of authority.

**Key points.**

- The Steering Committee decides; the Advisory Council advises
- The maintainers implement; the steward hosts
- No body, including the steward, outranks the Specification

| Body | Role | Authority |
|------|------|-----------|
| Steering Committee | Maintains and governs the standard | Maintains the Specification, the validator, and related infrastructure; reviews substantive changes; approves major or breaking changes; makes governance and policy decisions; manages its own membership; approves Advisory Council appointments |
| Advisory Council | Independent advisory body | Advises on strategy, clinical relevance, and adoption. Does not define VIDS conformance and does not exercise Steering Committee authority |
| Maintainers | Day-to-day operation | Run the repository, validator, CI, and releases; merge editorial and routine changes. No normative authority of their own |
| Steward (Princeton Medical Systems) | Hosts the standard | Provides infrastructure and staffing; no special normative authority. Its products conform like anyone else's |

**Current Steering Committee.** Dr. Joan S. Muthu (Co-Founder and CTO) · John Xavier (Co-Founder and Head of US and Global Operations) · John Shalen R. (Co-Founder and COO).

**The separation rule.** VIDS governance covers the VIDS standard, its normative extensions, the open-source implementation, and associated governance decisions. It does not govern the internal operations of Princeton Medical Systems or any other company. Neither body is involved in the steward's commercial operations, and commercial considerations carry no weight in conformance decisions.

**Remember.** The Advisory Council advises. The Steering Committee decides.

## Section 4 · Responsibilities

**Purpose.** What each body, and each member, is accountable for.

**Key points.**

- Committee: maintain the standard, review changes, decide governance
- Council: strategy, clinical grounding, adoption
- Every member: prepare, respond, disclose, keep confidences

**Steering Committee.**

- Maintain the Specification, the validator, and related infrastructure
- Review substantive changes and approve major or breaking changes
- Make governance and policy decisions, and manage its own membership
- Approve Advisory Council appointments and renewals
- Protect the neutrality and integrity of VIDS, including recusal discipline (Section 11)

**Advisory Council.**

- Strategic guidance: priorities, positioning, long-term development
- Clinical relevance: keep the standard grounded in real imaging practice
- Adoption guidance: what vendors, hospitals, researchers, and regulators need
- Connections: introductions and collaborations worth making

The Council may be asked for its view on major proposals during their public comment period. A written Council opinion is added to the relevant GitHub discussion so that it sits alongside the decision it informed.

**Every member, both bodies.**

- Prepare for and attend quarterly sessions, or send written input in advance
- Respond to review requests within the stated window
- Keep your conflict-of-interest disclosure current; honor confidentiality
- Speak as an individual expert, not for your employer, unless explicitly stated

**Remember.** Written input counts. Most VIDS work is asynchronous: presence in writing matters more than presence in the room.

## Section 5 · Membership terms

**Purpose.** How seats begin, renew, and end, so membership is never ambiguous.

**Key points.**

- Advisory Council terms are two years, renewable
- Resignation: written notice, effective on the stated date
- Removal: for cause, with notice and an opportunity to respond

### Appointment and term

- Advisory Council appointments are approved by the Steering Committee under the normal decision rule (Section 8), and confirmed to the member in writing.
- Terms run for two years from the effective date of appointment, renewable.

### Renewal

- Members are contacted before their term expires.
- Renewal requires the member's consent and Steering Committee approval under the normal decision rule.
- If no action is taken, the term lapses at expiry and the seat becomes vacant.

### Resignation

- Members may resign at any time by written notice, effective on the stated date.
- Departing members return or destroy confidential material.
- Recorded decisions remain in the record: history is append-only here too.

### Removal

- Removal is for cause: sustained non-participation (for example, two consecutive quarterly sessions missed with no written input), breach of confidentiality, or an unresolved conflict of interest.
- The member receives written notice of the grounds and an opportunity to respond, in writing or at a session, before any decision.
- Removal is decided by the Steering Committee under the normal decision rule (Section 8). A Steering Committee member whose own seat is in question takes no part in that decision. The decision is recorded on GitHub.

**Remember.** Seats change hands by the same discipline as everything else: in writing, on the record.

## Section 6 · Meetings & cadence

**Purpose.** A light, predictable rhythm. Most work happens in writing.

**Key points.**

- The Advisory Council meets quarterly (virtual)
- Steering Committee work happens mainly on GitHub, asynchronously
- Agendas go out 5 business days before a Council session

| Meeting | Cadence | Focus |
|---------|---------|-------|
| Advisory Council session | Quarterly, virtual | Strategic review, major proposals, adoption outlook |
| Steering Committee | Continuous on GitHub; meets as needed | Reviews, approvals, governance decisions |
| Joint session | As needed | Roadmap review; either body may invite the other at any time |

### How Council sessions run

- **Agenda:** circulated at least 5 business days ahead, with materials attached.
- **Notes:** circulated after the session. Notes record the advice given and any written opinion, not attributed debate.
- **Chair:** the Council chair convenes sessions and sets agendas with maintainer support.

**Time expectation.** Advisory Council: about 2–4 hours per quarter. This is a planning figure, not an obligation.

**Remember.** Sessions are for advice and discussion. Decisions are made and recorded through the process in Section 7.

## Section 7 · How decisions are made

**Purpose.** How proposals become decisions, predictably and in public.

**Key points.**

- Changes are graded, and the grade sets the process
- Major or breaking changes: public proposal, at least 30 days of comment, two approvals
- Routine work is not escalated to a Steering Committee vote

### Who decides what

| Change | Process |
|--------|---------|
| **Editorial and routine:** typos, formatting, broken links, documentation improvements, examples that do not alter requirements | Merged by a maintainer. No separate approval record |
| **Substantive specification changes:** backward-compatible changes that affect the meaning or implementation of a requirement | Review by at least one other Steering Committee member before merge. The approving pull request is the decision record |
| **Major or breaking changes:** new REQUIRED information, removed requirements, material changes of meaning, incompatible structure changes | Public proposal, a minimum 30-day comment period, consideration of material feedback, and approval by at least two eligible Steering Committee members |

Decisions concerning governance, Steering Committee membership, or other significant policy matters require approval from at least two eligible Steering Committee members. Unanimous consent is not required.

### The proposal path

A change is proposed as a pull request (or, for major changes, a public proposal first), reviewed at the level its grade requires, and merged. A pull request that changes the Specification states whether the change is normative, meaning it affects conformance, or editorial. That single line determines which path the change takes.

### Where the Advisory Council fits

The Council holds no vote on normative matters. Its advice informs decisions; it does not itself create requirements. For major proposals, the Council may be invited to comment during the comment period, and any written opinion is added to the GitHub discussion.

**Remember.** The grade sets the process. Two eligible approvals for anything major or governance-related.

## Section 8 · Approval and eligibility

**Purpose.** Make it clear who can approve what, and how an approval is shown.

**Key points.**

- Approval is given by Steering Committee members, on GitHub
- A member with a material conflict is not eligible for that decision
- No signatures, separate approval documents, or status registers

### The normal decision rule

Where this handbook refers to the normal decision rule, it means approval from at least two eligible Steering Committee members, as set out in GOVERNANCE.md.

### Eligibility

A Steering Committee member does not approve a decision where a material conflict of interest makes independent participation inappropriate. A recused member is excluded from that specific decision, and the resolution is documented in the relevant GitHub discussion or Maintainer Decision.

### How an approval is shown

Approvals are recorded as reviews and approvals on the relevant GitHub pull request or discussion. The merged pull request and the repository history are the approval record. Approvals are not collected as signatures or separate documents, and no status registers are kept.

**Remember.** If you can't find the approval on GitHub, it hasn't been given.

## Section 9 · Decision records

**Purpose.** Every governance outcome lands in the record, discoverably and permanently.

**Key points.**

- GitHub is the primary project record
- MD records what we decided and why; CN records what changed for adopters
- Records are append-only: reversal means a new record

### The record

GitHub is the primary project record: commits, pull requests, reviews, issues, releases, tags, and CI results.

| Record | What it captures |
|--------|------------------|
| Pull request and review | The change itself and its approval, at the level its grade requires |
| MD · Maintainer Decision | A durable governance or policy decision worth recording independently: what was decided, the reason, and its effective point. Accepted when the required approval is recorded and the pull request is merged |
| CN · Change Note | What changed, and what it means for adopters. Immutable once published |
| Errata | Corrections to released normative text, recorded inside the Specification itself, dated, at the point of the correction |

**Append-only.** A later decision that reverses or refines an earlier one is a new decision, and the earlier one is marked superseded. The earlier records stand unchanged as historical records.

**Where to find them.** The Decision Records page at vidsstandard.org lists each decision with its status and date, and links to the record in the repository.

**Remember.** If it isn't recorded, it wasn't decided.

## Section 10 · Release process

**Purpose.** Where governance becomes visible to adopters.

**Key points.**

- Specification versions follow semantic versioning
- Breaking changes require a major version and a migration path
- The validator implements the Specification; it never redefines it

### Versioning

- **Patch (1.0.x):** clarifications, typo fixes, example corrections.
- **Minor (1.x.0):** new optional features, annotation types, modality codes.
- **Major (x.0.0):** breaking changes to structure, required fields, or validation rules, with a documented migration path.

The approval each change needs is set by its grade (Section 7), not by the release it lands in.

### Validator and Specification

The validator implements the machine-checkable requirements of the Specification. If the two appear to disagree, the Specification governs, the discrepancy is reviewed, and the validator or Specification is corrected as appropriate. A validator defect does not by itself change the meaning of an existing VIDS requirement (MD-0001).

### Publishing

The maintainers tag and publish releases: the Specification on vidsstandard.org, the validator on PyPI. Reference-implementation deposits follow MD-0003 (reference datasets publish the metadata layer, not source images). Changes that adopters need to know about are explained in a Change Note.

**Remember.** Approval is a decision. Release is execution. Neither substitutes for the other.

## Section 11 · Conflict of interest

**Purpose.** Protect impartial technical decisions.

**Key points.**

- Declare conflicts: annually and per item
- Step back from decisions where you have a direct material interest
- Every recusal is documented

Members are chosen precisely because they are active in this field, so interests are expected. The obligation is not to have none; it is to disclose them and step back where they bite.

### Declare

- **Annually:** a short statement of affiliations, funding, advisory roles, and material interests relevant to imaging datasets and AI; refreshed yearly and whenever circumstances change.
- **Per item:** at the start of any agenda item or review, declare interests specific to that item.
- **Standing:** steward-affiliated members (Princeton Medical Systems) hold a standing declared interest in the steward's commercial offerings; noted once, assumed thereafter.

### Recuse

- **Steering Committee:** a member does not approve a decision where a material conflict of interest makes independent participation inappropriate. The recused member is excluded from that decision, and the resolution is documented in the relevant GitHub discussion or Maintainer Decision.
- **Advisory Council:** recusal means stepping back from the Council's advisory recommendation or opinion on that item. The member may continue to contribute relevant expertise unless the chair determines otherwise. The recusal is noted in the session notes.

**Example.** A Steering Committee member works for a company whose dataset is being discussed for conformance. Expected action: declare the conflict at the start of the item · contribute technical expertise if appropriate · do not approve. The recusal is documented with the decision.

**The neutrality backstop.** No rule may privilege a specific vendor, tool, or platform, and the steward's products must conform on the same terms as anyone else's. A proposal that would have that effect is out of order.

**Remember.** Doubtful cases go to the chair, and the resolution is noted. Erring on the side of disclosure is never wrong.

## Section 12 · Confidentiality

**Purpose.** Protect candid deliberation and unreleased work, never hide decisions.

**Key points.**

- Outcomes are always public; deliberation is not attributed
- Discussions follow the Chatham House Rule
- Confidentiality survives the end of membership

**Always public.**

- The Specification, the validator, and the repository record: pull requests, reviews, and merges
- Maintainer Decisions and Change Notes
- Membership of both bodies (names and affiliations), with each member's consent at appointment, may be published on the VIDS website and in other official project communications

**Confidential.**

- **Deliberation:** use what was said; don't attribute who said it. Session notes record advice and opinions, not attributed debate
- **Pre-release material:** draft Specification text, unreleased extensions, and unpublished decisions, until publication
- **Internal working material:** drafts and internal session notes
- **Third-party material** shared under explicit confidence (for example, a hospital's dataset details)
- **Prospective membership:** prospective member invitations and candidate identities remain confidential until an invitation has been accepted or the individual has agreed to public disclosure

**In practice.**

- You acknowledge these terms in writing at onboarding (Section 14).
- Confidentiality survives the end of membership, for material learned during it.
- Speaking publicly about VIDS? Speak to published material, which by design is almost everything.

**Remember.** VIDS is an open standard. Confidentiality here protects candor, not secrets: what we decide is public; who argued what is not.

## Section 13 · Member onboarding

**Purpose.** From acceptance to full participation in one quarter.

**Key points.**

- The Steering Committee approves the appointment; the chair owns the welcome
- Disclosures and acknowledgment are filed before your first session
- Nothing is expected of you before orientation

### Six steps

**1 · Accept** (invitation accepted) → **2 · Appoint** (Steering Committee approval recorded; appointment confirmed in writing) → **3 · Packet** (this handbook · How VIDS is Governed · current Specification · decision records) → **4 · Acknowledge** (conflict-of-interest disclosure and confidentiality acknowledgment, before the first session) → **5 · Orient** (introductory session with the chair and the maintainers) → **6 · Participate** (first Council session; calendar and shared workspace access)

### Your first 90 days

| By | You should have |
|----|-----------------|
| Week 2 | Packet read · disclosures filed · orientation scheduled |
| Week 6 | Orientation or first session attended · introduced to current work |
| Week 12 | First review or written input given · one area adopted as a personal focus |

Leaving? Resignation, renewal, and removal are covered in Section 5, Membership terms.

**Remember.** Nothing is expected of you before orientation, and everything you need arrives in the welcome packet.

## Section 14 · Member checklist & acknowledgment

One page. If you do these things, you are doing this job well.

**As a member, you should.**

- Attend quarterly sessions, or send written input ahead
- Review proposals within the stated window
- Declare conflicts; step back where they bite
- Respect confidentiality: Chatham House Rule
- Keep your annual disclosure current
- Speak as an individual expert, not for your employer

**You should never need to.**

- Decide anything off the record
- Interpret an unwritten rule: if it isn't here or in GOVERNANCE.md, propose it
- Weigh the steward's commercial interests in a conformance decision
- Accept a requirement that doesn't come from the Specification

### Member acknowledgment

Completed at onboarding using the Onboarding Forms, and kept on file.

I have received and read the **VIDS Governance Handbook v1.1**. I agree to the conflict-of-interest (Section 11) and confidentiality (Section 12) provisions, and I understand that only the Specification creates conformance requirements.

**Remember.** The Advisory Council advises. The Steering Committee decides. That's the whole model.

## Appendix A · Record types · quick reference

Condensed from GOVERNANCE.md. When in doubt, GOVERNANCE.md controls.

| Record | Purpose | Normative? | Visibility |
|--------|---------|------------|------------|
| Specification | The normative standard: requirements, rules, schemas. Versioned | Yes | Public |
| Pull request and review | The change and its approval; the primary decision record | No | Public |
| MD · Maintainer Decision | A durable governance or policy decision and its reason | No | Public |
| CN · Change Note | What changed and its impact on adopters. Immutable once published | No | Public |
| Errata | Dated corrections to released normative text, inside the Specification | Part of the Specification | Public |

## Appendix B · Glossary & revision history

| Term | Meaning |
|------|---------|
| Normative | Creates conformance requirements. In VIDS, only the Specification and its normative extensions are normative |
| Eligible member | A Steering Committee member who is not recused from the decision in question |
| Normal decision rule | Approval from at least two eligible Steering Committee members |
| Recusal | Standing back from a decision because of a declared interest |
| Maintainers | The team that runs the project day to day; implements decisions and holds no normative authority |
| Profiles (POC / Full) | The two adoption tiers of the Specification's validation rules |
| Chatham House Rule | Use what was said; do not attribute who said it |
| Errata | Corrections to released normative text; they live inside the Specification, not in Change Notes |

### Revision history

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-26 | Adopted per MD-0004. |
| 1.1 | On merge | Aligned with the governance model in GOVERNANCE.md as adopted in MD-0008: graded change process, approval by at least two eligible Steering Committee members, GitHub as the primary record. Section numbering for conflict of interest (11) and confidentiality (12) unchanged. Approval by at least two eligible Steering Committee members, recorded in the merging pull request. |
