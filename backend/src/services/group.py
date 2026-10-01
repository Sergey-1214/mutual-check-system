import secrets
import string
from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError

from src.models.group import StudyGroup
from src.models.user import User, UserRole
from src.repository.group import GroupRepository
from src.schemas.group import GroupCreate, GroupStudentRead, JoinGroupRequest


class GroupNotFoundError(Exception):
    pass


class GroupAccessError(Exception):
    pass


class AlreadyGroupMemberError(Exception):
    pass


class GroupService:
    def __init__(self, repository: GroupRepository):
        self.repository = repository

    async def create(self, data: GroupCreate, *, teacher_id: int) -> StudyGroup:
        for _ in range(10):
            invite_code = "".join(
                secrets.choice(string.ascii_uppercase + string.digits)
                for _ in range(8)
            )
            if await self.repository.get_by_invite_code(invite_code) is None:
                try:
                    group = await self.repository.create(
                        name=data.name,
                        teacher_id=teacher_id,
                        invite_code=invite_code,
                    )
                    await self.repository.commit()
                    return group
                except IntegrityError:
                    await self.repository.rollback()
        raise RuntimeError("Не удалось создать уникальный код приглашения")

    async def list_for_user(self, user: User) -> Sequence[StudyGroup]:
        if user.role == UserRole.TEACHER:
            return await self.repository.list_for_teacher(user.id)
        return await self.repository.list_for_student(user.id)

    async def join(self, data: JoinGroupRequest, *, student_id: int) -> StudyGroup:
        group = await self.repository.get_by_invite_code(data.invite_code)
        if group is None:
            raise GroupNotFoundError
        if await self.repository.is_member(group_id=group.id, student_id=student_id):
            raise AlreadyGroupMemberError
        try:
            await self.repository.add_student(group_id=group.id, student_id=student_id)
            await self.repository.commit()
        except IntegrityError as error:
            await self.repository.rollback()
            raise AlreadyGroupMemberError from error
        return group

    async def list_students(
        self,
        *,
        group_id: int,
        teacher_id: int,
    ) -> list[GroupStudentRead]:
        group = await self.repository.get_by_id(group_id)
        if group is None:
            raise GroupNotFoundError
        if group.teacher_id != teacher_id:
            raise GroupAccessError

        rows = await self.repository.list_students(group_id)
        return [
            GroupStudentRead(
                id=user.id,
                username=user.username,
                email=user.email,
                joined_at=joined_at,
            )
            for user, joined_at in rows
        ]
