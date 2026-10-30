# Interview guide

Read this guide before the first question. It is not needed when no question will be asked.

## Plan the interview

Work from the [coverage record](checklist.md#coverage-record) and apply its [answer rules](checklist.md#interpret-answers) after each reply. Settle these topics in order, using sources first. They are dependencies, not mandatory rounds; skip settled and irrelevant topics.

| Order | Establish | Ask only when needed |
| --- | --- | --- |
| 1. Readers | Who the model is for. | If unresolved, ask internal/public/undecided first. Resolve who may receive confidential findings before including them. |
| 2. Purpose and scope | What the application is intended to do and what is covered (C-01, C-04). | Confirm a source-derived purpose unless the user stated it. Do not substitute their personal use for the project's intended uses. |
| 3. Architecture and operating assumptions | Supported operating modes, exposed interfaces, and optional integrations (C-05, C-07, C-08, C-13). | Ask about missing architectural expectations only when they affect the assessment. Keep configuration-dependent flows conditional. |
| 4. Data and recipients | Which data the intended uses involve and who may receive it (C-03, C-10). | Reuse project-level statements. One person's synthetic test data does not establish the application's data scope. Ask about another category or recipient only when evidence or a concrete unresolved flow makes it relevant. |
| 5. Consequences | What people could lose or be unable to do (C-04). | Confirm concrete consequences grounded in the preceding context. Ask about the value of assets or disruption, not whether an attack can succeed. |

If a structural gap requires a [reading decision](../SKILL.md#optional-architecture-reading), ask about the reading itself: "The documentation leaves data flows unclear. May I read more of the source code to trace them?" Choices: "Yes, include more code" and "Continue with current sources." If needed, explain once that this reads files without running the application.

## Check each question

Before sending a question, check:

1. **Necessary:** Would the answer change a scenario, priority, treatment, scope, or authorized next action? Otherwise omit it, except outstanding context confirmations and permission checks.
2. **In scope and timely:** Does it concern the repository's application or the selected feature, and are the facts it depends on established? Remove questions about the user's installation.
3. **Answerable:** Does one short sentence ask for one concrete fact or choice? If the user could accept one clause and reject another, simplify or split it. Keep data policy, recipients, consequences, and permission distinct.
4. **Clear to answer:** Would a bare answer have one meaning? Use "Yes," "No," and "Unknown" for a single proposal and actual alternatives for a choice. Otherwise ask one short open question. One selection must not confirm several assets, several harms, a reinterpreted answer, or a permission.
5. **New:** Revisit an answered, skipped, or unknown point only when new evidence changes it or the user reopens it. A later round needs a specific remaining gap, not unused checklist items.

Ask what a loss would prevent, not whether a clearly harmful outcome counts as harm. Once confidential financial records and their permitted readers are established, do not ask whether disclosure to other customers is harmful; ask for the missing business consequence, such as which payment an approval triggers. This filter does not replace outstanding context confirmation. Attack feasibility is for the assistant to analyze.

## End the interview

Before another round, say which assessment or next action the remaining answer would affect.

Once context confirmations are answered, unknown, or skipped, stop when further answers would not change scenarios, priorities, or responses (REQ-03, REQ-14), and complete the operation: a supported draft for creation or update, observations for review. Do not continue merely to fill checklist entries. Insufficient system context still gives an incomplete outcome, and unresolved permissions still block dependent actions.

## Ask and wait

Use the host's interactive question tool when available and permitted; this skill enables no tools or modes. Put the complete question and choices there without repeating them in chat. Otherwise ask in chat and yield. Ask in the user's language, even when the model uses another language.

These rules apply to every question, including operation selection, audience, context confirmation, and reading permission:

- **Batches:** Up to three short, independent questions on related topics. Ask sequentially when one answer determines the next. Scope, audience, destination, and permission questions count toward the limit.
- **Each question:** One concrete point and at most one brief context sentence.
- **Selections:** Use short, parallel labels. A selection must suffice without typing: accept a bare "No" as rejection and "Unknown" as unresolved. Do not demand an explanation or ask again as free text.
- **Open questions:** Make clear that a short answer suffices and "unknown" is fine. Do not invent alternatives to fit a selection tool.
- **Neutrality:** Do not recommend factual answers. Choices cannot add claims or permissions; a negative or unknown permission answer leaves the action unauthorized.

### Waiting for answers

A displayed question is not an answered one. If an asynchronous tool returns before the user replies, the question is pending. It is neither skipped nor a reason to finish.

- While pending, do useful independent work within scope and budget, then use the host's waiting or yielding mechanism within its limits.
- Do not send a final "No files changed" or "Please select an option" while the host supports waiting. Do not repeat the question, perform filler reads, or treat a timeout or preselected option as a reply.
- After the answer, resume the pending step and carry the operation through to its deliverable. Do not restart the interview.
- If the host has only chat turns, present the questions and yield, making clear the task awaits answers. Do not invent a waiting tool or bypass host restrictions.

An explicit skip, stop-interview, or no-questions request follows the [skip rules](../SKILL.md#skipped-or-unanswered-questions). Cancellation stops work.

## Question examples

Use these only when their application context is supported; they are not a fixed interview. Ask about existing or intended rules; do not turn fact-finding into a request to adopt a protection measure (REQ-07).

- **Purpose:** "What main workflow does the application support?"
- **Permitted readers:** "Under the intended workflow, who may read uploaded customer records?" If the design names them: "The design limits access to assigned caseworkers. Is that correct?"
- **Business misuse:** "Does marking an invoice as paid trigger shipment of the order?" Use the answer to analyze the consequences of an unauthorized change, not as evidence that one is possible.
- **Availability:** "How long could order processing be unavailable before it causes serious problems?" A rough duration is enough. Propose a threshold only when project context supports it.
- **Permissions (C-06):** "Under the intended support role, may staff change customer records?"
- **Business rules (C-11):** "What approval is required before a payout?"
- **External recipients (C-03, C-07):** "Which data categories does the external analytics service receive?" Ask about an unresolved project-level data flow, not the user's provider choice.
- **Recovery (C-13):** "Can an accidentally released payment still be recalled?"
- **Detection (C-13):** "How would the team notice an unauthorized change to a payment recipient's bank details?"
- **Training application:** "The project is intended for security training and tool testing. Is that correct?" If participant separation is supported but its rules are unclear: "Under the intended exercise rules, may participants change another participant's progress?" Do not turn the training purpose into questions about the user's computer or work files.

Select follow-ups only when they could change a scenario or decision, such as affected recipients, one record versus bulk disclosure, recoverability, or a business deadline. Ask for data categories and qualitative consequences, not actual sensitive records. Retain unknown or skipped gaps with their effect on priority.
