from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.assignment import Assignment, Submission
from src.models.group import GroupStudent


class SubmissionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        student_id: int,
        assignment_id: int,
        file_path: str,
    ) -> Submission:
        submission = Submission(
            student_id=student_id,
            assignment_id=assignment_id,
            file_path=file_path,
        )
        self.session.add(submission)
        try:
            await self.session.flush()
            await self.session.refresh(submission)
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise
        return submission

    async def get_by_id(self, submission_id: int) -> Submission | None:
        return await self.session.get(Submission, submission_id)

    async def get_for_student_assignment(
        self,
        *,
        student_id: int,
        assignment_id: int,
    ) -> Submission | None:
        statement = select(Submission).where(
            Submission.student_id == student_id,
            Submission.assignment_id == assignment_id,
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_for_student(self, student_id: int) -> Sequence[Submission]:
        statement = (
            select(Submission)
            .where(Submission.student_id == student_id)
            .order_by(Submission.submitted_at.desc())
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def list_for_assignment(self, assignment_id: int) -> Sequence[Submission]:
        statement = (
            select(Submission)
            .where(Submission.assignment_id == assignment_id)
            .order_by(Submission.id)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def assignment_exists(self, assignment_id: int) -> bool:
        statement = select(Assignment.id).where(Assignment.id == assignment_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none() is not None

    async def get_assignment(self, assignment_id: int) -> Assignment | None:
        return await self.session.get(Assignment, assignment_id)


    async def student_can_submit(
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
            )
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none() is not None
