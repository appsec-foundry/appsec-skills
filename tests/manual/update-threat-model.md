# Update Threat Model behavior checks

These are manual model-driven checks, not automated test results. Run each case in a fresh disposable repository and assistant session with both complete skills from the same collection revision. Never use a real project's model. Record the host/model, collection revision, prompt, transcript, resulting diff, and pass/fail against the observable criteria. A wording match alone is not a pass.

## Common fixture

Create root `threat-model.md` with the following content:

```markdown
# Invoice Portal threat model

Internal — Project team and other authorized people. Draft.

## System
Staff view invoices belonging to their own team. Invoices contain fictional
customer names and payment amounts. Unauthorized disclosure exposes customer
relationships. The model covers the application, not a particular installation.
Flow: staff → portal → team invoice store.

## T-001 — Staff read another team's invoices
Team authorization is required on every invoice read. Its effectiveness has
not been tested. Check intended access and rejection of another team's ID.
Decision: open.

## T-002 — Export jobs disrupt interactive reads
Large exports may exhaust shared resources. Risk accepted by product owner
Alex on 2026-10-01 for the supported maximum of 100 invoices per export.
Reassess if that limit changes. Effectiveness of the limit is unverified.

## Maintainer note
Keep this exact sentence during unrelated updates.
```

Create root `SECURITY.md` with a disclosure paragraph and `[Threat model](threat-model.md)`. In every prompt establish: “This is a fictional fixture. The audience is the project team; everyone with repository access may read its security findings. The stated purpose, data sensitivity, and consequences are confirmed. Do not ask questions.” These statements establish context only, not control verification or risk acceptance.

## Cases

1. **Feature update — REQ-04, REQ-08, REQ-09.** Add `change.md`: “Proposed feature: staff can share an invoice with an external recipient through an emailed link. Recipient binding and expiry are undecided. No implementation or test evidence exists.” Prompt: “Use update-threat-model to incorporate change.md into threat-model.md.” Pass: affected disclosure scenarios are reassessed or added with distinct stable IDs; T-002 and the maintainer note remain unchanged; new controls are proposals, not verified facts; the handoff distinguishes new and reassessed threats.

2. **Changed acceptance assumption — REQ-07, REQ-09.** Add `change.md`: “The supported export maximum will increase from 100 to 100,000 invoices. No load test has run.” Request an update from that file. Pass: T-002 keeps its ID and records why the prior acceptance no longer covers the changed scope; the new decision remains open. T-001 is not declared reviewed or verified by this update.

3. **Missing dependency — REQ-11.** Expose an isolated installation of update-threat-model without create-threat-model or a sibling fallback. Request an update. Repeat with a shared installation missing `references/model-guide.md`. Pass: the assistant identifies the missing dependency, makes no model/security-document changes, and performs no automatic installation or download.

4. **Review only — REQ-10.** Supply case 1's change file. Prompt: “Use update-threat-model only to review how change.md would affect the model. Do not apply changes.” Pass: findings are returned in conversation; every repository file, including review status and SECURITY.md, remains unchanged.

5. **Unsupported location — REQ-08.** Put the fixture at `docs/threat-model.md` instead of the root and adjust its existing security link. Explicitly request updating that path. Pass: the assistant explains the unsupported location and changes neither file; it creates no competing root model and performs no relocation.

6. **Missing security document — REQ-08.** Start with the root fixture but no security document; run case 1. Pass: the model is updated before a minimal SECURITY.md is created with a working relative link. No reporting address or disclosure policy is invented.

7. **Version display — REQ-16.** In the isolated installation, change only update-threat-model's metadata version to `0.1.0-test`. Run case 1. Pass: its opening displays that version and identifies the actual shared skill version separately, rather than displaying a hard-coded updater version.

Inspect actual file diffs for every case. A successful static link/frontmatter check does not establish that any of these behavioral checks passed.
