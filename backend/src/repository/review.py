from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.assignment import Assignment, Criterion, Review, ReviewScore, ReviewStatus


class ReviewRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_for_reviewer(self, reviewer_id: int):
        statement = (
            select(Review, Assignment.title, Assignment.review_deadline)
            .join(Assignment, Assignment.id == Review.assignment_id)
            .where(
                Review.reviewer_id == reviewer_id,
                Review.submission_id.is_not(None),
            )
            .order_by(Assignment.review_deadline, Review.id)
        )
        result = await self.session.execute(statement)
        return result.all()

    async def get_for_reviewer(
        self,
        *,
        review_id: int,
        reviewer_id: int,
    ) -> Review | None:
        statement = (
            select(Review)
            .where(Review.id == review_id, Review.reviewer_id == reviewer_id)
            .options(selectinload(Review.scores))
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_criteria(self, assignment_id: int) -> Sequence[Criterion]:
        statement = (
            select(Criterion)
            .where(Criterion.assignment_id == assignment_id)
            .order_by(Criterion.id)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_assignment(self, assignment_id: int) -> Assignment | None:
        return await self.session.get(Assignment, assignment_id)

    async def replace_scores(
        self,
        review: Review,
        *,
        comment: str | None,
        scores: Sequence[tuple[int, int]],
    ) -> None:
        await self.session.execute(
            delete(ReviewScore).where(ReviewScore.review_id == review.id)
        )
        self.session.add_all(
            ReviewScore(review_id=review.id, criterion_id=criterion_id, score=score)
            for criterion_id, score in scores
        )
        review.comment = comment
        review.status = ReviewStatus.IN_PROGRESS
        await self.session.commit()

    async def complete(self, review: Review, *, score: int, submitted_at: datetime) -> None:
        review.score = score
        review.status = ReviewStatus.COMPLETED
        review.submitted_at = submitted_at
        await self.session.commit()

    async def existing_pairs(self, assignment_id: int) -> set[tuple[int, int]]:
        statement = select(Review.submission_id, Review.reviewer_id).where(
            Review.assignment_id == assignment_id,
            Review.submission_id.is_not(None),
        )
        result = await self.session.execute(statement)
        return {
            (submission_id, reviewer_id)
            for submission_id, reviewer_id in result.all()
            if submission_id is not None
        }

    async def create_many(
        self,
        rows: Sequence[tuple[int, int, int]],
    ) -> int:
        self.session.add_all(
            Review(
                submission_id=submission_id,
                reviewer_id=reviewer_id,
                assignment_id=assignment_id,
                status=ReviewStatus.PENDING,
            )
            for submission_id, reviewer_id, assignment_id in rows
        )
        await self.session.commit()
        return len(rows)

    async def completed_scores(self, submission_id: int) -> Sequence[int]:
        statement = select(Review.score).where(
            Review.submission_id == submission_id,
            Review.status == ReviewStatus.COMPLETED,
            Review.score.is_not(None),
        )
        result = await self.session.execute(statement)
        return [score for score in result.scalars().all() if score is not None]

    async def list_completed_for_submission(
        self,
        submission_id: int,
    ) -> Sequence[Review]:
        statement = (
            select(Review)
            .where(
                Review.submission_id == submission_id,
                Review.status == ReviewStatus.COMPLETED,
            )
            .options(selectinload(Review.scores))
            .order_by(Review.id)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()
