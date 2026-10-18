# Focused threat analysis

Use a question-first AppSec Analyzer workflow for a design or a selected code change. Install the complete `analyze-threats` directory using your assistant's skill mechanism. A compatible independently installed Analyzer and authenticated Claude CLI are required. Source/model-use authorization is separate from skill installation.

```text
Use analyze-threats to preview the staged changes for cross-tenant access risks. Do not make model calls yet.
```

See [dependencies](dependencies.json), the [workflow](SKILL.md), and [compatibility and lifecycle mapping](references/compatibility.md). The engine owns clarification, admitted source, bounded calls and validated results. Its per-call ceiling is not a total-job budget. Standalone installation does not replace Advisor's existing command or establish live-model/platform qualification.
