from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user, require_roles
from src.db.db import get_db_session
from src.models.group import StudyGroup
from src.models.user import User, UserRole
from src.repository.group import GroupRepository
from src.schemas.group import GroupCreate, GroupRead, GroupStudentRead, JoinGroupRequest
from src.services.group import (
    AlreadyGroupMemberError,
    GroupAccessError,
    GroupNotFoundError,
    GroupService,
)


router = APIRouter(prefix="/groups", tags=["groups"])


def get_group_service(
    session: AsyncSession = Depends(get_db_session),
) -> GroupService:
    return GroupService(GroupRepository(session))


@router.post("", response_model=GroupRead, status_code=status.HTTP_201_CREATED)
async def create_group(
    data: GroupCreate,
    service: GroupService = Depends(get_group_service),
    teacher: User = Depends(require_roles(UserRole.TEACHER)),
) -> StudyGroup:
    return await service.create(data, teacher_id=teacher.id)


@router.get("", response_model=list[GroupRead])
async def list_groups(
    service: GroupService = Depends(get_group_service),
    user: User = Depends(get_current_user),
) -> list[StudyGroup]:
    return list(await service.list_for_user(user))


@router.post("/join", response_model=GroupRead)
async def join_group(
    data: JoinGroupRequest,
    service: GroupService = Depends(get_group_service),
    student: User = Depends(require_roles(UserRole.STUDENT)),
) -> StudyGroup:
    try:
        return await service.join(data, student_id=student.id)
    except GroupNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Группа с таким кодом не найдена",
        ) from error
    except AlreadyGroupMemberError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Студент уже состоит в этой группе",
        ) from error


@router.get("/{group_id}/students", response_model=list[GroupStudentRead])
async def list_group_students(
    group_id: int,
    service: GroupService = Depends(get_group_service),
    teacher: User = Depends(require_roles(UserRole.TEACHER)),
) -> list[GroupStudentRead]:
    try:
        return await service.list_students(group_id=group_id, teacher_id=teacher.id)
    except GroupNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Группа не найдена",
        ) from error
    except GroupAccessError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Можно просматривать учеников только в своих группах",
        ) from error

