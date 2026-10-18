# Compatibility and limits

This standalone workflow delegates profiling to Analyzer's public `repo-profile` command. Advisor's older `--repo` option maps to the positional directory argument. Only local directories are supported; the command never clones.

The required interface and capability values are in [dependencies.json](../dependencies.json). Capability checks must happen before profiling; a package version alone is insufficient because distinct previews can have different commands. There is no private-script fallback. Existing Advisor workflows are not replaced by installing this standalone directory.

The engine owns the walk, the vendored-content rules, the language classification and the output. No algorithm is maintained in this skill. The numbers describe what a scan would have to read, not what is wrong with it. This distribution has no platform or live-model qualification claim.
