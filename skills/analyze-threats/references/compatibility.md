# Public command compatibility

Public commands, their argument validation and engine-owned contracts remain authoritative. Require the capabilities declared in [dependencies.json](../dependencies.json); never fall back to `scripts/appsec-analyst-cli` or another private script.

| Request | Public operation |
| --- | --- |
| Plain question/design file, staged/worktree, selected commits, hypothesis paths, defined abuse case | `analyze-threats` with explicit scope, `--non-interactive`, approved model and per-call ceiling. A hypothesis uses the question and selected `--path`/`--revision`; do not forward the legacy `--hypothesis` flag to this parser. |
| Preview | `analyze-threats --preview` for selected scope/documents; no model calls, but MR/PR retrieval still uses the network. |
| `--feature`, `--package`, required catalog/model context | `analyst design`, `analyst review`, or `analyst hypothesis` with corresponding public options. Use `--interactive` only for the requested interactive source/question behavior. Organization-required packages still apply. |
| Legacy `--hypothesis TEXT --revision REV --path PATH` | `analyst hypothesis --hypothesis TEXT --revision REV --path PATH --repo REPO`; the source remains the selected committed revision. |
| Legacy design text / file | `analyst design --text TEXT --interactive` or `--design-file FILE` when feature/package semantics are required. |
| Legacy review question | `analyst review --question TEXT` with the requested staged/worktree or commit scope; preserve `--exact-base`. |
| Saved answers and questions | `analyst answer` with job identity and actual answers; saving is opt-in with expected feature hash/identity. |
| Resume / cancel / remove saved answer | `analyze-threats --resume JOB`, `analyst cancel`, and `analyst forget`, using the corresponding selected source/job/feature identity. |
| Legacy abuse-case organization profile | `analyst hypothesis --abuse-case ID --revision REV --preview` or authorized execution with `--org-profile` / `--no-org-profile`. Do not forward these flags to a parser that does not support them. |

Use the chosen command's `--help` before mapping an option whose semantics are unclear. A total spending ceiling is not supplied by `--max-budget-usd`; if the requested limit cannot be enforced, stop. Do not silently drop required evidence or feature/package policy to use the simpler parser. Preview, setup, installed reference checks and offline replays are distinct from live quality qualification.
