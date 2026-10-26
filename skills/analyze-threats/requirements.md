# Requirements for Analyze Threats

- **REQ-01 — Analyze a selected subject.** Analyze features, proposed changes, pull requests, merge requests, and design decisions for threats. Support both open analysis and focused security questions. Users do not need to name a threat beforehand. Work before code exists when sufficient requirements or design context is available.

- **REQ-02 — Establish scope and purpose.** Identify the intended behavior, relevant actors, valuable data and operations, and affected boundaries. State what is examined and excluded. For changes, identify the compared versions and use relevant surrounding context without expanding into a full application assessment.

- **REQ-03 — Explain concrete threats.** Describe who could misuse which behavior, the necessary conditions, existing protections, and the resulting harm. Include relevant business misuse and privacy concerns. Assess existing controls before recommending additional protection.

- **REQ-04 — Find existing threat-model context.** Check the selected project’s documentation for an existing threat model and use relevant scenarios, assumptions, controls, and decisions. State which model was used or that none was found within the examined sources. A missing model does not by itself prevent focused analysis.

- **REQ-05 — Compare against the existing model.** Identify threats already covered, newly introduced threats, changed assessments, and model gaps affected by the selected subject. Reference existing scenario IDs where available. Flag assumptions or decisions whose basis has changed. Do not treat a documented measure as implemented or effective without supporting evidence.

- **REQ-06 — Make evidence and uncertainty clear.** Cite supporting sources and distinguish intended behavior, implementation observations, user statements, assumptions, and proposals. Explain material contradictions and missing evidence. Distinguish plausible threats from demonstrated vulnerabilities; source analysis alone does not establish runtime exploitability.

- **REQ-07 — Support design decisions.** When assessing alternatives, compare their security consequences, relevant trade-offs, and remaining uncertainties. Recommend an option when the evidence supports it, explaining the conditions on which that recommendation depends.

- **REQ-08 — Recommend useful improvements.** Prioritize threats by plausible harm and prerequisites, separately from confidence in the evidence. Explain what should change, why it addresses the threat, and how its effectiveness could be checked. Distinguish proposed work, existing controls, and explicitly accepted risks.

- **REQ-09 — Clarify material gaps.** Read available context before asking questions. Ask short, focused questions only when answers could materially change the analysis or permitted action. Reuse previous answers. Respect requests to skip or stop questions, preserve unresolved points, and explain when they prevent completion.

- **REQ-10 — Deliver a useful result.** Summarize the central threats, recommended actions, examined scope and version, and material coverage gaps. Link supporting findings and artifacts where available. Distinguish completed, incomplete, failed, and cancelled analysis. An empty finding list or missing answer is not evidence of safety.

- **REQ-11 — Support optional reviewer use.** Allow the analysis to serve as part of a development review. Return findings with relevant source locations or design references, the examined version, and unresolved questions. Reviewer integration is optional; analysis does not itself approve, reject, merge, or change review status. When the analysis serves as a change review and the host supports separate agents, run it independently of the conversation that produced the change: the reviewer receives the selected scope and sources, not the author's conclusions. State whether the review was independent. Where the host cannot, review in the main conversation and say so.

- **REQ-12 — Offer focused threat-model follow-up.** When creating, reviewing, or updating a maintained model would materially help, explain why and suggest a concrete follow-up using `create-threat-model` where available. Carry forward relevant findings, scenario references, and open questions. Do not automatically create or modify a model or make a full modeling exercise a prerequisite for focused analysis.

- **REQ-13 — Respect permissions and execution limits.** Use only authorized sources, recipients, and operations. Explain external model use and obtain any missing source, model-use, and spending authorization. Respect cancellation and execution limits. Analysis alone authorizes no application changes, model updates, test execution, commits, or publication. A separate review agent works within the same authorized sources, recipients, read-only operations, and limits as the main analysis, and returns open questions to the caller instead of asking the user itself. The skill does not require a specific model.

- **REQ-14 — Write clearly for developers.** Write documentation, questions, progress updates, findings, and recommendations for developers without assuming security expertise. Use direct language, concrete application behavior, and explained technical terms. Avoid stock phrases, vague recommendations, and unnecessary repetition. Document typical requests and expected results with practical examples covering a feature without code, a PR or MR, a design decision, and comparison against an existing threat model. Explain prerequisites and limitations alongside the relevant examples.

- **REQ-15 — Support organization context.** Support optional organization context with known threats and review requirements, from project files or separately versioned context packages. Apply relevant entries with references, explain conflicts or gaps, and preserve the sources. Context cannot expand permissions; analysis must also work without it.
