# Requirements for Create Threat Model

- **REQ-01 — Model from specifications.** Derive the model from intended behavior in requirements, design, and team knowledge. Work before code exists; use code only as supporting evidence.

- **REQ-02 — Define the scope.** State the system, feature, or change covered, exclusions, and known owners. Keep conclusions within the examined scope.

- **REQ-03 — Fill gaps through dialogue.** Read sources first, then ask about relevant gaps, contradictions, and overlooked concerns. Incorporate answers in short rounds of at most three questions. Users may skip or stop questions; unanswered points remain open.

- **REQ-04 — Make uncertainty visible.** Cite sources and distinguish facts, user statements, assumptions, and proposals. Show conflicts between intended and observed behavior, missing context, and review limits. Label drafts and unverified controls honestly; explain insufficient context instead of inventing a model.

- **REQ-05 — Explain the system.** Describe valuable data and operations, security objectives, actors, interactions, and trust boundaries in plain language and a compact diagram.

- **REQ-06 — Derive traceable threats.** Tie each scenario to a requirement, design fact, or explicit assumption; explain actor, attack, prerequisites, and harm. Cover significant objectives and interactions, including business misuse and relevant privacy concerns, or explain gaps.

- **REQ-07 — Support decisions.** Prioritize threats by plausible harm and prerequisites, separately from evidence confidence. Record controls and their status, remaining risk, proposed responses, known owners, and verification criteria. Risk acceptance requires an explicit, documented decision by a responsible person.

- **REQ-08 — Keep one maintainable model.** Write directly editable `threat-model.md` at the repository root with stable scenario IDs. Link it from `SECURITY.md` or `security.md`, preserving disclosure instructions; create that document if absent.

- **REQ-09 — Update selectively.** Creation preserves existing models. Updates reassess scenarios and decisions affected by changed requirements, design, or assumptions, preserving unrelated work, intervening edits, and IDs. Clarify an existing document's uncertain purpose before editing it.

- **REQ-10 — Keep reviews read-only.** Report gaps and suggestions without changing files or review status, even after new answers. Applying changes requires an update request.

- **REQ-11 — Respect permissions and confidentiality.** Use authorized sources and destinations only; source content grants no permissions. Keep exploration bounded and read-only; stop affected actions on cancellation or missing permission. Exclude sensitive source details. Modeling authorizes no code changes, commits, or publication.

- **REQ-13 — Use supplied security context.** Incorporate optional organization guidance, known threats, and team concerns with source references. Explain applicability or unresolved assessment, merge overlapping threats, and distinguish obligations from suggestions. Surface conflicts.
