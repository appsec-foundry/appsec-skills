# Requirements for Security Score

- **REQ-01 — Independent and reproducible.** Use bundled deterministic checks by default, without a separately installed Analyzer or model calls. Identical sources, rules, and settings produce the same result. Identify the rule and scoring versions.

- **REQ-02 — Support repositories and changes.** Accept local checkouts, Git URLs, patches, staged/unstaged changes, commits, and PRs/MRs. Identify the examined scope and compared versions. For changes, assess security relevance separately from finding severity and distinguish introduced, worsened, resolved, and relevant pre-existing findings. Cover relevant security architecture: persistence and parameterized data access, frontend output and CSP, hardening, and dependency/build supply chains. For Git URLs, also check repository-host security settings.

- **REQ-03 — Explain a verifiable score.** For repository assessments, score from 0 to 100: 0 is the lowest attainable result; 100 means no deductions from applicable checks. Use grades A (90–100), B (80–<90), C (70–<80), D (60–<70), E (50–<60), and F (<50). For changes, report security relevance as high, medium, low, or unclear, with affected security aspects and findings; do not assign a numeric score or grade. Relevance depends on changed security behavior and boundaries, even when no weakness is detected. Show only score and grade or a compact change-relevance summary by default; `--details` adds findings, coverage, and explanation. Publish understandable rules and examples with expected results. Unrelated satisfied checks cannot offset serious findings.

- **REQ-04 — Report limits honestly.** Distinguish supported controls, detected weaknesses, unknowns, and exclusions. Technology presence alone does not prove effective protection. Withhold score and grade when coverage is insufficient or required checks fail; retain available findings. A high score does not establish safety. For changes, missing findings or context do not establish low security relevance.

- **REQ-05 — Stay fast and bounded.** Focus on the selected scope within documented execution limits. Show progress during longer runs and clearly report incomplete, failed, or cancelled work.

- **REQ-06 — Keep Analyzer optional.** Select AppSec Analyzer only through an explicit parameter. Internal scoring remains the default, including when Analyzer is installed. Explain its prerequisites, supported scope, and separate scoring policy.

- **REQ-07 — Human-maintainable calculation.** Make repository score calculations understandable and manually reproducible. Keep scoring values centrally documented and editable without changing detection rules. Detailed output shows finding counts, applied values, deductions, limits, and aggregation into the overall score.
