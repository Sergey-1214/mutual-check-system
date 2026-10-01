from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime, timezone

from src.models.assignment import Assignment, AssignmentStatus
from src.models.user import UserRole
from src.repository.assignment import AssignmentRepository
from src.repository.group import GroupRepository
from src.repository.review import ReviewRepository
from src.repository.submission import SubmissionRepository
from src.schemas.assignment import AssignmentCreate, AssignmentUpdate
from src.schemas.submission import SubmissionResultRead


class AssignmentNotFoundError(Exception):
    pass


class AssignmentGroupNotFoundError(Exception):
    pass


class AssignmentGroupAccessError(Exception):
    pass


class NotEnoughSubmissionsError(Exception):
    pass


class AssignmentStateError(Exception):
    pass


class AssignmentDeadlineError(Exception):
    pass


class AssignmentService:
    def __init__(
        self,
        repository: AssignmentRepository,
        groups: GroupRepository,
        submissions: SubmissionRepository,
        reviews: ReviewRepository,
    ):
        self.repository = repository
        self.groups = groups
        self.submissions = submissions
        self.reviews = reviews

    async def create(self, data: AssignmentCreate, *, teacher_id: int) -> Assignment:
        group = await self.groups.get_by_id(data.group_id)
        if group is None:
            raise AssignmentGroupNotFoundError
        if group.teacher_id != teacher_id:
            raise AssignmentGroupAccessError
        if data.submission_deadline <= datetime.now(timezone.utc):
            raise AssignmentDeadlineError("Срок сдачи должен быть в будущем")
        return await self.repository.create(
            teacher_id=teacher_id,
            group_id=data.group_id,
            title=data.title,
            description=data.description,
            submission_deadline=data.submission_deadline,
            review_deadline=data.review_deadline,
            reviews_per_submission=data.reviews_per_submission,
            criteria=[
                (criterion.name, criterion.max_score)
                for criterion in data.criteria
            ],
        )

    async def list(
        self,
        *,
        user_id: int,
        role: UserRole,
    ) -> Sequence[Assignment]:
        if role == UserRole.TEACHER:
            return await self.repository.list_for_teacher(user_id)
        return await self.repository.list_for_student(user_id)

    async def get(
        self,
        assignment_id: int,
        *,
        user_id: int,
        role: UserRole,
    ) -> Assignment:
        assignment = await self.repository.get_by_id(assignment_id)
        if assignment is None:
            raise AssignmentNotFoundError

        if role == UserRole.TEACHER and assignment.teacher_id == user_id:
            return assignment
        if role == UserRole.STUDENT and await self.repository.student_has_access(
            assignment_id=assignment_id,
            student_id=user_id,
        ):
            return assignment
        raise AssignmentNotFoundError

    async def update(
        self,
        assignment_id: int,
        data: AssignmentUpdate,
        *,
        teacher_id: int,
    ) -> Assignment:
        assignment = await self.get(
            assignment_id,
            user_id=teacher_id,
            role=UserRole.TEACHER,
        )
        if assignment.status != AssignmentStatus.PUBLISHED:
            raise AssignmentStateError("Закрытое задание нельзя редактировать")

        values = data.model_dump(exclude_unset=True)
        criteria_data = values.pop("criteria", None)
        submission_deadline = values.get(
            "submission_deadline",
            assignment.submission_deadline,
        )
        review_deadline = values.get("review_deadline", assignment.review_deadline)
        if review_deadline <= submission_deadline:
            raise AssignmentDeadlineError("Срок проверки должен быть позже срока сдачи")

        criteria = None
        if criteria_data is not None:
            criteria = [
                (criterion["name"], criterion["max_score"])
                for criterion in criteria_data
            ]
        return await self.repository.update(
            assignment,
            values=values,
            criteria=criteria,
        )

    async def delete(self, assignment_id: int, *, teacher_id: int) -> None:
        assignment = await self.get(
            assignment_id,
            user_id=teacher_id,
            role=UserRole.TEACHER,
        )
        if assignment.status != AssignmentStatus.PUBLISHED:
            raise AssignmentStateError("Закрытое задание нельзя удалить")
        await self.repository.delete(assignment)

    async def close(self, assignment_id: int, *, teacher_id: int) -> Assignment:
        assignment = await self.get(
            assignment_id,
            user_id=teacher_id,
            role=UserRole.TEACHER,
        )
        if assignment.status != AssignmentStatus.PUBLISHED:
            raise AssignmentStateError("Закрыть можно только опубликованное задание")
        await self._create_reviews(assignment)
        return await self.repository.set_status(assignment, AssignmentStatus.CLOSED)

    async def list_submissions(
        self,
        assignment_id: int,
        *,
        teacher_id: int,
    ):
        await self.get(
            assignment_id,
            user_id=teacher_id,
            role=UserRole.TEACHER,
        )
        return await self.submissions.list_for_assignment(assignment_id)

    async def _create_reviews(
        self,
        assignment: Assignment,
    ) -> None:
        assignment_id = assignment.id
        submissions = list(await self.submissions.list_for_assignment(assignment_id))
        if len(submissions) < 2:
            raise NotEnoughSubmissionsError

        reviews_count = min(assignment.reviews_per_submission, len(submissions) - 1)
        existing = await self.reviews.existing_pairs(assignment_id)
        rows: list[tuple[int, int, int]] = []
        for index, submission in enumerate(submissions):
            for shift in range(1, reviews_count + 1):
                reviewer = submissions[(index + shift) % len(submissions)]
                pair = (submission.id, reviewer.student_id)
                if pair not in existing:
                    rows.append((submission.id, reviewer.student_id, assignment_id))

        if rows:
            await self.reviews.create_many(rows)

    async def results(
        self,
        assignment_id: int,
        *,
        teacher_id: int,
    ) -> list[SubmissionResultRead]:
        await self.get(
            assignment_id,
            user_id=teacher_id,
            role=UserRole.TEACHER,
        )
        submissions = await self.submissions.list_for_assignment(assignment_id)
        result: list[SubmissionResultRead] = []
        for submission in submissions:
            scores = await self.reviews.completed_scores(submission.id)
            result.append(
                SubmissionResultRead(
                    id=submission.id,
                    student_id=submission.student_id,
                    assignment_id=submission.assignment_id,
                    original_filename=submission.original_filename,
                    submitted_at=submission.submitted_at,
                    completed_reviews=len(scores),
                    average_score=(round(sum(scores) / len(scores), 2) if scores else None),
                )
            )
        return result
