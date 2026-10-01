from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.models.assignment import AssignmentStatus


class CriterionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    max_score: int = Field(gt=0)


class AssignmentCreate(BaseModel):
    group_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    submission_deadline: datetime
    review_deadline: datetime
    reviews_per_submission: int = Field(default=2, ge=1, le=5)
    criteria: list[CriterionCreate] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_deadlines(self) -> "AssignmentCreate":
        if self.review_deadline <= self.submission_deadline:
            raise ValueError("Срок проверки должен быть позже срока сдачи")
        return self


class AssignmentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = None
    submission_deadline: datetime | None = None
    review_deadline: datetime | None = None
    reviews_per_submission: int | None = Field(default=None, ge=1, le=5)
    criteria: list[CriterionCreate] | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_update(self) -> "AssignmentUpdate":
        if not self.model_fields_set:
            raise ValueError("Передайте хотя бы одно поле для изменения")
        required_fields = {
            "title",
            "submission_deadline",
            "review_deadline",
            "reviews_per_submission",
            "criteria",
        }
        null_fields = [
            field
            for field in self.model_fields_set & required_fields
            if getattr(self, field) is None
        ]
        if null_fields:
            raise ValueError("Эти поля не могут быть null: " + ", ".join(sorted(null_fields)))
        return self


class CriterionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    max_score: int


class AssignmentListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: int
    group_id: int | None
    title: str
    description: str | None
    submission_deadline: datetime
    review_deadline: datetime
    reviews_per_submission: int
    status: AssignmentStatus


class AssignmentRead(AssignmentListItem):
    max_score: int
    criteria: list[CriterionRead]
