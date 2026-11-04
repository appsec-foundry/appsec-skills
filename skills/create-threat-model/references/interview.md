# Interview guide

Read this guide before the first question. It governs every question the skill asks, in any phase and operation, and the threat dialogue after delivery.

## Form of a question

A question about a scenario or checklist item, after phase 2 or in the threat dialogue, has four parts:

1. **Heading** in chat: position, ID, and title with the provisional priority.
2. **Background** in chat, two or three sentences: what could happen, what the sources already establish, and what is open. Name the decisive source.
3. **Question**: one short sentence on one fact or choice, beginning with the ID, so it is clear without the background.
4. **Effect**: each option says what that answer changes in priority, applicability, or recommendation. For an open question, the background says what the answer decides.

> Question 1 of about 3 · T-003 Payment details can change after approval (provisional: high)
>
> Background: The payment-edit rules let supplier staff correct the recipient after approval. The approval design does not say whether a correction cancels the approval.
>
> T-003: Does an approval stay valid when the recipient changes?
> - Yes: T-003 stays high; renewed approval is recommended.
> - No: the cancellation is a reported control; the next step is to verify it.
> - Unknown: T-003 stays high under that condition.

Before the candidates exist, only these questions are allowed, each on one point: the target or scope, the audience, the purpose when no source states it, the operation when it is unclear, the use of another threat model document found in the project, and permission to read more code. The reading question explains the gap: "The documentation leaves data flows unclear. May I read more of the source code to trace them?" with the choices "Yes, include more code" and "Continue with current sources."

Check each question before sending it:

1. **Necessary.** Would the answer change a scenario, priority, treatment, scope, or authorized action? Otherwise omit it.
2. **In scope.** It concerns the application or the selected feature, not the user's installation, and the facts it depends on are established.
3. **Answerable.** One short sentence asks for one fact or choice. If the user could accept one clause and reject another, split it. Keep data, recipients, consequences, and permissions separate.
4. **Clear to answer.** A bare answer has one meaning: "Yes," "No," and "Unknown" for a proposal, actual alternatives for a choice, otherwise one short open question that says a short answer or "unknown" is fine. One selection must not confirm several assets, several harms, or a permission. No option asks for additional text; ask a needed detail, such as where a rule is documented, as its own follow-up question.
5. **New.** Revisit an answered, skipped, or unknown point only when new evidence changes it or the user reopens it.

Ask what a loss would prevent, not whether a clearly harmful outcome counts as harm. Ask about existing or intended rules, not whether the team wants a protection measure. Attack feasibility is yours to analyze; the user need not prove an attack or assign probabilities. Do not recommend factual answers, and remember that a choice cannot add a claim or a permission: a negative or unknown permission answer leaves the action unauthorized.

## Rounds

- Ask a question about a scenario or checklist item alone, one per round. Target, scope, audience, destination, document-use, and permission questions may share a round of at most three, never with a scenario question. Ask dependent questions sequentially.
- Order by effect: first the facts that move the most candidates or the highest provisional priority. Announce the expected number with the candidate list and keep it current in the headings.
- After each answer, state its effect in one line before the next question: "→ T-003 stays high; recommendation: renewed approval. Basis: your statement, unverified." Say so when an answer changes nothing.
- Give the team room to add concerns without a mandatory extra round.
- Stop when further answers would not change a scenario, priority, or response. Do not continue to fill checklist entries. Show what the answers changed, one line per affected scenario with its previous and current priority or recommendation, plus the points that remain open; then complete the operation.

## Ask and wait

Use the host's interactive question tool when available and permitted. Put the heading and background in chat directly before it, and the question and choices in the tool without repeating them in chat. Ask an open question in chat. Without such a tool, ask in chat and yield. Ask in the user's language, even when the model uses another language.

A displayed question is not an answered one. If an asynchronous tool returns before the user replies, the question is pending: do useful independent work within scope and budget, then use the host's waiting mechanism within its limits. Do not send a final "no files changed" while the host supports waiting, repeat the question, perform filler reads, or treat a timeout or preselected option as a reply. After the answer, resume the pending step and carry the operation through to its deliverable; do not restart the workflow. If the host has only chat turns, present the questions and yield, making clear that the task awaits answers.

## Interpret answers

Apply these rules to every statement from the user, including facts in the request. Update only what a statement establishes and drop questions it makes unnecessary.

- A concern, a desired limit, a factual description, and a permission are different answers.
- Confirming that a consequence matters does not establish that an attack can cause it.
- Keep contradictions unless the user clearly corrects the earlier fact for the same scope. If an ambiguous bundled answer matters, ask one focused clarification.
- A statement keeps its scope. A note that limits "no material harm" to a training exercise says nothing about harm outside it; if the scope is unclear, ask only whether the statement refers to the exercise alone.
- A user answer clarifies a checklist item as an attributed, unverified statement. If the user cannot answer, the point stays open.

Skipped and unknown facts remain open and do not lower risk. No-questions mode, requested by the user or by stopping the interview, means continuing with conditional candidates and stating what remains unconfirmed. A skipped permission or operation choice does not authorize the dependent action. Cancellation stops the work.

## Continue the dialogue

Use this section when the user asks to go through identified threats together, to discuss measures, or to choose treatments (REQ-12). An earlier request for that dialogue remains sufficient; do not ask again whether to start. A request for an assessment or recommendations alone starts no dialogue.

Enter directly at the scenarios of the existing model with their recorded scope, audience, sources, and previous answers. Do not restart phases 1 and 2; read more or ask only when a material gap affects the discussion. Start with the user's selected scenarios, otherwise those with the greatest supported harm or the uncertainty most likely to change a decision; for updates, stay with affected scenarios. Work through one scenario at a time.

For each scenario:

1. **Explain it** in a few sentences: ID, actor, action, prerequisites, concrete harm, relevant existing protection, and the uncertainty that matters.
2. **Clarify decisive facts** one question at a time in the form above: business rules, permitted actions, reach, recovery, or control behavior that could change the assessment. The explanation from step 1 is the background of the first question.
3. **Propose the assessment** under the model guide's [priority guidance](model-guide.md#explain-priorities) and say how the answers changed or supported it. A reported control stays reported until evidence shows it works. If the user disagrees, clarify the differing premise; keep an unresolved difference visible rather than changing the rating to obtain agreement.
4. **Develop measures** under the [improvement guidance](model-guide.md#derive-actionable-improvements): a concrete change that addresses the cause, alternatives only where protection, workflow, effort, or remaining exposure differ materially, and questions about constraints only when they determine the choice. State the expected remaining risk and the checks for intended behavior and representative abuse. Effective existing protection may make verification the next step instead of another control.
5. **Show the outcome**: the changed or retained assessment and its reason, the proposed or explicitly chosen measure, the remaining uncertainty, and the next check or decision. Include owners and dates only when known. A planned measure establishes no current risk reduction.

Continue with the next scenario without asking for permission after every answer. Stop when the user skips further dialogue or no material points remain, and summarize pending scenarios without marking them reviewed or accepted. For a measures-only request, go directly to the responses and end without requiring a treatment selection, owner, date, or risk acceptance.

Under the skill's write rule, outcomes are saved only within an authorized creation or update, with the delivery guide's [write checks](delivery.md#write-and-check); otherwise return the proposed records in the conversation. Save concise conclusions and their source, not a transcript.

### Treatment decisions

Enter this round only when the user asks to choose treatments, accept a risk, or work through treatment decisions. Explain the proposals and trade-offs first, then ask about the most important open scenarios in priority order, with the actual alternatives in the team's language and an option to leave the decision open: "Plan renewed approval after a recipient change," not "Plan a response." Do not force a risk-acceptance option into every choice, and make clear that the round asks for decisions, not system facts.

| Answer | Record |
| --- | --- |
| Plan a response | The measure, responsible person, and target date. A plan, not an implementation. |
| Accept | Who accepts, the rationale, and the review date or trigger. |
| Clarify first | What is missing; the scenario stays open. |

Record only explicit decisions with the details the team states; do not fill in a person or date. An acceptance without a named responsible person stays open. A decision does not authorize implementing the measure, creating tickets, or changing code.

### Example

T-003 already establishes that supplier staff can edit the recipient after approval and that a diverted payment is a substantial, unrecoverable loss. Whether approval survives the edit is unknown.

Ask: "T-003: What happens to the existing approval when the recipient changes? A short answer or 'unknown' is fine." If unknown, keep the path conditional, explain the provisional priority from the established harm, and name the next check. If renewed approval is reported, attribute the statement to the user and say what would verify it, including a change concurrent with payout; do not call the threat resolved.

If a measure is needed: "Invalidating approval when payment details change would require finance to approve the new recipient. Locking details after approval is another option, but legitimate corrections would then need a new payment request." Ask "Must staff be able to correct an approved payment before it is sent?" only if that affects the choice. If the user requested choosing measures, ask one explicit choice: "Shall we plan renewed approval after recipient changes, or leave that decision open?" "Sounds serious" confirms neither a measure nor an acceptance.

## Question examples

Use these only when the project context supports them.

- Permitted readers (C-03): "T-002: Under the intended workflow, who may read uploaded customer records?"
- Business misuse (C-11): "T-005: Does marking an invoice as paid trigger shipment of the order?" Use the answer for consequences, not as evidence that an unauthorized change is possible.
- Availability (C-04): "T-006: How long could order processing be unavailable before it causes serious problems? A rough duration is enough."
- Permissions (C-06): "T-004: Under the intended support role, may staff change customer records?"
- Recovery and detection (C-13): "T-003: Can an accidentally released payment still be recalled?" "T-003: How would the team notice a changed bank account on a payment recipient?"
- External recipients (C-07): "T-007: Which data categories does the external analytics service receive?"
