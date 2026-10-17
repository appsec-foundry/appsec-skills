# Working on AppSec Skills

These instructions apply to maintaining this repository. They do not extend a skill user's task or permissions in a target project.

## Create Threat Model

Before changing `skills/create-threat-model/`, read its [requirements](skills/create-threat-model/requirements.md). They define the expected user-facing behavior and guide further development.

- Use the affected `TM-` IDs to connect behavior changes and their validation to the requirements.
- If the requested behavior changes a requirement, update it within the authorized task and explain why. Do not silently change requirements to make an implementation appear correct.
- Keep `SKILL.md`, supporting references, and the skill README consistent. Keep user-facing requirements short; put procedural detail in the skill instructions.
- Check changed behavior with a small relevant example, including a failure case when a security boundary changes. For documentation-only edits, check clarity, links, and consistency; do not claim unexecuted behavior was tested.

The [repository README](README.md) introduces the collection. Each skill's README explains installation and usage; its `SKILL.md` contains the assistant workflow. Preserve that separation when adding material.
