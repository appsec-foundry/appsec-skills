# Create Threat Model

Create a threat model from requirements, design documents, and team knowledge. Use the same skill to update it as the design changes or review it without editing files. Source code is optional.

The model connects security objectives, system interactions, threat scenarios, controls, and remaining risks. It is a Markdown document the team can review and maintain alongside the project.

## Quick start

You need a coding assistant that supports skills. For the [Skills CLI](https://github.com/vercel-labs/skills/tree/v1.7.2) installation, use Node.js 22.20 or newer, npm, and Git.

Run this from the project you want to model, then select your assistant when prompted:

```bash
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill create-threat-model
```

This requires the skill to be published on GitHub. For an unpublished checkout, use the local command below. The CLI version is pinned so the installation example uses a specific release.

Open your assistant in the target project and send:

```text
Use create-threat-model to create a threat model for this project.
Start with docs/requirements.md and docs/architecture.md.
Ask about material gaps before writing the draft.
```

Replace those paths with your own requirements, specifications, ADRs, or design documents. If you have no documents yet, describe the system's purpose, valuable data or operations, users, and main interactions in the prompt.

The `npx` command installs the skill. The assistant performs the modeling and may ask up to three contextual questions per round.

### Install from a local checkout

From the target project, replace `/path/to/appsec-skills` with the absolute path to your checkout:

```bash
npx skills@1.7.2 add /path/to/appsec-skills --skill create-threat-model
```

For manual installation, copy this entire `create-threat-model` directory, including `references/`, into your assistant's skill location. The assistant entry point is [SKILL.md](SKILL.md).

## What the conversation looks like

The assistant briefly explains the scope and next steps, then reads the available sources. It shares a working system summary and compact diagram when enough context exists, so you can correct misunderstandings early. A focused update concentrates on the affected flows and boundaries.

Questions target gaps whose answers could change system understanding, a relevant threat, its priority, or a response. Each explains why the missing information matters. Some arise during the initial reading; others emerge while examining scenarios. You can answer "unknown," skip questions, or stop the dialogue. Unresolved points stay visible with a next clarification step where possible; you do not need to complete a questionnaire before receiving a supported draft.

After the draft, the conversation switches from factual clarification to treatment decisions. Reviews and requests without questions list open decisions instead.

## What you get

- `threat-model.md` at the target repository root: scope, a compact action overview near the start, sources, assets, actors, system flows and trust boundaries, threat scenarios, treatments, verification criteria, and open questions. The overview links important scenarios to their priority rationale, proposed or decided response, known owner, and next check.
- A relative link from the existing `SECURITY.md` or `security.md`. If neither exists, the skill creates a short `SECURITY.md` containing the link.

The result starts as a draft. It distinguishes current exposure from expected residual risk after effective treatment. Proposed controls and unresolved assumptions stay visible; they are not recorded as verified controls or accepted risks. The skill does not commit or publish the files.

After writing, the skill asks for decisions on the most important open scenarios, at most three at a time: plan a response, accept the risk, or clarify first. Planning records the decision; it does not implement the measure or create tickets. It records only explicit answers and the details you supply; missing details and unanswered decisions stay open. Risk acceptance requires an explicit decision by a responsible person, with rationale and a review date or trigger. You can leave remaining decisions for a later update.

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

The skill derives components, entry points, data stores, external connections, and authentication paths from code and configuration. Without this request, it offers architecture reading when the documents leave such points open and reads more code only after you agree. It shows where the code differs from the documents; it does not scan for vulnerabilities.

**Record decisions later**

```text
Use create-threat-model to update threat-model.md with our decisions:
T-001 plan the proposed response, owner Finance Platform team, target 2026-12-15.
```

**Review an existing model**

```text
Use create-threat-model to review threat-model.md against docs/design.md.
Report gaps and proposed changes without editing files.
```

A creation request never replaces an existing model. Updates integrate features into that model; reviews leave the model and security document unchanged. If there is too little context to model a concrete system, the skill explains what is missing.

## Use the model during development

Before implementing a feature, model its design and use the scenarios' verification criteria to plan the work. Reference the stable scenario IDs in your existing tickets and pull requests. After implementation, request a focused model update using the actual change and test evidence. A merged pull request does not by itself establish that a control works. When a later feature changes the underlying assumptions, revisit the affected scenarios and decisions.

For example, the following fictional workflow continues [scenario T-003](references/model-guide.md#t-003-an-approval-survives-a-change-to-the-payment-destination):

1. **Design input:** Suppliers may correct payment requests after approval. The design does not say whether changing the recipient invalidates approval.
2. **Targeted question:** "The design allows post-approval corrections but leaves approval validity open. If approval survives a recipient change, settlement could pay an unreviewed recipient. What should happen to approval when the recipient changes?"
3. **Team answer:** "A recipient change must require renewed approval. We do not know whether the current implementation does that."
4. **Model result:** Record the answer as the intended rule. Keep the current implementation and exposure unresolved; the answer does not verify a control. T-003 proposes binding approval to the reviewed payment details. Its next check is whether an edited request can settle under its previous approval.
5. **Treatment decision:** The team explicitly plans that response, assigns the Payments team, and gives a target of 2026-12-15. The control becomes planned. No risk acceptance or implementation is implied.
6. **Development and evidence:** Developers reference T-003 in their PR and implement and test the response in a separate task. A later update incorporates the supplied revision and test results. Evidence that an unchanged authorized request settles and a changed recipient requires reapproval supports those checked conditions; concurrent editing and settlement remain unverified until corresponding evidence is supplied.
7. **Later change:** A bulk-edit feature can affect the same approval rule. Update T-003 and its affected flows, retaining its ID and unrelated scenarios, and reassess whether the earlier evidence covers the new path.

At step 4, the action overview could contain:

| Scenario | Priority and reason | Response / decision | Owner | Next check |
| --- | --- | --- | --- | --- |
| [T-003](references/model-guide.md#t-003-an-approval-survives-a-change-to-the-payment-destination) | High if edits reach settlement without reapproval; payment diversion | Proposed: invalidate approval after a recipient change | Open | Check whether an edited request can settle under its old approval |

If the team instead answers "unknown" to the design question, keep both the intended edit rule and the scenario's applicability unresolved. Record clarifying the rule with the payment-process owner as a next step, leaving that owner unidentified if necessary. Do not infer that the existing system is vulnerable or repeat the same question without new context.

To incorporate evidence later, replace these illustrative paths with your actual sources:

```text
Use create-threat-model to update T-003 using docs/payment-change.md
and docs/payment-test-results.md. Record the evidence and remaining gaps,
preserving unrelated scenarios and decisions.
```

## Adapt the checklist

Before asking questions, the skill checks the sources against a short [checklist](references/checklist.md) of aspects such as scope, actors, trust boundaries, and personal data. Material open items inform questions; the checklist is not a mandatory interview. Items that remain open, do not apply, or were not examined are listed in the model's open questions.

To adapt the checklist for your project, add `threat-model-checklist.md` at the repository root. It contains only your changes; the skill applies them to the default list, so later skill updates still reach your project.

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

Use `P-` IDs for your own items and keep them unique. A not-applicable entry needs a reason; if the sources contradict it, the item stays open. The file only adjusts what is checked. It cannot change the skill's permissions, question limit, or where it writes.

## Further reading

- [Requirements for developing this skill](requirements.md)
- [Assistant instructions](SKILL.md)
- [Model structure and scenario example](references/model-guide.md)
- [Modeling checklist](references/checklist.md)
- [Using selected organization guidance and known threats](references/security-context.md)
- [All AppSec Skills](../../README.md)
