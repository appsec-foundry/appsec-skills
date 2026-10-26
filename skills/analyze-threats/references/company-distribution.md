# Company context packages and distribution

How a company prepares and distributes context for `analyze-threats`. Use context files for company knowledge and review criteria. Keep a fork only for deliberate changes to the analysis workflow itself.

## Create a context package

Start from the [fictional company-context example](company-context.example.md). Put the company's actual content in `review-context.md`, name the package and version, and give requirements and known threats stable IDs. For example:

```text
invoice-review-context/
  review-context.md
  known-threats.md
  architecture.md
```

The entry point can hold everything or link to local files. Useful entries explain when a threat applies, who could exploit it, what harm it could cause, and which controls or checks matter. Separate company requirements from suggestions and architecture assumptions. No executable plugin, installer, or special catalog format is needed.

## Keep upstream and company sources separate

A small internal distribution repository can hold them separately:

```text
company-review/
  upstream/appsec-skills/
  context/invoice-review-context/review-context.md
  releases/2026-10/analyze-threats/
```

1. Keep the upstream source at an explicitly selected release or commit. Record that revision alongside the company context version in your internal release notes.
2. Maintain company context under `context/`, outside the upstream checkout and the active skill installation.
3. Assemble each release in a fresh directory: copy the complete upstream `skills/analyze-threats/` directory, then add the context package contents under `references/company-context/`. Keep relative document links intact.
4. Review the assembled files, then distribute the complete `analyze-threats` directory through your approved skill distribution mechanism. Keep confidential company context restricted to its intended recipients.
5. Users install that directory in their assistant's local skill location (`<skills directory>/analyze-threats/`). To update, build a new release from the selected upstream revision and the company sources instead of overwriting company edits.

Alternatively, install the upstream skill unchanged and select the context package path in each request. That avoids rebuilding a company variant for every upstream update. The skill reads context without modifying it and does not manage releases or merge updates.

See [organization context](organization-context.md) for applicability, conflicts, and coverage. These packages are Markdown documents for this skill; they are not interchangeable with Analyzer's engine-package format.
