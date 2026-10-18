# Legacy option compatibility

The existing Advisor review remains available. Do not silently replace an unsupported option with a weaker operation.

| Existing request | Standalone public mapping |
| --- | --- |
| `--repo`, `--requirements`, `--save`, `--gate` | Corresponding `authnz-review` flags; gate failures and incomplete outcomes remain visible. |
| `--pentest-tasks`, `--pentest-format`, `--pentest-target` | Corresponding flags; the target is metadata, not an execution destination. |
| `--with-threat-model` | No equivalent declared. Stop and explain that prior STRIDE deduplication is unavailable; keep the existing Advisor workflow for this request. |
| `--slug` | No equivalent declared. Stop instead of inventing a private export path. |
| `--no-pentest-tasks` or organization export defaults | Do not forward unsupported flags or assume default precedence. Ask for explicit public `--outputs` selection when the request requires it; preserve the old plugin workflow until defaults are mapped. |
| `.authnz-report.json` and old saved layouts | Do not fabricate legacy filenames. Use engine-returned artifacts; old private-sidecar consumers are not declared compatible. |

Required capabilities are in [dependencies.json](../dependencies.json). The Analyzer interface alone does not establish compatibility with every historical Advisor option. Missing capabilities stop execution without another engine, private scripts, or assistant-authored review. PDF/export tools not declared by this command are not implicit dependencies.
