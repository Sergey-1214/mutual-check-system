from datetime import datetime, timezone

from src.models.assignment import Review, ReviewStatus
from src.repository.review import ReviewRepository
from src.schemas.review import (
    ReviewCriterionRead,
    ReviewListItem,
    ReviewRead,
    ReviewUpdate,
)


class ReviewNotFoundError(Exception):
    pass


class ReviewLockedError(Exception):
    pass


class ReviewValidationError(Exception):
    pass


class ReviewDeadlineError(Exception):
    pass


class ReviewService:
    def __init__(self, repository: ReviewRepository):
        self.repository = repository

    async def list_for_reviewer(self, reviewer_id: int) -> list[ReviewListItem]:
        rows = await self.repository.list_for_reviewer(reviewer_id)
        return [
            ReviewListItem(
                id=review.id,
                assignment_id=review.assignment_id,
                assignment_title=title,
                status=review.status,
                review_deadline=deadline,
            )
            for review, title, deadline in rows
        ]

    async def get(self, review_id: int, *, reviewer_id: int) -> ReviewRead:
        review = await self._get_model(review_id, reviewer_id=reviewer_id)
        return await self._to_read(review)

    async def update(
        self,
        review_id: int,
        data: ReviewUpdate,
        *,
        reviewer_id: int,
    ) -> ReviewRead:
        review = await self._get_model(review_id, reviewer_id=reviewer_id)
        if review.status == ReviewStatus.COMPLETED:
            raise ReviewLockedError
        await self._ensure_deadline(review)

        criteria = await self.repository.get_criteria(review.assignment_id)
        limits = {criterion.id: criterion.max_score for criterion in criteria}
        provided_ids = [item.criterion_id for item in data.scores]
        if len(provided_ids) != len(set(provided_ids)):
            raise ReviewValidationError("Критерий нельзя указывать дважды")
        if set(provided_ids) != set(limits):
            raise ReviewValidationError("Нужно выставить балл по каждому критерию")
        for item in data.scores:
            if item.score > limits[item.criterion_id]:
                raise ReviewValidationError(
                    f"Балл по критерию {item.criterion_id} не может быть больше {limits[item.criterion_id]}"
                )

        await self.repository.replace_scores(
            review,
            comment=data.comment.strip() if data.comment else None,
            scores=[(item.criterion_id, item.score) for item in data.scores],
        )
        return await self.get(review_id, reviewer_id=reviewer_id)

    async def submit(self, review_id: int, *, reviewer_id: int) -> ReviewRead:
        review = await self._get_model(review_id, reviewer_id=reviewer_id)
        if review.status == ReviewStatus.COMPLETED:
            raise ReviewLockedError
        await self._ensure_deadline(review)

        criteria = await self.repository.get_criteria(review.assignment_id)
        scores = {item.criterion_id: item.score for item in review.scores}
        if set(scores) != {criterion.id for criterion in criteria}:
            raise ReviewValidationError("Сначала выставьте баллы по всем критериям")
        if not review.comment or not review.comment.strip():
            raise ReviewValidationError("Добавьте комментарий к отзыву")

        await self.repository.complete(
            review,
            score=sum(scores.values()),
            submitted_at=datetime.now(timezone.utc),
        )
        return await self.get(review_id, reviewer_id=reviewer_id)

    async def _get_model(self, review_id: int, *, reviewer_id: int) -> Review:
        review = await self.repository.get_for_reviewer(
            review_id=review_id,
            reviewer_id=reviewer_id,
        )
        if review is None or review.submission_id is None:
            raise ReviewNotFoundError
        return review

    async def _to_read(self, review: Review) -> ReviewRead:
        criteria = await self.repository.get_criteria(review.assignment_id)
        scores = {item.criterion_id: item.score for item in review.scores}
        return ReviewRead(
            id=review.id,
            assignment_id=review.assignment_id,
            status=review.status,
            comment=review.comment,
            submitted_at=review.submitted_at,
            download_url=f"/api/v1/submissions/{review.submission_id}/file",
            criteria=[
                ReviewCriterionRead(
                    criterion_id=criterion.id,
                    name=criterion.name,
                    max_score=criterion.max_score,
                    score=scores.get(criterion.id),
                )
                for criterion in criteria
            ],
        )

    async def _ensure_deadline(self, review: Review) -> None:
        assignment = await self.repository.get_assignment(review.assignment_id)
        if assignment is None or assignment.review_deadline <= datetime.now(timezone.utc):
            raise ReviewDeadlineError
