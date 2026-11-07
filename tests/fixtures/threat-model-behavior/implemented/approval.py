"""Fictional read-only architecture sample, intentionally incomplete.
Not executable as a service; no entry point, data, credentials or network.
Identity/assignment checks live at an upstream boundary outside this sample.
"""

class ApprovalService:
    def __init__(self, documents, reviews, approvals):
        self.documents = documents
        self.reviews = reviews
        self.approvals = approvals

    def record_review(self, application_id, worker_id):
        version = self.documents.latest_version(application_id)
        self.reviews.save(application_id, worker_id, version.id)

    def approve(self, application_id, worker_id):
        review = self.reviews.get(application_id, worker_id)
        if review is None:
            raise ValueError("Review required")
        current = self.documents.latest_version(application_id)
        self.approvals.save(application_id, worker_id, current.id)
