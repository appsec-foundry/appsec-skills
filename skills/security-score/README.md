# Security score skill

This skill runs the standalone [Security Score Python tool](https://github.com/appsec-foundry/appsec-tools/tree/main/security-score). Repository output is one line, such as **`59/100 (Bad)`**. Request details for the colored overview with bars and five evidence-qualified subscores. Changes retain **high, medium, low, or unclear security relevance**. Scanning and calculation make no model calls.

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

The skill uses tool version 0.3.2 or later. The default and `--score` show only the overall number and rating; `--details` shows the version, bars and the five areas: Architecture & isolation, Identity & access, Data & processing, Dependencies & supply chain, and Deployment & operations. Ratings run from Very good to Very bad. The overall number is the lowest assessed subscore when the overall evidence gate is met; serious weaknesses limit the result, and partial positive evidence alone never yields a favorable overall score. Insufficient evidence leaves an area or the overall result Not assessed. `--version` explicitly shows the tool version and source commit.

`--details` adds grouped findings, point deductions, readable architecture and dependency-check results, SSO endpoint URLs and artifact repositories such as Nexus or Artifactory. Incomplete processing is summarized once. Internal check states and exact calculations remain available through `--json` and `--yaml`. Useful endpoint paths are retained without credentials or query tokens; configuration and lockfile observations do not prove runtime use. Architecture is assessed automatically from supported request-to-database flows and declared isolation or privilege controls. Concrete weaknesses yield deductions; sufficient independent controls can establish a positive static score. Wider trust boundaries, authorization and unsupported flows still need additional review. A high score does not establish safety.

Under **Deployment & operations**, details show Compose service profiles: declared ports and bind addresses, networks, privileges, mounts, image references, healthchecks and operating limits, with source locations. Text omits absent-field placeholders and services without recognized settings or unresolved evidence; JSON/YAML retain all captured declarations. Each file is reported independently; interpolation, inheritance and override order remain unresolved. Missing settings do not by themselves create findings or improve scores.

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
