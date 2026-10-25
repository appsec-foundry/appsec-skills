# Scoring and rule maintenance

The internal score describes patterns covered by the bundled catalog. It does not estimate attack probability, business loss or verified runtime exploitability. It is separate from Analyzer's numeric policy.

## Calculation

A rule/file outcome is `violated` when a violation is recognized, otherwise `unclear` when evidence is ambiguous, otherwise `satisfied` when a specific control is recognized, otherwise `not_applicable`. Unknown aliases, indirect flows, external configuration and technology names do not establish a control. Syntax or lexical failures prevent a complete headline.

The [catalog](../rules.json) starts with all editable scoring values under `scoring`. Internal scoring version 2 uses these whole-point weights and caps:

| Severity | Weight | Maximum affected area score |
| --- | ---: | ---: |
| Critical | 50 | 39 |
| High | 25 | 59 |
| Medium | 10 | 79 |
| Low | 3 | 89 |

Calculate each assessed area in three steps:

1. Count the findings for each rule across all examined files in that area. Each finding deducts its severity's weight: `count × weight`.
2. Add those deductions and subtract the total from 100.
3. Apply the lowest severity cap present in the area, and a floor of 0.

```text
rule deduction = finding count × severity weight
area deduction = sum of rule deductions in that area
area cap       = lowest cap of its findings, or 100 without findings
area score     = max(0, min(100 − area deduction, area cap))
overall score  = lowest assessed area score
```

All arithmetic uses whole points; there is no logarithm, rounding or positive credit. Only areas with recognized control or violation evidence are scored. Unknown-only areas stay unscored; findings need no positive-control baseline to deduct points. Passing checks never cancel deductions.

The headline is the lowest assessed area score. One high observation limits it to 59 (E), even if other areas score 100. Further observations can lower it to 0. `--details` and structured output show each rule's count, points per instance, deduction and cap, followed by area and overall calculations. These initial values are a documented heuristic, not a calibrated risk model.

### Worked examples

Each row assumes complete coverage with recognized checks; findings are in one area unless stated otherwise.

| Evidence | Deduction | Cap | Area / overall result |
| --- | ---: | ---: | --- |
| Recognized control, no findings | 0 | 100 | 100 (A) |
| One high finding | 1 × 25 = 25 | 59 | min(75, 59) = 59 (E) |
| Two high findings, same or different rules | 2 × 25 = 50 | 59 | min(50, 59) = 50 (E) |
| Three high findings | 3 × 25 = 75 | 59 | min(25, 59) = 25 (F) |
| Five high findings | 5 × 25 = 125 | 59 | max(0, min(−25, 59)) = 0 (F) |
| Three medium findings | 3 × 10 = 30 | 79 | min(70, 79) = 70 (C) |
| One high and three medium findings | 25 + 3 × 10 = 55 | 59 | min(45, 59) = 45 (F) |
| One high finding in each of two areas | 25 per area | 59 per area | min(59, 59) = 59 (E) |
| Areas scoring 50 and 100 | Separate area deductions | Separate caps | min(50, 100) = 50 (E) |
| Unknown evidence only | No scored area | — | Undetermined; no score or grade |

Caps express the maximum grade for an observed severity, while weights make additional findings accumulate. For example, a first high finding deducts 25 points but its cap lowers the result further to 59. A second high finding brings the deduction to 50, so the cap no longer changes the result. Findings in different areas are not added together.

A headline requires at least one recognized source/dependency check, complete required processing and unchanged selected local sources. Host settings alone cannot award an application score. Insufficient evidence yields `undetermined`; failed or limited required processing yields `incomplete`. Both withhold score and grade while retaining available observations. One recognized check is still narrow coverage, explicitly shown in details and structured output.

## Change relevance

Changes, diffs, commits and PRs/MRs receive relevance and findings, with no numeric score, grade or scored area. The catalog's `change_relevance` policy is separate from severity weights and has its own version. A high relevance signal can describe a correctly implemented security feature or a fix, not just a detected weakness.

| Relevance | Meaning |
| --- | --- |
| High | Recognized changes to identity, authorization, data/entry-point boundaries, security controls, cryptography, dependency/build authority, agent instructions or executable permissions. |
| Medium | Recognized frontend/input/output changes or security-relevant documentation/policy changes. |
| Low | The complete examined change is positively identified as ordinary documentation or supported non-functional changes, without a recognized security signal. |
| Unclear | Changed behavior or context cannot be classified by the available deterministic rules. An empty finding list alone never establishes low relevance. |

Signals examine changed lines, up to two nearby lines of control context, and explicit sensitive file types. Existing scanner observations also identify relevant controls, including satisfied controls. Comment/format-only equivalence is established only where parsing supports it (Python AST and JSON structure); no generic claim is made for opaque languages. Executable flags are captured from local/Git source metadata. Unsupported or excluded files prevent a low classification. Positive signals can remain visible during incomplete processing, but the result remains marked incomplete.

For local comparisons, line matching is bounded to 10,000 lines per file. Larger files use conservative affected-file context and remain listed as unclassified. Patch inputs use the explicit added/removed line positions and process hunks separately. Metadata-only entries, permission changes, symlinks and rename/copy metadata require a local Git comparison; the parser rejects these instead of silently omitting them. At most 1,000 relevance signals are retained, with truncation reported and evidence for the headline level preserved. Signals contain rule references, aspects, source locations and explanations, not source snippets.

Findings are compared by rule, file and normalized observation signatures, with named Python context where available. New observations are `introduced`, additional instances are `worsened`, matches are `pre_existing`, and removed observations are `resolved`. Incomplete comparisons remain `unresolved`. Pre-existing observations are shown only in the affected nearby context. Signatures cannot establish whole-flow identity; a relevance check is not a full semantic review. A deeper model-backed review is a separate explicit choice.

A complete relevance check exits 0, including an unclear result. Missing knowledge is not an execution failure and does not approve the change. Incomplete processing exits 1. Repository-only score coverage can still return exit 2. Structured consumers use `analysis: change-relevance`, `relevance`, `relevance_version`, `signals` and `finding_changes`; no score/grade fields are assigned.

## Grades

| Score | Grade |
| --- | --- |
| 90–100 | A |
| 80 to below 90 | B |
| 70 to below 80 | C |
| 60 to below 70 | D |
| 50 to below 60 | E |
| 0 to below 50 | F |

100 means no deductions from applicable checks; 0 is the lowest attainable result. Grades describe only the reported scope and coverage. Undetermined, incomplete, failed and cancelled work receives no grade. The labels also describe Analyzer's own numbers without making its scoring equivalent.

## Architecture and supply chain

React, Angular, Vue, persistence libraries and Python DB imports are source-linked architecture observations, with no score credit for presence. Separate rules recognize direct SQL construction/parameterization, intrinsic JSX or Angular text binding, HTML/trust bypasses, literal CSP headers, debug/TLS settings and container hardening.

CSP checks recognize literal header declarations and nginx `add_header`. A positive declaration restricts scripts and includes `object-src 'none'`, `base-uri 'none'` and `frame-ancestors`. Delivery, proxy overrides, nonce generation and complete route coverage remain unverified. Missing declarations with frontend evidence stay unclear. Meta policies, dynamic Helmet/Django configuration and wider control flows are not fully assessed.

Supply-chain checks cover insecure/mutable dependency sources, download-and-execute lifecycle scripts, matching npm v2/v3 root lock declarations, Python requirement pins/hashes, immutable Action/container references, and explicit workflow permissions. Lock consistency does not establish all package integrity or vulnerability status. Other managers, included requirement files and scoped/inherited permissions can remain unclear. No package install, build, project script, hook or vulnerability-feed query runs.

## Repository hosts

Explicit Git URLs resolve through host metadata to an identified commit and bounded archive. Default-branch protection, applicable review requirements and exposed security settings are read separately. Explicitly disabled settings can become host findings; missing fields, denied requests and unavailable endpoints remain unknown. A feature-availability flag does not prove scanner execution.

GitHub security/analysis and branch details can require additional permissions. GitLab approval rules require authentication; positive rules explicitly covering the default branch are recognized, while other/inherited/further pages remain unresolved. Credential values are sent only to the selected API host, never exposed in output or forwarded to an archive host. Connected IPs are checked as public, TLS hostname verification stays enabled, and archives are parsed in memory without filesystem extraction.

API references: [GitHub repositories](https://docs.github.com/en/rest/repos/repos), [GitHub branch protection](https://docs.github.com/en/rest/branches/branch-protection), [GitLab projects](https://docs.gitlab.com/api/projects/), [GitLab approval rules](https://docs.gitlab.com/api/merge_request_approvals/).

## Maintain rules by hand

`rules.json` is the authoritative editable catalog. Each entry has a stable `id`, detector `kind`, area, severity, title, criteria, next action and executable examples. Its `scoring` object owns repository weights, caps and fixed grade bands. `change_relevance` owns path/content signals, area-to-relevance mappings, documentation criteria, executable-mode handling and before/after examples. The runtime validates it and fingerprints catalog and implementation. The examined project cannot override it.

### Adjust the calculation

Change the trusted installed skill's `rules.json`, not a catalog in the examined repository:

| Desired change | Edit | Effect |
| --- | --- | --- |
| Deduct more or fewer points per finding | `scoring.weights.<severity>` | Changes the linear deduction for every finding of that severity; whole points from 1 to 100. |
| Change the maximum score allowed by a finding | `scoring.severity_caps.<severity>` | Limits each affected area; whole points from 0 to 100. |
| Reclassify one rule | That rule's `severity` | Selects a different weight and cap without changing its detector. |
| Change what a rule recognizes | Its named Python detector | Changes finding recognition, separately from score arithmetic. |
| Change the formula itself | `scripts/score_calculation.py` | Changes aggregation; update this guide and scoring tests as well. |

For example, changing only `scoring.weights.high` from 25 to 15 makes three high findings deduct `3 × 15 = 45`. The result becomes `min(55, 59) = 55 (E)`. The cap stays 59, so a single high finding still scores 59. To change that maximum too, edit `severity_caps.high`. This illustrates configuration, not a recommended severity calibration.

Grade bands are fixed by REQ-03. `aggregation` and `repetitions` identify supported formulas; changing their text alone is rejected rather than silently ignored. The formula is implemented in `calculate_area` and `calculate`, independently of detector code. `areas[].breakdown` is produced by that same calculation and includes `rule`, `severity`, `instances`, `points_per_instance`, `deduction` and `severity_cap`.

After an adjustment, bump `scoring_version` for changed score meaning; bump `rule_version` for detection/rule changes. Recalculate affected catalog examples' `expected_score` and `expected_grade`, then run `--verify-rules` and the scoring tests below. Compare a representative repository using `--details` before and after the edit. Version 1 used logarithmic repetition deductions; version 2 counts every finding at its full weight, so old and new repeated-finding scores are not comparable.

### Maintain recognition

Edit catalog wording/severity directly. Recognition changes also edit the named detector: criteria are documentation, so changing their text alone does not change detection. The detectors are ordinary readable Python:

| Rule families | Detector location |
| --- | --- |
| `py-*` calls and AST | `scripts/score_core.py`, `python_observations` |
| Basic `js-*`, Action and Docker rules | `scripts/score_core.py`, `other_observations` |
| SQL, frontend, CSP, dependency declarations | `scripts/score_architecture.py`, `observations` and named helpers |
| Host API fields and outcomes | `scripts/score_remote.py`, `host_settings` and `settings_checks` |
| Change relevance | `scripts/score_relevance.py`, `analyze`; signal definitions and examples in `rules.json` |
| Score arithmetic, breakdown and grades | `scripts/score_calculation.py`, `calculate_area`, `calculate` and `grade`; values at the top of `rules.json` |

Keep IDs stable when refining rules. Register new detector kinds in policy validation and source applicability. Add positive, negative and relevant unclear examples, plus representative boundary tests. Source examples contain a filename, text, expected outcome and optional companion files. Host examples use explicit API states. Relevance examples contain before/after text, an expected level and optional executable flags; `--verify-rules` runs these as well. Signal patterns are compiled from the installed catalog only, never from target content. Use artificial examples with no real credentials or personal data.

```sh
python3 /installed/security-score/scripts/score.py --list-rules --json
python3 /installed/security-score/scripts/score.py --verify-rules
```

From this repository, run `python3 -B -m unittest discover -s tests -p test_security_score.py -v`. These tests connect behavior to REQ-01–07 through real local scans/comparisons, worked calculations, editable catalog values and representative failures. Examples do not prove completeness or absence of false positives; check representative project sources when widening recognition. Bump `rule_version` when recognition or the rule catalog changes, `scoring_version` when repository score meaning changes, and `change_relevance.version` when relevance classification changes. Catalog/implementation fingerprints also prevent accidental comparison across changed policies.

## Limits

The default execution budget is 15 seconds, selectable with `--timeout` from 0.1 to 120 seconds. It includes source work, tools and network reads, checked between bounded operations. It is not a completion promise for arbitrary repositories.

Limits are 3,000 inventory/archive entries, 512 KiB per selected source file, 20 MiB selected source per side, a 4 MiB supplied patch, and 24 MiB tool/download output. Archive expansion is capped at the source limit plus 8 MiB metadata. Scanning stops at 5,000 observations per side; available observations remain incomplete without a grade. Private filenames, unsupported sources and common dependency/build directories are excluded with recorded reasons. Unreadable or linked paths, source changes and malformed patches cannot produce a successful score.

No project code, tests or hooks run. Local source is rechecked before publication; Git filters, external diffs and text conversion are disabled for comparisons. Results contain locations/explanations, not raw source snippets or credential literals. JSON/YAML retain the complete bounded result; compact text deliberately omits details unless requested.
