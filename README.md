# AppSec Skills

Application security skills for coding assistants. Part of [AppSec Foundry](https://github.com/appsec-foundry). Each skill provides a workflow, examples, and references for a specific AppSec task.

## Skills

| Skill | Purpose |
| --- | --- |
| [create-threat-model](skills/create-threat-model/README.md) | Create, update, or review a threat model from requirements, design documents, and team context. Works before code exists; no Analyzer required. |
| [security-score](skills/security-score/README.md) | Present Analyzer scoring version 2 without model calls. |
| [repo-profile](skills/repo-profile/README.md) | Show size, languages and build manifests of a local repository via Analyzer, without model calls. |
| [authnz-review](skills/authnz-review/README.md) | Run an independent Analyzer AuthN/AuthZ review with explicit Claude/model-use authorization. |
| [analyze-threats](skills/analyze-threats/README.md) | Use Analyzer question-first focused analysis, preview, clarification and lifecycle operations. |

## Quick start

You need a coding assistant that supports skills. The installation command uses the [Skills CLI](https://github.com/vercel-labs/skills/tree/v1.7.2), which requires Node.js 22.20 or newer, npm, and Git.

From the project you want to model, install the skill and select your assistant when prompted:

```bash
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill create-threat-model
```

The GitHub command requires the skill to be published in this repository. For an unpublished checkout, use the [local installation instructions](skills/create-threat-model/README.md#install-from-a-local-checkout).

Then open your assistant in that project and ask:

```text
Use create-threat-model to create a threat model from docs/requirements.md
and docs/architecture.md. Ask about material gaps before writing the draft.
```

Replace the example paths with your documents. The assistant writes `threat-model.md` and links it from `SECURITY.md` or `security.md`. An existing model is preserved unless you request an update.

The `npx` command installs the skill; modeling happens in your assistant. See the [skill guide](skills/create-threat-model/README.md) for updates, reviews, and working without questions.

## Repository layout

Each skill lives in `skills/<name>/`: `README.md` explains usage, `SKILL.md` contains the assistant instructions, and `references/` holds supporting material. For manual installation, copy the complete skill directory into your assistant's skill location.

`create-threat-model` requires neither AppSec Advisor nor AppSec Analyzer. The other skills require an independently installed compatible Analyzer; their `dependencies.json` files declare interface versions, commands, capabilities, optional tools and model prerequisites using the [dependency schema](schemas/skill-dependencies.schema.json). Model-backed skills require explicit source/model-use authorization. No skill installs packages automatically. A plugin may provide a trusted binding to its bundled tested engine; portable instructions contain no plugin-root or sibling-checkout paths. Existing Advisor commands remain available until their compatibility gaps and qualification gates are closed.

For development, follow [AGENTS.md](AGENTS.md) and the relevant skill's requirements, starting with [create-threat-model](skills/create-threat-model/requirements.md).
