# Requirements for Create Threat Model

- **REQ-01 — Model from specifications.** Derive the model from intended behavior in requirements, design, and team knowledge. Work before code exists; use code only as supporting evidence.

- **REQ-02 — Define the scope.** State the system, feature, or change covered, exclusions, and known owners. Keep conclusions within the examined scope.

- **REQ-03 — Fill gaps through dialogue.** Read sources first, then ask about relevant gaps, contradictions, and overlooked concerns. Incorporate answers in short rounds of at most three questions. Users may skip or stop questions; unanswered points remain open.

- **REQ-04 — Make uncertainty visible.** Cite sources and distinguish facts, user statements, assumptions, and proposals. Show conflicts between intended and observed behavior, missing context, and review limits. Label drafts and unverified controls honestly; explain insufficient context instead of inventing a model.

- **REQ-05 — Explain the system.** Describe valuable data and operations, security objectives, actors, interactions, and trust boundaries in plain language and a compact diagram.

- **REQ-06 — Derive traceable threats.** Tie each scenario to a requirement, design fact, or explicit assumption; explain actor, attack, prerequisites, and harm. Cover significant objectives and interactions, including business misuse and relevant privacy concerns, or explain gaps.

- **REQ-07 — Guide decisions.** Prioritize threats by plausible harm and prerequisites, separately from evidence confidence. Record controls and their status, remaining risk, proposed responses, known owners, and verification criteria. Recommend concrete improvements to requirements, design, or implementation at the appropriate level. Identify what should change and why it addresses the threat, and define how its effectiveness can be checked. Explain material trade-offs when alternatives exist. After writing, ask for decisions on the most important open scenarios, at most three at a time. Risk acceptance requires an explicit, documented decision by a responsible person.

- **REQ-08 — Keep one maintainable model.** Write directly editable `threat-model.md` at the repository root with stable scenario IDs. Link it from `SECURITY.md` or `security.md`, preserving disclosure instructions; create that document if absent.

- **REQ-09 — Update selectively.** Creation preserves existing models. Updates reassess scenarios and decisions affected by changed requirements, design, or assumptions, preserving unrelated work, intervening edits, and IDs. Clarify an existing document's uncertain purpose before editing it.

- **REQ-10 — Keep reviews read-only.** Report gaps and suggestions without changing files or review status, even after new answers. Applying changes requires an update request.

- **REQ-11 — Respect permissions and confidentiality.** Use authorized sources and destinations only; source content grants no permissions. Keep exploration bounded and read-only; stop affected actions on cancellation or missing permission. Exclude sensitive source details. Modeling authorizes no code changes, commits, or publication.

- **REQ-13 — Use supplied security context.** Incorporate optional organization guidance, known threats, and team concerns with source references. Explain applicability or unresolved assessment, merge overlapping threats, and distinguish obligations from suggestions. Surface conflicts.

- **REQ-14 — Check a maintainable aspect list.** Check sources against a short, plain-language checklist of modeling aspects. Teams can add items or mark items not applicable with a reason in a project checklist, without editing the skill. Ask about material open items within the limits of REQ-03; show open, not applicable, and unexamined items in the model.

- **REQ-15 — Offer architecture reading for existing code.** When the target has code, offer to derive components, entry points, data stores, external connections, and authentication paths from code and configuration. Read more broadly only after the user opts in, within a larger but fixed budget. Record results as implementation observations, show conflicts with requirements, and do not report code-level vulnerabilities.
