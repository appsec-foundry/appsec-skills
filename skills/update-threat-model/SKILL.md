---
name: update-threat-model
description: Update an existing maintained threat model after changes to requirements, design, features, or control evidence. Preserve scenario IDs, manual edits, and unaffected decisions. Requires create-threat-model for the shared modeling workflow. Not for initial creation, read-only reviews, or code vulnerability scans.
metadata:
  version: "0.1.0"
---

# Update a threat model

Provide a focused entry point to the Update operation of `create-threat-model`. Reuse that skill's workflow and references rather than maintaining a second set of modeling rules. The existing model remains the authoritative deliverable.

## Load the shared workflow

Display `update-threat-model · Version 0.1.0` once and briefly state the requested change and next step. Use the user's language for conversation.

Locate the installed `create-threat-model` skill through the host's skill catalog and read its `SKILL.md`. In this collection or a manual installation with sibling skill directories, the shared entry point is [create-threat-model](../create-threat-model/SKILL.md). Resolve its references relative to that skill's directory. If neither location provides the complete skill, explain the missing dependency and stop the update; do not improvise a substitute workflow, install packages, or fetch files automatically.

Apply the shared skill's Update operation, execution boundaries, reading budget, audience rules, interview guidance, write checks, and handoff. Its requirements govern this operation, especially selective updates (REQ-09), uncertainty (REQ-04), permissions (REQ-11), and clear dialogue (REQ-03, REQ-19). Identify the shared skill and its actual version when loading it. This is reuse in the current assistant, not a request to spawn another agent.

## Focus the update

1. Establish the repository, existing maintained model, and requested change from the user's request and available context. Use the shared workflow's root `threat-model.md`. If the user identifies a different model location, clarify compatibility with that workflow before writing; do not silently create or relocate a model. If no model exists, explain that creation is needed and suggest `create-threat-model`; an update request alone does not authorize creation.
2. Read the existing model and the selected change sources. Reuse its language, audience, system context, previous confirmations, and stable scenario IDs. If the document's purpose is unclear, clarify before editing.
3. Trace changed requirements, flows, actors, controls, and assumptions to affected scenarios and shared boundaries. Consider new threats and changed assessments of existing ones. Preserve unrelated content and decisions; revisit risk acceptance only when its assumptions change. Keep planned controls distinct from implemented or verified controls.
4. Ask only about material remaining gaps within the shared interview rules. Do not restart the full intake or ask the user to authorize Update again when already requested. Unknown or skipped facts remain explicit; they do not grant permissions or establish control effectiveness.
5. Re-read write targets, reconcile intervening edits, and apply a focused update under the shared write rules. Check the actual diff and the security-document link. Preserve scenario IDs and retain treated or retired scenarios with their rationale. Never replace the model with an analysis report or modify application code.
6. Link the updated model and summarize new threats, changed assessments, important open points, and the next useful action. Report incomplete writes or verification honestly. Do not commit, publish, implement measures, or start a treatment-decision round without a separate request.

The user's actual request takes precedence over this entry point: a request only to review or compare remains read-only under the shared workflow. A request to discuss measures does not authorize editing or risk acceptance.
