# Optional OTM export

Read this guide only when the user requests a structured export. Markdown stays authoritative; exports are derived snapshots, not separately maintained models. Use Open Threat Model (OTM) **0.2.0**, with `otmVersion: "0.2.0"`, in the requested JSON or YAML syntax. OTM is maintained by IriusRisk, not OWASP. Do not substitute TM-BOM or invent an unrelated JSON/YAML schema.

Use the versioned upstream [specification](https://github.com/iriusrisk/OpenThreatModel/blob/0.2.0/README.md) and [JSON Schema](https://raw.githubusercontent.com/iriusrisk/OpenThreatModel/0.2.0/otm_schema.json) through authorized readers. Do not silently switch to `main`: the release and main schemas have different validation behavior despite identifying the same OTM version. Use an available local copy when its provenance matches the pinned version. Source links do not grant network permission; if the schema cannot be accessed or checked, explain the validation obstacle instead of claiming a validated export. Do not install packages or contact an importer as part of export.

## Decide what the request covers

For an export-only request, reuse the established scope and audience. Clarify only material export gaps; do not reopen the modeling interview or reassess threats.

- If no maintained model exists, explain that an export needs one. Create it only when creation is also requested.
- For creation or update plus export, complete the normal modeling workflow first.
- A review alone produces no export files. An explicit additional export request authorizes those derivative files, not changes to the reviewed model.

## Select the output and preserve the source

- Honor the requested syntax. If the user requests OTM without specifying syntax, use YAML and state that choice; this is not a reason for an extra interview question. An explicit JSON or YAML export request uses OTM and names the format to the user.
- Default to `<repo>/threat-model.otm.json` or `<repo>/threat-model.otm.yaml`. Write both only when requested. Honor another authorized local destination. Preserve unrelated or manually edited files; inspect any existing export before replacing it. If its provenance or intervening edits are unclear, clarify before overwriting it.
- An export-only task reads the model and necessary local evidence but does not rewrite `threat-model.md`, add metadata to it, change the security document, or reassess threats. When creation or update is also requested, finish that Markdown work first, then export the resulting state.
- Apply the same [audience and destination rules](audience.md) and [content check](delivery.md#2-check-audience-and-content) as for the model, including descriptions, attributes, source paths, and export diagnostics. Do not restore confidential details omitted from a public model. A public export of an internal model needs content suitable for public readers; disclose any omissions without exposing the omitted text. No export request authorizes an upload, publication, or importer execution.
- In `project.attributes`, record string values for `appsec.sourceModel` (relative path), `appsec.sourceSha256` (hash of the exact source file bytes), `appsec.audience`, and `appsec.exportLimitations`. Include referenced model appendices' paths and hashes in `appsec.sourceReferences` if they are separate files. These are local attribute conventions, not standardized OTM fields. Hash the source after any authorized model update and recheck before finalizing the export; a changed source requires regeneration.

## Check feasibility before writing

OTM's required ratings are **integers from 0 to 100** in the specification. Check each relevant object; never infer a number from labels such as high, low confidence, local-only, planned, or unverified.

| Included object | Required numerical input |
| --- | --- |
| Threat | `risk.likelihood`, `risk.impact` |
| Mitigation | `riskReduction` |
| Trust zone | `risk.trustRating` |
| Asset | `risk.confidentiality`, `risk.integrity`, `risk.availability` |

Use existing, attributed assessments for the same scope and scale. If the user supplies additional export ratings, preserve their source and rationale in the export; this does not authorize altering the Markdown assessment. These values are ratings, not measured probabilities or verified control effectiveness. A schema's acceptance of `null` or an out-of-range number does not establish that it satisfies the specification or a receiving tool.

When required inputs are missing, summarize them by object and explain the effect in plain language. For example: “The model describes T-001 qualitatively. OTM also needs likelihood and impact ratings, and a reduction estimate for M-001. I have kept the Markdown model unchanged and have not produced the export.” Offer to use existing team assessments or help document them if the user wants that work. Do not start a long scoring questionnaire or block separately requested Markdown delivery. Honor skipped questions and no-questions mode. Do not fill unknowns with zero, midpoint values, or `null`, omit known threats or measures to pass validation, or write a knowingly incomplete file as a finished export. Leave an existing export intact when regeneration is blocked; state that it was not refreshed.

## Map the model without changing its meaning

Use normal OTM objects and their references. Keep source scenario IDs exactly, including uppercase `T-001`. Retain existing component and measure IDs; where an export needs an ID absent from Markdown, derive a stable ID from the source section and record its source reference without editing Markdown. Preserve those mappings on later exports of the same model. Do not infer architecture merely to satisfy required parents or links.

| Model content | OTM mapping |
| --- | --- |
| Scope, purpose, draft status, audience and review limits | `project.name`, `project.description`, and string-valued `project.attributes` |
| Components and stores | `components` with source-supported `type` and `parent` |
| Trust zones | `trustZones`; use their documented trust ratings |
| Valuable data | `assets`, with the documented ratings and component/flow references |
| Interactions | `dataflows` with existing component IDs in `source` and `destination` |
| Scenario | Root `threats` definition with ID, name, description and supplied risk ratings; attach references to applicable components or flows |
| Measure | Root `mitigations` definition with ID, description and supplied estimate; reference from affected threat instances |
| Decisions, owners, dates, assumptions, confidence, evidence and verification criteria | Keep readable context in descriptions; add string-valued `attributes` to the relevant root object for details without a dedicated OTM field |

Use names such as `appsec.decision`, `appsec.assumptions`, `appsec.evidence`, `appsec.verification`, and `appsec.sourceReference` for those additional attributes. Preserve distinctions between a proposal, an agreed plan, implementation, verification, acceptance and retirement. Preserve explicit unknowns and source conflicts; do not turn a proposed control into an implemented one. If an OTM instance state cannot express the source decision faithfully, state the mapping limit and retain the full decision in the root object's description/attributes. Do not claim importer compatibility for custom state values. A receiving tool may ignore additional attributes; local preservation is not proof of a lossless import/export cycle.

Keep priority and evidence confidence separate from OTM's numerical ratings. Preserve the source's actual risk acceptance record, including who accepted and on what basis; an OTM state alone is not acceptance. When a decision is specific to one component or flow, identify that instance in the retained decision text rather than applying it to every instance of the same threat.

Maintain a short mapping inventory while exporting: each source scenario, measure, decision, material assumption and evidence reference must have a destination or an explained limitation. Preserve relevant review and coverage gaps too. Do not discard narrative merely because OTM lacks a native field. If information cannot be represented without misleading the reader, explain the obstacle before writing a finished export. Link references from the export's directory; mark unverified references as unverified instead of silently repairing them with invented paths.

## Validate and deliver

Parse the candidate with an available safe JSON/YAML reader and validate the parsed object against the pinned schema. Use plain YAML mappings, sequences and scalars; no custom tags or executable objects. Check duplicate keys before relying on a parsed result. When both syntaxes are requested, their parsed objects must be equal. If the required reader or validator is unavailable, explain that limitation instead of installing dependencies or calling the export validated.

Also check the specification and source semantics. The released 0.2.0 schema does not fully check array items for assets and representations, numeric ranges, ID uniqueness, or reference integrity. Therefore check:

- Required fields and types for every object, including assets and representations; integer ratings in 0–100 and the exact declared OTM version.
- Unique IDs within each object collection, unambiguous references, existing flow endpoints and parents, and no component/zone parent cycles. A component's parent identifies either a component or a trust zone, not both.
- Every referenced threat, mitigation, asset and representation exists; required instance states are present and consistent with the source. Use `destination` for a flow endpoint even where an upstream example says `target`.
- The mapping inventory is complete, decisions and uncertainty remain explicit, and exported ratings are attributable. No numerical value was introduced merely to pass a check.
- The source hash still matches; all write targets, references and content satisfy the existing audience, permissions and preservation rules. Re-read existing targets before replacement and do not expose an unsanitized intermediate file.

Do not deliver a finished export if a required validation check cannot be completed or fails. Describe the particular obstacle and preserve existing files. Schema validity is only one check; it is not evidence that a third-party tool imports the file correctly. State “OTM 0.2.0; schema and reference checks passed; importer compatibility not tested” only when those checks actually ran. Name additional-attribute limitations. An importer check requires a separately authorized task and appropriate destination; do not upload a model merely to complete validation.

Link the files actually produced and state their OTM version, source model, validation performed, and material mapping or importer limits. If blocked, explain the missing input or check and any partial result without reopening the modeling interview. Keep the ordinary Markdown workflow free of export prompts and metadata. Future model updates do not silently refresh exports; regenerate them only when requested.
