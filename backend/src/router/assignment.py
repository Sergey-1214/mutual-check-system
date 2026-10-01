from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user, require_roles
from src.db.db import get_db_session
from src.models.assignment import Assignment, Submission
from src.models.user import User, UserRole
from src.repository.assignment import AssignmentRepository
from src.repository.group import GroupRepository
from src.repository.review import ReviewRepository
from src.repository.submission import SubmissionRepository
from src.schemas.assignment import (
    AssignmentCreate,
    AssignmentListItem,
    AssignmentRead,
    AssignmentUpdate,
)
from src.schemas.submission import SubmissionRead, SubmissionResultRead
from src.services.assignment import (
    AssignmentGroupAccessError,
    AssignmentGroupNotFoundError,
    AssignmentDeadlineError,
    AssignmentNotFoundError,
    AssignmentService,
    AssignmentStateError,
    NotEnoughSubmissionsError,
)


router = APIRouter(prefix="/assignments", tags=["assignments"])


def get_assignment_service(
    session: AsyncSession = Depends(get_db_session),
) -> AssignmentService:
    return AssignmentService(
        AssignmentRepository(session),
        GroupRepository(session),
        SubmissionRepository(session),
        ReviewRepository(session),
    )


@router.post("", response_model=AssignmentRead, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    data: AssignmentCreate,
    service: AssignmentService = Depends(get_assignment_service),
    teacher: User = Depends(require_roles(UserRole.TEACHER)),
) -> Assignment:
    try:
        return await service.create(data, teacher_id=teacher.id)
    except AssignmentGroupNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Группа не найдена",
        ) from error
    except AssignmentGroupAccessError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Можно создавать задания только для своих групп",
        ) from error
    except AssignmentDeadlineError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("", response_model=list[AssignmentListItem])
async def list_assignments(
    service: AssignmentService = Depends(get_assignment_service),
    user: User = Depends(get_current_user),
) -> list[Assignment]:
    return list(await service.list(user_id=user.id, role=user.role))


@router.get("/{assignment_id}", response_model=AssignmentRead)
async def get_assignment(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service),
    user: User = Depends(get_current_user),
) -> Assignment:
    try:
        return await service.get(
            assignment_id,
            user_id=user.id,
            role=user.role,
        )
    except AssignmentNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задание не найдено",
        ) from error


@router.patch("/{assignment_id}", response_model=AssignmentRead)
async def update_assignment(
    assignment_id: int,
    data: AssignmentUpdate,
    service: AssignmentService = Depends(get_assignment_service),
    teacher: User = Depends(require_roles(UserRole.TEACHER)),
) -> Assignment:
    try:
        return await service.update(assignment_id, data, teacher_id=teacher.id)
    except AssignmentNotFoundError as error:
        raise HTTPException(status_code=404, detail="Задание не найдено") from error
    except AssignmentStateError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except AssignmentDeadlineError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assignment(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service),
    teacher: User = Depends(require_roles(UserRole.TEACHER)),
) -> Response:
    try:
        await service.delete(assignment_id, teacher_id=teacher.id)
    except AssignmentNotFoundError as error:
        raise HTTPException(status_code=404, detail="Задание не найдено") from error
    except AssignmentStateError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{assignment_id}/close", response_model=AssignmentRead)
async def close_assignment(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service),
    teacher: User = Depends(require_roles(UserRole.TEACHER)),
) -> Assignment:
    try:
        return await service.close(assignment_id, teacher_id=teacher.id)
    except AssignmentNotFoundError as error:
        raise HTTPException(status_code=404, detail="Задание не найдено") from error
    except AssignmentStateError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except NotEnoughSubmissionsError as error:
        raise HTTPException(
            status_code=400,
            detail="Для закрытия нужны хотя бы две сданные работы",
        ) from error


@router.get("/{assignment_id}/submissions", response_model=list[SubmissionRead])
async def list_assignment_submissions(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service),
    teacher: User = Depends(require_roles(UserRole.TEACHER)),
) -> list[Submission]:
    try:
        return list(await service.list_submissions(assignment_id, teacher_id=teacher.id))
    except AssignmentNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задание не найдено",
        ) from error


@router.get("/{assignment_id}/results", response_model=list[SubmissionResultRead])
async def get_assignment_results(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service),
    teacher: User = Depends(require_roles(UserRole.TEACHER)),
) -> list[SubmissionResultRead]:
    try:
        return await service.results(assignment_id, teacher_id=teacher.id)
    except AssignmentNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задание не найдено",
        ) from error
