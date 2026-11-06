# Security score skill

Score a repository's security or rate how security-relevant a change is. The skill runs the separate [Security Score tool](https://github.com/appsec-foundry/appsec-tools/tree/main/security-score); scanning and scoring make no model calls.

## Install

```sh
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill security-score
```

The skill does not download or install the tool. Clone a trusted copy of [appsec-tools](https://github.com/appsec-foundry/appsec-tools) over HTTPS; public repositories need no GitHub account or SSH key. Repository assessments need tool version 0.3.2 or later. The tool needs Python 3.10+ on Linux or macOS, and Git for local comparisons. The default engine needs no third-party Python packages and no AppSec Analyzer.

## Use

```text
Use security-score for this repository.
Use security-score for the staged changes with --details.
Use security-score for PR https://github.com/owner/project/pull/42.
Use security-score for https://gitlab.company.example/team/project
with --token-env GITLAB_READ_TOKEN.
```

A repository gets one line, such as `59/100 (Bad)`. Ratings run from Very good to Very bad. The score is the lowest assessed subscore among five areas: Architecture & isolation, Identity & access, Data & processing, Dependencies & supply chain, and Deployment & operations. Serious weaknesses cap it, and partial positive evidence alone never gives a good score. Where evidence is insufficient, an area or the whole result shows Not assessed.

A change gets a security relevance of high, medium, low, or unclear, with findings listed separately. PR/MR checks need read access or a supplied diff.

| Option | Output |
| --- | --- |
| none or `--score` | Overall score and rating |
| `--details` | Tool version, colored bars for the five subscores, grouped findings with point deductions, and the evidence behind them, such as SSO endpoints (without credentials or query tokens), artifact repositories, Compose services, Terraform targets, and dependency locking |
| `--json`, `--yaml` | Full structured result, including internal check states and exact calculations |
| `--version` | Tool version and source commit |

Configuration and lockfiles show what is declared, not what runs. Architecture is scored from supported request-to-database flows and declared isolation or privilege controls; wider trust boundaries, authorization, and unsupported flows still need review. A high score does not mean the system is secure.

## Remote repositories

Remote scans support GitHub.com, GitLab.com, and self-managed GitLab over HTTPS, including internal hosts and custom ports. Source files and host security settings are read through the API without a checkout. URLs work with or without `.git`.

For GitLab, use a token with `read_api` and project access. Set it in an environment variable before you start your assistant and name the variable with `--token-env`. Alternatively, map API hosts to token variables once in the tool's `token-hosts.json`; the tool then tries anonymous access first and uses the token only after an authentication failure. HTTPS scans honor `HTTPS_PROXY`, `ALL_PROXY`, `HTTP_PROXY`, and `NO_PROXY`. See [tokens](https://github.com/appsec-foundry/appsec-tools/blob/main/security-score/references/usage.md#tokens-and-rate-limits) and [proxies](https://github.com/appsec-foundry/appsec-tools/blob/main/security-score/references/usage.md#http-proxies).

## Further reading

The [tool README](https://github.com/appsec-foundry/appsec-tools/tree/main/security-score#readme) covers direct CLI use, supported inputs, limits, rule maintenance, and the optional `--engine analyzer` variant; self-managed GitLab uses the default engine. See also the [assistant workflow](SKILL.md) and [requirements](requirements.md).
