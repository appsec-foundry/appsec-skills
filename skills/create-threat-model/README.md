# Create Threat Model

Create a threat model from requirements, design documents, and team knowledge. Use the same skill to update it as the design changes or review it without editing files. Source code is optional.

The model connects security objectives, system interactions, threat scenarios, controls, and remaining risks. It is a Markdown document the team can review and maintain alongside the project.

New models are written in **English by default**, even when the conversation or source documents use another language. Explicitly request another document language if needed. Updates preserve the existing model's language unless you request a translation; questions and conversation can remain in your language.

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

Each invocation starts by showing the installed skill's name and version, for example `create-threat-model · Version 0.1.0`. This applies to creation, updates, and reviews, including requests without questions. The version comes from `metadata.version` in the installed [SKILL.md](SKILL.md); it identifies the skill, separately from the Skills CLI version in the installation command.

The assistant briefly explains the scope and next steps, then reads the available sources. It shares a working system summary and compact diagram when enough context exists, so you can correct misunderstandings early. A focused update concentrates on the affected flows and boundaries.

Questions target gaps whose answers could change system understanding, a relevant threat, its priority, or a response. Each explains why the missing information matters. Some arise during the initial reading; others emerge while examining scenarios. You can answer "unknown," skip questions, or stop the dialogue. Unresolved points stay visible with a next clarification step where possible; you do not need to complete a questionnaire before receiving a supported draft.

After delivering the draft or update, the assistant summarizes important open decisions and briefly offers an optional review or decision round. It finishes without asking you to respond. Follow-up questions start only when you explicitly request that dialogue, either in your original request or afterward. Factual questions during modeling remain part of the workflow above.

## Internal or public models

New models are **internal by default**. Request a public model explicitly, for example: "Create a public threat model using only information suitable for publication." Existing audience settings and project guidance are respected. The assistant asks only when conflicting audience information or an unclear reader group affects which details may be included, within the usual question limit.

Internal models can describe confidential open security issues, missing controls, attack prerequisites, and architecture details needed to address risks. Those details must be suitable for the repository's readers; a private repository or an "internal" heading alone is not sufficient. Public models exclude confidential details while retaining a useful explanation of the risks and required responses.

Each model has a prominent English notice immediately below its title: **INTERNAL — NOT FOR PUBLIC DISTRIBUTION** or **PUBLIC USE INTENDED — NOT A PUBLICATION APPROVAL**. Internal models identify the intended readers when known. If the readers or repository access are unresolved, the notice explicitly states **AUDIENCE OR REPOSITORY ACCESS UNCONFIRMED — CONFIDENTIAL DETAILS OMITTED**, and the affected details are left out. The [notice templates](references/model-guide.md#audience-notice) keep this distinction separate from draft/review status; a notice does not provide access control or authorize publication.

Before first writing confidential findings, the assistant checks whether the repository is suitable using available project context and asks once if that remains unclear. It does not first save a confidential draft and then sanitize it.

Neither version includes real secrets or unnecessary personal data. Before each write, the assistant checks the content, including diagrams, source links, appendices, and later decisions. If the destination is unsuitable for confidential details, it withholds them and explains the limitation. An unanswered clarification or a request without questions retains the internal default or established audience; unresolved access or disclosure questions remain visible and the affected confidential details are omitted. Updates retain the existing audience unless circumstances change; the skill does not silently convert a model's audience.

These are assistant workflow checks, not an automated guarantee that every sensitive detail will be detected. The [audience example](references/model-guide.md#audience-example) shows how the same issue can be documented for different readers.

## What you get

- `threat-model.md` at the target repository root: a short opening with the main concerns and next actions, a system summary with a diagram, and concise threat scenarios explaining recommended changes, checks, and decisions. The overview highlights the most important actions rather than listing every scenario. Sources and detailed checklist coverage follow in an appendix in the same document; uncertainty affecting a decision stays beside the relevant scenario.
- A relative link from the existing `SECURITY.md` or `security.md`. If neither exists, the skill creates a short `SECURITY.md` containing the link.

The result starts as a draft. It distinguishes current exposure from expected residual risk after effective treatment. Proposed controls and unresolved assumptions stay visible; they are not recorded as verified controls or accepted risks. The overview reflects recorded decisions, including agreed clarification steps whose outcomes are still pending. Future checks, actual results, and decisions are clearly separated, and shared limitations are stated once. Scenarios that depend on an explicitly excluded use are kept brief, with a reason to revisit them if the scope changes. The skill does not commit or publish the files.

Scenarios link directly to the relevant requirements, design sections, or available evidence using readable link names. These references let you check the reasoning without decoding IDs or searching the appendix. Existing rules, proposed changes, and evidence that a control works remain distinct. Missing sources are marked as gaps or assumptions; a document link alone is not proof that a control works.

If you request a decision round, the skill asks about the most important open scenarios, at most three at a time: plan a response, accept the risk, or clarify first. The options name the scenario's concrete response, exposure, and missing information. For updates, questions stay with affected scenarios and use decisions you already supplied; a decision is revisited only when its assumptions change. If no decisions remain open in scope, there is no decision round. With an update request, the skill records explicit decisions and the details you supply in the model; during a review or discussion, it returns proposed changes in the conversation. Planning does not implement the measure or create tickets. Missing details and unanswered decisions stay open. Risk acceptance requires an explicit decision by a responsible person, with rationale and a review date or trigger. You can leave remaining decisions for a later update.

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

**Start a decision round and record the results**

```text
Use create-threat-model to guide me through the open decisions in threat-model.md.
Update the model with the decisions I explicitly make.
```

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

The model recommends concrete improvements to requirements, design, or implementation where a scenario needs treatment. Each recommendation explains what to change, where, why it addresses the threat, and how to check its effectiveness. It uses the relevant levels rather than filling every level for every scenario. Where alternatives matter, it recommends a preferred option and explains material trade-offs. These proposals help the team decide what to improve; applying them to requirements, design documents, or code is a separate task.

Before implementing a feature, model its design and use the scenarios' verification criteria to plan the work. Reference the stable scenario IDs in your existing tickets and pull requests. After implementation, request a focused model update using the actual change and test evidence. A merged pull request does not by itself establish that a control works. When a later feature changes the underlying assumptions, revisit the affected scenarios and decisions.

You can read and extend `threat-model.md` directly in any Markdown editor; no assistant or generator is needed. Add explanations, recommendations, decisions, evidence, or open questions under the relevant scenario heading. For a new scenario, use a descriptive heading and an unused scenario ID, keeping existing IDs stable. The document should make sense without the chat history, and later skill updates preserve manual additions while revisiting content affected by the requested change.

For example, the following fictional workflow continues [scenario T-003](references/model-guide.md#t-003-an-approval-survives-a-change-to-the-payment-destination):

1. **Design input:** Suppliers may correct payment requests after approval. The design does not say whether changing the recipient invalidates approval.
2. **Targeted question:** "The design allows post-approval corrections but leaves approval validity open. If approval survives a recipient change, settlement could pay an unreviewed recipient. What should happen to approval when the recipient changes?"
3. **Team answer:** "A recipient change must require renewed approval. We do not know whether the current implementation does that."
4. **Model result:** Record the answer as the intended rule and recommend making it explicit in the payment-edit requirements. For the design, recommend binding approval to the reviewed payment details; for implementation, identify the need to preserve that binding during concurrent editing and settlement. The [scenario example](references/model-guide.md#t-003-an-approval-survives-a-change-to-the-payment-destination) shows concrete recommendations, verification criteria, and an alternative. Keep the current implementation and exposure unresolved; the answer does not verify a control. The next check is whether an edited request can settle under its previous approval.
5. **Optional treatment decision:** After delivery, the team requests a decision round and an update to the model. It explicitly plans that response, assigns the Payments team, and gives a target of 2026-12-15. The control becomes planned. No risk acceptance or implementation is implied.
6. **Development and evidence:** Developers reference T-003 in their PR and implement and test the response in a separate task. A later update links the supplied test results from T-003 and records the checked revision and conditions. Evidence that an unchanged authorized request settles and a changed recipient requires reapproval supports those checked conditions; concurrent editing and settlement remain unverified until corresponding evidence is supplied. Linking test code alone does not establish that these checks passed.
7. **Later change:** A bulk-edit feature can affect the same approval rule. Update T-003 and its affected flows, retaining its ID and unrelated scenarios, and reassess whether the earlier evidence covers the new path.

At step 4, the action overview could contain:

| Scenario | Priority and reason | Response / decision | Owner | Next check |
| --- | --- | --- | --- | --- |
| [T-003](references/model-guide.md#t-003-an-approval-survives-a-change-to-the-payment-destination) | High if edits reach settlement without reapproval; payment diversion | Proposed: invalidate approval after a recipient change | Open | Check whether an edited request can settle under its old approval |

If the team instead answers "unknown" to the design question, keep both the intended approval rule after an edit and the scenario's applicability unresolved. The permission to edit is already established by the requirements. Record clarifying the approval rule with the payment-process owner as a next step, leaving that owner unidentified if necessary. Do not infer that the existing system is vulnerable or repeat the same question without new context.

To incorporate evidence later, replace these illustrative paths with your actual sources:

```text
Use create-threat-model to update T-003 using docs/payment-change.md
and docs/payment-test-results.md. Record the evidence and remaining gaps,
preserving unrelated scenarios and decisions.
```

## Adapt the checklist

Before asking questions, the skill checks the sources against a short [checklist](references/checklist.md) of aspects such as scope, actors, trust boundaries, and personal data. Material open items inform questions; the checklist is not a mandatory interview. Items that remain open, do not apply, or were not examined are listed in the model's open questions or coverage appendix. "Clarified" means the information is described with a source or attributed answer, not that a control has been tested. Missing facts and missing verification evidence are recorded separately.

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

## Maintain abuse patterns

The skill checks a small [default collection of abuse patterns](references/abuse-cases.md) against the described system: acting on another owner's resources, misusing delegated privileges, bypassing workflow steps, replaying actions, racing for shared state, changing approved data, repurposing services, exhausting resources, exposing retained data, and steering model-driven actions. Patterns are analysis prompts, not automatic findings or questions. The skill considers existing controls, merges overlapping scenarios, and records material uncertainty. It does not treat the list as complete coverage or copy the entire catalog into the model.

Teams can maintain project-specific additions, refinements, and exclusions in **`threat-model-abuse-cases.md` at the project root**. Use normal Markdown and review changes like other project documentation. The file supplements the defaults and stays separate from the installed skill, so updating the skill preserves your project changes. It is optional; no catalog setup is required to create a model.

For example, a payment project could use the following entries. Replace the illustrative business rules with your own confirmed rules and sources:

```markdown
# Project abuse patterns

## Additions

### PAC-01 — Split requests to bypass an approval threshold

- Applies when: Approval limits apply to an employee's total requested amount.
- Abuse and harm: An employee splits one purchase into smaller requests to avoid approval and spend beyond their authority.
- Project basis: Payment policy requires approval of the total purchase, including related requests.
- Examine: How related requests are identified and how the aggregate limit is enforced.

## Refinements

### AC-06 — Change payment details after approval

- Project basis: Suppliers may edit the recipient after submitting a payment request.
- Project variant: Check both individual edits and bulk imports that change the recipient before settlement.
- Open fact: Whether either edit path invalidates the existing approval.

## Exclusions

| ID | Reason and supporting context |
| --- | --- |
| AC-10 | This service has no language-model feature; the current design describes deterministic request processing only. |
```

Use stable `PAC-` IDs for new project patterns. To improve a default for your project, reference its `AC-` ID and add the relevant facts or variants; the original mechanism remains available. Keep IDs when wording improves, and merge duplicates through scenario references rather than renumbering existing threats. You can improve the shared defaults by proposing edits to the skill's `references/abuse-cases.md`; project-only details belong in the project file.

An exclusion needs a reason supported by the project context. If the design contradicts it, applicability remains unresolved; a claimed mitigation does not make a mechanism inapplicable. Missing facts stay distinct from evidence that a control works. Malformed entries are reported, and unclear entries cannot silently replace defaults. A removed entry does not erase an existing supported threat or its decisions.

The modeling workflow reads this file without changing it. After maintaining it, request a focused update, for example:

```text
Use create-threat-model to update threat-model.md against the revised
threat-model-abuse-cases.md. Reassess affected scenarios and preserve
unrelated content, existing IDs, and decisions.
```

You can instead request a read-only review. Catalog entries do not authorize commands, external access, extra questions, or changes to other files. A reference to a source does not itself grant access to it. Existing question limits and the optional post-delivery decision round still apply.

## Further reading

- [Requirements for developing this skill](requirements.md)
- [Assistant instructions](SKILL.md)
- [Model structure and scenario example](references/model-guide.md)
- [Modeling checklist](references/checklist.md)
- [Reusable abuse patterns and customization rules](references/abuse-cases.md)
- [Using selected organization guidance and known threats](references/security-context.md)
- [All AppSec Skills](../../README.md)
