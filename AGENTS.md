# Working on AppSec Skills

These instructions apply to maintaining this repository. They do not extend a skill user's task or permissions in a target project.

## Requirements changes

Before changing any `requirements.md`:

- Check whether the proposed addition, change, or removal is relevant to the user's task and necessary. Keep implementation details in the skill instructions.
- Show the user the proposed wording and explain plainly what changes and why, referencing existing `REQ-` IDs where applicable.
- Write requirements in clear, concise language focused on user-facing behavior, without unnecessary details.
- Obtain explicit user approval for the concrete proposal before editing the file. General permission to implement a task or silence does not count as approval of requirements changes.

## Create Threat Model

Before changing `skills/create-threat-model/`, read its [requirements](skills/create-threat-model/requirements.md). They define the expected user-facing behavior and guide further development.

- Use the affected `REQ-` IDs to connect behavior changes and their validation to the requirements.
- If the requested behavior requires a requirement change, follow the approval process above. Do not silently change requirements to make an implementation appear correct.
- Keep `SKILL.md`, supporting references, and the skill README consistent. Keep user-facing requirements short; put procedural detail in the skill instructions.
- Check changed behavior with a small relevant example, including a failure case when a security boundary changes. For documentation-only edits, check clarity, links, and consistency; do not claim unexecuted behavior was tested.

The [repository README](README.md) introduces the collection. Each skill's README explains installation and usage; its `SKILL.md` contains the assistant workflow. Preserve that separation when adding material.
