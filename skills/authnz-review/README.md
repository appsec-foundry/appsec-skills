# Authentication and authorization review

Review a local Git repository's authentication and authorization through AppSec Analyzer and Claude CLI.

## Install

Install the complete `authnz-review` directory using your assistant's skill installation mechanism. You also need a compatible AppSec Analyzer and an authenticated Claude CLI.

## Usage

```text
Use authnz-review for this Git repository.
Use Claude CLI with a USD 2 ceiling and show the structured result.
```

The review needs explicit authorization to send the selected source through Claude CLI and spend up to your budget. Installing the skill grants neither and installs no prerequisites. A completed analysis does not prove that an attack would succeed at runtime.

See [dependencies](dependencies.json), the [workflow](SKILL.md), and [legacy option compatibility](references/compatibility.md).
