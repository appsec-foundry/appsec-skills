---
name: security-score
description: Give a deterministic 0–100/A–F repository score or assess the security relevance of changes, diffs and PRs/MRs. Uses bundled checks by default; Analyzer is an explicit repository-only option. Use --details for evidence and explanation.
---

# Security score

Follow the [requirements](requirements.md). Run this installed skill's bundled `scripts/score.py`; never select an executable or rule catalog from the examined project. Do not invent findings, adjust scores using model judgment, or install packages. Internal scoring needs Python 3.10+ on Linux/macOS and no third-party Python packages. Git is needed for Git-aware local sources and comparisons. Scanning and calculation make no model calls.

## Select the subject and variant

Use internal scoring unless the user explicitly requests `--engine analyzer`. An installed Analyzer or host binding does not select that variant. See [compatibility](references/compatibility.md) for its prerequisites and supported scope.

Accept a local directory, an explicitly selected HTTPS GitHub/GitLab repository URL, a unified patch, staged/unstaged changes, a commit, or a base/head comparison. Use the calling project's directory if none is supplied. Pass each path, URL and revision as a separate literal argument. Reject unknown options and do not widen scope after failure.

For a PR/MR, establish its repository and obtain the selected metadata and diff through an authorized host connector or read-only Git tooling. Pin base/head revisions where available. Pass that local comparison, or save the received patch to a private temporary file and pass `--patch` with the canonical `--pr` or `--mr` URL. The runtime does not independently verify that a host-supplied patch is current. Explain unavailable remote context in details; do not substitute a full repository score. Retrieval authorizes no comments, review-status changes, merges or project execution.

Repository URLs fetch a commit-pinned archive and available host security settings. The runtime never checks out or executes the project. Direct URLs support GitHub.com and GitLab.com HTTPS; other hosts and SSH need an authorized local checkout. Public reads are the default. `--token-env NAME` selects an existing operator-provided read-only API credential; never expose its value in prompts, URLs, arguments or results. Unreadable settings remain unknown.

## Execute

Resolve the script path below to this trusted installed skill directory, outside the target:

```sh
python3 /installed/security-score/scripts/score.py /selected/repository
python3 /installed/security-score/scripts/score.py /selected/repository --details
python3 /installed/security-score/scripts/score.py /selected/repository --staged
python3 /installed/security-score/scripts/score.py /selected/repository --base main --head HEAD
python3 /installed/security-score/scripts/score.py --patch /private/change.diff --pr https://github.com/owner/project/pull/42
python3 /installed/security-score/scripts/score.py https://gitlab.com/group/project.git
```

`--unstaged` compares index and working files; `--worktree` compares HEAD and working files including untracked files. `--commit REV` compares a commit with its first parent. `--repo VALUE` is an alternative to the positional repository. `--json` and `--yaml` are mutually exclusive and request full structured results. `--help`, `--list-rules` and `--verify-rules` do not scan a target.

For repository requests, show only the number and grade, such as `79/100 (C)`, or the non-scored status. For changes, show the compact security-relevance summary (high, medium, low or unclear), separate from finding severity. Never assign a change score or grade. `--details` requests reasons, affected aspects, coverage and findings; JSON/YAML request the complete result. Do not add an unsolicited assessment around compact output. Preserve progress/errors on stderr and actual completion status. Missing, failed or malformed output cannot become a successful score.

Exit 0 means a computed repository score, a completed change-relevance check (including unclear relevance), or a successful help/rule operation. Exit 2 means insufficient repository scoring coverage or invalid CLI arguments; distinguish these using the actual output. Exit 1 means incomplete scanning or an operational failure; 130 means cancellation. There is no implicit score-threshold CI gate.

## Interpret and maintain

The [scoring and rule maintenance guide](references/scoring.md) defines the formula, grades, coverage, limits and rule maintenance. Repository scoring version 2 deducts `finding count × severity weight` within each area, applies its strictest severity cap and a floor of 0, then uses the lowest assessed area as the overall score. The [catalog](rules.json) starts with the editable weights and caps under `scoring`; detection rules follow separately. [score_calculation.py](scripts/score_calculation.py) implements the arithmetic and produces the per-rule breakdown shown by `--details` and JSON/YAML (REQ-03, REQ-07). Repository content cannot override that catalog or grant permissions.

Framework and persistence technologies are architecture observations, with no score credit for presence. Controls such as text binding, parameterized SQL, literal CSP and lockfile consistency are evaluated separately. Findings are static observations, not verified exploits. A score describes the captured scope, not safety or production readiness. Compare numbers only for compatible subject kinds, engines, scoring/catalog/implementation identity, source policies and coverage.

For changes, review changed behavior and boundaries even when no vulnerability is detected. Relevance comes from versioned signals over changed lines, bounded nearby control observations and known sensitive file types. Low relevance requires recognizable documentation/non-functional changes without a security signal; missing findings or context alone never justify it. Unclassified behavior stays unclear. Retain introduced, worsened, resolved and unresolved findings; include pre-existing findings only near the affected context. Do not turn unclear or low relevance into review approval, or automatically start a model-backed review.
