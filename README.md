# AppSec Skills

Application security skills for coding assistants. Part of [AppSec Foundry](https://github.com/appsec-foundry). Each skill provides a workflow, examples, and references for a specific AppSec task.

## Skills

| Skill | Purpose |
| --- | --- |
| [create-threat-model](skills/create-threat-model/README.md) | Create, update, or review a threat model from requirements, design documents, and team context. Works before code exists. |

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

These skills do not require AppSec Advisor or AppSec Analyzer.

For development, follow [AGENTS.md](AGENTS.md) and the relevant skill's requirements, starting with [create-threat-model](skills/create-threat-model/requirements.md).
