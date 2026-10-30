# Audience and destination

Read this guide before the opening system summary. It applies to creation, updates, reviews, and exports.

## Establish the audience

The audience is established when the request explicitly specifies it, by project guidance, or, for updates and reviews, by an existing model unless its audience is provisional or unresolved.

- Name a reused audience and its basis briefly in the opening or system summary, so the user can correct it without an extra round.
- Local operation, synthetic data, repository visibility, and an earlier fallback to "internal" do not establish the audience.
- For updates and reviews, ask again only if information is missing, contradictory, or indicates a possible change.

If it is not established, make this the first question after initial source reading, in the user's language:

> Who should be able to read this threat model?

- Internal — your team and other authorized people.
- Public — anyone.
- Not decided yet.

Explain briefly that the answer determines which security details the document can contain, independently of whether the application is internally or publicly reachable. The question counts toward the three-question limit; purpose, data, and consequence questions must not displace it. Honor no-questions mode and previously skipped questions; a fallback is not a reason to omit an otherwise required audience question.

Clarify a materially unclear reader group or conflict before sharing confidential system summaries or scenarios.

| Audience | Content |
| --- | --- |
| Internal | Confidential unresolved issues, missing controls, attack prerequisites, and architecture details needed for risk treatment, when the intended repository readers may receive them. Internal status is not permission to copy every source detail. |
| Public | Only information suitable for public disclosure. Abstract confidential details while preserving the threat mechanism, impact, uncertainty, and needed response. Do not present an omitted detail as an absent risk. |

## Check the destination

Before the first write containing confidential findings, establish from authorized context that the destination's readers may receive them. If this is unclear, ask once, within the three-question limit:

> May everyone who can read this repository also see confidential security findings?

Offer "Yes," "No," and "Unknown," and explain that "No" or "Unknown" means omitting those details. Choosing "internal," a private repository, or an "internal" notice alone does not establish suitability. This check authorizes no external access or permission changes.

## Fallback rules

If a necessary answer is missing, including a skipped question or no-questions mode:

- Retain the established audience or the existing provisional default, or use **internal** provisionally for a new model. The default is not user confirmation and does not become an established audience in a later update or review.
- Record the unresolved audience, access, or disclosure question.
- Omit the affected confidential details and explain the limitation without exposing them. Continue with suitable content.
- Do not silently change the destination, create another model, convert an existing model's audience, or remove unrelated content.

If existing confidential content conflicts with repository access, report the mismatch without repeating it and leave the affected write pending clarification.

## Audience notice

Place a visible Markdown blockquote with a bold uppercase heading immediately below the title, before the overview.

- Write it in the model's language (REQ-17), preserving the meaning of the templates below.
- Use the established reader group; never invent one. Write in the third person: "Project team and other authorized people," not "your team."
- Use established project classification labels when required, without weakening the handling instruction.
- Keep draft/review status in the overview. A notice neither restricts access nor grants permission to commit, share, or publish.
- During updates, preserve an equivalent notice. Revisit it only when the request, repository access, or source restrictions change.
- During review, propose missing or corrected notices without editing the document.

Internal model with an established audience:

```markdown
# Threat Model

> **INTERNAL — NOT FOR PUBLIC DISTRIBUTION**
>
> This document may contain confidential information about unresolved security issues.
>
> **Intended readers:** [Established reader group]
> Store and share only where access is appropriate for these readers.
```

Unresolved readers or destination, only after the content check confirms the affected details are omitted. A new notice cannot make existing confidential content safe.

```markdown
# Threat Model

> **INTERNAL — NOT FOR PUBLIC DISTRIBUTION**
>
> **AUDIENCE OR REPOSITORY ACCESS UNCONFIRMED — CONFIDENTIAL DETAILS OMITTED**
>
> Resolve the intended readers and repository access before adding confidential details.
```

Public model:

```markdown
# Threat Model

> **PUBLIC USE INTENDED — NOT A PUBLICATION APPROVAL**
>
> This version is intended for public readers and must exclude confidential details.
> This notice does not authorize publication.
```

## Audience example

Fictional case: a confidential design note says the `settlement-retry` worker does not recheck approval after a recipient change. The general payment-edit threat is suitable for public disclosure.

| Situation | Handling |
| --- | --- |
| Not established, authorized repository | Ask first. If internal and the destination is suitable, name the worker, the missing check, and the prerequisites. Cite the note only if the reference suits those readers. |
| Already established | State it and its basis; do not ask again. |
| Question skipped | Internal provisionally, unresolved audience recorded, finding omitted, unconfirmed notice. Do not treat the skip as an internal-use decision or repeat the question without new evidence. |
| Internal chosen, repository readers unknown | Clarify the destination. Until resolved, omit the finding and use the unconfirmed notice. |
| Public | Public notice. Describe the risk that edits can invalidate an approval and recommend rechecking approved details. State that implementation evidence is omitted and the risk remains unresolved. |
| No audience, access unknown, no questions | Internal default, finding omitted before writing, unconfirmed notice. Claim no reader group or publication approval. |
| Internal requested, destination public | Withhold the detail and explain the mismatch. Do not write it for later cleanup. If an abstraction cannot support a useful model, leave the write pending. |

No version includes access tokens from source URLs or unrelated customer records.
