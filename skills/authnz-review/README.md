# Authentication and authorization review

Review authentication and authorization in a local Git repository with AppSec Analyzer and Claude CLI.

## Install

Install the complete `authnz-review` directory with your assistant's skill installation mechanism. You also need a compatible AppSec Analyzer and an authenticated Claude CLI.

## Usage

```text
Use authnz-review for this Git repository.
Use Claude CLI with a USD 2 ceiling and show the structured result.
```

The review sends the selected source through Claude CLI and spends up to your budget, so it needs your explicit authorization for both. Installing the skill does not grant this and does not install the prerequisites. A finished analysis does not prove that an attack would work at runtime.

See [dependencies](dependencies.json), the [workflow](SKILL.md), and [legacy option compatibility](references/compatibility.md).
