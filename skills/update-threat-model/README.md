# Update Threat Model

Update an existing `threat-model.md` after a feature, design, requirement, or control changes. The assistant preserves scenario IDs, manual edits, and unaffected decisions, and explains which threats are new or reassessed.

This skill uses the update workflow from [create-threat-model](../create-threat-model/README.md). Install both skills. If you already use `create-threat-model`, you can also request updates through it directly.

## Install

Using the collection's [installation instructions](../../README.md#installation-and-development), install both skills:

```bash
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill create-threat-model
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill update-threat-model
```

Install or update both skills from the same collection revision where possible. For a local checkout, replace `appsec-foundry/appsec-skills` in both commands with the same checkout path.

For manual installation, copy both complete skill directories, including `create-threat-model`'s `requirements.md` and `references/`, into your assistant's skill location. If required guidance is missing or conflicting, the assistant explains the problem and leaves the model unchanged.

## Use

```text
Use update-threat-model to incorporate the sharing feature in docs/sharing.md
into threat-model.md.
```

To incorporate evidence about a control:

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

1. Reads the existing model and the documents describing the change.
2. Traces the change to affected scenarios and asks about important gaps, reusing earlier answers.
3. Updates those sections, preserves unrelated content and IDs, and checks the document and its security-document link.
4. Summarizes new threats, changed assessments, open questions, and next steps.

Questions use your language; the model keeps its existing language. Unknowns remain visible, and a planned measure is not recorded as verified. The shared rules for [reading code and configuration](../create-threat-model/README.md#when-code-is-available) apply here too: targeted reading can clarify architecture questions; broader reading requires your opt-in.

The supported model location is `<repo>/threat-model.md`. A model at another location is left unchanged; the assistant does not move or duplicate it. An update may also add a missing model link to the repository's `SECURITY.md` or `security.md`, preserving existing disclosure instructions. If neither security document exists, it creates a minimal root `SECURITY.md` with the link.

If no maintained model exists, use [create-threat-model](../create-threat-model/README.md) first. An update request does not create a replacement model or authorize code changes, commits, publication, or risk acceptance. Read-only review requests remain read-only.

See the shared guide for [audience and confidentiality](../create-threat-model/README.md#internal-or-public-models), [reading limits](../create-threat-model/SKILL.md#discovery-budget), and [the update workflow](../create-threat-model/SKILL.md#update-affected-scenarios).
