from datetime import datetime

from pydantic import BaseModel, Field

from src.models.assignment import ReviewStatus


class ReviewListItem(BaseModel):
    id: int
    assignment_id: int
    assignment_title: str
    status: ReviewStatus
    review_deadline: datetime


class ReviewCriterionRead(BaseModel):
    criterion_id: int
    name: str
    max_score: int
    score: int | None


class ReviewRead(BaseModel):
    id: int
    assignment_id: int
    status: ReviewStatus
    comment: str | None
    submitted_at: datetime | None
    download_url: str
    criteria: list[ReviewCriterionRead]


class ReviewScoreInput(BaseModel):
    criterion_id: int = Field(gt=0)
    score: int = Field(ge=0)


class ReviewUpdate(BaseModel):
    comment: str | None = Field(default=None, max_length=5000)
    scores: list[ReviewScoreInput] = Field(min_length=1)


class ReviewAssignmentResult(BaseModel):
    submissions: int
    reviews_created: int

