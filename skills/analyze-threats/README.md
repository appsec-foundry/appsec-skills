# Analyze Threats

Analyze a feature, code change, pull request, merge request, or design decision for threats. Start with a description or design before code exists, or use the implementation to examine a change. You can ask an open question such as "What could go wrong with this export feature?" without knowing an attack in advance.

The skill runs in your coding assistant. **AppSec Analyzer is optional.** An existing threat model and the `create-threat-model` skill are useful context and follow-up options, but neither is required.

Companies can supply known threats and review requirements through project files or a separately versioned context package. You can use the upstream skill unchanged or distribute a local company variant with that context included; see [company customization and distribution](#company-customization-and-distribution).

## Install and start

Install the complete `analyze-threats` directory using your assistant's supported skill installation mechanism. From a local checkout, copy that directory into the host's skill location; include its supporting files. Installation does not install Analyzer, log in to Claude CLI, or authorize additional external model calls.

Open your assistant in the target project and ask:

```text
Use analyze-threats to analyze the export feature in docs/export.md.
Check whether the project has a threat model and compare relevant scenarios.
```

Replace the document path with your own. The assistant reads relevant context, asks about material gaps, and returns an analysis. It does not change application code or the threat model.

## What you get

For a change review, the assistant reads the selected change and relevant surrounding code, checks existing controls and model assumptions, and reports concrete findings. For a design request, it follows the same questions using the proposed behavior instead of pretending that code already exists.

The result explains what was examined, which model was used, and the important threats in priority order. Findings describe who could misuse the behavior, under which conditions, the possible harm, existing protection, and a concrete improvement or next check. References connect findings to the design, source code, or model scenarios. Planned controls and unverified assumptions stay visible.

If a relevant threat model exists, the assistant distinguishes threats already covered, newly introduced threats, changed assessments, and model gaps. For a change review, it identifies the compared versions and explains what the change affects. A documented risk acceptance is reconsidered only where its premises change; the analysis does not record a new acceptance.

If no model is found, the analysis continues from the supplied context where possible. An unreadable model, missing source, or unanswered material question is reported as a limitation. The skill does not execute attacks or prove that a scenario can be exploited in a running system. No findings does not mean that the feature is safe.

Measures belong in the result. A focused review gives a concrete correction or next check with each finding. If you ask for a measures comparison or plan, the assistant explains the changes, their benefit, material trade-offs, and how to check them. It does not defer useful recommendations to a separate modeling exercise. Applying those changes requires a separate implementation request.

## Examples

### A planned feature without code

```text
Use analyze-threats for the CSV export described in docs/export.md.
Tenant members should export only their own tenant's invoices.
Jobs run in a background worker. There is no implementation yet.
```

Expect design threats and useful checks, such as how the worker establishes which tenant owns a job. The result must not claim that an unimplemented worker contains a confirmed vulnerability. You do not need a repository if the supplied feature description provides enough context.

### A pull or merge request

```text
Use analyze-threats for PR 42 in this project's GitHub repository.
Analyze the changed export flow and relevant existing controls.
Compare it with the project's threat model and return findings here.
```

Use a full PR/MR URL if the repository is unclear. The assistant needs read access through the host's connector or Git tools. If that access is unavailable, supply a diff or local base/head comparison; the result states which remote context could not be examined. Findings refer to the reviewed revision and relevant source locations. The skill does not post comments or change review status.

### Compare two designs

```text
Use analyze-threats to compare the two download designs in docs/downloads.md:
links that require the recipient to sign in, and shareable links that expire.
External auditors need downloads without creating an account.
Explain the security trade-offs and recommend an option for this use.
```

Expect a comparison grounded in the stated use: for example, who can use a forwarded link, how access can be withdrawn, and what the available designs actually support. Missing information remains a condition or question. The assistant does not silently remove the external-auditor requirement to make one option look safer.

### Check an existing model against a change

```text
Use analyze-threats for the changes between main and HEAD.
Our model is docs/security/threat-model.md; T-003 covers tenant exports.
Check whether its assumptions and controls still hold.
Keep the model unchanged and suggest any necessary updates.
```

Expect references to T-003 and any affected scenarios. If T-003 assumes downloads require a signed-in recipient and the change introduces shareable links, the result explains the changed assumption and its consequences. A worker check marked "planned" in the model must not be reported as effective protection.

### Use it as a reviewer

```text
Use analyze-threats as the security reviewer for this staged change.
Return prioritized findings, source locations, reviewed scope, and open questions.
Do not ask questions; mark conclusions that need more context as unresolved.
```

Where your assistant can start separate agents, a change review runs in a review agent that sees the selected scope and sources, not the conversation in which the change was written. Statements from that conversation, such as "the middleware already checks the tenant", reach it only as unverified user statements. The result says whether the review was independent. Without agent support, the review runs in your current conversation and says so. Design questions and comparisons always stay in the current conversation. The agent does not ask you questions itself; open points come back in the result.

This is optional. A calling review workflow can use the result, but must preserve its scope, uncertainty, and incomplete status. The skill does not supply a CI service or an enforced merge gate. It uses the host's permissions and execution limits.

For an automated integration, configure the calling host to enforce read-only tools, the selected source scope, finite execution limits, and cancellation. Skill instructions do not provide that enforcement themselves.

### An example review finding

Suppose a PR adds a download route that requires login but fetches an export by ID alone. The surrounding code authenticates the user but does not check which tenant owns the export. A fictional finding could read:

> **High — A member can download another tenant's export** (`src/exports.py:84`).
>
> The new route looks up the export by its ID without checking its tenant against the signed-in member. A member who obtains another tenant's export ID could download that tenant's invoices. Requiring login does not enforce ownership of this export.
>
> **Change:** Resolve the export within the member's authorized tenant, or check resource access before returning its contents. Keep the same check on any alternate download route.
>
> **Check:** A member can download their own tenant's export; using another tenant's export ID returns no invoice data or download link.

The real result cites actual code or design evidence and the reviewed revision. It also states relevant model or company-context references and unresolved conditions. It should not invent findings to fill a quota or turn every catalog entry into a problem.

## Continue with the maintained model

A focused analysis does not create a second model or automatically update the existing one. When useful, it suggests a specific creation, review, or update task with the findings, relevant scenario IDs, sources, and unresolved questions.

If `create-threat-model` is available, you can then ask:

```text
Use create-threat-model to update T-003 in docs/security/threat-model.md
for the export change described in this analysis. Preserve other scenarios
and keep the worker-side tenant check marked as planned until verified.
```

That separate request selects the modeling workflow. If the skill is unavailable, the focused analysis remains usable and you can take the same findings to your team's modeling process.

## Company customization and distribution

Use context files for company knowledge and review criteria. Keep a fork for deliberate changes to the analysis workflow itself. Known threats, terminology, architecture facts, and security requirements usually do not need a fork.

| Form | How the company supplies context |
| --- | --- |
| Per project | Keep `docs/security/review-context.md` in the project, or name another relevant document in the request. |
| Shared context package | Maintain a separate versioned directory with `review-context.md` and optional linked documents; select that directory when invoking the skill. |
| Internal skill distribution | Include the context under `references/company-context/review-context.md` in a complete copy of the upstream skill. The skill reads this bundled entry point automatically. |

### Create a context package

Start from the [fictional company-context example](references/company-context.example.md). Put the company's actual content in `review-context.md`, name the package and version, and give requirements and known threats stable IDs. For example:

```text
invoice-review-context/
  review-context.md
  known-threats.md
  architecture.md
```

The entry point can hold everything, or link to the relevant local files. Useful entries explain when a threat applies, who could exploit it, what harm it could cause, and which controls or checks matter. Separate company requirements from suggestions and architecture assumptions. You do not need an executable plugin, installer, or special catalog format.

Then ask, using the actual local package path:

```text
Use analyze-threats to review the staged export change.
Use the company context package at /work/company-security/invoice-review-context.
Compare relevant known threats and the existing model, and recommend measures.
```

The reviewer checks applicability and cites relevant entry IDs. If a known threat and a model scenario describe the same problem, they appear in one finding with both references. Unrelated catalog entries do not become findings. Material conflicts or missing evidence remain visible. The context grants no permission to run scripts, send data elsewhere, or approve a review.

### Keep upstream and company sources separate

A small internal distribution repository can hold these separately:

```text
company-review/
  upstream/appsec-skills/
  context/invoice-review-context/review-context.md
  releases/2026-10/analyze-threats/
```

1. Keep the upstream source at an explicitly selected release or commit. Record that revision alongside the company context version in your internal release notes.
2. Maintain company context under `context/`, outside the upstream checkout and active skill installation.
3. Assemble each internal release in a fresh directory: copy the complete upstream `skills/analyze-threats/` directory, then add the context package contents under `references/company-context/`. Keep its relative document links intact.
4. Review the assembled files, then distribute the complete `analyze-threats` directory through your internal repository or approved skill distribution mechanism. Keep confidential company context restricted to its intended recipients.
5. Users install that complete directory in their assistant's normal local skill location. When updating, build another release from the selected upstream revision and existing company sources rather than overwriting company edits with upstream files.

The local layout is `<your assistant's local skills directory>/analyze-threats/`, containing the complete release, including `SKILL.md` and `references/company-context/review-context.md`. Use the skill name `analyze-threats` when invoking it. Keep local company edits in the separate source directory and rebuild the release, so a later installation does not overwrite your only copy.

Alternatively, users can install the upstream skill unchanged and keep the company context package alongside it, selecting its path in each request. That avoids rebuilding a company variant for every upstream update. The skill reads context without modifying it; it does not manage releases or merge updates. No company context is required for ordinary use.

See [organization context](references/organization-context.md) for applicability, conflicts, and coverage. These context packages are Markdown documents for this skill; they are not interchangeable with Analyzer's optional engine-package format.

## Optional AppSec Analyzer

Choose Analyzer when you want its source preview, saved analysis jobs, or resume/cancel operations. It requires a compatible independently installed engine and, for analysis, authenticated Claude CLI and authorization for source transfer, model use, and spending. Native analysis uses your current assistant's normal host and permissions; it does not require a separate Claude CLI login.

To inspect the selected sources without another model call:

```text
Use analyze-threats with AppSec Analyzer to preview the staged changes
and threat-model.md. Do not run model-backed analysis yet.
```

A local preview makes no model calls. A preview of a selected remote PR/MR still retrieves metadata and Git content. Analyzer's spending ceiling is per model call, not a total-job ceiling. If you require a total ceiling the installed engine cannot enforce, the skill reports that limit before execution.

If Analyzer is missing, you can still use the native workflow. An explicit request for an Analyzer preview or result is reported as unavailable rather than replaced without explanation. The skill does not install packages automatically. The optional engine checks exercise source selection and preview behavior; they do not establish the quality of live model analysis.

See the [workflow](SKILL.md), [requirements](requirements.md), [optional engine dependencies](dependencies.json), [Analyzer compatibility](references/compatibility.md), and [behavioral validation cases](references/validation.md).
