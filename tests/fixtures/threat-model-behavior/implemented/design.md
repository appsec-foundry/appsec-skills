# GrantDesk design

Fictional local modeling fixture; do not deploy or execute its code.
The production design serves applicants and assigned caseworkers. Applicants
upload confidential income records and may replace them until approval.
Only the applicant and their assigned caseworker may read those records.
A caseworker reviews a specific immutable document version. Approval must
refer to that reviewed version and a later replacement requires another review.
Approval authorizes a substantial non-recoverable grant payment. The product
team owns the approval rule; the application team implements it.
The application service uses a document repository; no external integration
is part of this fixture. Identity and assignment are enforced by its existing
service boundary, whose implementation is outside the inspected fixture.
No runtime evidence or completed security verification is supplied.
