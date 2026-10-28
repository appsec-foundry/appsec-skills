# Update Threat Model

Update an existing `threat-model.md` after a feature, design, requirement, or control changes. The assistant preserves scenario IDs, manual edits, and unaffected decisions, and explains which threats are new or reassessed.

This is a dedicated entry point to the update workflow in **create-threat-model**. Both skills must be installed, including the latter's `references/` directory. It does not maintain a separate modeling workflow.

## Install

Using the collection's [installation instructions](../../README.md#installation-and-development), install both skills:

```bash
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill create-threat-model
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill update-threat-model
```

For an unpublished checkout, replace `appsec-foundry/appsec-skills` with the checkout path. Install or update both skills from the same collection revision where possible; using the same checkout for both commands provides a consistent source. For manual installation, copy both complete skill directories into your assistant's skill location, including `create-threat-model`'s `requirements.md` and `references/`. Equal version labels alone do not guarantee compatibility. If required guidance is missing or conflicting, the assistant explains the problem and leaves the model unchanged without installing anything automatically.

## Use

```text
Use update-threat-model to incorporate the sharing feature in docs/sharing.md
into threat-model.md. Preserve unrelated scenarios and decisions.
```

To incorporate evidence about a control:

```text
Use update-threat-model to reassess T-003 using docs/payment-change.md
and docs/payment-test-results.md. Keep remaining uncertainty explicit.
```

To work without questions:

```text
Use update-threat-model to update threat-model.md from docs/design-change.md.
Do not ask questions; record unresolved assumptions in the model.
```

The assistant reads the existing model and change sources, asks only about material gaps, updates affected sections, and checks the resulting document and its security-document link. Questions use your language; the model keeps its existing language. Unknowns remain visible, and a planned measure is not recorded as verified.

The supported model location is `<repo>/threat-model.md`. A model at another location is left unchanged; the assistant does not move or duplicate it. An update may also add a missing model link to the repository's `SECURITY.md` or `security.md`, preserving existing disclosure instructions. If neither security document exists, it creates a minimal root `SECURITY.md` with the link.

If no maintained model exists, use [create-threat-model](../create-threat-model/README.md) first. An update request does not create a replacement model or authorize code changes, commits, publication, or risk acceptance. Read-only review requests remain read-only.

See the shared guide for [audience and confidentiality](../create-threat-model/README.md#internal-or-public-models), [reading limits](../create-threat-model/SKILL.md#discovery-budget), and [the update workflow](../create-threat-model/SKILL.md#update-affected-scenarios).
