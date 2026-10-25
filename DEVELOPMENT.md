# Developing Create Threat Model

These instructions require a clone of the full AppSec Skills repository. The Makefile and scripts are not included in an installed skill directory. Run the commands below from the repository root.

Follow [AGENTS.md](AGENTS.md) and the [skill requirements](skills/create-threat-model/requirements.md) when making changes. For installation and everyday use, see the [user guide](skills/create-threat-model/README.md).

## Load a development version into Codex or Claude Code

From the root of this checkout, install or update your current working version:

```bash
make install-dev          # Codex and Claude Code
make install-dev-codex    # Codex only
make install-dev-claude   # Claude Code only
```

This requires Make and Python 3 and installs a snapshot named **create-threat-model-dev** under `~/.agents/skills/` for Codex or `~/.claude/skills/` for Claude Code. The regular `create-threat-model` installation remains intact. Without Make, run `python3 scripts/install-dev-skill.py both` (or select `codex` or `claude`). To install only for one project, use `python3 scripts/install-dev-skill.py both --project /path/to/project`.

In a fresh session in your target project, invoke:

```text
Codex:       $create-threat-model-dev
Claude Code: /create-threat-model-dev
```

Then describe the modeling task as usual. The opening displays the dev name and a version containing a fingerprint of the local source files (REQ-16). **After editing the source skill, rerun the same installation command** to refresh the snapshot; uncommitted changes are included. Make edits in this checkout, not the installed copy. The installer preserves unrelated installations and refuses to replace a dev copy with local edits or an unmanaged folder. It installs no packages and starts no model session. These paths apply to local Codex and Claude Code, not Claude web chat or Cowork.

Anyone with a local checkout can use these targets; paths are resolved from that checkout and the current user's home directory. Run `make help` to list targets and `make test` for the local installer and test-starter checks without model calls.

See the official [Codex local skill documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) and [Claude Code skill documentation](https://code.claude.com/docs/en/skills#choose-where-skills-load).

## Optional: try a fictional project

From the root of this repository, run:

```bash
bash scripts/test-threat-model.sh
```

The starter creates a fresh temporary project, copies the current skill into it, adds a fictional customer-portal description, and opens an interactive Codex CLI session with the prompt already supplied. It requires Bash and an installed, configured Codex CLI; it uses your existing login and configuration. Each run copies your latest local changes. Results remain in the printed test directory; move them elsewhere if you need to keep them beyond temporary-directory cleanup.

To use the app instead of the CLI, run `bash scripts/test-threat-model.sh --prepare-only`, open the printed folder, and send the text from `PROMPT.txt` in a fresh conversation.

The example deliberately leaves audience, data sensitivity, and business impact unspecified. Check that the early dialogue clarifies these within the three-question limit (REQ-03, REQ-05–07, REQ-11, REQ-14), and that your answers inform the scenarios and priorities. In a fresh run, skip an answer or add "Do not ask questions" to the prompt and check that the uncertainty stays visible (REQ-04). This is a manual behavior test; the starter does not automatically evaluate the resulting model.
