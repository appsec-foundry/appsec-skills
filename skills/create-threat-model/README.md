# Create Threat Model

Create a threat model from requirements, design documents, and team knowledge, even before code exists. The model describes what could go wrong, what harm it could cause, and what to change. No security expertise is required.

This skill also supports reviews, updates, and discussions of protective measures. For an existing model, [update-threat-model](../update-threat-model/README.md) provides a shortcut to the same update workflow; it requires this skill to be installed.

## Quick start

Use a coding assistant that supports skills. Installation with the [Skills CLI](https://github.com/vercel-labs/skills/tree/v1.7.2) needs Node.js 22.20+, npm, and Git.

From your project, run the command and select your assistant when prompted:

```bash
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill create-threat-model
```

For an unpublished checkout, see [local installation](#install-from-a-local-checkout).

Then ask your assistant:

```text
Use create-threat-model to create a threat model for this project.
Start with docs/requirements.md and docs/architecture.md.
```

Replace the paths with your documents. Without documents, describe what the system does, who uses it, what data it handles, and what needs protection.

New models use **English** unless you request another language. Updates keep the model's language; the conversation can use yours.

## What you get

The assistant writes **`threat-model.md` at the project root** and links it from `SECURITY.md` or `security.md`, creating that file if needed. The draft contains:

- A system overview and diagram, using Mermaid by default.
- Threat scenarios: who could do what, under which conditions, and with what harm.
- Existing controls, recommended changes, priorities, and checks.
- Open decisions, source references, and important gaps in the evidence.

Scenarios have stable IDs such as `T-003` for tickets and pull requests. You can edit the model in any Markdown editor. Proposed controls remain distinct from implemented or verified ones. The closing summary highlights the main threats and recommended next steps.

A shortened example from a fictional payment system:

> **T-003 — Payment details can change after approval**
>
> **Threat:** A supplier could change the recipient after approval and redirect the money if the original approval remains valid. Whether edits cancel approval is unknown.
>
> **Recommended change:** Require approval again when the amount or recipient changes.
>
> **Proposed check:** An unchanged approved payment succeeds; changing its recipient blocks payment until renewed approval. These checks have not run.

See the [full scenario and its evidence](references/model-guide.md#t-003-payment-details-can-change-after-approval). Priorities reflect possible harm and the conditions needed for an attack; missing information stays visible.

After delivery, the assistant may offer to add a reminder to consult the model in an existing `AGENTS.md` or `CLAUDE.md`. It edits that file only with your explicit approval. See [optional agent integration](SKILL.md#optional-agent-integration) for details.

| Request | Result |
| --- | --- |
| Create | Writes an initial model; preserves an existing one and offers an update. |
| Update | Revises affected sections while preserving unrelated content, manual edits, and IDs. |
| Review | Reports gaps and suggestions without changing files or review status. |
| Discuss measures | Explains options and recommends changes without editing files. |
| Export | Creates an OTM JSON or YAML copy on request; Markdown remains the main document. |

Modeling does not change application code, create tickets, commit files, or publish the model.

## How it works

1. **Read and summarize.** The assistant reads requirements, design documents, and other supplied sources, then sketches the system and its main data flows. It can read selected code to answer specific architecture questions.
2. **Clarify the context.** It asks about important gaps, who may read the model, and the system's purpose, sensitive data, and possible harm. You can correct its understanding in short rounds of up to three questions.
3. **Identify threats.** It examines how actors could misuse the system's operations or cross permission boundaries, taking existing protections into account. Each scenario is tied to a source or an explicit assumption.
4. **Recommend changes.** It prioritizes scenarios by possible harm and attack conditions, proposes measures, and describes how to check them. Proposed measures stay distinct from agreed decisions and verified controls.
5. **Write and check.** It writes `threat-model.md`, checks the document and its security-document link, and summarizes the main threats, open decisions, and next steps.

You can answer “unknown,” skip questions, or request no questions. Unconfirmed assumptions stay visible. If there is too little context to describe a concrete system, the assistant explains what is missing.

The model covers the application and its supported configurations, including optional features. To assess a particular installation, request that scope explicitly. Later, use [update-threat-model](../update-threat-model/README.md) to revise the affected parts when requirements, design, or control evidence changes.

### When code is available

The assistant can read selected code and configuration to resolve specific architecture questions. It also offers broader architecture reading once, even when documentation is sufficient. **Broader reading requires your opt-in**, which you can include in the initial request.

That reading identifies components, entry points, data stores, external connections, authentication and authorization paths, and deployment configuration. Code observations support the model; conflicts with requirements remain visible. This is not a code vulnerability scan, and the assistant does not run the application or tests.

Reading has [fixed limits](SKILL.md#discovery-budget), so large projects may be only partly examined. Name the service or feature to focus on; the model records coverage gaps.

## Common requests

**Create without existing documents**

```text
Use create-threat-model for a service where suppliers submit invoices
and finance staff approve payments. It stores invoices and bank details
and sends approved payments to a payment provider.
Ask me about missing details before writing the model.
```

**Create without questions**

```text
Use create-threat-model to create a threat model from docs/design.md.
Do not ask questions; record assumptions and unresolved decisions in the draft.
```

**Update for a feature**

```text
Use create-threat-model to update threat-model.md for the sharing feature
in docs/sharing.md.
```

**Include architecture reading from code**

```text
Use create-threat-model to create a threat model for this service.
Start with docs/requirements.md. Read the code and configuration too
to understand the architecture and permission checks.
```

**Review an existing model**

```text
Use create-threat-model to review threat-model.md against docs/design.md.
Report gaps and proposed changes without editing files.
```

**Discuss measures and record decisions**

```text
Use create-threat-model to work through practical measures for T-001 and T-002.
Explain the options and trade-offs and recommend where to start.
Update the model with the decisions I explicitly make.
```

Use your actual scenario IDs. Include an update request to save decisions; discussion alone does not edit the model. Accepting a risk requires an explicit decision by a responsible person, with a rationale and review date or trigger.

## Internal or public models

If the intended audience is unknown, the assistant asks whether the model is internal, public, or undecided. You can specify it in the request:

```text
Create a public threat model using only information suitable for publication.
```

Internal models may include confidential findings only when the repository's readers may receive them. Public models omit confidential details. Neither includes real secrets or unnecessary personal data.

If you skip the audience question, a new model is provisionally marked internal. Disclosure questions remain recorded as unresolved; affected confidential details are omitted. The audience notice does not restrict file access or authorize publication. See the [audience notices](references/model-guide.md#audience-notice).

## Use the model during development

After implementing a measure, supply evidence for a focused update. For the payment example above:

```text
Use update-threat-model to reassess T-003 using docs/payment-change.md
and docs/payment-test-results.md.
```

This example requires [both skills to be installed](../update-threat-model/README.md#install). You can also make the same request with `create-threat-model` alone.

A link to test code or a merged PR alone does not establish that a control works.

## Adapt the checklist

The [modeling checklist](references/checklist.md) helps find missing context. Add project-specific items or exclusions in `threat-model-checklist.md` at the project root:

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

Use unique `P-` IDs for additions and reasons for exclusions. Contradicted exclusions stay open. “Clarified” means the information is available, not that a control has been tested. Project files survive skill updates.

## Add project abuse patterns

The skill checks [reusable abuse patterns](references/abuse-cases.md), such as bypassing approvals or repeating one-time actions, against your system and its controls.

Add project patterns in `threat-model-abuse-cases.md` at the project root:

```markdown
# Project abuse patterns

## Additions

### PAC-01 — Split requests to bypass an approval threshold

- Applies when: Approval limits apply to an employee's total requested amount.
- Abuse and harm: An employee splits one purchase to avoid approval and spend beyond their authority.
- Project basis: Payment policy requires approval of the total purchase, including related requests.
- Examine: How related requests are identified and the aggregate limit is enforced.
```

Use your actual policy and stable `PAC-` IDs. To refine or exclude default `AC-` patterns, see the [customization format](references/abuse-cases.md#project-customizations). Then request an update against the revised file.

You can also name organization guidance or known threats in your request. The skill records their sources and applicability; see [supported security context](references/security-context.md).

## Optional JSON or YAML export

```text
Use create-threat-model to export threat-model.md as OTM YAML.
Keep the Markdown model unchanged and explain any export limitations.
```

The skill supports **Open Threat Model (OTM) 0.2.0** in JSON and YAML. Default filenames are `threat-model.otm.json` and `threat-model.otm.yaml`. Exports are snapshots; regenerate them after model changes.

OTM needs numerical assessments that a qualitative model may lack. The assistant explains missing inputs instead of inventing numbers. IDs and context are retained, but other tools may not preserve additional attributes. Schema validation does not establish importer compatibility. See the [export guide](references/otm-export.md).

## Install from a local checkout

From your project, replace the path with your checkout:

```bash
npx skills@1.7.2 add /path/to/appsec-skills --skill create-threat-model
```

For manual installation, copy the complete `create-threat-model` directory, including `references/`, into your assistant's skill location.

## Company distribution and customization

You can distribute a customized copy from your company's skills repository. Track the upstream commit and keep company changes separate so later updates can be merged without losing them.

Keep company requirements and known threats in separate context files where possible. Select them explicitly when invoking the skill; this skill does not automatically load a company context directory.

See the [technical distribution guide](references/company-distribution.md) for importing the skill, making company changes, installing from your repository, and merging upstream updates.

## Further reading

- [Model structure and scenario example](references/model-guide.md)
- [Assistant workflow](SKILL.md)
- [Requirements](requirements.md)
- [Development installation and fictional test project](../../DEVELOPMENT.md)
- [All AppSec Skills](../../README.md)
