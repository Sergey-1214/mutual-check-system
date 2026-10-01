from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user, require_roles
from src.db.db import get_db_session
from src.models.assignment import Assignment, Review, Submission
from src.models.user import User, UserRole
from src.repository.submission import SubmissionRepository
from src.repository.review import ReviewRepository
from src.schemas.submission import SubmissionFeedbackRead, SubmissionRead
from src.services.submission import (
    SubmissionAccessError,
    SubmissionAlreadyExistsError,
    SubmissionAssignmentNotFoundError,
    SubmissionClosedError,
    SubmissionFileError,
    SubmissionNotFoundError,
    SubmissionService,
)


router = APIRouter(prefix="/submissions", tags=["submissions"])


def get_submission_service(
    session: AsyncSession = Depends(get_db_session),
) -> SubmissionService:
    return SubmissionService(
        SubmissionRepository(session),
        ReviewRepository(session),
    )


@router.post("", response_model=SubmissionRead, status_code=status.HTTP_201_CREATED)
async def create_submission(
    assignment_id: int = Form(..., gt=0),
    file: UploadFile = File(...),
    service: SubmissionService = Depends(get_submission_service),
    student: User = Depends(require_roles(UserRole.STUDENT)),
) -> Submission:
    try:
        return await service.create(
            student_id=student.id,
            assignment_id=assignment_id,
            file=file,
        )
    except SubmissionFileError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    except SubmissionAssignmentNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задание не найдено",
        ) from error
    except SubmissionAccessError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Задание недоступно: студент не состоит в его группе",
        ) from error
    except SubmissionAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Работа на это задание уже отправлена",
        ) from error
    except SubmissionClosedError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Приём работ на это задание закрыт",
        ) from error


@router.get("/my", response_model=list[SubmissionRead])
async def list_my_submissions(
    service: SubmissionService = Depends(get_submission_service),
    student: User = Depends(require_roles(UserRole.STUDENT)),
) -> list[Submission]:
    return list(await service.list_for_student(student.id))


@router.get("/{submission_id}", response_model=SubmissionRead)
async def get_submission(
    submission_id: int,
    service: SubmissionService = Depends(get_submission_service),
    session: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> Submission:
    try:
        submission = await service.get(submission_id)
        await ensure_submission_access(submission, user, session)
        return submission
    except SubmissionNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Работа не найдена",
        ) from error


@router.get("/{submission_id}/file", response_class=FileResponse)
async def download_submission_file(
    submission_id: int,
    service: SubmissionService = Depends(get_submission_service),
    session: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> FileResponse:
    try:
        submission, file_path = await service.get_file(submission_id)
        access = await ensure_submission_access(
            submission,
            user,
            session,
            allow_reviewer=True,
        )
    except (SubmissionNotFoundError, SubmissionFileError) as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Файл работы не найден",
        ) from error
    return FileResponse(
        path=file_path,
        filename=(
            f"anonymous-work{file_path.suffix}"
            if access == "reviewer"
            else submission.original_filename
        ),
        media_type="application/octet-stream",
    )


@router.get("/{submission_id}/feedback", response_model=SubmissionFeedbackRead)
async def get_submission_feedback(
    submission_id: int,
    service: SubmissionService = Depends(get_submission_service),
    session: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> SubmissionFeedbackRead:
    try:
        submission = await service.get(submission_id)
        await ensure_submission_access(submission, user, session)
        return await service.get_feedback(submission_id)
    except SubmissionNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Работа не найдена",
        ) from error


async def ensure_submission_access(
    submission: Submission,
    user: User,
    session: AsyncSession,
    *,
    allow_reviewer: bool = False,
) -> str:
    if user.role == UserRole.STUDENT and submission.student_id == user.id:
        return "owner"
    if user.role == UserRole.TEACHER:
        assignment = await session.get(Assignment, submission.assignment_id)
        if assignment is not None and assignment.teacher_id == user.id:
            return "teacher"
    if allow_reviewer and user.role == UserRole.STUDENT:
        statement = select(Review.id).where(
            Review.submission_id == submission.id,
            Review.reviewer_id == user.id,
        )
        result = await session.execute(statement)
        if result.scalar_one_or_none() is not None:
            return "reviewer"
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Нет доступа к этой работе",
    )
