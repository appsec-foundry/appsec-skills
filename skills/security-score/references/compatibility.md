# Compatibility and limits

This standalone workflow delegates scoring to Analyzer's public `score` command. Advisor's older `--repo` option maps to the positional repository argument. JSON/YAML output is mutually exclusive. Non-Git directories supported by an older scanner are not silently treated as compatible with a top-level Git-checkout interface.

The required interface and capability values are in [dependencies.json](../dependencies.json). Capability checks must happen before analysis; a package version such as `0.1.0a0` alone is insufficient because distinct previews can have different commands. There is no private-script fallback. Existing Advisor workflows are not replaced by installing this standalone directory.

The engine owns rules, evidence validation, calculation, output schema, scanner status, cancellation and cleanup. No algorithm or copied analysis contract is maintained in this skill. This distribution has no platform or live-model qualification claim. The design-oriented `create-threat-model` skill remains independent of Analyzer.
