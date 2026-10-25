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

## What you get

- `threat-model.md` at the target repository root: scope, sources, assets, actors, system flows and trust boundaries, threat scenarios, treatments, verification criteria, and open questions.
- A relative link from the existing `SECURITY.md` or `security.md`. If neither exists, the skill creates a short `SECURITY.md` containing the link.

The result starts as a draft. It distinguishes current exposure from expected residual risk after effective treatment. Proposed controls and unresolved assumptions stay visible; they are not recorded as verified controls or accepted risks. The skill does not commit or publish the files.

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

**Review an existing model**

```text
Use create-threat-model to review threat-model.md against docs/design.md.
Report gaps and proposed changes without editing files.
```

A creation request never replaces an existing model. Updates integrate features into that model; reviews leave the model and security document unchanged. If there is too little context to model a concrete system, the skill explains what is missing.

## Adapt the checklist

Before asking questions, the skill checks the sources against a short [checklist](references/checklist.md) of aspects such as scope, actors, trust boundaries, and personal data. Open items lead to questions. Items that remain open, do not apply, or were not examined are listed in the model's open questions.

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
