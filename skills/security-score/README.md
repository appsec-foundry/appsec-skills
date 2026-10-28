# Security score skill

This skill runs the standalone [Security Score Python tool](https://github.com/appsec-foundry/appsec-analyzer-tools/tree/main/tools/security-score) and explains its results. The tool scores repositories from 0–100/A–F and classifies the security relevance of changes as high, medium, low, or unclear. It makes no model calls for scanning or calculation.

## Install

Install the `security-score` skill from this repository, then separately obtain a trusted `appsec-analyzer-tools` checkout containing `tools/security-score/`. The skill does not download or install the tool. Python 3.10+ on Linux/macOS is required; local Git comparisons also need Git. The default engine needs no third-party Python packages or AppSec Analyzer.

```sh
npx skills@1.7.2 add appsec-foundry/appsec-skills --skill security-score
```

## Use

```text
Use security-score for this repository.
Use security-score for the staged changes with --details.
Use security-score for PR https://github.com/owner/project/pull/42.
```

The assistant resolves the trusted tool path outside the examined repository and invokes its CLI. A repository receives a numeric score and grade; a change receives a relevance classification and findings, never a numeric score. `--details` adds reasons, coverage, findings, and calculation details. `--json` and `--yaml` request structured output. A high score does not establish safety; insufficient coverage withholds the score.

For direct CLI use, supported inputs, limitations, rule maintenance, and the optional `--engine analyzer` variant, see the [tool README](https://github.com/appsec-foundry/appsec-analyzer-tools/tree/main/tools/security-score#readme). The assistant workflow is in [SKILL.md](SKILL.md), and its user-facing contract is in [requirements.md](requirements.md).
