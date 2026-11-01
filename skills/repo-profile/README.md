# Repo profile

Show a local repository's size, languages, build manifests, and tracked versus untracked content. The skill reads directory entries, not file contents, and makes no model calls. It does not assess security.

## Install

Copy the complete `repo-profile` directory into your assistant's skill location, or use its supported installation mechanism. Install a [compatible AppSec Analyzer](dependencies.json) separately.

## Usage

```text
Use repo-profile for the current repository.
```

Use `--repo /absolute/path` to select another local directory or `--json` for structured output. Git URLs are not supported.

See [dependencies](dependencies.json), the [workflow](SKILL.md), and [compatibility](references/compatibility.md).
