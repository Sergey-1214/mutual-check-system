from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError

from src.core.settings import settings
from src.models.assignment import AssignmentStatus, Submission
from src.repository.submission import SubmissionRepository
from src.repository.review import ReviewRepository
from src.schemas.submission import (
    FeedbackCriterionRead,
    FeedbackReviewRead,
    SubmissionFeedbackRead,
)


class SubmissionNotFoundError(Exception):
    pass


class SubmissionFileError(Exception):
    pass


class SubmissionAssignmentNotFoundError(Exception):
    pass


class SubmissionAccessError(Exception):
    pass


class SubmissionAlreadyExistsError(Exception):
    pass


class SubmissionClosedError(Exception):
    pass


class SubmissionService:
    def __init__(
        self,
        repository: SubmissionRepository,
        reviews: ReviewRepository,
        upload_dir: Path = settings.submission_upload_dir,
    ):
        self.repository = repository
        self.reviews = reviews
        self.upload_dir = upload_dir.resolve()

    async def create(
        self,
        *,
        student_id: int,
        assignment_id: int,
        file: UploadFile,
    ) -> Submission:
        assignment = await self.repository.get_assignment(assignment_id)
        if assignment is None:
            raise SubmissionAssignmentNotFoundError
        if not await self.repository.student_can_submit(
            assignment_id=assignment_id,
            student_id=student_id,
        ):
            raise SubmissionAccessError
        if (
            assignment.status != AssignmentStatus.PUBLISHED
            or assignment.submission_deadline <= datetime.now(timezone.utc)
        ):
            raise SubmissionClosedError
        if await self.repository.get_for_student_assignment(
            student_id=student_id,
            assignment_id=assignment_id,
        ) is not None:
            raise SubmissionAlreadyExistsError

        original_filename = Path(file.filename or "").name
        if not original_filename or original_filename in {".", ".."}:
            raise SubmissionFileError("У файла отсутствует имя")
        if len(original_filename) > 255:
            raise SubmissionFileError("Имя файла слишком длинное")

        submission_dir = self.upload_dir / uuid4().hex
        submission_dir.mkdir(parents=True, exist_ok=False)
        destination = submission_dir / original_filename
        written_bytes = 0

        try:
            with destination.open("wb") as output:
                while chunk := await file.read(1024 * 1024):
                    output.write(chunk)
                    written_bytes += len(chunk)

            if written_bytes == 0:
                raise SubmissionFileError("Нельзя сохранить пустой файл")

            return await self.repository.create(
                student_id=student_id,
                assignment_id=assignment_id,
                file_path=str(destination),
            )
        except IntegrityError as error:
            destination.unlink(missing_ok=True)
            submission_dir.rmdir()
            raise SubmissionAlreadyExistsError from error
        except BaseException:
            destination.unlink(missing_ok=True)
            submission_dir.rmdir()
            raise
        finally:
            await file.close()

    async def get(self, submission_id: int) -> Submission:
        submission = await self.repository.get_by_id(submission_id)
        if submission is None:
            raise SubmissionNotFoundError
        return submission

    async def list_for_student(self, student_id: int):
        return await self.repository.list_for_student(student_id)

    async def get_file(self, submission_id: int) -> tuple[Submission, Path]:
        submission = await self.get(submission_id)
        file_path = Path(submission.file_path).resolve()
        if not file_path.is_relative_to(self.upload_dir) or not file_path.is_file():
            raise SubmissionFileError("Файл работы не найден")
        return submission, file_path

    async def get_feedback(self, submission_id: int) -> SubmissionFeedbackRead:
        submission = await self.get(submission_id)
        criteria = await self.reviews.get_criteria(submission.assignment_id)
        criteria_by_id = {criterion.id: criterion for criterion in criteria}
        completed = await self.reviews.list_completed_for_submission(submission_id)

        feedback: list[FeedbackReviewRead] = []
        totals: list[int] = []
        for review in completed:
            score_items = []
            for item in review.scores:
                criterion = criteria_by_id.get(item.criterion_id)
                if criterion is not None:
                    score_items.append(
                        FeedbackCriterionRead(
                            name=criterion.name,
                            max_score=criterion.max_score,
                            score=item.score,
                        )
                    )
            total = review.score if review.score is not None else sum(
                item.score for item in review.scores
            )
            totals.append(total)
            feedback.append(
                FeedbackReviewRead(
                    score=total,
                    comment=review.comment or "",
                    criteria=score_items,
                )
            )

        return SubmissionFeedbackRead(
            submission_id=submission.id,
            assignment_id=submission.assignment_id,
            average_score=(round(sum(totals) / len(totals), 2) if totals else None),
            completed_reviews=len(feedback),
            reviews=feedback,
        )
