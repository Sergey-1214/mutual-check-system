

from datetime import datetime
from enum import StrEnum
from pathlib import Path

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db import Base


class AssignmentStatus(StrEnum):
    PUBLISHED = "published"
    CLOSED = "closed"


class ReviewStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    group_id: Mapped[int | None] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    submission_deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    review_deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    reviews_per_submission: Mapped[int] = mapped_column(default=2)
    status: Mapped[AssignmentStatus] = mapped_column(
        SqlEnum(
            AssignmentStatus,
            name="assignment_status",
            native_enum=False,
            values_callable=lambda statuses: [status.value for status in statuses],
        ),
        default=AssignmentStatus.PUBLISHED,
    )

    criteria: Mapped[list["Criterion"]] = relationship(
        back_populates="assignment",
        cascade="all, delete-orphan",
        order_by="Criterion.id",
    )

    @property
    def max_score(self) -> int:
        return sum(criterion.max_score for criterion in self.criteria)


class Criterion(Base):
    __tablename__ = "criterions"

    id: Mapped[int] = mapped_column(primary_key=True)
    assignment_id: Mapped[int] = mapped_column(
        ForeignKey("assignments.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String(255))
    max_score: Mapped[int]

    assignment: Mapped[Assignment] = relationship(back_populates="criteria")


class Submission(Base):
    __tablename__ = "submissions"
    __table_args__ = (
        UniqueConstraint("student_id", "assignment_id", name="uq_submission_student_assignment"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    assignment_id: Mapped[int] = mapped_column(
        ForeignKey("assignments.id", ondelete="CASCADE")
    )
    file_path: Mapped[str] = mapped_column(String(500))
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    @property
    def original_filename(self) -> str:
        return Path(self.file_path).name


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("submission_id", "reviewer_id", name="uq_review_submission_reviewer"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    reviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    assignment_id: Mapped[int] = mapped_column(
        ForeignKey("assignments.id", ondelete="CASCADE")
    )
    submission_id: Mapped[int | None] = mapped_column(
        ForeignKey("submissions.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    score: Mapped[int | None]
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[ReviewStatus] = mapped_column(
        SqlEnum(
            ReviewStatus,
            name="review_status",
            native_enum=False,
            values_callable=lambda statuses: [status.value for status in statuses],
        ),
        default=ReviewStatus.PENDING,
    )
    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    scores: Mapped[list["ReviewScore"]] = relationship(
        back_populates="review",
        cascade="all, delete-orphan",
        order_by="ReviewScore.criterion_id",
    )


class ReviewScore(Base):
    __tablename__ = "review_scores"
    __table_args__ = (
        UniqueConstraint("review_id", "criterion_id", name="uq_review_score_criterion"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    review_id: Mapped[int] = mapped_column(
        ForeignKey("reviews.id", ondelete="CASCADE"),
        index=True,
    )
    criterion_id: Mapped[int] = mapped_column(
        ForeignKey("criterions.id", ondelete="CASCADE"),
    )
    score: Mapped[int]

    review: Mapped[Review] = relationship(back_populates="scores")
