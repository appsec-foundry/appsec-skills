# Requirements for Security Score

- **REQ-01 — Independent and reproducible.** Use deterministic checks from the separately installed Security Score Python tool by default, without AppSec Analyzer or model calls. Identical sources, rules, and settings produce the same result. Identify the rule and scoring versions.

- **REQ-02 — Support repositories and changes.** Accept local checkouts, Git URLs, patches, staged/unstaged changes, commits, and PRs/MRs. Identify the examined scope and compared versions. For changes, assess security relevance separately from finding severity and distinguish introduced, worsened, resolved, and relevant pre-existing findings. Cover relevant security architecture: persistence and parameterized data access, frontend output and CSP, hardening, and dependency/build supply chains. For Git URLs, also check repository-host security settings.

- **REQ-03 — Compact score and detailed overview.** For repository assessments, show only the overall 0–100 score and its plain-language rating by default. Use the lowest assessed subscore as the overall score; serious weaknesses must limit the result. With `--details`, show the five subscores, evidence and calculation in a clear, colored overview with bars, and include the tool version. Changes retain a separate security-relevance assessment without a numeric score.

- **REQ-04 — Evidence and limits.** Distinguish findings, supported controls, unknowns and exclusions, and report coverage and incomplete checks separately from ratings. Leave areas without sufficient evidence unassessed; positive ratings require evidence of effective protection. Technology presence, high scores and absence of findings do not establish safety, and missing evidence does not establish low change relevance.

- **REQ-05 — Stay fast and bounded.** Focus on the selected scope within documented execution limits. Show progress during longer runs and clearly report incomplete, failed, or cancelled work.

- **REQ-06 — Keep Analyzer optional.** Select AppSec Analyzer only through an explicit parameter. Internal scoring remains the default, including when Analyzer is installed. Explain its prerequisites, supported scope, and separate scoring policy.

- **REQ-07 — Explainable calculation.** Publish understandable, manually reproducible criteria and calculations, centrally editable scoring values, and comparison examples. Count each underlying weakness once, and prevent unrelated strengths from offsetting serious weaknesses. Detailed output explains the subscores, decisive evidence and gaps.

- **REQ-08 — Automatic architecture assessment.** Assess Architecture & isolation automatically from recognized data-access boundaries and declared isolation and privilege controls. Base scores on concrete weaknesses or sufficient independent control evidence; a missing manual architecture review alone must not prevent assessment of these supported checks. Report unsupported wider architecture separately, without awarding points for technology presence.
