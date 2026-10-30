# Write, check, and hand off

Read this guide before the first write of a creation or update, before reporting a review, and before reporting an incomplete outcome.

For review, perform the content checks below without writes, including the model guide's [review checks](model-guide.md#review-and-maintenance). Report each finding with the affected section, rationale, and proposed change. A review remains read-only and ends with observations.

## Write and check

### 1. Re-read the write targets

Edit only the selected model and security document, plus exports explicitly requested under the [export guide](otm-export.md) and an agent-instruction reference approved under [Optional agent integration](#optional-agent-integration).

Re-read write targets immediately before editing. Reconcile intervening changes before applying a focused patch; never replace them with a stale full document. If the remaining discovery budget cannot cover these checks, do not edit, and report the limitation.

### 2. Check audience and content

Before every write, including later decision patches:

- Check prose, diagrams, tables, source paths, link labels and URLs, appendices, and team answers against the [audience rules](audience.md).
- Exclude real secrets and unnecessary personal data.
- Use roles, data categories, or safe source descriptions where needed. Do not copy access tokens or confidential identifiers into references.
- Check whether each source is suitable to cite, not just to read. If no safe reference exists, state the evidence limitation without inventing a link.
- Check that the audience notice is prominent and accurate. It does not replace the content check.

Do not write a confidential draft to the repository as an intermediate step before sanitizing it.

### 3. Write the model and its link

Write the model before adding its link.

- Preserve the location, naming, disclosure instructions, and valid model links in an existing `SECURITY.md` or `security.md`.
- If several security documents exist, use the documented entry point; ask if it remains ambiguous.
- Add one relative link to the model, resolved from the security document's directory.
- If no security document exists, create `<repo>/SECURITY.md` with a short security heading and the link. Do not invent a reporting address or disclosure policy.

### 4. Review the actual diff

| Check | What to verify |
| --- | --- |
| Scope and integrity | No unrelated changes, duplicate or broken IDs, unresolved local links, unsupported claims, or accidentally retained review or acceptance status. |
| Confidentiality | No content unsuitable for the audience, real secrets, or unnecessary personal data. |
| Coverage | Each significant objective and interaction has a scenario or an explained gap. Each checklist item is clarified in the model or listed with its status. |
| Readability | Summary and scenario decisions agree. Future checks are distinct from observed results. Repetition is removed while decision-relevant detail remains. The model guide's readability check passes. |
| Recommendations | Each names the affected component or file supported by the sources, or is marked as an operator task. |
| Diagram | Each trust boundary described in the system section appears in the diagram, or its omission is explained. |
| Scenario length | Simple scenarios stay near the model guide's length guide. Detail moves to the appendix without dropping material facts. |

### 5. Confirm the result

Before claiming creation or update, confirm from the content and diff that the target contains the intended changes and that its security-document link resolves. File existence alone does not establish that an update was applied.

If a write or required check failed, report the incomplete deliverable, the obstacle, the partial result, and the next action. Do not claim success or start a decision round instead. If the basis is insufficient, authorization is missing, or preservation or audience rules prevent the write, report an incomplete outcome rather than creating an empty placeholder.

## Finish

Give a concise handoff in the user's language (REQ-07, REQ-19):

1. **Consequence:** State the main consequence and what needs action or clarification. Unknown controls are not confirmed weaknesses; do not invent a score or release gate.
2. **Central threats:** In priority order, pair each scenario ID, concrete harm, and material condition with the recommended change and why it helps. Include important open decisions without filling a quota. Do not defer supported recommendations to a later discussion.
3. **Result:** Link the file actually written or report the review observations. State whether it was created, updated, reviewed without edits, or remains incomplete. Identify draft status and material coverage limits, and distinguish new threats from changed assessments in updates. State once when application behavior was not tested. Do not repeat routine checks or source inventories.
4. **Next task:** Recommend one concrete task and its expected result, such as checking a named assumption, planning a priority measure, or choosing between responses. Tie a proposed verification to the decision it informs. Implementation and runtime checks need separate authorization.

Name a follow-up skill and a copyable example request only when its capabilities and prerequisites are known, including material installation or model-use prerequisites. Do not discover or install one to fill the handoff, and do not bundle review, implementation, and approval in one continuation.

A draft, successful format check, or empty threat list is not team approval or proof of coverage. Record only actual review participation.

Finish after delivery unless further dialogue was explicitly requested or the agent-integration question below applies.

- Make at most one optional invitation: the agent-integration question when applicable, otherwise an invitation to review the model or plan measures.
- In no-questions mode, phrase any next task as a suggestion.
- An invitation is not permission to start a question tool, select treatments, or edit files.
- If the user requested a measures discussion or treatment decisions, continue with the [decisions guide](decisions.md) after delivering any requested draft. A request to plan measures alone does not authorize recording decisions.

### Optional agent integration

After handing off a created or updated model, offer once to reference it in the project's active agent instructions (REQ-08). This never blocks delivery.

Do not offer it during review or export-only work, in no-questions mode, after a decline in the current conversation, when a suitable reference already exists, or when no existing candidate file exists. Reuse explicit approval that already identifies the destination and this change.

Candidates are existing root `AGENTS.md` and `CLAUDE.md`, or an existing instruction file the user identifies. Their presence alone does not establish which is active. If the active file is known, ask whether to add the reference there. Otherwise combine approval and destination in one question in the user's language, offering only existing files:

> Should I add a reminder to consult the threat model to your agent instructions?

- Add to `AGENTS.md`.
- Add to `CLAUDE.md`.
- Do not add it.

State that the reminder asks future agents to consult relevant model sections before security-relevant changes and to flag needed model updates. Follow the [ask-and-wait rules](interview.md#ask-and-wait). Silence, a preselected option, or permission to create the model does not authorize this edit; without an answer, leave agent instructions unchanged.

After approval, re-read the selected file under the same write checks and add one short reminder with a relative link, matching the file's language and preserving its other instructions:

> Before security-relevant changes, read the relevant sections of [threat-model.md](threat-model.md). Consider their assumptions, threats, and decisions, and flag any needed model updates.

Do not copy model content or source instructions into the reminder, authorize automatic updates or implementation, create missing instruction files, add a duplicate, or edit both files without explicit approval for both. Check the diff and link, then report which file was updated.
