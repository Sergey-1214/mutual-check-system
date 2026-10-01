from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.group import GroupStudent, StudyGroup
from src.models.user import User


class GroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        name: str,
        teacher_id: int,
        invite_code: str,
    ) -> StudyGroup:
        group = StudyGroup(
            name=name,
            teacher_id=teacher_id,
            invite_code=invite_code,
        )
        self.session.add(group)
        await self.session.flush()
        await self.session.refresh(group)
        return group

    async def get_by_id(self, group_id: int) -> StudyGroup | None:
        return await self.session.get(StudyGroup, group_id)

    async def get_by_invite_code(self, invite_code: str) -> StudyGroup | None:
        statement = select(StudyGroup).where(
            func.upper(StudyGroup.invite_code) == invite_code.upper()
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_for_teacher(self, teacher_id: int) -> Sequence[StudyGroup]:
        statement = (
            select(StudyGroup)
            .where(StudyGroup.teacher_id == teacher_id)
            .order_by(StudyGroup.id)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def list_for_student(self, student_id: int) -> Sequence[StudyGroup]:
        statement = (
            select(StudyGroup)
            .join(GroupStudent, GroupStudent.group_id == StudyGroup.id)
            .where(GroupStudent.student_id == student_id)
            .order_by(StudyGroup.id)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def add_student(self, *, group_id: int, student_id: int) -> None:
        self.session.add(GroupStudent(group_id=group_id, student_id=student_id))
        await self.session.flush()

    async def is_member(self, *, group_id: int, student_id: int) -> bool:
        statement = select(GroupStudent.group_id).where(
            GroupStudent.group_id == group_id,
            GroupStudent.student_id == student_id,
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none() is not None

    async def list_students(self, group_id: int):
        statement = (
            select(User, GroupStudent.joined_at)
            .join(GroupStudent, GroupStudent.student_id == User.id)
            .where(GroupStudent.group_id == group_id)
            .order_by(User.username)
        )
        result = await self.session.execute(statement)
        return result.all()

    async def commit(self) -> None:
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise

    async def rollback(self) -> None:
        await self.session.rollback()

