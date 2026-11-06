# Update Threat Model

Update an existing `threat-model.md` after a feature, design, requirement, or control changes. The assistant keeps scenario IDs, manual edits, and unaffected decisions, and explains which threats are new or reassessed.

This skill uses the update workflow of [create-threat-model](../create-threat-model/README.md), so you need both. If you already use `create-threat-model`, you can also ask it for updates directly.

## Install

Install both skills, as described in the collection's [installation instructions](../../README.md#installation-and-development):

```bash
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill create-threat-model
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill update-threat-model
```

Where possible, install and update both from the same revision of this collection. For a local checkout, replace `appsec-foundry/appsec-skills` with the checkout path in both commands. For manual installation, copy both complete skill directories into your assistant's skill location.

## Use

The model must be `threat-model.md` at the project root; other locations are not supported. If there is no model yet, use [create-threat-model](../create-threat-model/README.md) first.

```text
Use update-threat-model to incorporate the sharing feature in docs/sharing.md
into threat-model.md.
```

To include evidence about a control:

```text
Use update-threat-model to reassess T-003 using docs/payment-change.md
and docs/payment-test-results.md.
```

To work without questions:

```text
Use update-threat-model to update threat-model.md from docs/design-change.md.
Do not ask questions; record unresolved assumptions in the model.
```

## How it works

1. Reads the existing model and the documents that describe the change.
2. Finds the affected scenarios and asks about important gaps, reusing earlier answers.
3. Updates those sections and keeps unrelated content and IDs. It checks the result and makes sure the model is linked from `SECURITY.md` or `security.md`, creating a minimal `SECURITY.md` if needed.
4. Summarizes new threats, changed assessments, open questions, and next steps.

Questions use your language; the model keeps its own. Unknowns stay visible, and planned measures are not recorded as verified. As in create-threat-model, the assistant can read code and configuration to answer architecture questions; [broader reading](../create-threat-model/README.md#when-code-is-available) needs your opt-in.

Updates do not change application code, commit files, publish the model, or accept risks on your behalf.

See also [audience and confidentiality](../create-threat-model/README.md#internal-or-public-models), [reading limits](../create-threat-model/SKILL.md#discovery-budget), and [the update workflow](../create-threat-model/SKILL.md#operations).
