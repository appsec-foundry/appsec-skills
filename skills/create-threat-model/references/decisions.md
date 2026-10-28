# Discuss measures and record decisions

Read this guide only when the user requests a measures discussion or treatment-decision round (REQ-07). Use the [model guide](model-guide.md#derive-actionable-improvements) for actionable recommendations and treatment semantics. Recommendations in the normal delivery do not start either dialogue. When creation or update is also requested, deliver and check the supported draft first. Record later decisions only when updates are authorized; otherwise return proposed records in the conversation.

## Discuss or plan measures

When the user asks to explain, compare, or plan measures, provide concrete proposals and recommendations using the existing model under the skill's [operation rules](../SKILL.md#choose-the-operation). Where meaningful alternatives exist, compare their protection, effect on intended use, effort, and unresolved prerequisites; recommend a starting point supported by the model. Identify where each change belongs, such as application logic, component design, maintained configuration, or the operating environment, so developers can distinguish repository work from deployment work. Apply the same improvement guidance here as in the model; a comparison of container, VM, or network choices alone is insufficient when a relevant application change addresses the cause. If a missing fact determines the choice, explain which check would resolve it and ask only when necessary under the material-gap rules. End a comparison or proposed plan without requiring a treatment selection, owner, date, or risk-acceptance decision. A reply accepting an invitation to plan measures selects this discussion, not automatically a decision round or write permission. Developing proposals stays within modeling; implementing them needs a separate task.

## Explicit treatment decisions

Only when the user asks to choose treatments, accept a risk, or work through treatment decisions, enter this decision round. A creation/update request, a request merely to discuss or plan measures, confirmation of system facts, or an unanswered optional invitation does not select it. First explain the concrete proposals and trade-offs as above; do not require "plan," "accept," or "clarify" before the user understands the response.

Ask about the most important open scenarios, at most three at a time, in priority order. For updates, limit this round and subsequent rounds to scenarios affected by the requested update, including new scenarios and changed shared boundaries. Use decisions already supplied; do not ask the team to decide them again unless their assumptions changed. If no decisions remain open in scope, finish without a decision round.

Make clear that this round requests treatment decisions, not facts about the system. Use the [question and waiting rules](checklist.md#ask-and-wait), within the host tool's permitted uses. For each scenario, summarize the harm and uncertainty and name the decision needed. Offer the actual alternatives in the team's language, with an option to leave the decision open. For example, when two measures are viable, offer those two measures and clarification or deferral; do not force a risk-acceptance option into every choice. Use the categories below to record the selected response, not as a fixed answer menu. For example, use "Plan renewed approval after a recipient change" instead of only "Plan a response."

| Answer category | Record |
| --- | --- |
| Plan a response | The measure, responsible person, and target date. This records a plan, not implementation. |
| Accept | Who accepts, the rationale, and the review date or trigger. |
| Clarify first | What is missing; the scenario stays open. |

The proposed response may eliminate, mitigate, or transfer the risk, as appropriate to the scenario. When updates are authorized, record answers as the matching treatment from the model guide with a focused patch under the [write rules](../SKILL.md#write-and-check); otherwise return proposed decision records in the conversation. Record only explicit decisions with the details the team states; do not fill in a missing person or date. An acceptance without a named responsible person stays open, as do unanswered scenarios. Within the requested dialogue, offer the next scenarios while enough budget remains for the required checks; the team can stop and revisit open decisions later. If the budget cannot cover recording another round, list the pending decisions and explain the limit. A decision does not authorize implementing the measure, creating tickets, or changing code.
