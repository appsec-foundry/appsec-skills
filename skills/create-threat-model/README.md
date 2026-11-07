# Create Threat Model

Create a threat model from requirements, design documents, and what your team knows, even before code exists. The model describes what could go wrong, what harm it could cause, and what to change. You do not need security expertise.

The skill can also review or update a model and walk through its threats with you. [update-threat-model](../update-threat-model/README.md) is a shortcut to the update workflow and needs this skill installed.

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

Select a current top-tier model with high reasoning effort before you start; the skill cannot check this.

New models are written in English unless you ask for another language. Updates keep the model's language. The conversation can use yours.

## What you get

The assistant writes `threat-model.md` at the project root and links it from `SECURITY.md` or `security.md`, creating that file if needed. The model contains:

- a system overview with a diagram (Mermaid by default)
- threat scenarios: who could do what, under which conditions, and with what harm
- existing controls, recommended changes, priorities, and checks
- open decisions, source references, and gaps in the evidence

Each scenario has a stable ID such as `T-003` that you can use in tickets and pull requests. Proposed controls are kept apart from implemented or verified ones. The model is plain Markdown, so you can edit it in any editor. The closing summary names the main threats and next steps.

A shortened example from a fictional payment system:

> **T-003 — Payment details can change after approval**
>
> **Threat:** A supplier could change the recipient after approval and redirect the money if the original approval remains valid. Whether edits cancel approval is unknown.
>
> **Recommended change:** Require approval again when the amount or recipient changes.
>
> **Proposed check:** An unchanged approved payment succeeds; changing its recipient blocks payment until renewed approval. These checks have not run.

See the [full scenario and its evidence](references/model-guide.md#t-003-payment-details-can-change-after-approval). Priorities depend on the possible harm and on what an attacker needs to succeed. Missing information is marked as such.

At the end, the assistant may offer to add a pointer to the model in an existing `AGENTS.md` or `CLAUDE.md`. It edits that file only with your approval; see [agent integration](references/delivery.md#optional-agent-integration).

| Request | Result |
| --- | --- |
| Create | Writes a new model. If one exists, keeps it and offers an update. |
| Update | Revises affected sections; keeps unrelated content, manual edits, and IDs. |
| Review | Reports gaps and suggestions without changing files or the review status. |
| Walk through threats | Discusses threats one at a time, clarifies the facts that decide their priority, and develops measures. Saves the results only if you approve or asked for an update. |
| Discuss measures | Explains options and recommends changes without editing files. |
| Export | Writes an OTM JSON or YAML copy; Markdown stays the main document. |

The skill does not change application code, create tickets, commit files, or publish the model.

## How it works

At the start, the assistant shows the skill version and its steps, then a short status line whenever it begins a step or longer work.

1. **Understand the system.** The assistant reads your documents and summarizes who uses the system, what it handles, and where trust changes, with a text diagram. Each element is marked as intended, observed in code, or assumed. A single requirements file is enough to start; the picture is then smaller, not invented. If it cannot tell which data, operations, actors, or protection needs matter, it asks before deriving threats.
2. **List threat candidates.** One line per candidate, with an ID and a provisional priority.
3. **Ask what decides them.** One question at a time, each tied to a candidate or checklist item, for example "T-003: Does an approval stay valid when the recipient changes?". Each question gives brief background, and each answer option says what it would change. After each answer the assistant shows the effect. If an answer reveals new data, actors, or flows, it revisits the affected threats and adds scenarios where needed. You can skip or stop; unknowns stay visible.
4. **Assess and recommend.** It explains priorities, considers existing protections, and recommends changes and how to check them.
5. **Write the model.** It saves `threat-model.md` and summarizes the main threats, open decisions, and next steps.

The questions cover only what is needed to find threats; they are not a full questionnaire. Factual questions come individually; up to three independent questions about scope, readers, or permissions may share a round. If essential context is still missing, the assistant says the result is incomplete instead of inventing a model.

After delivery, the assistant offers to walk through the threats with you, one scenario at a time. If you asked for this at the start, it continues directly. Planned measures stay separate from verified protection.

The model covers the application as designed, including optional features. To focus on one deployment, say so in your request.

### When code is available

The assistant can read selected code and configuration to answer architecture questions. It may offer to read more broadly; that needs your opt-in, which you can give in the first request.

Code shows how the system is built. It does not replace requirements or settle conflicting evidence. This is not a code vulnerability scan, and the assistant does not run the application or tests.

For large projects, name the service or feature to focus on. Reading has [fixed limits](SKILL.md#discovery-budget), and the model records what was not covered.

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

**Create, then assess threats and develop measures together**

```text
Use create-threat-model to create a threat model from docs/design.md.
After the draft, walk through the identified threats with me, assess their
impact and prerequisites, and develop suitable measures. Incorporate the
clarified assessments and proposed measures into the model.
```

**Walk through existing threats without editing files**

```text
Use create-threat-model to walk through T-001 and T-002 with me.
Explain what could happen, clarify the facts that affect their priority,
and help me identify practical measures. Keep the files unchanged.
```

**Choose measures and record decisions**

```text
Use create-threat-model to help me choose practical measures for T-001 and T-002.
Explain the options and trade-offs and recommend where to start.
Update the model with the decisions I explicitly make.
```

Use your own scenario IDs. Discussion alone does not change the model. If your request asks for an update, decisions are saved directly; otherwise the assistant asks at the end. Accepting a risk needs an explicit decision by a responsible person, with a reason and a review date or trigger.

## Internal or public models

If the audience is unclear, the assistant asks whether the model is internal, public, or undecided. You can state it in the request:

```text
Create a public threat model using only information suitable for publication.
```

Internal models may include confidential findings only if everyone who can read the repository may see them. Public models leave confidential details out. Neither contains real secrets or unnecessary personal data.

If you skip the question, a new model is marked internal for now, the disclosure question stays open, and affected confidential details are left out. The audience notice in the model never restricts file access or approves publication. See [audience notices](references/audience.md#audience-notice).

## Keep the model current

When requirements, design, or evidence about controls change, use [update-threat-model](../update-threat-model/README.md) or ask this skill for an update. Supply the change documents and any verification results; a merged PR or test code alone does not show that a control works.

## Add project context

The skill uses a checklist to find missing context and a set of abuse patterns to explore what could go wrong. You can extend both with files at the project root, without editing the skill:

| File | Content |
| --- | --- |
| `threat-model-checklist.md` | Project-specific questions or reasons for exclusions ([format](references/checklist.md#project-checklist)) |
| `threat-model-abuse-cases.md` | Abuse cases, such as splitting purchases to stay under approval limits ([format](references/abuse-cases.md#project-customizations)) |

These files survive skill updates. After changing them, request a model update. You can also name company guidance or known threats in your request; see [supported security context](references/security-context.md).

## Optional JSON or YAML export

```text
Use create-threat-model to export threat-model.md as OTM YAML.
Keep the Markdown model unchanged and explain any export limitations.
```

Open Threat Model (OTM) exports are snapshots; regenerate them after the model changes. The assistant points out missing inputs and compatibility limits. The [export guide](references/otm-export.md) lists the supported version, required assessments, and filenames.

## Install from a local checkout

From your project, replace the path with your checkout:

```bash
npx skills@1.7.2 add /path/to/appsec-skills --skill create-threat-model
```

For manual installation, copy the complete `create-threat-model` directory, including `references/`, into your assistant's skill location.

## Company distribution and customization

You can distribute a customized copy from your company's skills repository. Record the upstream commit and keep company changes separate so you can merge later updates.

Where possible, put company requirements and known threats in separate context files and name them in your request. The skill does not load a company context directory automatically.

The [distribution guide](references/company-distribution.md) covers importing the skill, making company changes, installing from your repository, and merging upstream updates.

## Further reading

- [Model structure and scenario example](references/model-guide.md)
- [Assistant workflow](SKILL.md)
- [Requirements](requirements.md)
- [Development installation and fictional test project](../../DEVELOPMENT.md)
- [All AppSec Skills](../../README.md)
