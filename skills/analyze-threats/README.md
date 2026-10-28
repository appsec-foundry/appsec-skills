# Analyze Threats

Examine a feature, code change, PR/MR, or design decision for threats. You can start before code exists and ask an open question such as “What could go wrong with this export feature?”

The skill runs in your coding assistant. **AppSec Analyzer and an existing threat model are optional.**

## Install and start

Install the complete `analyze-threats` directory, including supporting files, using your assistant's skill installation mechanism. From a local checkout, copy that directory into its skill location.

Then ask your assistant in the target project:

```text
Use analyze-threats to analyze the export feature in docs/export.md.
Check whether the project has a threat model and compare relevant scenarios.
```

Replace the path with your document. The assistant reads relevant context, asks about important gaps, and returns findings. It does not change application code or the threat model.

## What you get

Each finding explains who could misuse the behavior, under which conditions, what harm follows, what protection exists, and what to change or check. Findings cite design documents, code locations, or model scenarios and are ordered by priority. The result states the examined scope and version, the model used, and important evidence gaps.

With an existing model, findings distinguish threats already covered, new threats, changed assessments, and model gaps. Planned controls remain marked as planned. Without a model, analysis continues from the supplied context.

The skill does not run attacks or prove exploitability. An empty finding list does not establish safety. Recommendations include concrete changes and checks; implementation requires a separate request.

## Examples

### A planned feature without code

```text
Use analyze-threats for the CSV export described in docs/export.md.
Tenant members should export only their own tenant's invoices.
Jobs run in a background worker. There is no implementation yet.
```

The result identifies design threats and checks, such as how the worker determines which tenant owns a job. It does not claim a confirmed code vulnerability. A description with enough context can replace a repository.

### A pull or merge request

```text
Use analyze-threats for PR 42 in this project's GitHub repository.
Analyze the changed export flow and relevant existing controls.
Compare it with the project's threat model and return findings here.
```

Use a full PR/MR URL if the repository is unclear. The assistant needs read access through a connector or Git tools; otherwise, supply a diff or local base/head comparison. Findings identify the reviewed revision and locations. The skill does not post comments or change review status.

### Compare two designs

```text
Use analyze-threats to compare the two download designs in docs/downloads.md:
links that require the recipient to sign in, and shareable links that expire.
External auditors need downloads without creating an account.
Explain the security trade-offs and recommend an option for this use.
```

The comparison addresses who can use a forwarded link, how access can be withdrawn, and how each option meets the auditor requirement. Missing information remains a question or condition on the recommendation.

### Check an existing model against a change

```text
Use analyze-threats for the changes between main and HEAD.
Our model is docs/security/threat-model.md; T-003 covers tenant exports.
Check whether its assumptions and controls still hold.
Keep the model unchanged and suggest any necessary updates.
```

If T-003 assumes signed-in recipients and the change introduces shareable links, the result explains the changed assumption and its consequences, referencing T-003.

### Use it as a reviewer

```text
Use analyze-threats as the security reviewer for this staged change.
Return prioritized findings, source locations, reviewed scope, and open questions.
Do not ask questions; mark conclusions that need more context as unresolved.
```

Where the host supports separate agents, change reviews run in an agent that receives the selected scope and sources without the author's conversation. Author claims reach it as unverified statements. Without agent support, review runs in the current conversation. The result states whether it was independent.

The skill supplies no CI service or merge gate. Automated use needs host-enforced read-only tools, source scope, execution limits, and cancellation.

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

Analysis leaves the model unchanged. To record its findings, request a focused update:

```text
Use create-threat-model to update T-003 in docs/security/threat-model.md
for the export change described in this analysis. Preserve other scenarios
and keep the worker-side tenant check marked as planned until verified.
```

If `create-threat-model` is unavailable, take the findings and scenario references to your team's modeling process.

## Company context

Supply known threats and review requirements through one of these sources:

| Form | Location |
| --- | --- |
| Project document | `docs/security/review-context.md`, or another document named in the request |
| Shared context package | A versioned directory with `review-context.md` and optional linked documents |
| Internal skill distribution | `references/company-context/review-context.md` in a complete copy of the skill; read automatically |

```text
Use analyze-threats to review the staged export change.
Use the company context package at /work/company-security/invoice-review-context.
```

The reviewer cites applicable entries, combines overlapping threats, and reports conflicts or missing evidence. Company context is optional and grants no permission to run scripts, send data, or approve a review.

See [context package distribution](references/company-distribution.md) and [organization context](references/organization-context.md).

## Optional AppSec Analyzer

Choose Analyzer for source previews, saved analysis jobs, or resume/cancel operations. It needs a separately installed compatible engine. Analysis also needs authenticated Claude CLI and authorization for source transfer, model use, and spending. Analysis in your current assistant needs no separate Claude CLI login.

```text
Use analyze-threats with AppSec Analyzer to preview the staged changes
and threat-model.md. Do not run model-backed analysis yet.
```

A local preview makes no model calls; a remote PR/MR preview still retrieves metadata and Git content. Analyzer's spending ceiling is per model call, not per job. Unsupported total-job limits are reported before execution.

The skill installs no packages. If you explicitly request an Analyzer result and the engine is unavailable, the assistant reports that limitation.

See the [workflow](SKILL.md), [requirements](requirements.md), [engine dependencies](dependencies.json), [compatibility](references/compatibility.md), and [validation cases](references/validation.md).
