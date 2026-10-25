# AppSec Skills

Application security skills for coding assistants. Part of [AppSec Foundry](https://github.com/appsec-foundry). Each skill provides a workflow, examples, and references for a specific AppSec task.

## Skills

| Skill | Purpose |
| --- | --- |
| [create-threat-model](skills/create-threat-model/README.md) | Create, update, or review a threat model from requirements, design documents, and team context. Works before code exists; no Analyzer required. |
| [security-score](skills/security-score/README.md) | Present Analyzer scoring version 2 without model calls. |
| [repo-profile](skills/repo-profile/README.md) | Show size, languages and build manifests of a local repository via Analyzer, without model calls. |
| [authnz-review](skills/authnz-review/README.md) | Run an independent Analyzer AuthN/AuthZ review with explicit Claude/model-use authorization. |
| [analyze-threats](skills/analyze-threats/README.md) | Analyze features, changes, PRs/MRs, and design decisions against relevant threat-model context. Works independently; Analyzer is optional. |

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

`create-threat-model` and `analyze-threats` work without AppSec Advisor or AppSec Analyzer. `analyze-threats` also supports an optional Analyzer workflow. `security-score`, `repo-profile`, and `authnz-review` require an independently installed compatible Analyzer. Engine integrations use `dependencies.json` to declare interface versions, commands, capabilities, optional tools, and model prerequisites using the [dependency schema](schemas/skill-dependencies.schema.json). `engine_required: false` marks an optional integration; when omitted, the engine is required. These prerequisites apply only when that engine workflow is selected. Additional external model use requires source/model-use authorization. No skill installs packages automatically. A plugin may provide a trusted binding to its bundled tested engine; portable instructions contain no plugin-root or sibling-checkout paths. Existing Advisor commands remain available until their compatibility gaps and qualification gates are closed.

For development, follow [AGENTS.md](AGENTS.md) and the relevant skill's requirements: [Create Threat Model](skills/create-threat-model/requirements.md) or [Analyze Threats](skills/analyze-threats/requirements.md).

For company-specific review criteria, see [Analyze Threats customization and distribution](skills/analyze-threats/README.md#company-customization-and-distribution). Keep known threats and security requirements in project documents or a separate versioned context package; an internal distribution can bundle that context with the upstream skill without maintaining a workflow fork.

To load the current working version into Codex and Claude Code, run `make install-dev` from this checkout. Use `make install-dev-codex` or `make install-dev-claude` for just one host. These targets require Make and Python 3 and install a separate `create-threat-model-dev` snapshot for the current user; rerun after local changes. See the [development installation instructions](DEVELOPMENT.md#load-a-development-version-into-codex-or-claude-code) for project-only installation or use without Make. `make help` lists the targets; `make test` runs local tests without model calls.

For an optional fictional test project, run `bash scripts/test-threat-model.sh`. See the [example test instructions](DEVELOPMENT.md#optional-try-a-fictional-project).
