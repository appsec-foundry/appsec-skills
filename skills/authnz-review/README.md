# Authentication and authorization review

Run a focused review through a compatible independently installed AppSec Analyzer and authenticated Claude CLI. Install the complete `authnz-review` directory using your assistant's skill mechanism. Analyzer installation, Claude login, and model-use authorization are separate prerequisites; this skill installs nothing.

```text
Use authnz-review for this Git repository. Use Claude CLI with a USD 2 ceiling and show the structured result.
```

See [dependencies](dependencies.json), the [workflow](SKILL.md), and [legacy option compatibility](references/compatibility.md). The engine owns scanners, model calls, validation and exports. Installing this standalone skill does not replace the existing Advisor plugin skill or establish live-model/platform qualification.
