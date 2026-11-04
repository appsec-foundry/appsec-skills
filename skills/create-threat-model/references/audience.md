# Audience and destination

Read this guide in phase 1, before showing confidential details. It applies to creation, updates, reviews, exports, and the conversation itself.

## What is confidential

A detail is confidential when it describes an unresolved weakness specifically enough to exploit it, names a missing control together with its prerequisites, or comes from a source marked as restricted (REQ-11). The threat mechanism, its impact, the uncertainty, and the needed response are not confidential by themselves; they can be stated for any audience at a level that does not identify the exploitable gap.

## Establish the audience

The audience is established when the request specifies it, by project guidance, or, for updates and reviews, by an existing model whose audience is not provisional. Name a reused audience and its basis briefly in the system summary so the user can correct it. Local operation, synthetic data, repository visibility, and an earlier fallback to "internal" do not establish it.

If it is not established, ask first, in the user's language:

> Who should be able to read this threat model?

- Internal — your team and other authorized people.
- Public — anyone.
- Not decided yet.

Explain briefly that the answer determines which security details the document can contain, independently of whether the application is reachable internally or publicly. The question counts toward the three-question limit.

| Audience | Content |
| --- | --- |
| Internal | Confidential unresolved issues, missing controls, attack prerequisites, and architecture details needed for risk treatment, when the intended repository readers may receive them. Internal status is not permission to copy every source detail. |
| Public | Only information suitable for public disclosure. Abstract confidential details while preserving the mechanism, impact, uncertainty, and needed response. Do not present an omitted detail as an absent risk. |

## Check the destination

Before the first write containing confidential findings, establish from authorized context that the destination's readers may receive them. If unclear, ask once:

> May everyone who can read this repository also see confidential security findings?

Offer "Yes," "No," and "Unknown," and explain that "No" or "Unknown" means omitting those details. Choosing "internal," a private repository, or an internal notice alone does not establish suitability.

## Fallback

If a necessary answer is missing, including a skipped question or no-questions mode: keep the established audience or the existing provisional default, or use **internal** provisionally for a new model; record the unresolved question; omit the affected confidential details and explain the limitation without exposing them. The default is not user confirmation and does not become an established audience in a later update. Do not change the destination, create another model, or convert an existing model's audience. If existing confidential content conflicts with repository access, report the mismatch without repeating the content and leave the affected write pending.

## Audience notice

Place a Markdown blockquote with a bold uppercase heading immediately below the title, in the model's language, in the third person. Use established project classification labels when required without weakening the handling instruction. The notice neither restricts access nor grants permission to commit, share, or publish. During updates, preserve an equivalent notice; during review, propose corrections without editing.

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

Unresolved readers or destination, only after the content check confirms the affected details are omitted:

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

## Example

A confidential design note says the `settlement-retry` worker does not recheck approval after a recipient change. The general payment-edit threat is suitable for public disclosure.

| Situation | Handling |
| --- | --- |
| Not established, authorized repository | Ask first. If internal and the destination is suitable, name the worker, the missing check, and the prerequisites. |
| Question skipped, or no-questions mode | Internal provisionally, unresolved audience recorded, finding omitted, unconfirmed notice. |
| Internal chosen, repository readers unknown | Clarify the destination. Until resolved, omit the finding and use the unconfirmed notice. |
| Public | Public notice. Describe that edits can invalidate an approval and recommend rechecking approved details. State that implementation evidence is omitted and the risk remains unresolved. |
| Internal requested, destination public | Withhold the detail and explain the mismatch. Do not write it for later cleanup. |

No version includes access tokens from source URLs or unrelated customer records.
