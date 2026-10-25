# Model guide

Use this reading order for a new model; adapt an existing model's structure instead of reformatting it wholesale. Keep the document readable by developers, product owners, and reviewers.

The structure below is a content guide, not a form or serialization schema. Use descriptive headings and short prose; use compact tables for comparisons and overviews, and keep long explanations in the scenario text. Explain unfamiliar terms and IDs in context. A reader should understand what can go wrong, why it matters, and what to do next without reading the skill or assistant conversation.

Keep each scenario's reasoning, recommendations, decisions, and open questions together so a person can extend them directly in Markdown. Preserve meaningful manual additions and the team's layout during updates. Do not require generated metadata, special delimiters, or a separate machine-readable copy to maintain the model.

| Section | Include |
| --- | --- |
| At a glance | Purpose, scope, exclusions, draft/review status, known owner, and the few most important next actions linked to scenarios. Give each action a brief priority reason, proposed or decided response, known owner, and next check. |
| System in brief | Valuable data and operations, their sensitivity and security objectives, actors, main interactions and trust boundaries, with a compact diagram. Integrate relevant constraints and assumptions into this explanation. |
| Threats and recommended changes | Short scenario sections with stable IDs, reasoning, concrete recommendations, verification, and decisions together. |
| Open decisions and review | Remaining decisions, actual review participation and scope, and reassessment triggers. Link to scenario details instead of repeating them. |
| Appendix: sources and coverage | Source locations, revisions and status, detailed evidence, conflicts, coverage gaps, and the checklist items that are not clarified. Keep decision-relevant uncertainty beside the affected scenario as well. |

Use stable scenario IDs such as `T-001`. Add other IDs only when repeated cross-references benefit from them; named source links and plain-language references are often sufficient. Preserve established identifiers and do not renumber them just to close gaps. Every source reference must resolve to an inspected source or be marked unverified; do not invent filenames, requirement IDs, or evidence.

Aim for an opening that fits roughly one screen, usually highlighting three to five next actions rather than repeating the entire scenario list. Derive it from the scenario records, which hold the full reasoning and decision details. Preserve conditional priorities and unresolved owners. Do not imply that the overview is complete coverage or maintain a separate task list. In an existing model, reuse an equivalent summary and update only affected entries.

Keep the main text focused on understanding and action. State shared caveats once, and repeat only conditions that materially change a scenario's meaning. Combine related open questions and link to their details. Keep source inventories and coverage accounting in the appendix of the same document; omit tool-by-tool activity logs and routine checks with no effect on the result. Moving text to an appendix is not a substitute for removing repetition. Add detail when it changes a decision or enables verification, not merely to fill a field; never omit a significant threat, uncertainty, or recorded decision to meet a length target.

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

Use these questions to check content, not as mandatory output fields. A descriptive scenario heading and a few short paragraphs covering risk, recommendation, verification, and decision will usually suffice. Combine actor, mechanism, prerequisites, harm, and priority in the explanation. Keep detailed evidence in the appendix with a direct reference when needed. Readers should not have to decode chains of IDs to understand a scenario.

Keep these dimensions distinct in meaning; they need not be separate labeled fields:

| Dimension | Meaning |
| --- | --- |
| Applicability | Applicable, not applicable with rationale, or unresolved. Unexamined context has no applicability verdict. |
| Control state | Proposed, planned, reported implemented, observed implemented, or verified under recorded conditions. Evidence supports only what was actually checked. |
| Treatment | Proposed or explicitly decided elimination, mitigation, transfer, or acceptance. Transfer still identifies retained control and residual-risk responsibilities. |
| Confidence | Strength and limitations of the source support, independent of the risk priority. |

An applicable scenario can have effective treatment and remain in the model. A proposed response is not a decision. A stakeholder's report that a control exists does not establish that it works. Verification criteria describe future checks until results and conditions are recorded.

Distinguish current exposure, based on available evidence, from expected residual risk conditional on effective treatment. Proposed or planned controls do not establish current risk reduction. If applicability or effectiveness is unresolved, keep that uncertainty explicit.

Explicit acceptance records the responsible person's decision, rationale, scope, remaining exposure, and review date or trigger. A constraint or ordinary dialogue answer does not waive an obligation. Surface conflicts and alternatives without silently accepting the risk.

## Make scenarios checkable

Put the few decisive source links beside the claims they support in each scenario. Use descriptive labels such as "Payment requirements: changes after approval" and link to the relevant section or requirement where possible. Prefer repository-relative links for local documents. Keep the full source inventory and revision details in the appendix; readers should not need it to understand the argument.

Explain what each source establishes: intended behavior in a requirement, a design choice, an implementation observation, or a recorded test result. A proposed requirement belongs in the recommendation, not among existing obligations. When the basis is a team statement or assumption, identify it as such; record a missing requirement as a gap and propose wording where useful. Do not invent a document or anchor to make a scenario appear supported.

Check that the cited passage supports the claim, not just that the link resolves. Verify local targets and anchors within the authorized sources; mark inaccessible references and their limits. For effectiveness claims, link available test results or review evidence and state the checked revision and conditions when known. A link to test code describes a check, not a passing result; a requirement, design document, or merged PR alone does not verify effectiveness. Keep missing evidence explicit.

## Derive actionable improvements

For significant scenarios needing treatment, recommend changes at the level that addresses the cause: clarify a missing business or security rule in requirements, change a design decision or interaction, or identify an implementation measure supported by the available context. Use only the relevant levels; do not fill every level mechanically or prescribe additional controls when existing effective treatment is sufficient.

Name the affected requirement, design element, or component, citing its source when available. State the proposed change, explain how it interrupts the scenario, and give observable verification criteria for intended behavior and a representative failure or abuse case. If a rule is missing, propose wording rather than inventing an existing requirement ID. If technical detail is unknown, keep the recommendation at the supported level and identify what must be clarified. For material alternatives, recommend a preferred option and explain differences in protection, functionality, or implementation effort.

Keep these recommendations with the scenario and summarize the next action in the overview. They are proposals for the team's decision; editing the referenced requirements, design, or code is a separate task.

## Example

This fictional example illustrates a compact scenario, not a default threat or a mandatory set of fields. Its links point to fictional source excerpts below; actual models link to the inspected project sources.

### T-003 An approval survives a change to the payment destination

**Risk — high if edits bypass renewed approval.** A supplier allowed to edit an approved payment could redirect funds to another recipient. The [payment-edit rules](#payment-edit-rules) allow corrections, but the [approval design](#approval-design) does not say whether they invalidate approval. Current exposure and control effectiveness remain unresolved.

**Recommended change.** Add this requirement: "Changing the amount or recipient invalidates the existing approval. Settlement requires approval of the changed payment details." In the design, bind approval to the reviewed version and have settlement use those details. During implementation, prevent concurrent edits from changing them between the approval check and payment; the transaction and external-payment boundaries still need clarification. If corrections are needed, prefer this approach. Making approved requests immutable is an alternative, but requires suppliers and approvers to process replacement requests.

**How to check.** An unchanged, authorized request can settle. Changing its amount or recipient requires renewed approval, including when editing and settlement occur concurrently. These checks have not been performed. Even if effective, the response does not prevent a compromised approver from approving an unwanted recipient; recovery needs separate treatment.

**Decision — open.** First clarify which post-approval corrections are permitted. The response is proposed; owner and target date are unset. No risk acceptance is recorded.

### Fictional source excerpts for the example

#### Payment-edit rules

Suppliers may correct the amount and recipient of a submitted payment request, including after approval.

#### Approval design

An approver reviews the payment details and marks the request approved. Settlement processes approved requests. The handling of later edits is unspecified.

## Review and maintenance

Check coverage of significant objectives, actors, interactions, boundaries, checklist items, and supplied known threats. Explain exclusions and gaps. Check whether each treatment addresses the actual mechanism and whether verification includes intended behavior and a representative failure or abuse case. Check that recommendations identify the appropriate level, affected element, concrete change, rationale, and verification criteria, with material trade-offs where relevant. In updates, reassess recommendations affected by changed sources or decisions. Do not run these tests or change application code merely because they appear in the model.

Check readability and traceability together: can a team member identify the main concerns and next actions from the opening, understand each scenario without chasing IDs, and follow its key links to passages that support the claims? Remove duplicated explanations and repeated default status text, keeping material conditions and decisions intact. Do not force existing human-written models into this layout during an unrelated update.

Keep risk priority proportionate to stated prerequisites and controls. Do not turn lack of evidence into certainty that a control is absent, or treat a planned control as a completed mitigation.

When the team supplies implementation or verification evidence in an update request, attach it to the affected scenario with its revision, result, and checked conditions where available. Existing ticket or pull-request references can connect the work to the scenario ID; a closed ticket or merged change alone does not verify a control. Record supplied test results as evidence with their provenance, not as tests performed by this skill. Preserve remaining untested conditions and reassess affected exposure and decisions without declaring unrelated scenarios reviewed.
