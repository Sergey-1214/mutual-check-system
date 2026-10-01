from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.assignment import Assignment, AssignmentStatus, Criterion
from src.models.group import GroupStudent


class AssignmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        teacher_id: int,
        group_id: int,
        title: str,
        description: str | None,
        submission_deadline: datetime,
        review_deadline: datetime,
        reviews_per_submission: int,
        criteria: Sequence[tuple[str, int]],
    ) -> Assignment:
        assignment = Assignment(
            teacher_id=teacher_id,
            group_id=group_id,
            title=title,
            description=description,
            submission_deadline=submission_deadline,
            review_deadline=review_deadline,
            reviews_per_submission=reviews_per_submission,
            status=AssignmentStatus.PUBLISHED,
            criteria=[
                Criterion(name=name, max_score=max_score)
                for name, max_score in criteria
            ],
        )
        self.session.add(assignment)
        try:
            await self.session.flush()
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise
        return assignment

    async def list_for_teacher(self, teacher_id: int) -> Sequence[Assignment]:
        statement = (
            select(Assignment)
            .where(Assignment.teacher_id == teacher_id)
            .order_by(Assignment.id)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def list_for_student(self, student_id: int) -> Sequence[Assignment]:
        statement = (
            select(Assignment)
            .join(GroupStudent, GroupStudent.group_id == Assignment.group_id)
            .where(
                GroupStudent.student_id == student_id,
                Assignment.status.in_([
                    AssignmentStatus.PUBLISHED,
                    AssignmentStatus.CLOSED,
                ]),
            )
            .order_by(Assignment.id)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_by_id(self, assignment_id: int) -> Assignment | None:
        statement = (
            select(Assignment)
            .where(Assignment.id == assignment_id)
            .options(selectinload(Assignment.criteria))
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def student_has_access(
        self,
        *,
        assignment_id: int,
        student_id: int,
    ) -> bool:
        statement = (
            select(Assignment.id)
            .join(GroupStudent, GroupStudent.group_id == Assignment.group_id)
            .where(
                Assignment.id == assignment_id,
                GroupStudent.student_id == student_id,
                Assignment.status.in_([
                    AssignmentStatus.PUBLISHED,
                    AssignmentStatus.CLOSED,
                ]),
            )
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none() is not None

    async def update(
        self,
        assignment: Assignment,
        *,
        values: dict[str, object],
        criteria: Sequence[tuple[str, int]] | None,
    ) -> Assignment:
        for field, value in values.items():
            setattr(assignment, field, value)
        if criteria is not None:
            assignment.criteria = [
                Criterion(name=name, max_score=max_score)
                for name, max_score in criteria
            ]
        await self.session.commit()
        return assignment

    async def set_status(
        self,
        assignment: Assignment,
        status: AssignmentStatus,
    ) -> Assignment:
        assignment.status = status
        await self.session.commit()
        return assignment

    async def delete(self, assignment: Assignment) -> None:
        await self.session.delete(assignment)
        await self.session.commit()
