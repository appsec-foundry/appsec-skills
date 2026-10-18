# Repo profile

Show what is in a repository before scanning it: working-tree size, language split, build manifests and tracked versus untracked content, using an independently installed AppSec Analyzer. This skill makes no model calls, reads no file contents and is not a security check.

Install the complete `repo-profile` directory using your assistant's supported skill installation mechanism. Install/select Analyzer separately through its trusted distribution; this skill never runs an installer. [Dependencies](dependencies.json) require interface 1 and the `repo_profile` capability. See the [workflow](SKILL.md) and [compatibility notes](references/compatibility.md).

Ask your assistant:

```text
Use repo-profile for the current repository.
```

You can also request `--repo /absolute/path` or `--json`. A host plugin can bind the workflow to its bundled tested engine. The standalone skill does not depend on Advisor or a sibling checkout.
