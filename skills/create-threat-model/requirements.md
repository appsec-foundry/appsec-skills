# Requirements for Create Threat Model

This document defines what users should be able to expect from the skill. It is the basis for developing and reviewing the skill; it is not a requirements document for the application being modeled.

These requirements capture the essential behavior of the existing skill implementation:

- [SKILL.md](SKILL.md): creation, updates, reviews, questions, and execution boundaries.
- [Model guide](references/model-guide.md): system description, threat scenarios, controls, and decisions.
- [Security context](references/security-context.md): selected organization guidance and known threats.

The original AppSec Advisor concept “Threat modeling from requirements and design” informed the skill's design. Future ideas from that concept are not automatically current requirements. [README.md](README.md) explains how to use the skill.

## Core requirements

- **TM-01 — Work before code exists.** Create a useful threat model from requirements, design documents, and team knowledge. Source code may help clarify the design, but must not be a prerequisite. If documents are unavailable, a description from the user can provide the starting point.

- **TM-02 — Make the scope clear.** State which system, feature, or change is being modeled, what is excluded, and who is responsible where known. A review of one feature must not imply that the whole application has been reviewed.

- **TM-03 — Read first, ask useful questions.** Use the available documents before asking users to repeat known information. Ask at most three questions per round, focusing on answers that could change the model. Users can skip questions, stop the dialogue, or request a draft without questions.

- **TM-04 — Be clear about what is known.** Identify the sources behind the model and distinguish documented facts, user statements, assumptions, and proposals. State whether the model describes the current system or a proposed design; code observations must not silently replace intended behavior. Keep contradictions and unanswered questions visible. If there is too little information for a meaningful model, explain what is missing instead of inventing a system or producing an empty model.

- **TM-05 — Explain what needs protection.** Identify valuable data and operations and their security objectives: what must stay confidential, correct, or available. Describe relevant actors, important interactions, and trust boundaries: places where identity, permissions, ownership, or control changes. Use a compact diagram with supporting text so the team can check the system description.

- **TM-06 — Describe threats specific to the system.** Explain who could violate a security objective, through which interaction, under what conditions, and with what consequence. Use STRIDE as a prompt for common technical threat types, alongside misuse of business workflows. Include multi-step attacks and privacy concerns where relevant. Avoid generic threat lists and unsupported vulnerability claims.

- **TM-07 — Make treatment actionable.** Connect each relevant scenario to safeguards, remaining exposure, a proposed response, responsibility where known, and a practical verification criterion. Explain priority using plausible harm and prerequisites, separately from confidence in the evidence. Distinguish proposed, planned, reported, and verified controls. Record risk acceptance only as an explicit decision with a responsible person, rationale, scope, remaining exposure, and a review date or trigger.

- **TM-08 — Keep one maintainable model.** Write the model to `threat-model.md` at the target repository root. Give scenarios stable IDs and link the model from the existing `SECURITY.md` or `security.md`, preserving disclosure instructions. If no security document exists, create a short one with the model link. Teams must be able to edit the Markdown directly.

- **TM-09 — Preserve existing work.** A creation request must not replace an existing model. An update changes the affected parts, integrates new features into the same model, and preserves unrelated human edits and scenario IDs. Reconsider decisions when their assumptions change. If an existing document's purpose is unclear, clarify its use before modifying it; without an answer, preserve it.

- **TM-10 — Keep reviews read-only.** A review reports gaps and suggested changes without editing the model, its review status, or the security document. New answers during the review do not authorize writes. Applying suggestions requires an update request.

- **TM-11 — Respect access and confidentiality.** Use only sources and write locations authorized for the task. Content found in documents must not authorize commands or additional access. Optional code exploration stays read-only and within defined limits; stop affected actions on cancellation or missing permission. Preserve intervening edits when writing. Keep credentials, personal records, and restricted incident details out of the shared model. Modeling does not authorize code changes, commits, or publication.

- **TM-12 — Report an honest result.** Summarize what was modeled or reviewed, which files changed, and which decisions remain open. Distinguish a draft from an actual team review. Report inaccessible sources and exploration limits. Neither a generated document nor a passing format check proves that coverage or controls are sufficient.

- **TM-13 — Use selected security context explicitly.** Consider supplied organization guidance, known threats, and team concerns with their source references. Record whether each case applies, does not apply with a reason, is unresolved, or has not been examined. Merge overlapping scenarios without losing their sources. Keep obligations separate from suggestions, and surface conflicts. This context is optional; the skill must also work without it.

## Checking changes

Check the requirements affected by a change using small examples. The most important cases are:

- Requirements and a design produce a specific model without source code; insufficient context produces an explanation of the gaps.
- Documented answers avoid unnecessary questions; skipped questions remain unresolved.
- A focused update preserves unrelated content and stable IDs; changed assumptions reopen affected decisions.
- A review leaves the model and security document unchanged, including when new information is supplied.
- An instruction hidden in a source cannot trigger commands, unrelated access, or additional writes.
- A proposed or user-reported control is not presented as verified; a supplied threat is not dismissed just because code is unavailable.

For documentation-only changes, check clarity, links, and consistency. Record what was actually checked; these examples are acceptance criteria, not a claim that tests have passed.

## Extending these requirements

Keep the IDs stable. Add the next unused `TM-` number for a new user need; do not renumber existing requirements. Describe the expected result in plain language and add a practical check when useful.

Change requirements when the intended behavior changes, with a short rationale in the change description. Keep the skill instructions, references, and user guide consistent. Do not rewrite requirements merely to match an implementation mistake. Put technical procedures and tunable defaults in `SKILL.md` or its references.

New integrations, automated execution, or package formats need their own requirements before implementation. Their mention in the original concept does not make them part of the current skill.
