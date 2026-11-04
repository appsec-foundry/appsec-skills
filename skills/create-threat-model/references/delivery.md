# Write, check, and hand off

Read this guide before the first write of a creation or update, before reporting a review, and before reporting an incomplete outcome.

For a review, perform the content checks below without writing, including the model guide's [review checks](model-guide.md#review-and-maintenance), and report each finding with the affected section, rationale, and proposed change.

## Write and check

1. **Re-read the write targets** immediately before editing: the model, the security document, requested exports, and an approved agent-instruction file. Reconcile intervening changes before applying a focused patch; never replace them with a stale full document. If the remaining budget cannot cover this, do not edit, and report the limitation.
2. **Check audience and content** before every write, including later decision patches: prose, diagrams, tables, source paths, link labels and URLs, appendices, and team answers against the [audience rules](audience.md). Exclude real secrets and unnecessary personal data. Check whether each source is suitable to cite, not only to read; if no safe reference exists, state the evidence limitation without inventing a link. Do not write a confidential draft as an intermediate step before sanitizing it.
3. **Write the model, then its link.** Preserve the location, naming, disclosure instructions, and valid links of an existing `SECURITY.md` or `security.md`; if several exist, use the documented entry point and ask if it remains ambiguous. Add one relative link to the model. If no security document exists, create `<repo>/SECURITY.md` with a short security heading and the link; do not invent a reporting address or disclosure policy.
4. **Review the actual diff:**

   | Check | Verify |
   | --- | --- |
   | Scope and integrity | No unrelated changes, duplicate or broken IDs, unresolved local links, unsupported claims, or accidentally retained review or acceptance status. |
   | Confidentiality | Nothing unsuitable for the audience, no real secrets, no unnecessary personal data. |
   | Coverage | Each significant objective and interaction has a scenario or an explained gap; each checklist item is clarified in the model or listed with its status. |
   | Readability | Overview and scenario decisions agree; future checks are distinct from observed results; repetition is removed while decision-relevant detail remains. |
   | Recommendations | Each names the affected component or file supported by the sources, or is marked as an operator task. |
   | Diagram | Each trust boundary in the system section appears in the diagram, or its omission is explained. |
   | Length | Simple scenarios stay near the model guide's length guide; detail moves to the appendix without dropping material facts. |

5. **Confirm the result** from the content and the diff: the target contains the intended changes and the security-document link resolves. If a write or required check failed, report the incomplete deliverable, the obstacle, the partial result, and the next action; do not claim success or start a dialogue instead. If the basis is insufficient or authorization is missing, report an incomplete outcome rather than writing a placeholder.

## Finish

Give a concise handoff in the user's language (REQ-12, REQ-19):

1. **Consequence.** The main consequence and what needs action or clarification. Unknown controls are not confirmed weaknesses; do not invent a score or release gate.
2. **Central threats.** In priority order, each scenario ID with its concrete harm and material condition, paired with the recommended change and why it helps. Include important open decisions. Do not defer supported recommendations to a later discussion.
3. **Result.** Link the file actually written, or report the review observations. State whether it was created, updated, reviewed without edits, or remains incomplete; name draft status and material coverage limits; for updates, distinguish new threats from changed assessments. State once when application behavior was not tested.
4. **Next task.** One concrete task and its expected result, such as checking a named assumption or choosing between responses.

Name a follow-up skill with a copyable example request only when its capabilities and prerequisites are known; do not discover or install one to fill the handoff. A draft, a passed format check, or an empty threat list is not team approval or proof of coverage.

After delivery, continue a dialogue the user already requested under the interview guide's [continue the dialogue](interview.md#continue-the-dialogue). Otherwise offer it once and concretely, for example: "We can work through T-003 and T-007 together, clarify their remaining assumptions, and compare suitable measures." In no-questions mode, phrase the next task as a suggestion. The offer is not permission to start a question tool, select treatments, or edit files.

### Optional agent integration

After handing off a created or updated model, offer once to reference it in the project's active agent instructions (REQ-08), in one sentence of the closing: "On request, I can add a reminder to consult the threat model to your agent instructions." Finish without waiting for a reply. Skip the offer during review or export-only work, in no-questions mode, after a decline in the current conversation, when a suitable reference already exists, or when no root `AGENTS.md` or `CLAUDE.md` exists. Do not let it replace or interrupt the dialogue offer.

Only after the user requests the integration, clarify a missing destination or approval in one question offering only existing files: "Which file should receive the reminder to consult the threat model?" with "Add to `AGENTS.md`," "Add to `CLAUDE.md`," and "Do not add it." Reuse explicit approval that already names the destination. Silence, a preselected option, or permission to create the model does not authorize this edit.

After approval, re-read the selected file under the write checks and add one short reminder with a relative link, in the file's language, preserving its other instructions:

> Before security-relevant changes, read the relevant sections of [threat-model.md](threat-model.md). Consider their assumptions, threats, and decisions, and flag any needed model updates.

Do not copy model content into the reminder, create missing instruction files, add a duplicate, or edit both files without explicit approval for both. Check the diff and link, then report which file was updated.
