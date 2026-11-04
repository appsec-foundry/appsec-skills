# Optional OTM export

Read this guide only when the user requests a structured export (REQ-20). Markdown stays authoritative; exports are derived snapshots. Use Open Threat Model (OTM) **0.2.0**, `otmVersion: "0.2.0"`, in the requested JSON or YAML syntax. OTM is maintained by IriusRisk. Do not substitute another schema.

Use the pinned upstream [specification](https://github.com/iriusrisk/OpenThreatModel/blob/0.2.0/README.md) and [JSON Schema](https://raw.githubusercontent.com/iriusrisk/OpenThreatModel/0.2.0/otm_schema.json) through authorized readers, or a local copy whose provenance matches; do not silently switch to `main`, whose schema validates differently. Source links grant no network permission: if the schema cannot be accessed, explain the validation obstacle instead of claiming a validated export. Do not install packages or contact an importer.

## Scope of the request

- An export-only request reuses the established scope and audience, reads the model and necessary local evidence, and does not rewrite `threat-model.md`, the security document, or the assessment. Clarify only material export gaps; do not reopen the interview.
- Creation or update plus export completes the Markdown work first, then exports the resulting state. A review alone produces no export.
- Without a maintained model, explain that an export needs one; create it only when creation is also requested.

## Output

- Honor the requested syntax. For OTM without a stated syntax, use YAML and say so. Default to `<repo>/threat-model.otm.json` or `<repo>/threat-model.otm.yaml`; write both only when requested. Inspect an existing export before replacing it and clarify unclear provenance or intervening edits.
- Apply the [audience rules](audience.md) and the delivery guide's [content check](delivery.md#write-and-check) to descriptions, attributes, source paths, and diagnostics. Do not restore details omitted from a public model; a public export of an internal model discloses that omissions exist without exposing them. No export request authorizes an upload or publication.
- In `project.attributes`, record string values for `appsec.sourceModel` (relative path), `appsec.sourceSha256` (hash of the exact source bytes), `appsec.audience`, and `appsec.exportLimitations`. These are local conventions, not OTM fields. Recheck the hash before finalizing; a changed source requires regeneration.

## Feasibility

OTM requires integer ratings from 0 to 100: `risk.likelihood` and `risk.impact` for threats, `riskReduction` for mitigations, `risk.trustRating` for trust zones, and `risk.confidentiality`, `risk.integrity`, and `risk.availability` for assets. Never infer a number from labels such as high, planned, or unverified, and never fill unknowns with zero, midpoints, or `null`.

Use existing attributed assessments for the same scope and scale. If the user supplies export ratings, preserve their source and rationale in the export without altering the Markdown assessment. When required inputs are missing, summarize them by object in plain language, for example: "The model describes T-001 qualitatively. OTM also needs likelihood and impact ratings, and a reduction estimate for M-001. I have kept the Markdown model unchanged and have not produced the export." Offer to use existing team assessments; do not start a scoring questionnaire, omit threats to pass validation, or write a knowingly incomplete file as a finished export. Leave an existing export intact when regeneration is blocked and say it was not refreshed.

## Mapping

| Model content | OTM |
| --- | --- |
| Scope, purpose, status, audience, review limits | `project.name`, `project.description`, string-valued `project.attributes` |
| Components and stores | `components` with source-supported `type` and `parent` |
| Trust zones | `trustZones` with their documented trust ratings |
| Valuable data | `assets` with documented ratings and references |
| Interactions | `dataflows` with existing component IDs as `source` and `destination` |
| Scenario | Root `threats` entry with ID, name, description, supplied ratings, and references to applicable components or flows |
| Measure | Root `mitigations` entry with ID, description, and supplied estimate, referenced from affected threat instances |
| Decisions, owners, assumptions, confidence, evidence, verification | Readable context in descriptions plus string-valued `attributes` such as `appsec.decision`, `appsec.assumptions`, `appsec.evidence`, `appsec.verification`, `appsec.sourceReference` |

Keep source scenario IDs exactly, including uppercase `T-001`. Retain existing component and measure IDs; derive a stable ID from the source section where the export needs one, record its source reference, and preserve the mapping on later exports. Do not infer architecture to satisfy required parents or links. Preserve the distinctions between proposal, plan, implementation, verification, acceptance, and retirement; where an OTM state cannot express a decision, state the limit and keep the full decision in the description or attributes. Keep a mapping inventory: every scenario, measure, decision, material assumption, and evidence reference has a destination or an explained limitation.

## Validate and deliver

Parse the candidate with an available safe JSON or YAML reader using plain mappings, sequences, and scalars, and validate it against the pinned schema. The released schema does not fully check array items, numeric ranges, ID uniqueness, or reference integrity, so also check: required fields and types for every object; integer ratings in range and the exact OTM version; unique IDs per collection; existing flow endpoints and parents without cycles (a parent is a component or a trust zone, not both); every referenced threat, mitigation, asset, and representation exists; the mapping inventory is complete; no number was introduced to pass a check; and the source hash still matches. When both syntaxes are requested, their parsed objects must be equal.

Do not deliver a finished export if a required check cannot be completed or fails; describe the obstacle and preserve existing files. State "OTM 0.2.0; schema and reference checks passed; importer compatibility not tested" only when those checks ran. An importer check needs a separately authorized task. Link the files produced with their OTM version, source model, validation performed, and material mapping limits. Future model updates do not refresh exports; regenerate them only when requested.
