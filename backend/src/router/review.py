from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import require_roles
from src.db.db import get_db_session
from src.models.user import User, UserRole
from src.repository.review import ReviewRepository
from src.schemas.review import ReviewListItem, ReviewRead, ReviewUpdate
from src.services.review import (
    ReviewDeadlineError,
    ReviewLockedError,
    ReviewNotFoundError,
    ReviewService,
    ReviewValidationError,
)


router = APIRouter(prefix="/reviews", tags=["reviews"])


def get_review_service(
    session: AsyncSession = Depends(get_db_session),
) -> ReviewService:
    return ReviewService(ReviewRepository(session))


@router.get("", response_model=list[ReviewListItem])
async def list_reviews(
    service: ReviewService = Depends(get_review_service),
    student: User = Depends(require_roles(UserRole.STUDENT)),
) -> list[ReviewListItem]:
    return await service.list_for_reviewer(student.id)


@router.get("/{review_id}", response_model=ReviewRead)
async def get_review(
    review_id: int,
    service: ReviewService = Depends(get_review_service),
    student: User = Depends(require_roles(UserRole.STUDENT)),
) -> ReviewRead:
    try:
        return await service.get(review_id, reviewer_id=student.id)
    except ReviewNotFoundError as error:
        raise HTTPException(status_code=404, detail="Проверка не найдена") from error


@router.patch("/{review_id}", response_model=ReviewRead)
async def update_review(
    review_id: int,
    data: ReviewUpdate,
    service: ReviewService = Depends(get_review_service),
    student: User = Depends(require_roles(UserRole.STUDENT)),
) -> ReviewRead:
    try:
        return await service.update(review_id, data, reviewer_id=student.id)
    except ReviewNotFoundError as error:
        raise HTTPException(status_code=404, detail="Проверка не найдена") from error
    except ReviewLockedError as error:
        raise HTTPException(status_code=409, detail="Отправленный отзыв нельзя изменить") from error
    except ReviewDeadlineError as error:
        raise HTTPException(status_code=409, detail="Срок проверки истёк") from error
    except ReviewValidationError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/{review_id}/submit", response_model=ReviewRead)
async def submit_review(
    review_id: int,
    service: ReviewService = Depends(get_review_service),
    student: User = Depends(require_roles(UserRole.STUDENT)),
) -> ReviewRead:
    try:
        return await service.submit(review_id, reviewer_id=student.id)
    except ReviewNotFoundError as error:
        raise HTTPException(status_code=404, detail="Проверка не найдена") from error
    except ReviewLockedError as error:
        raise HTTPException(status_code=409, detail="Отзыв уже отправлен") from error
    except ReviewDeadlineError as error:
        raise HTTPException(status_code=409, detail="Срок проверки истёк") from error
    except ReviewValidationError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
