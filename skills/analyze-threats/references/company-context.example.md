# Example company review context

Package: example-tenant-services
Version: 1.0.0

This fictional example shows the contents of a company's `review-context.md`.
Replace it with the company's actual context; it is not a mandatory baseline.

## Business context

The application stores invoices for separate customer organizations (tenants).
Tenant members request exports. External auditors need selected downloads
without creating an account. Invoice contents are confidential. The current
project design must establish which operations and controls are implemented.

## Review requirements

### ORG-EXPORT-01 — Export only authorized tenant data

An export may contain invoices only from a tenant the requester is authorized
to access. Passing a tenant ID into a queue does not itself establish access.

### ORG-DOWNLOAD-01 — Withdraw shared export access

The tenant must be able to withdraw access to a shared export. A withdrawn link
must no longer return invoice contents. Account-free auditor access remains an
intended use; signing in is not the only possible way to meet this requirement.

## Known threat patterns

### KT-TENANT-01 — A worker trusts a caller-selected tenant

Applies to queued or delayed tenant operations. A member could substitute another
tenant's ID and obtain its invoices if the worker relies on that ID without an
effective authorization boundary. Check the request-to-job binding and the
worker's access checks. Test a permitted job and an attempted cross-tenant job.

### KT-LINK-01 — Export links reach unintended recipients

Applies when possession of a shareable link authorizes a download. Forwarding or
leakage could expose invoices beyond the intended auditor. Examine link scope,
expiry, withdrawal, and token exposure. Do not assume these controls are absent
when the supplied design simply does not describe them.

### KT-CI-01 — Untrusted build changes reach release credentials

Applies to changes in build execution or credential access. An untrusted build
step could read release credentials if the job exposes them. Examine that
boundary only when it is affected or relied on by the selected change.

## Review priorities

For export changes, first examine tenant separation and who can receive invoice
contents. Report the relevant requirement and threat IDs alongside project
evidence. Assess priority from actual impact and prerequisites; do not generate
a finding just because a pattern is present in this catalog.
