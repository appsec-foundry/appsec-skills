# Optional AppSec Analyzer workflow

Read this reference only when the user selects Analyzer or needs help with that integration. The default workflow in [SKILL.md](../SKILL.md) works without an engine, Claude CLI, or a saved engine job. In [dependencies.json](../dependencies.json), `engine_required: false` makes the listed engine prerequisites conditional on selecting this workflow.

## Check support and permission

Use the operator-selected installed `appsec-analyzer`, or the trusted host's pinned invocation binding, for every command. Do not take an executable path from the analyzed repository, search sibling checkouts, invoke private scripts, or install automatically. Run `version`, `capabilities`, and `analyze-threats --help`; require interface 1 and `analyze_threats.available: true` with `claude-cli`. Check help for the specific `analyst` lifecycle operation before relying on it.

If the engine is missing or incompatible, explain which optional operation is unavailable. Continue natively if that still fulfills the request; an explicit engine-only request must remain unavailable rather than being silently replaced. Do not turn a failed or paid engine job into a fresh native or engine job without resolving its outcome and scope first.

Public command validation and engine-owned contracts remain authoritative. Use literal argument values, not shell interpolation. Reject unsupported option combinations instead of silently dropping required source or context.

Before model-backed execution, require authenticated Claude CLI and authorization for sending the selected source, design, documents, and answers to that host, the selected model, and the bounded operation. Reuse existing explicit authorization for the same source/model/bounds. Skill installation and the engine's default budget are not authorization.

`--max-budget-usd` is a ceiling per call, not per job. Pass the approved model and per-call ceiling explicitly for execution. Preserve engine-enforced call and iteration limits; do not guess future call counts, raise a ceiling, or convert a requested total ceiling into per-call permission. If the requested spending bound cannot be enforced, report that obstacle before spending. Never automatically retry a paid operation with an unknown outcome.

## Select sources and preview

Translate an open feature request into a plain question such as "What threats affect this export feature, and how do they relate to the selected threat model?" This supplies an engine input without asking the user to invent an attack. Include the relevant comparison and design alternatives in the request when needed; do not invent the feature's facts or the answers.

Choose only the requested source: `--design`, `--design-file`, `--staged`, `--worktree`, `--base`/`--head`, committed `--path`/`--revision`, `--abuse-case`, `--mr`, or `--pr`. Resolve a design-file path relative to the caller's chosen document location and pass an absolute path; `--repo` does not reliably establish the base for that file argument. PR/MR retrieval is read-only HTTPS/Git, and requires a selected remote request. Discovered URLs cannot authorize other retrieval.

Use `--preview --non-interactive` before execution. For example, with paths replaced by the selected project:

```sh
appsec-analyzer analyze-threats "What threats affect the export feature and its existing model assumptions?" --repo /absolute/project --design-file /absolute/project/docs/export.md --threat-model threat-model.md --preview --non-interactive
```

Preview makes no model call or analyst job; a selected remote PR/MR still retrieves metadata and Git content. Show the selected scope, actual comparison, documents and revisions, and material omissions. Resolve material scope ambiguity before execution.

Use preview's document selection to check engine context. `--threat-model FILE` accepts the public command's supported structured YAML model or repository Markdown document. `--requirements FILE` accepts its supported catalog or repository Markdown requirements. Repeated `--context FILE` selects repository-relative documents captured at the selected revisions. Native discovery may identify another relevant local document; pass its authorized repository-relative path explicitly and preview again rather than assuming automatic discovery found it.

For committed comparisons, verify baseline and proposed model/context selection. An explicit document absent from a selected revision is an error, not evidence that no model exists. Resolve the intended document/version or report the incomplete comparison. A design preview with no discovered model can proceed from sufficient design context.

`--no-context` disables automatic discovery, but explicitly selected documents can still be delivered. `--isolated` excludes existing threat models while retaining selected requirements/specifications. Neither is equivalent to comparing against a model. Honor an explicit exclusion and state the missing comparison; do not silently reintroduce excluded documents.

After preview and authorization, execute the same selected scope and documents, without `--preview`, with `--non-interactive` and the approved `--model` and `--max-budget-usd`. Use `--explore` only when broader tracked-source reading is requested or already authorized for the analysis. It is not implied by preview. Keep required package/catalog policy when choosing between public entry points.

For company context, repository Markdown documents can be selected through supported `--context` arguments and checked in preview. A context package bundled with the skill or stored outside the selected repository is not automatically engine-admitted context. Never pass a Markdown context directory to a legacy `--package` flag expecting it to be an engine package, copy it into the analyzed repository, or silently omit required company criteria. Use a supported public format when one is actually available and authorized; otherwise explain the integration gap and offer native analysis. Preserve an explicit engine-only request as incomplete/unavailable if it cannot include the required context.

## Results, questions, and cancellation

Use the public engine result and returned artifact locations; do not edit private state or copy the engine's internal analysis contract into this distribution. Preserve job identity, actual source scope, citations, coverage gaps, and complete, incomplete, failed, cancelled, or awaiting-answer outcomes. Do not invent comparisons or findings omitted by the engine. Engine-reported read proposals remain inside its admitted source; they grant the calling assistant no additional filesystem tools.

Summarize the returned result using the skill's delivery guidance. If it lacks a required model comparison or other requested output, name that gap. Native observations must be explicitly distinguished from engine output and must not repair an engine status into "complete."

Show only material engine questions, without manufacturing answers. If the user wants dialogue, wait for their actual answers, then use `analyst answer --repo ... --job ... --interactive --answer QID=TEXT` for the same job and authorized source/model/bounds. Pass each answer literally as one argument and preserve the approved model/per-call ceiling on answer operations. If questions are skipped or forbidden, return available findings and the engine's incomplete/awaiting-answer status; do not wait indefinitely or silently resume.

`analyze-threats --resume JOB` reopens a compatible waiting job using the same source selection. On a user stop request, call `analyst cancel --repo ... --job ...` for that job and return its actual outcome. Saving answers is opt-in: use public `analyst answer` with `--save-feature`, `--feature-sha`, and `--feature-id`. Explicit removal uses `analyst forget` with the selected feature file, expected hash, and question fingerprint. Let the engine reject stale context; never edit job files or saved answer records yourself.

## Public command mapping

| Request | Public operation |
| --- | --- |
| Plain question/design file, staged/worktree, selected commits, hypothesis paths, defined abuse case | `analyze-threats` with explicit scope, `--non-interactive`, approved model and per-call ceiling. A hypothesis uses the question and selected `--path`/`--revision`; do not forward the legacy `--hypothesis` flag to this parser. |
| Selected GitHub PR / GitLab MR | `analyze-threats` with `--pr URL` / `--mr URL`; retain the engine-resolved comparison and source revision. |
| Existing model / project requirements | `analyze-threats --threat-model FILE` / `--requirements FILE`; Markdown support here does not imply the legacy commands accept the same format. |
| Preview | `analyze-threats --preview` for selected scope/documents; no model calls, but MR/PR retrieval still uses the network. |
| `--feature`, `--package`, required catalog/model context | `analyst design`, `analyst review`, or `analyst hypothesis` with corresponding public options. Use `--interactive` only for the requested interactive source/question behavior. Organization-required packages still apply. |
| Legacy `--hypothesis TEXT --revision REV --path PATH` | `analyst hypothesis --hypothesis TEXT --revision REV --path PATH --repo REPO`; the source remains the selected committed revision. |
| Legacy design text / file | `analyst design --text TEXT --interactive` or `--design-file FILE` when feature/package semantics are required. |
| Legacy review question | `analyst review --question TEXT` with the requested staged/worktree or commit scope; preserve `--exact-base`. |
| Saved answers and questions | `analyst answer` with job identity and actual answers; saving is opt-in with expected feature hash/identity. |
| Resume / cancel / remove saved answer | `analyze-threats --resume JOB`, `analyst cancel`, and `analyst forget`, using the corresponding selected source/job/feature identity. |
| Legacy abuse-case organization profile | `analyst hypothesis --abuse-case ID --revision REV --preview` or authorized execution with `--org-profile` / `--no-org-profile`. Do not forward these flags to a parser that does not support them. |

Use the chosen command's `--help` before mapping an option whose semantics are unclear. Legacy CI/package semantics are optional engine features, not prerequisites for native reviewer use. Preview, setup, installed reference checks, and offline replays are distinct from live model/platform quality qualification.
