# Contributing to VIDS

Thank you for helping improve the Verified Imaging Dataset Standard (VIDS).

VIDS is maintained as an open standard. We aim to keep contribution and review simple while giving changes that affect conformance appropriate review.

## 1. Ways to Contribute

You can contribute by:

- reporting a specification ambiguity or documentation problem;
- reporting a validator bug;
- proposing an improvement to the specification;
- proposing support for a new modality or annotation type;
- improving examples or documentation;
- contributing validator fixes or tests.

Use GitHub issues when discussion would be useful before making a change. Otherwise, a pull request is sufficient.

## 2. Pull Requests

Keep pull requests focused on one logical change.

A pull request should briefly explain:

- what is changing;
- why the change is needed; and
- whether it affects VIDS conformance.

Avoid unrelated formatting or cleanup in the same pull request.

The pull request and repository history are the record of the change. Separate approval documents or signatures are not required.

## 3. Types of Changes

### Editorial Changes

Examples include:

- typo fixes;
- broken links;
- clearer wording that does not change a requirement;
- example corrections;
- formatting improvements.

These changes may be merged by a maintainer without additional governance process.

### Specification Changes

A specification change affects or may affect the meaning of VIDS requirements.

Examples include:

- adding or changing fields;
- adding modality codes;
- changing annotation requirements;
- changing file or directory rules;
- changing PASS, FAIL, or WARN expectations.

Submit a pull request describing the proposed change and its conformance impact.

A substantive specification change requires review by at least one other Steering Committee member before merge.

### Major or Breaking Changes

Changes that could make an existing conformant dataset non-conformant, remove requirements, or materially alter the structure of VIDS require broader review.

Examples include:

- new REQUIRED fields;
- removal or material revision of existing requirements;
- incompatible file or directory changes;
- other breaking conformance changes.

These changes should first be discussed publicly through GitHub and receive a minimum 30-day comment period.

Approval follows the decision rules in GOVERNANCE.md.

## 4. Validator Changes

The validator implements the VIDS Specification. It does not independently define VIDS requirements.

If the validator and the specification disagree, the specification governs and the validator should be corrected.

For validator changes:

1. make the change;
2. add or update tests where appropriate;
3. run the relevant test suite; and
4. submit a pull request explaining the behavior being changed.

Changes that correct the validator to match an existing specification requirement do not require a specification change.

Changes that introduce a new conformance requirement must first be reflected in the specification.

A validator change that materially changes validation outcomes requires review by at least one other maintainer before merge.

## 5. New Modalities and Extensions

New modality support or domain-specific extensions may be proposed through a GitHub issue or pull request.

Include enough information for maintainers to understand:

- the modality or use case;
- why existing VIDS fields are insufficient;
- the proposed fields or conventions; and
- an example where useful.

Small backward-compatible additions can follow the normal specification-change process.

A separate formal proposal template is not required.

## 6. Testing

Changes to validator behavior should include appropriate tests.

Before merging validator changes, maintainers should confirm that relevant automated tests pass.

Continuous integration is the primary automated check. Contributors do not need to create separate testing evidence documents when the required results are already recorded by GitHub and CI.

## 7. Review and Approval

VIDS uses a lightweight review model.

- **Editorial and routine documentation changes:** may be merged by a maintainer.
- **Substantive specification changes:** require review by at least one other Steering Committee member.
- **Major or breaking changes:** follow the additional public-review and approval rules in GOVERNANCE.md.

Routine contributions do not require formal votes, signatures, approval forms, or separate decision records.

A Maintainer Decision is used only when there is a durable governance or policy decision worth recording separately.

## 8. Versioning

VIDS uses semantic versioning.

- **Major:** breaking or incompatible changes.
- **Minor:** backward-compatible additions.
- **Patch:** editorial corrections and clarifications that do not change conformance.

Specification and validator versions may advance independently.

Existing VIDS 1.x datasets should remain conformant under later VIDS 1.x specifications unless the earlier result depended on a validator defect or under-enforcement of an existing requirement.

Breaking specification changes require a major version and an appropriate migration path.

## 9. Project Governance

Only the VIDS Specification and its normative extensions define conformance requirements.

Project governance, maintainer authority, and decision rules are defined in GOVERNANCE.md.

Internal company processes, commercial activities, and implementation decisions do not become part of the VIDS standard unless they are adopted through the VIDS governance process.

## 10. Community Conduct

Be professional, constructive, and evidence-based.

Disagreement is welcome. Focus discussion on improving the standard, its implementation, and its usefulness to adopters.

## 11. Contact

For technical questions, bug reports, and proposed changes, use GitHub issues or pull requests.

For partnership or governance inquiries: [standards@vidsstandard.org](mailto:standards@vidsstandard.org)

---

**VIDS was created by Princeton Medical Systems and is maintained as an open standard.**
