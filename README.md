# AppSec Skills

Application security skills for coding assistants. Part of [AppSec Foundry](https://github.com/appsec-foundry).

## Skills

| Skill | Purpose | Needs AppSec Analyzer? |
| --- | --- | --- |
| [create-threat-model](skills/create-threat-model/README.md) | Create, update, or review a threat model, including before code exists. | No |
| [update-threat-model](skills/update-threat-model/README.md) | Focused updates to an existing threat model; requires create-threat-model. | No |
| [analyze-threats](skills/analyze-threats/README.md) | Examine features, changes, PRs/MRs, or design decisions for threats. | Optional |
| [security-score](skills/security-score/README.md) | Score repositories or assess the security relevance of changes; requires a separate Python tool. | Optional |
| [repo-profile](skills/repo-profile/README.md) | Show repository size, languages, and build manifests. | Yes |
| [authnz-review](skills/authnz-review/README.md) | Review authentication and authorization through Analyzer and Claude CLI. | Yes |

## Quick start: threat modeling

Use a coding assistant that supports skills. The [Skills CLI](https://github.com/vercel-labs/skills/tree/v1.7.2) needs Node.js 22.20+, npm, and Git.

From your project, install the skill and select your assistant when prompted:

```bash
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill create-threat-model
```

For an unpublished checkout, use the [local installation instructions](skills/create-threat-model/README.md#install-from-a-local-checkout).

Then ask your assistant:

```text
Use create-threat-model to create a threat model from docs/requirements.md
and docs/architecture.md. Ask about material gaps before writing the draft.
```

Replace the paths with your documents. The assistant writes `threat-model.md` and links it from `SECURITY.md` or `security.md`. See the [skill guide](skills/create-threat-model/README.md) for other uses.

## Quick start: security scoring and change relevance

```bash
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill security-score
```

Install the [Security Score Python tool](https://github.com/appsec-foundry/appsec-analyzer-tools/tree/main/tools/security-score) separately. The skill calls that tool; installing the skill alone does not provide the scorer.

```text
Use security-score for this repository.
Use security-score for the staged changes with --details.
Use security-score for PR https://github.com/owner/project/pull/42.
```

Repositories receive a **0–100 score and A–F grade**. Changes receive **high, medium, low, or unclear security relevance** and separate findings. PR/MR checks need read access or a supplied diff. The Python tool needs Python 3.10+ and Git for local comparisons. See the [skill guide](skills/security-score/README.md) for details.

## Installation and development

Each `skills/<name>/` directory contains a usage guide (`README.md`), assistant instructions (`SKILL.md`), and supporting files. For manual installation, copy the complete directory into your assistant's skill location. `update-threat-model` also needs `create-threat-model`. Analyzer integrations list their prerequisites in `dependencies.json`.

For company use, see [Create Threat Model distribution and updates](skills/create-threat-model/README.md#company-distribution-and-customization) or [Analyze Threats company context](skills/analyze-threats/README.md#company-context).

To work on this collection, follow [AGENTS.md](AGENTS.md) and the affected skill's requirements. Run `make test` for local tests without model calls. `make install-dev` installs a separate `create-threat-model-dev` snapshot for Codex and Claude Code; rerun it after changes. See [DEVELOPMENT.md](DEVELOPMENT.md) for host-specific installation and a fictional test project.
