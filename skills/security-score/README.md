# Security score

Run bundled static checks without model calls. Repositories receive a **0–100 score and A–F grade**; changes receive **security relevance and findings**. The same captured sources, rules, and settings produce the same result.

## Install

Use the [Skills CLI prerequisites](../../README.md#quick-start-threat-modeling):

```bash
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill security-score
```

For a local checkout, replace `appsec-foundry/appsec-skills` with its path. For manual installation, copy the complete `security-score` directory, including scripts, catalog, and references, into your assistant's skill location.

Bundled checks need Python 3.10+ on Linux/macOS and Git for local Git sources and comparisons. They need no third-party Python packages or Analyzer installation.

## Usage

```text
Use security-score for this repository.
Use security-score for the staged changes with --details.
Use security-score for PR https://github.com/owner/project/pull/42.
Use security-score for https://gitlab.com/group/project.git with --details.
```

| Input | Result |
| --- | --- |
| Local checkout or supported Git URL | Score and grade, such as `79/100 (C)` |
| Changes, commits, comparisons, or supplied diffs | High, medium, low, or unclear security relevance, plus finding changes |
| PR/MR with read access or a supplied diff | Security relevance and findings for the selected change |

Output is compact by default. Add `--details` for reasons, findings, coverage, and calculation details. Use `--json` or `--yaml` for the complete structured result.

## Read the result

Grades are **A: 90–100, B: 80–<90, C: 70–<80, D: 60–<70, E: 50–<60, F: 0–<50**.

Each security area starts at 100. Findings deduct points by severity; severity caps also apply. The lowest area score becomes the overall score. For example, two high findings deduct 50 points in one area. If another area scores 100, the overall score is still 50 (E). Insufficient coverage or failed processing withholds the score.

A score of 100 means the applicable checks made no deductions. Coverage is limited: checks cover selected Python and JavaScript/TypeScript operations, React/Angular output, literal CSP, dependencies and lockfiles, GitHub Actions, Dockerfiles, and host settings. They do not comprehensively assess authorization, runtime exploitability, reverse-proxy controls, or package vulnerability databases.

Change relevance describes what needs security review, separately from finding severity:

| Relevance | Meaning |
| --- | --- |
| High | Signals involving access decisions, security functions, exposed interfaces, trust boundaries, or dependency/build authority. Fixes can also be high. |
| Medium | Recognized frontend, input/output, or security-documentation changes. |
| Low | Recognized ordinary documentation or non-functional changes, with complete processing and no security signal. |
| Unclear | Rules or context cannot classify the change. |

For example, changing `can_read(actor, owner)` can be high relevance even without a detected weakness. No findings does not establish low relevance or approve a merge. Findings distinguish introduced, worsened, resolved, and relevant pre-existing observations; incomplete comparisons retain unresolved findings.

Local comparisons use limited function context. Supplied patches provide only their hunks, so missing context can leave relevance unclear. See the [scoring and relevance guide](references/scoring.md) for examples, calculations, and coverage details.

## Run directly

Replace `/installed/security-score` with the installed skill path:

```sh
python3 /installed/security-score/scripts/score.py /project
python3 /installed/security-score/scripts/score.py /project --details
python3 /installed/security-score/scripts/score.py /project --base main --head HEAD --json
python3 /installed/security-score/scripts/score.py /project --staged --yaml
python3 /installed/security-score/scripts/score.py --patch /private/change.diff --mr https://gitlab.com/group/project/-/merge_requests/42
python3 /installed/security-score/scripts/score.py https://github.com/owner/project.git
```

| Option | Comparison |
| --- | --- |
| `--unstaged` | Index against working files |
| `--worktree` | HEAD against working files, including untracked files |
| `--commit REV` | Commit against its first parent |
| `--base REV --head REV` | Two revisions |

The CLI's `--pr`/`--mr` options label a supplied patch or local comparison; they do not fetch the change. Your assistant retrieves it through authorized tools. Permission changes, metadata-only entries, and rename/copy metadata need a local Git comparison.

Repository URLs support GitHub.com and GitLab.com HTTPS. The script reads a commit-pinned archive and available host security settings. Use a local checkout for other hosts or SSH. Unreadable settings stay unknown.

For private repositories, select an existing read-access API token by its environment variable name:

```sh
python3 /installed/security-score/scripts/score.py https://github.com/owner/private-project.git --token-env GIT_TOKEN --details
```

Pass the variable name, never the token value. The script does not automatically use Git credential helpers or SSH agents.

The default timeout is 15 seconds; `--timeout` accepts 0.1–120 seconds. Exceeded source, file, or output limits produce an incomplete result. Checks do not install dependencies, build, or execute the examined project. See [exact limits](references/scoring.md#limits).

## Optional Analyzer variant

```text
Use security-score for this repository with --engine analyzer --details.
```

Direct use adds the same `--engine analyzer` option to `score.py`. This variant requires a separately installed compatible Analyzer and supports repository scoring only. Its scores use a different policy and are not directly comparable with bundled scores. A missing or incompatible engine stops this variant. See [compatibility](references/compatibility.md) and [dependencies](dependencies.json).

## Maintain the rules

Edit weights, caps, criteria, severities, and examples in [rules.json](rules.json). Recognition changes also require updating the Python detector associated with a rule's `kind`. The catalog's `change_relevance` section controls relevance signals separately.

```sh
python3 /installed/security-score/scripts/score.py --list-rules --json
python3 /installed/security-score/scripts/score.py --verify-rules
```

See the [maintenance guide](references/scoring.md#adjust-the-calculation), [requirements](requirements.md), and [assistant workflow](SKILL.md).
