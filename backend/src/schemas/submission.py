from datetime import datetime

from pydantic import BaseModel, ConfigDict, computed_field


class SubmissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    assignment_id: int
    original_filename: str
    submitted_at: datetime

    @computed_field
    @property
    def download_url(self) -> str:
        return f"/api/v1/submissions/{self.id}/file"


class SubmissionResultRead(SubmissionRead):
    completed_reviews: int
    average_score: float | None


class FeedbackCriterionRead(BaseModel):
    name: str
    max_score: int
    score: int


class FeedbackReviewRead(BaseModel):
    score: int
    comment: str
    criteria: list[FeedbackCriterionRead]


class SubmissionFeedbackRead(BaseModel):
    submission_id: int
    assignment_id: int
    average_score: float | None
    completed_reviews: int
    reviews: list[FeedbackReviewRead]
