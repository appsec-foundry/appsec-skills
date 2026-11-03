# Security score skill

This skill runs the standalone [Security Score Python tool](https://github.com/appsec-foundry/appsec-tools/tree/main/security-score). Repositories receive a **0–100 score and A–F grade**; changes receive a **high, medium, low, or unclear security relevance** classification. Scanning and calculation make no model calls.

## Install

Install the `security-score` skill from this repository, then separately obtain a trusted `appsec-tools` checkout containing `security-score/`. Clone over HTTPS; public repositories need no GitHub account or SSH key. The skill does not download or install the tool. Python 3.10+ on Linux/macOS is required; local Git comparisons also need Git. The default engine needs no third-party Python packages or AppSec Analyzer.

```sh
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill security-score
```

## Use

```text
Use security-score for this repository.
Use security-score for the staged changes with --details.
Use security-score for PR https://github.com/owner/project/pull/42.
Use security-score for https://gitlab.company.example/team/project
with --token-env GITLAB_READ_TOKEN.
```

`--details` adds reasons, coverage, findings, and calculation details. `--json` and `--yaml` request structured output. A high score does not establish safety; insufficient coverage withholds the score.

Remote scans support GitHub.com, GitLab.com and self-managed GitLab over HTTPS,
including internal addresses and custom ports. The GitLab token needs `read_api`
and project access; set it in the named environment variable before starting
your assistant. Source files and host settings are read through the API without
a local checkout. Self-managed GitLab uses the internal engine.

For direct CLI use, supported inputs, limitations, rule maintenance, and the optional `--engine analyzer` variant, see the [tool README](https://github.com/appsec-foundry/appsec-tools/tree/main/security-score#readme). See also the [assistant workflow](SKILL.md) and [requirements](requirements.md).
