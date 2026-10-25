# Create Threat Model

Create a threat model from requirements, design documents, and team knowledge. Use the same skill to update it as the design changes or review it without editing files. You can start before any code exists. The conversation and model are written primarily for developers: clear language, concrete examples from your application, and no assumed security expertise. Technical details are included when they help explain a risk or make and check a change.

## Quick start

You need a coding assistant that supports skills. Installation with the [Skills CLI](https://github.com/vercel-labs/skills/tree/v1.7.2) requires Node.js 22.20 or newer, npm, and Git.

From the project you want to model, run this command and select your assistant when prompted:

```bash
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill create-threat-model
```

This installs the skill from GitHub. To use an unpublished checkout, follow the [local installation instructions](#install-from-a-local-checkout).

Open your assistant in the target project and send:

```text
Use create-threat-model to create a threat model for this project.
Start with docs/requirements.md and docs/architecture.md.
Ask about material gaps before writing the draft.
```

Replace the paths with your own documents. If you have none yet, describe what the system does, who uses it, what data it handles, and what needs protection.

New models are written in **English by default**. To use another language, ask explicitly, for example: “Write the threat model in German.” Updates keep the existing document's language; the conversation can use your language throughout.

## What you get

The assistant writes **`threat-model.md` at the project root** and links it from `SECURITY.md` or `security.md`, creating a short `SECURITY.md` if needed. The model contains:

- The main concerns and prioritized next steps.
- A system summary and diagram showing interactions and trust boundaries.
- Threat scenarios explaining what could go wrong, the harm, recommended changes, and how to check them.
- Open decisions, assumptions, and source references, with detailed coverage in an appendix.

Before detailed scenario analysis, the assistant asks you to confirm or correct the business purpose, relevant data sensitivity, and plausible worst-case consequences. It proposes context from the sources and reuses answers you have already given for the same scope. Audience or deployment questions do not replace this step; clarification may take another short round of at most three questions. You can skip questions or request work without questions; unconfirmed context stays explicit. Updates revisit only affected context.

The first model is a draft for the team to review. It separates proposed measures from implemented or verified controls and explains what remains unknown. Each scenario has a stable ID, such as `T-003`, for use in tickets and pull requests. You can edit the document in any Markdown editor.

| Request | Result |
| --- | --- |
| Create | Writes an initial model. Preserves an existing one and offers an update. |
| Update | Revises affected sections, preserving unrelated content, manual additions, and scenario IDs. |
| Review | Reports gaps and suggestions in the conversation without changing files or review status. |

Modeling does not change application code, create tickets, commit files, or publish the model.

## Common requests

**Create without questions**

```text
Use create-threat-model to create a threat model from docs/design.md.
Do not ask questions; record assumptions and unresolved decisions in the draft.
```

**Update for a feature**

```text
Use create-threat-model to update threat-model.md for the sharing feature
in docs/sharing.md. Preserve unrelated content and existing scenario IDs.
```

**Include the code of an existing application**

```text
Use create-threat-model to create a threat model for this service.
Start with docs/requirements.md and include architecture reading of the code.
```

Architecture reading identifies components, entry points, data stores, external connections, and authentication paths. It records differences between the code and the intended design. Without your opt-in, code reading stays limited to specific structural questions; the assistant offers broader reading when the documents leave those questions open. This is not a code vulnerability scan.

**Review an existing model**

```text
Use create-threat-model to review threat-model.md against docs/design.md.
Report gaps and proposed changes without editing files.
```

**Discuss open decisions and record the results**

```text
Use create-threat-model to guide me through the open decisions in threat-model.md.
Update the model with the decisions I explicitly make.
```

**Record decisions later**

```text
Use create-threat-model to update threat-model.md with our decisions:
T-001 plan the proposed response, owner Finance Platform team, target 2026-12-15.
```

Replace the example ID, owner, and date with your team's decision.

## What to expect

The assistant starts with the installed skill's name and version and reads the available sources. Before the interview, it gives a short summary in your language: one sentence about who uses the system and why, a small diagram, then the important unknowns and source basis. The diagram uses clearly named boxes and aligned arrows, readable directly in the console. Optional connections appear on a separate labeled branch; technology names appear only where helpful. Planned features are not presented as already implemented. If there is not enough information for a sketch, it explains what is known and missing. You do not need to read diagram syntax or know security terminology to understand the summary.

The dialogue uses your language and normally asks one short question at a time, with concrete answer choices where helpful. When your assistant supports an interactive question interface in the current mode, the skill uses it; otherwise, it asks in chat. It may group up to three simple, independent questions. It briefly names the remaining topics, uses the sources and your previous answers, and asks only about gaps that matter or confirmations it still needs. It clarifies relevant operating facts before proposing consequences that depend on them. Disabled features do not trigger a questionnaire about their configuration. You can correct any proposed answer in your own words.

The assistant uses a checklist internally to keep the dialogue focused; you do not have to answer every checklist item. Questions about consequences concern what people could lose or be unable to do. You are not expected to determine whether an attack would succeed, and asking the assistant to examine a concern does not confirm that it is an actual weakness.

You can answer “unknown,” skip questions, or stop the dialogue. Missing information stays visible in the draft. If there is too little context to describe a concrete system, the assistant explains what is missing instead of producing generic threats.

Source reading has fixed limits on files, text, tool calls, and exploration time. Larger projects may be only partly examined, even with architecture reading enabled. Name the service or feature you want to focus on; the model records important coverage gaps. The exact limits are in the [assistant workflow](SKILL.md#execution-boundaries).

After creating or updating the model, the assistant summarizes the central threats and next steps. Updates distinguish new threats from changed assessments of existing ones. Where useful, it suggests a follow-up skill and an example request, with any prerequisites.

The assistant offers an optional review or decision round after delivery. A discussion of risk decisions starts only when you request it. You can plan a response, accept a risk, or clarify a missing fact first. Acceptance requires an explicit decision by a responsible person, with a rationale and review date or trigger. To save decisions in the model, include an update request; a review stays read-only.

## Internal or public models

When the model's intended readers are not yet established, the first interview question asks whether it is for internal or public use. You can also choose "Not decided yet." This applies to updates and reviews too when the existing model leaves its audience open. Local operation or made-up exercise data does not answer who should read the document. You can specify this in the initial prompt:

```text
Create a public threat model using only information suitable for publication.
```

Internal models can include confidential security findings only when the repository's readers are authorized to receive them. If that is unclear, the assistant asks before writing those details. Public models omit confidential details while explaining the risks and needed responses. Neither includes real secrets or unnecessary personal data.

If you skip the audience question or request no questions, a new model is provisionally marked internal, with the uncertainty recorded and confidential details affected by it omitted. That provisional label does not settle the audience for future updates. When your request, project guidance, or an existing model already establishes the audience, the assistant briefly states that choice and its basis instead of asking again. Updates retain the established audience unless circumstances change.

The model carries a visible audience notice. That notice does not restrict access or approve publication, and the assistant's content checks are not a guarantee that every sensitive detail will be detected. See the [notice templates and examples](references/model-guide.md#audience-notice).

## Use the model during development

Use the recommendations to plan changes to requirements, design, or implementation. Each explains what to change, why it addresses the threat, and how to check the result. Applying those changes is a separate task.

For example, consider [T-003: changing a payment destination after approval](references/model-guide.md#t-003-payment-details-can-change-after-approval):

1. The design lets suppliers edit approved payment requests but does not say whether a recipient change cancels approval.
2. The assistant asks what should happen. The team answers: “A recipient change must require renewed approval. We do not know whether the implementation does that.”
3. The model records the intended rule and recommends binding approval to the reviewed payment details. It proposes checks for normal payments, changed recipients, and concurrent editing and settlement. The current implementation remains unverified.
4. The team requests an update recording its decision to implement the response, with an owner and target date. Developers reference T-003 in their work.
5. After implementation, a focused update records supplied test results and what they actually demonstrate. A later bulk-edit feature prompts another review of T-003 because it may introduce a new path around the same rule.

If the team cannot answer the question in step 2, the model leaves the approval rule open and identifies clarification as the next step. It does not conclude that the application is vulnerable just because information is missing.

To incorporate evidence later:

```text
Use create-threat-model to update T-003 using docs/payment-change.md
and docs/payment-test-results.md. Record the evidence and remaining gaps,
preserving unrelated scenarios and decisions.
```

Use your actual source paths. Test results support the conditions they checked; a link to test code or a merged pull request alone does not establish that a control works.

## Adapt the checklist

The skill uses a [modeling checklist](references/checklist.md) to find missing context, such as actors, trust boundaries, and personal data. It records open, inapplicable, and unexamined items without turning every item into a question.

To add project-specific items or exclusions, create `threat-model-checklist.md` at the project root:

```markdown
# Threat model checklist

## Additional items

| ID | Aspect | Clarified when the model states |
| --- | --- | --- |
| P-01 | Payment provider | Which payment data reaches the provider and how refunds are authorized. |

## Not applicable

| ID | Reason |
| --- | --- |
| C-10 | The service processes no personal data. |
```

Use unique `P-` IDs for additions and give a reason for exclusions. If the project sources contradict an exclusion, the item stays open. “Clarified” means the information is available, not that a control has been tested. The project file supplements the defaults and survives skill updates.

## Add project abuse patterns

The skill also checks [reusable abuse patterns](references/abuse-cases.md), such as bypassing approvals, repeating one-time actions, or accessing another user's data. It assesses each pattern against your system and existing controls; a pattern is not automatically a finding.

Add your own patterns in `threat-model-abuse-cases.md` at the project root. For example:

```markdown
# Project abuse patterns

## Additions

### PAC-01 — Split requests to bypass an approval threshold

- Applies when: Approval limits apply to an employee's total requested amount.
- Abuse and harm: An employee splits one purchase into smaller requests to avoid approval and spend beyond their authority.
- Project basis: Payment policy requires approval of the total purchase, including related requests.
- Examine: How related requests are identified and how the aggregate limit is enforced.
```

Replace the example rule with your actual project policy. Use stable `PAC-` IDs for additions. You can also refine a default pattern by its `AC-` ID or exclude one with a supported reason; see the [customization format](references/abuse-cases.md#project-customizations). These project files guide analysis without changing the skill's permissions and remain intact across skill updates.

After changing the patterns, request a focused update:

```text
Use create-threat-model to update threat-model.md against the revised
threat-model-abuse-cases.md. Reassess affected scenarios and preserve
unrelated content, existing IDs, and decisions.
```

You can also supply organization guidance or known threats as Markdown or plain-text documents. Name them in your request; the skill records their sources and applicability. See [supported security context](references/security-context.md).

## Install from a local checkout

From the target project, replace `/path/to/appsec-skills` with the absolute path to your checkout:

```bash
npx skills@1.7.2 add /path/to/appsec-skills --skill create-threat-model
```

For manual installation, copy the entire `create-threat-model` directory, including `references/`, into your assistant's skill location. The entry point is [SKILL.md](SKILL.md).

To work on the skill itself, see the repository's [development guide](../../DEVELOPMENT.md). It covers installing a separate dev snapshot and trying a fictional project. Those commands require the full repository checkout; they are not part of the installed skill directory.

## Further reading

- [Model structure and scenario example](references/model-guide.md)
- [Assistant workflow](SKILL.md)
- [Requirements for developing this skill](requirements.md)
- [All AppSec Skills](../../README.md)
