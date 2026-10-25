# Security score

Get a fast, deterministic indication from bundled static checks. Repositories receive a **0–100 score and A–F grade**; changes receive **security relevance and findings**. Identical captured sources, rules and settings produce the same result. Analysis makes no model calls.

## Install

Install with the [repository's Skills CLI prerequisites](../../README.md#quick-start-threat-modeling):

```bash
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill security-score
```

For an unpublished checkout, replace `appsec-foundry/appsec-skills` with its local path. For manual installation, copy the complete `security-score` directory, including its scripts, catalog and references, into your assistant's skill location.

Running the bundled checks needs Python 3.10+ on Linux/macOS; local Git sources and comparisons also need Git. No third-party Python packages or Analyzer installation are required. An installed Analyzer does not change the default.

## Choose the assessment

| Input | Default result |
| --- | --- |
| Local checkout or supported Git repository URL | Repository score and grade, such as `79/100 (C)` |
| Staged/unstaged changes, commits, base/head comparisons or supplied diffs | Security relevance and finding changes, without a score or grade |
| PR or MR with a supplied patch or authorized comparison | Security relevance for the selected change, without a score or grade |

```text
Use security-score for this repository.
Use security-score for the staged changes.
Use security-score for PR https://github.com/owner/project/pull/42.
```

Output is compact by default:

```text
79/100 (C)
```

For a change, for example:

```text
Security relevance: high · 0 introduced, 0 worsened findings
```

Add `--details` for reasons, affected aspects, findings, coverage and rule/scoring identity. Use `--json` or `--yaml` for the complete structured result.

## Interpret the result

Repository grades are **A: 90–100, B: 80–<90, C: 70–<80, D: 60–<70, E: 50–<60, F: 0–<50**. A score of 100 means no deductions from applicable checks; 0 is the lowest attainable result. The weakest assessed security area determines the headline, so unrelated passing checks cannot cancel serious findings. Insufficient coverage or failed processing withholds the score and grade.

Within each area, subtract `number of findings × points per severity` from 100, then apply the strictest severity cap and a floor of 0. For example, two high findings deduct `2 × 25 = 50` points: the area scores 50 (below the high cap of 59). If another area scores 100, the overall score is still 50 (E). `--details` shows each rule's count, points, deduction, cap and the overall calculation. The editable weights and caps are at the top of [rules.json](rules.json); see the [worked examples and adjustment guide](references/scoring.md#adjust-the-calculation).

Change relevance is an indication of whether a change touches access controls, security functions, interface exposure or other security-related behavior. It uses deterministic rules over the before/after change, bounded function context and configuration paths. This makes it useful even when no weakness is detected:

| Relevance | Meaning |
| --- | --- |
| High | Indications of changes to access decisions, security functions, routes/listeners, trust boundaries or dependency/build authority. Safe additions and fixes can also be high. |
| Medium | Recognized frontend/input/output changes or security-relevant documentation changes. |
| Low | Positively identified ordinary documentation or supported non-functional changes, with complete processing and no security signal. |
| Unclear | Available rules or context cannot classify the changed behavior. An empty finding list does not establish low relevance. |

Findings distinguish introduced, worsened, resolved and relevant pre-existing observations. Incomplete comparisons retain unresolved findings. Relevance does not imply that a weakness exists, and a completed check does not approve a merge.

For example, changing the return value inside `can_read(actor, owner)` is a high-relevance indication even when its name is several lines away from the diff. Changing a listener from `127.0.0.1` to `0.0.0.0` also indicates a possible change in interface exposure. An unchanged security helper elsewhere in the file does not by itself classify the changed function.

Local comparisons provide captured function bodies: Python uses AST boundaries; JavaScript/TypeScript and selected other languages use declaration and brace heuristics. Function context is limited to 200 lines. Patches use only the supplied hunks, independently; they cannot reconstruct an omitted function header or its callers. `--details` shows the matching rule, location, side and relationship to the change. See the [relevance rules and examples](references/scoring.md#change-relevance) to adjust this policy. Unrecognized names, indirect calls and missing context can remain unclear.

## Select sources and coverage

```text
Use security-score for this repository with --details.
Use security-score between main and HEAD.
Use security-score for this supplied patch.
Use security-score for MR https://gitlab.com/group/project/-/merge_requests/42 with --details.
Use security-score for https://gitlab.com/group/project.git with --details.
```

A PR/MR needs authorized host read access or a supplied patch/local comparison. The assistant obtains the selected diff and metadata; it does not post a review. Repository URL mode supports GitHub.com and GitLab.com HTTPS, captures a commit-pinned archive and reads available host security settings. Use a local checkout for other hosts or SSH. Private API access uses an existing credential selected by name with `--token-env NAME`; never pass its value as an argument. Unreadable settings stay unknown.

Checks cover selected Python and JavaScript/TypeScript operations, React/Angular output mechanisms, literal CSP, dependency/lockfile declarations, GitHub Actions, Dockerfiles and host settings. Architecture output identifies declared frontend and persistence technologies; presence alone earns no points. Wider authorization, external reverse-proxy controls, runtime exploitability and package vulnerability databases are not comprehensively assessed.

## Run directly

Replace the first path with the installed skill location:

```sh
python3 /installed/security-score/scripts/score.py /project
python3 /installed/security-score/scripts/score.py /project --details
python3 /installed/security-score/scripts/score.py /project --base main --head HEAD --json
python3 /installed/security-score/scripts/score.py /project --staged --yaml
python3 /installed/security-score/scripts/score.py --patch /private/change.diff --mr https://gitlab.com/group/project/-/merge_requests/42
python3 /installed/security-score/scripts/score.py https://github.com/owner/project.git
```

For private repositories, select an environment variable that already holds a GitHub or GitLab API token with read access. For example, with a token available in `GIT_TOKEN`:

```sh
python3 /installed/security-score/scripts/score.py https://github.com/owner/private-project.git --token-env GIT_TOKEN --details
python3 /installed/security-score/scripts/score.py https://gitlab.com/group/private-project.git --token-env GIT_TOKEN --json
```

Use the token for the selected host. The script reads through its API; it does not automatically use Git credential helpers or SSH agents. Pass the variable's name to `--token-env`, not its value. Host settings that the token cannot read remain unknown.

`--unstaged` compares index and working files; `--worktree` compares HEAD and working files including untracked files. `--commit REV` compares a commit with its first parent. The CLI's `--pr`/`--mr` options identify a supplied patch or local base/head comparison; they do not fetch the change themselves. Patch fragments and unsupported input can leave coverage incomplete. Patches with permission changes, metadata-only entries or rename/copy metadata need a local Git comparison.

The default time budget is 15 seconds, selectable with `--timeout` from 0.1 to 120 seconds. Source, file and output limits bound the work. An exceeded limit is reported as incomplete. The checks do not install dependencies, build or execute the examined project. See the [scoring guide](references/scoring.md#limits) for exact limits.

## Optional Analyzer variant

```text
Use security-score for this repository with --engine analyzer --details.
```

For direct use:

```sh
python3 /installed/security-score/scripts/score.py /project --engine analyzer --details
```

This explicit variant needs a separately installed compatible Analyzer. It supports repository scoring and rejects change selectors. Analyzer scoring version 2 and internal scoring version 2 use different policies despite sharing a version number; their numbers are not directly comparable. A missing or incompatible Analyzer stops the selected variant without installing it or silently changing engines. See [compatibility](references/compatibility.md) and the optional [dependency declaration](dependencies.json).

## Understand and maintain the rules

The [scoring guide](references/scoring.md) explains calculation, grades and human maintenance. The editable [catalog](rules.json) contains rule criteria, severities, examples and scoring values. Recognition changes also update the readable Python detector linked by each rule's `kind`. The `change_relevance` catalog separately owns signal levels, patterns, explanations and before/after examples. Relevance levels express review needs, independently of finding severity.

```sh
python3 /installed/security-score/scripts/score.py --list-rules --json
python3 /installed/security-score/scripts/score.py --verify-rules
```

The [requirements](requirements.md) define expected behavior; [SKILL.md](SKILL.md) defines the assistant workflow. A favorable repository score describes limited scanner coverage, not application safety. A completed change check is not merge approval; low relevance does not mean that a change is safe. Relevance can be unclear even when processing completed successfully.
