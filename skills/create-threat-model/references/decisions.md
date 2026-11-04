# Walk through threats, develop measures, and record decisions

Read this guide when the user requests a joint assessment of identified threats, a measures discussion, or treatment decisions (REQ-07). An earlier request for that dialogue remains sufficient; do not ask again whether to start. Recommendations or an unanswered invitation start no dialogue. When creation or update is also requested, deliver and check the supported draft first, then continue the requested conversation.

## Start from the identified scenarios

Enter directly at the relevant scenarios of the existing model, using their recorded scope, audience, sources, uncertainty, and previous answers (REQ-07, REQ-09, REQ-10).

- Do not restart the system intake, interview, or model-creation workflow. Read more or ask only when a material gap, contradiction, or change affects the comparison.
- Apply the existing audience and confidentiality rules to the conversation.
- If no suitable model exists, explain the missing basis and use supplied context where sufficient. Do not silently create one.

## Guided threat walkthrough

Use this walkthrough when the user asks to go through identified threats together to assess them or develop suitable measures. A request for an assessment or recommendations alone does not select an interactive walkthrough. A request to jointly assess threats permits focused questions about those threats; it does not require another invitation (REQ-03, REQ-07, REQ-19).

Start with the user's selected scenarios, otherwise those with the greatest supported harm or uncertainty that could change a decision. For updates, stay with affected scenarios. Work through one scenario at a time, grouping shared facts or measures only when that avoids repetition. Do not require the user to review every threat before delivering useful outcomes.

For each scenario:

1. **Explain the threat.** Give its ID, actor, action, prerequisites, concrete harm, relevant existing protection, and the uncertainty that matters. Keep the introduction short enough to discuss without reading the whole model.
2. **Clarify decisive facts.** Read available evidence first. Ask about missing business rules, permitted actions, reach, recovery, or control behavior that could change the assessment. Ask one concrete point per question and at most three questions per round; dependent questions follow the preceding answer. Reuse settled context and accept unknown or skipped answers under the [interview rules](interview.md#ask-and-wait). The assistant analyzes attack feasibility; the user need not assign probabilities or prove an attack.
3. **Propose and explain the assessment.** Apply the model's [priority guidance](model-guide.md#explain-priorities) to harm, prerequisites, reach, and existing controls. Explain how the answers change or support that assessment. Keep evidence confidence separate; missing information does not lower risk. A reported control remains reported until evidence establishes its effectiveness. If the user disagrees, clarify the differing premise where useful; keep unresolved differences visible rather than changing the rating solely to obtain agreement.
4. **Develop suitable measures.** Recommend a concrete change that addresses the cause under the [improvement guidance](model-guide.md#derive-actionable-improvements). Compare alternatives only where protection, workflow, effort, or remaining exposure materially differs. Ask about practical constraints when they determine the choice, and adapt the recommendation to the answers. Explain the expected remaining risk and checks for both intended behavior and representative abuse. Effective existing protection may make verification the useful next step instead of another control.
5. **Show the outcome.** Summarize the changed or retained assessment and its reason, the proposed or explicitly chosen measure, the remaining uncertainty, and the next check or decision. Preserve the scenario ID and distinguish facts, user reports, proposals, plans, and verified results. Include owners and dates only when known. A planned measure establishes no current risk reduction.

When creation or update includes this walkthrough, incorporate its outcomes into that model using the [write checks](delivery.md#write-and-check), preserving unrelated content (REQ-04, REQ-09). A standalone walkthrough or review returns proposed changes in the conversation without changing files or review status (REQ-10). Save concise conclusions and their source, not a transcript.

Continue with the next relevant scenario within the requested scope and budget. Do not ask for permission to continue after every answer. Stop questions when the user skips further dialogue or no material points remain; summarize pending scenarios without marking them reviewed or accepted. Cancellation stops the task. Reuse explicit treatment choices already supplied; enter a [treatment-decision round](#explicit-treatment-decisions) only when choosing responses was requested. Identifying measures alone does not require a treatment choice, owner, date, or risk acceptance.

### Example: payment recipient changes after approval

This fictional example illustrates the dialogue; use only questions supported by the actual project's open points. Assume T-003 already establishes that supplier staff can edit the recipient after approval and that a diverted payment could cause a substantial, unrecoverable loss. Whether approval remains valid is unknown.

> **T-003:** Supplier staff could redirect an approved payment if changing the recipient leaves the old approval valid. The serious financial consequence is established; the approval behavior is still open.

Ask: "What happens to the existing approval when the recipient changes?" A short answer or "unknown" suffices.

- **If unknown:** Keep the path conditional and the control unresolved. Explain the provisional priority using the established harm; do not label the attack proven or lower the risk because evidence is missing. The next check is whether an approval can authorize changed payment details.
- **If renewed approval is reported:** Attribute that statement to the user and identify what would verify it, including changes concurrent with payout. Do not call the control verified or the threat resolved from the answer alone.

If a measure is needed, explain: "Invalidating approval when payment details change would require finance to approve the new recipient. Locking details after approval is another option, but legitimate corrections would need a new payment request."

Then ask, only if this affects the choice: "Must staff be able to correct an approved payment before it is sent?" If corrections are required, recommend renewed approval tied to the exact payment details. Proposed checks: an unchanged approved payment succeeds; changing the recipient prevents payout under the old approval, including a concurrent change. These are future checks, not results.

If the user requested choosing measures, ask one explicit choice: "Shall we plan renewed approval after recipient changes, or leave that decision open?" Otherwise keep the recommendation as a proposal. "Sounds serious" confirms neither a measure nor risk acceptance. If the user selects the measure, summarize it as planned, with verification and any unstated owner or date still open.

## Discuss or plan measures

For a measures-only request, go directly to the relevant responses without requiring the full walkthrough.

Provide concrete proposals under the [improvement guidance](model-guide.md#derive-actionable-improvements):

- Where alternatives exist, compare protection, effect on intended use, effort, and unresolved prerequisites, and recommend a starting point.
- Identify where each change belongs: application logic, component design, maintained configuration, or the operating environment. A comparison of container, VM, or network choices alone is insufficient when an application change addresses the cause.
- If a missing fact determines the choice, name the check that would resolve it. Ask only when necessary.
- End without requiring a treatment selection, owner, date, or risk-acceptance decision.

A request to compare or plan measures is not permission to edit the model, record acceptance, or implement changes. An accepted invitation to plan selects this discussion only. An accompanying update request authorizes focused changes under the [write rules](delivery.md#write-and-check). Implementing proposals needs a separate task.

## Explicit treatment decisions

Enter this round only when the user asks to choose treatments, accept a risk, or work through treatment decisions. A creation or update request, a request to discuss or plan measures, confirmation of system facts, or an unanswered invitation does not select it.

1. Explain the concrete proposals and trade-offs first.
2. Ask about the most important open scenarios in priority order, with at most three independently answerable questions per round. One scenario may need several rounds; ask dependent questions sequentially. For updates, limit rounds to scenarios affected by the update, including new scenarios and changed shared boundaries.
3. Reuse decisions already supplied, unless their assumptions changed. If none remain open in scope, finish without a round.
4. Make clear that this round requests treatment decisions, not system facts. Follow the [question and waiting rules](interview.md#ask-and-wait).
5. For each scenario, summarize the harm and uncertainty, name the decision, and offer the actual alternatives in the team's language with an option to leave it open: "Plan renewed approval after a recipient change," not "Plan a response." Do not force a risk-acceptance option into every choice.

| Answer category | Record |
| --- | --- |
| Plan a response | The measure, responsible person, and target date. This records a plan, not implementation. |
| Accept | Who accepts, the rationale, and the review date or trigger. |
| Clarify first | What is missing; the scenario stays open. |

The categories record the selected response; they are not a fixed answer menu. A response may eliminate, mitigate, or transfer the risk.

- When updates are authorized, record answers as the matching treatment from the [model guide](model-guide.md#treatment-semantics) with a focused patch under the [write rules](delivery.md#write-and-check). Otherwise return proposed records in the conversation.
- Record only explicit decisions with the details the team states; do not fill in a person or date. An acceptance without a named responsible person stays open, as do unanswered scenarios.
- Offer the next scenarios while enough budget remains for the required checks. Otherwise list the pending decisions and explain the limit. The team can stop and revisit decisions later.
- A decision does not authorize implementing the measure, creating tickets, or changing code.
