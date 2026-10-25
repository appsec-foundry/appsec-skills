# Model guide

Use these sections for a new model; adapt an existing model's structure instead of reformatting it wholesale. Keep the document readable by developers, product owners, and reviewers.

| Section | Include |
| --- | --- |
| Scope and ownership | System or feature, purpose, responsible team, intended audience, exclusions, current/proposed/transition state, and actual review status. Leave unknown ownership explicit. |
| Action overview | A compact table of the most important scenarios, linked by stable ID, with a short priority rationale, proposed or decided response, known owner, and next verification or clarification step. |
| Sources and assumptions | Source IDs, locations and revisions where available, source status, assumptions, conflicts, inaccessible or unexamined context. |
| Assets and security objectives | Data classification, valuable operations, confidentiality, integrity and availability needs, and consequences of violating them. Public data may still need strong integrity. |
| Actors and constraints | Goals, starting access, privileges, controlled inputs, binding obligations, negotiable choices, and dependencies. |
| System model | Components, stores, external parties, interactions, and changes in trust assumptions. Include a compact diagram and supporting prose. |
| Threat scenarios | Stable IDs, system-specific mechanisms, prerequisites, objectives, consequences, applicability, and explained priority. |
| Treatment and verification | Controls and their states, treatment decisions, current exposure, expected residual risk, responsible roles, target dates, evidence, and testable criteria. May be kept with each scenario. |
| Review and open questions | Participants and reviewed scope, unresolved decisions, coverage gaps, checklist items that are not clarified, and reassessment triggers. |

Assign stable identifiers where elements are referenced, for example `S-001` for sources, `O-001` for objectives, `F-001` for flows, and `T-001` for scenarios. Preserve established identifiers and do not renumber them just to close gaps. Every source reference must resolve to an inspected source or be marked unverified; do not invent filenames, requirement IDs, or evidence.

Keep the action overview near the start and derive it from the scenario records; those records hold the full reasoning and decision details. Preserve conditional priorities and unresolved owners. Do not imply that the overview is complete coverage or maintain a separate task list. In an existing model, reuse an equivalent summary and update only affected entries.

## Reasoning perspectives

Organize the work around system understanding, plausible failures, responses, and review, following the [OWASP threat modeling guidance](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html).

Use STRIDE to examine impersonation, unauthorized modification, disputed actions, disclosure, disruption, and excess privilege at relevant interactions. Business abuse may use legitimate permissions: approval reuse after a material edit, manipulation of a recovery process, or an exception that bypasses a business restriction. Ground these mechanisms in actual requirements rather than importing examples as findings.

Describe actors through access and capabilities. An authenticated customer who controls an uploaded record is more actionable than an unsupported attribution to a named adversary. For serious scenarios, explain the most harmful plausible outcome, prerequisites, affected parties, and reach. Use multi-step paths only when they clarify the attack.

## Scenario records

A scenario should answer:

- Which actor can violate which objective, through which interaction?
- What access, input, condition, or sequence makes that plausible?
- Which requirement, design statement, known threat, or explicit assumption supports it?
- Who or what is harmed, and why is it prioritized at this level?
- Which controls address the mechanism, what is their actual state, and what remains?
- What decision is needed, who is responsible, and how could the response be verified?

Keep these dimensions separate:

| Dimension | Meaning |
| --- | --- |
| Applicability | Applicable, not applicable with rationale, or unresolved. Unexamined context has no applicability verdict. |
| Control state | Proposed, planned, reported implemented, observed implemented, or verified under recorded conditions. Evidence supports only what was actually checked. |
| Treatment | Proposed or explicitly decided elimination, mitigation, transfer, or acceptance. Transfer still identifies retained control and residual-risk responsibilities. |
| Confidence | Strength and limitations of the source support, independent of the risk priority. |

An applicable scenario can have effective treatment and remain in the model. A proposed response is not a decision. A stakeholder's report that a control exists does not establish that it works. Verification criteria describe future checks until results and conditions are recorded.

Distinguish current exposure, based on available evidence, from expected residual risk conditional on effective treatment. Proposed or planned controls do not establish current risk reduction. If applicability or effectiveness is unresolved, keep that uncertainty explicit.

Explicit acceptance records the responsible person's decision, rationale, scope, remaining exposure, and review date or trigger. A constraint or ordinary dialogue answer does not waive an obligation. Surface conflicts and alternatives without silently accepting the risk.

## Example

This fictional design example illustrates the record shape, not a default scenario for every project.

### T-003 An approval survives a change to the payment destination

A supplier account changes the destination on an approved payment request, and settlement uses the revised destination without renewed approval.

- Objective: `O-002` — Payment approval covers the amount and recipient used for settlement.
- Basis: `S-001` allows suppliers to correct submitted requests; `S-002` describes approval and settlement but leaves post-approval edits unresolved.
- Actor and prerequisites: An authenticated supplier account with permission to edit a request that has already been approved.
- Interaction: `F-004` — Request edit to approval state to settlement instruction.
- Consequence: Funds may be redirected outside the recipient intended by the approver.
- Applicability: Unresolved until the permitted edits and approval invalidation rule are clarified.
- Priority: High if the edit reaches settlement without reapproval; payment diversion has direct integrity impact. Confidence is limited by the missing rule.
- Proposed response: Bind approval to the reviewed amount and destination; require renewed approval after a relevant change.
- Control state: Proposed; implementation and effectiveness are unverified.
- Current exposure: Unresolved until post-approval edit rules are clarified; the proposed control establishes no current risk reduction.
- Expected residual risk if the response is implemented and effective: A compromised approver could still approve an unwanted destination; recovery after settlement needs separate treatment.
- Verification criteria: A destination change prevents settlement under the old approval; an unchanged, authorized request can still settle. Include concurrent edit and settlement behavior.
- Decision: Proposed. Control owner and treatment decision remain open; no risk acceptance is recorded.
- Open question: Which post-approval corrections are permitted without renewed approval?

## Review and maintenance

Check coverage of significant objectives, actors, interactions, boundaries, checklist items, and supplied known threats. Explain exclusions and gaps. Check whether each treatment addresses the actual mechanism and whether verification includes intended behavior and a representative failure or abuse case. Do not run these tests or change application code merely because they appear in the model.

Keep risk priority proportionate to stated prerequisites and controls. Do not turn lack of evidence into certainty that a control is absent, or treat a planned control as a completed mitigation.

When the team supplies implementation or verification evidence in an update request, attach it to the affected scenario with its revision, result, and checked conditions where available. Existing ticket or pull-request references can connect the work to the scenario ID; a closed ticket or merged change alone does not verify a control. Record supplied test results as evidence with their provenance, not as tests performed by this skill. Preserve remaining untested conditions and reassess affected exposure and decisions without declaring unrelated scenarios reviewed.
