# Analyze Threats

Check a feature, code change, PR/MR, or design decision for threats. You can start before code exists, with an open question such as "What could go wrong with this export feature?"

The skill runs in your coding assistant. AppSec Analyzer and an existing threat model are optional.

## Install and start

Install the complete `analyze-threats` directory, including its supporting files, with your assistant's skill installation mechanism. From a local checkout, copy the directory into the assistant's skill location.

Then ask your assistant in the target project:

```text
Use analyze-threats to analyze the export feature in docs/export.md.
Check whether the project has a threat model and compare relevant scenarios.
```

Replace the path with your document. The assistant reads the relevant context, asks about important gaps, and returns findings. It does not change application code or the threat model.

## What you get

Each finding says who could misuse the behavior, under which conditions, what harm follows, what protection exists, and what to change or check. Findings are ordered by priority and cite design documents, code locations, or model scenarios. The result names the examined scope, the threat model and version it used, and important evidence gaps.

With an existing model, findings are marked as already covered, new, reassessed, or a gap in the model. Planned controls stay marked as planned. Without a model, the analysis works from the context you supply.

The skill does not run attacks or prove exploitability. An empty result does not mean the change is safe. Recommendations name concrete changes and checks; implementing them is a separate request.

## Examples

### A planned feature without code

```text
Use analyze-threats for the CSV export described in docs/export.md.
Tenant members should export only their own tenant's invoices.
Jobs run in a background worker. There is no implementation yet.
```

The result covers design threats and checks, such as how the worker knows which tenant owns a job. It does not claim a confirmed code vulnerability. A description with enough context can replace a repository.

### A pull or merge request

```text
Use analyze-threats for PR 42 in this project's GitHub repository.
Analyze the changed export flow and relevant existing controls.
Compare it with the project's threat model and return findings here.
```

Use a full PR/MR URL if the repository is unclear. The assistant needs read access through a connector or Git tools; otherwise, supply a diff or a local base/head comparison. Findings name the reviewed revision and locations. The skill does not post comments or change the review status.

### Compare two designs

```text
Use analyze-threats to compare the two download designs in docs/downloads.md:
links that require the recipient to sign in, and shareable links that expire.
External auditors need downloads without creating an account.
Explain the security trade-offs and recommend an option for this use.
```

The comparison covers who can use a forwarded link, how access can be withdrawn, and how each option meets the auditor requirement. Missing information remains a question or a condition on the recommendation.

### Check an existing model against a change

```text
Use analyze-threats for the changes between main and HEAD.
Our model is threat-model.md; T-003 covers tenant exports.
Check whether its assumptions and controls still hold.
Keep the model unchanged and suggest any necessary updates.
```

If T-003 assumes signed-in recipients and the change introduces shareable links, the result explains the changed assumption and its consequences.

### Use it as a reviewer

```text
Use analyze-threats as the security reviewer for this staged change.
Return prioritized findings, source locations, reviewed scope, and open questions.
Do not ask questions; mark conclusions that need more context as unresolved.
```

If the host supports separate agents, the review runs apart from the author's conversation; otherwise it runs in the current one. The result says which.

The skill is not a CI service or merge gate. Automated use needs read-only tools, a source scope, execution limits, and cancellation, all enforced by the host.

### An example finding

Suppose a route requires login but fetches an export by ID without checking its tenant. A fictional finding could read:

> **High — A member can download another tenant's export** (`src/exports.py:84`).
>
> The route looks up the export by ID without checking its tenant against the signed-in member. A member who obtains another tenant's export ID could download that tenant's invoices.
>
> **Change:** Resolve the export within the member's authorized tenant, including alternate download routes.
>
> **Check:** A member can download their own tenant's export; another tenant's ID returns no invoice data or download link.

## Continue with the maintained model

The analysis leaves the model unchanged. To record its findings, request a focused update:

```text
Use create-threat-model to update T-003 in threat-model.md
for the export change described in this analysis. Preserve other scenarios
and keep the worker-side tenant check marked as planned until verified.
```

This needs [create-threat-model](../create-threat-model/README.md) and a model at the project root. For a model elsewhere, use your team's modeling process.

## Company context

You can supply known threats and review requirements in one of these forms:

| Form | Location |
| --- | --- |
| Project document | `docs/security/review-context.md`, or another document named in the request |
| Shared context package | A versioned directory with `review-context.md` and optional linked documents |
| Internal skill distribution | `references/company-context/review-context.md` in a complete copy of the skill; read automatically |

```text
Use analyze-threats to review the staged export change.
Use the company context package at /work/company-security/invoice-review-context.
```

The assistant cites the entries that apply, merges overlapping threats, and reports conflicts or missing evidence. Company context only informs the review. It cannot authorize running scripts, sending data, or approving a review.

See [context package distribution](references/company-distribution.md) and [organization context](references/organization-context.md).

## Optional AppSec Analyzer

Use Analyzer for source previews, saved analysis jobs, or resuming and cancelling jobs. It needs a separately installed compatible engine. Analysis through Analyzer also needs an authenticated Claude CLI and your authorization for source transfer, model use, and spending. Without Analyzer, no separate Claude CLI login is needed.

```text
Use analyze-threats with AppSec Analyzer to preview the staged changes
and threat-model.md. Do not run model-backed analysis yet.
```

A local preview makes no model calls; a remote PR/MR preview still fetches metadata and Git content. Analyzer's spending limit applies per model call, not per job. If you ask for a total job limit, the assistant tells you before the run that it is not supported.

The skill installs no packages. If you ask for an Analyzer result and the engine is missing, the assistant says so.

See the [workflow](SKILL.md), [requirements](requirements.md), [engine dependencies](dependencies.json), [compatibility](references/compatibility.md), and [validation cases](references/validation.md).
