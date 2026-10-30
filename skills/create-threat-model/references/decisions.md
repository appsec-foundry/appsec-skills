# Discuss measures and record decisions

Read this guide only when the user requests a measures discussion or a treatment-decision round (REQ-07). Recommendations in the normal delivery start neither dialogue. When creation or update is also requested, deliver and check the supported draft first.

## Discuss or plan measures

Enter directly at the relevant scenarios of the existing model, using their recorded scope, audience, sources, uncertainty, and previous answers (REQ-07, REQ-09, REQ-10).

- Do not restart the system intake, interview, or model-creation workflow. Read more or ask only when a material gap, contradiction, or change affects the comparison.
- Apply the existing audience and confidentiality rules to the conversation.
- If no suitable model exists, explain the missing basis and use supplied context where sufficient. Do not silently create one.

Provide concrete proposals under the [improvement guidance](model-guide.md#derive-actionable-improvements):

- Where alternatives exist, compare protection, effect on intended use, effort, and unresolved prerequisites, and recommend a starting point.
- Identify where each change belongs: application logic, component design, maintained configuration, or the operating environment. A comparison of container, VM, or network choices alone is insufficient when an application change addresses the cause.
- If a missing fact determines the choice, name the check that would resolve it. Ask only when necessary.
- End without requiring a treatment selection, owner, date, or risk-acceptance decision.

A request to compare or plan measures is not permission to edit the model, record acceptance, or implement changes. An accepted invitation to plan selects this discussion only. An accompanying update request authorizes focused changes under the [write rules](delivery.md#write-and-check). Implementing proposals needs a separate task.

## Explicit treatment decisions

Enter this round only when the user asks to choose treatments, accept a risk, or work through treatment decisions. A creation or update request, a request to discuss or plan measures, confirmation of system facts, or an unanswered invitation does not select it.

1. Explain the concrete proposals and trade-offs first.
2. Ask about the most important open scenarios, at most three at a time, in priority order. For updates, limit rounds to scenarios affected by the update, including new scenarios and changed shared boundaries.
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
