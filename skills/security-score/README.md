# Security score skill

This skill runs the standalone [Security Score Python tool](https://github.com/appsec-foundry/appsec-tools/tree/main/security-score). Repositories receive **five evidence-qualified 0–100 subscores with plain-language ratings**, plus an overall verdict and its main reason. Changes retain **high, medium, low, or unclear security relevance**. Scanning and calculation make no model calls.

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

The skill uses tool version 0.2.1 or later, which reports the five subscores by default; no extra `--score` option is needed. Its five areas are Architecture & isolation, Identity & access, Data & processing, Dependencies & supply chain, and Deployment & operations. Ratings run from Very good to Very bad; coverage is shown separately, and insufficient evidence leaves an area Not assessed. A serious design or control weakness can determine the overall verdict; there is no overall numeric average. Text assessments and CLI help/argument errors show the tool version; `--version` also shows its source commit.

`--details` adds reasons, coverage, findings and calculations, plus recognized SSO endpoint URLs and artifact repositories such as Nexus or Artifactory. Useful endpoint paths are retained without credentials or query tokens; configuration and lockfile observations do not prove runtime use. `--json` and `--yaml` request structured output. The bounded architecture checks cover declared isolation and privileges; wider trust boundaries and authorization need additional review. A high score does not establish safety.

Details also show declared Terraform/cloud targets and selected security properties, plus Python/Node dependency-management evidence: version and lock consistency, artifact hashes, and applicable locked-install declarations. Unsupported formats and unresolved build workflows remain visible as gaps.

Remote scans support GitHub.com, GitLab.com and self-managed GitLab over HTTPS,
including internal addresses and custom ports. The GitLab token needs `read_api`
and project access; set it in the named environment variable before starting
your assistant. You can also configure automatic token selection once in the
tool's user-level `token-hosts.json`, mapping exact HTTPS API origins to variable
names such as `GIT_TOKEN`. It starts anonymously and retries an authentication
failure once with the matching token; `--token-env` overrides that mapping.
See the [token configuration](https://github.com/appsec-foundry/appsec-tools/blob/main/security-score/references/usage.md#tokens-and-rate-limits).
Source files and host settings are read through the API without
a local checkout. Self-managed GitLab uses the internal engine.

Repository URLs work with or without `.git`. HTTP proxies for HTTPS scans are
selected from `HTTPS_PROXY`, `ALL_PROXY`, then `HTTP_PROXY`, with `NO_PROXY` for
host exclusions. See the [proxy reference](https://github.com/appsec-foundry/appsec-tools/blob/main/security-score/references/usage.md#http-proxies)
for supported proxy URLs and CONNECT behavior.

For direct CLI use, supported inputs, limitations, rule maintenance, and the optional `--engine analyzer` variant, see the [tool README](https://github.com/appsec-foundry/appsec-tools/tree/main/security-score#readme). See also the [assistant workflow](SKILL.md) and [requirements](requirements.md).
