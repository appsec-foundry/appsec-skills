# Security score

Get a deterministic **0–100 score and A–F grade for repositories**, or **security relevance and findings for changes, diffs and PRs/MRs**. The bundled runtime is the default; Analyzer is an optional repository-scoring variant. Analysis makes no model calls.

Install the complete `security-score` directory with your assistant's skill mechanism. Internal scoring needs Python 3.10+ on Linux/macOS; local Git sources and comparisons also need Git. It requires no third-party Python packages or Analyzer installation.

## Start with a score

```text
Use security-score for this repository.
```

Repository output is one line, such as `79/100 (C)`. Change output starts with `Security relevance: high`, `medium`, `low` or `unclear`, plus finding counts. Changes receive no score or grade. Add `--details` for the explanation, affected aspects, findings and coverage:

```text
Use security-score for this repository with --details.
Use security-score for the staged changes.
Use security-score between main and HEAD.
Use security-score for this supplied patch.
Use security-score for PR https://github.com/owner/project/pull/42.
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

`--unstaged` compares index and working files; `--worktree` compares HEAD and working files including untracked files. `--commit REV` compares a commit with its first parent. A change can be highly relevant without a detected weakness: adding authentication, changing a query safely, removing a protection, or updating a build dependency all deserve review. Unclassified business logic remains unclear; an empty finding list does not establish low relevance. Recognized documentation/comment/formatting-only changes can be low relevance. Patch fragments and unsupported input can leave coverage incomplete. Patches with permission changes, metadata-only entries or rename/copy metadata need a local Git comparison. The default time budget is 15 seconds, selectable with `--timeout` up to 120 seconds.

## Optional Analyzer variant

```text
Use security-score for this repository with --engine analyzer --details.
```

This variant needs a separately installed compatible Analyzer. It supports repository scoring and rejects change selectors. Analyzer version 2 and internal version 1 use different scoring policies. Grades label each engine's own number; the numbers are not directly comparable. See [compatibility](references/compatibility.md) and the optional [dependency declaration](dependencies.json).

## Understand and maintain the rules

The [scoring guide](references/scoring.md) explains calculation, grades and human maintenance. The editable [catalog](rules.json) contains rule criteria, severities, examples and scoring values. Recognition changes also update the readable Python detector linked by each rule's `kind`. The `change_relevance` catalog separately owns signal levels, patterns, explanations and before/after examples. Relevance levels express review needs, independently of finding severity.

```sh
python3 /installed/security-score/scripts/score.py --list-rules --json
python3 /installed/security-score/scripts/score.py --verify-rules
```

The [requirements](requirements.md) define expected behavior; [SKILL.md](SKILL.md) defines the assistant workflow. A favorable repository score describes limited scanner coverage, not application safety. A completed change check is not merge approval; low relevance does not mean that a change is safe. Relevance can be unclear even when processing completed successfully.
