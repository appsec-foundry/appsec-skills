# Create Threat Model

Create a threat model from requirements, design documents, and team knowledge, even before code exists. The model describes what could go wrong, what harm it could cause, and what to change. No security expertise is required.

This skill also supports reviews, updates, and guided discussions to assess identified threats and develop protective measures. For an existing model, [update-threat-model](../update-threat-model/README.md) provides a shortcut to the same update workflow; it requires this skill to be installed.

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

Use a current top-tier model at high reasoning effort. The skill cannot check or enforce this, so select the model before you start.

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

In its closing, the assistant may offer to add a reminder to consult the model in an existing `AGENTS.md` or `CLAUDE.md`. It finishes without waiting for a reply to that offer. If you request the addition, it clarifies the destination only when needed and edits the selected file only with your explicit approval, reusing approval already given. See [optional agent integration](references/delivery.md#optional-agent-integration) for details.

| Request | Result |
| --- | --- |
| Create | Writes an initial model; preserves an existing one and offers an update. |
| Update | Revises affected sections while preserving unrelated content, manual edits, and IDs. |
| Review | Reports gaps and suggestions without changing files or review status. |
| Walk through threats | Discusses identified threats, clarifies decisive facts, explains their priority, and develops measures. Saves outcomes only within a requested creation or update. |
| Discuss measures | Explains options and recommends changes without editing files. |
| Export | Creates an OTM JSON or YAML copy on request; Markdown remains the main document. |

Modeling does not change application code, create tickets, commit files, or publish the model.

## How it works

1. **Understand the system.** The assistant reads your documents and shows what it understood: who uses the system, what it handles, and where trust changes, with a text diagram of the recognized architecture. Each element is marked as intended, observed in code, or assumed. A single requirements file is enough to start; the picture is then smaller, not invented.
2. **Derive threat candidates.** It lists what could go wrong, with a stable ID, the harm, and the one fact that decides each candidate.
3. **Ask what decides them.** Each question names the candidate it belongs to and what your answer changes, for example: "T-003: Does an approval stay valid when the recipient changes?" Each round has at most three questions; you can skip or stop, and unknowns remain visible.
4. **Assess and recommend.** It explains priorities, considers existing protections, and recommends changes and ways to check them.
5. **Write the model.** It saves `threat-model.md` and summarizes the main threats, open decisions, and next steps.

If essential context is missing, the assistant explains what it needs instead of inventing a model.

**Work through threats together, when requested.** After delivery, the assistant can continue the dialogue scenario by scenario: explain the threat, clarify decisive facts, propose an assessment, and develop measures with you. Choosing measures is optional, and planned measures remain distinct from verified protection. An ordinary creation or update offers this after delivery; if you requested it at the start, the assistant continues directly without asking again.

The model covers the application as designed, including optional features. To focus on a particular deployment, say so in your request.

### When code is available

The assistant can read selected code and configuration to clarify architecture questions. It also offers to read more broadly to understand the architecture. **Broader reading requires your opt-in**, which you can include in the initial request.

Code helps explain how the system is built; it does not replace requirements or resolve conflicting evidence. This is not a code vulnerability scan, and the assistant does not run the application or tests.

For large projects, name the service or feature to focus on. Reading has [fixed limits](SKILL.md#discovery-budget), and the model records coverage gaps.

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

Use your actual scenario IDs. Include an update request to save decisions; discussion alone does not edit the model. Accepting a risk requires an explicit decision by a responsible person, with a rationale and review date or trigger.

## Internal or public models

If the intended audience is unknown, the assistant asks whether the model is internal, public, or undecided. You can specify it in the request:

```text
Create a public threat model using only information suitable for publication.
```

Internal models may include confidential findings only when the repository's readers may receive them. Public models omit confidential details. Neither includes real secrets or unnecessary personal data.

If you skip the audience question, a new model is provisionally marked internal. Disclosure questions remain recorded as unresolved; affected confidential details are omitted. The audience notice does not restrict file access or authorize publication. See the [audience notices](references/audience.md#audience-notice).

## Keep the model current

Use [update-threat-model](../update-threat-model/README.md) or request an update through this skill when requirements, design, or evidence about controls changes. Supply the change documents and any verification results; a merged PR or test code alone does not establish that a control works.

## Add project context

The skill uses a checklist to find missing context and common abuse patterns to explore what could go wrong. You can adapt both without editing the skill:

- **Checklist:** Add project-specific questions or explain exclusions in `threat-model-checklist.md` at the project root. See the [project checklist format](references/checklist.md#project-checklist).
- **Abuse patterns:** Add cases such as splitting purchases to bypass approval limits in `threat-model-abuse-cases.md` at the project root. See the [customization format](references/abuse-cases.md#project-customizations).

These files survive skill updates. After changing them, request a model update. You can also name company guidance or known threats in your request; see [supported security context](references/security-context.md).

## Optional JSON or YAML export

```text
Use create-threat-model to export threat-model.md as OTM YAML.
Keep the Markdown model unchanged and explain any export limitations.
```

Open Threat Model (OTM) exports are snapshots; regenerate them after model changes. The assistant explains missing inputs and compatibility limits. See the [export guide](references/otm-export.md) for the supported version, required assessments, and filenames.

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
