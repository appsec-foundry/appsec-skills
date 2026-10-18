# Security score

Get a deterministic security score using an independently installed AppSec Analyzer. This skill makes no model calls and does not perform a full assessment.

Install the complete `security-score` directory using your assistant's supported skill installation mechanism. Install/select Analyzer separately through its trusted distribution; this skill never runs an installer. [Dependencies](dependencies.json) require interface 1 and scoring version 2. See the [workflow](SKILL.md) and [compatibility notes](references/compatibility.md).

Ask your assistant:

```text
Use security-score for the current Git repository.
```

You can also request `--repo /absolute/path`, an explicitly selected Git URL, `--json`, or `--yaml`. A host plugin can bind the workflow to its bundled tested engine. The standalone skill does not depend on Advisor or a sibling checkout.
