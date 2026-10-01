from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from src.core.settings import settings
from src.db.db import Base, dispose_db_engine, engine
from src.models import (  # noqa: F401
    Assignment,
    Criterion,
    GroupStudent,
    RefreshToken,
    Review,
    ReviewScore,
    StudyGroup,
    Submission,
    User,
)
from src.router.auth import router as auth_router
from src.router.assignment import router as assignment_router
from src.router.group import router as group_router
from src.router.review import router as review_router
from src.router.submission import router as submission_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        # create_all не изменяет уже существующие таблицы. Эта небольшая
        # совместимая миграция сохраняет ранее созданные задания.
        await connection.execute(
            text(
                "ALTER TABLE assignments "
                "ADD COLUMN IF NOT EXISTS group_id INTEGER "
                "REFERENCES groups(id) ON DELETE CASCADE"
            )
        )
        await connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_assignments_group_id "
                "ON assignments (group_id)"
            )
        )
        await connection.execute(
            text(
                "ALTER TABLE assignments "
                "ADD COLUMN IF NOT EXISTS reviews_per_submission INTEGER "
                "NOT NULL DEFAULT 2"
            )
        )
        await connection.execute(
            text(
                "UPDATE assignments SET status = 'published' "
                "WHERE status = 'draft'"
            )
        )
        await connection.execute(
            text(
                "ALTER TABLE reviews "
                "ADD COLUMN IF NOT EXISTS submission_id INTEGER "
                "REFERENCES submissions(id) ON DELETE CASCADE"
            )
        )
        await connection.execute(
            text(
                "ALTER TABLE reviews "
                "ADD COLUMN IF NOT EXISTS submitted_at TIMESTAMPTZ"
            )
        )
        await connection.execute(
            text(
                "CREATE UNIQUE INDEX IF NOT EXISTS uq_review_submission_reviewer "
                "ON reviews (submission_id, reviewer_id) "
                "WHERE submission_id IS NOT NULL"
            )
        )
        await connection.execute(
            text(
                "DO $$ BEGIN "
                "IF NOT EXISTS ("
                "SELECT 1 FROM submissions "
                "GROUP BY student_id, assignment_id HAVING COUNT(*) > 1"
                ") THEN "
                "CREATE UNIQUE INDEX IF NOT EXISTS uq_submission_student_assignment "
                "ON submissions (student_id, assignment_id); "
                "END IF; END $$"
            )
        )
    yield
    await dispose_db_engine()


app = FastAPI(
    title="Mutual Checks API",
    description="API платформы взаимной проверки для учителей и учеников",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(group_router, prefix="/api/v1")
app.include_router(assignment_router, prefix="/api/v1")
app.include_router(submission_router, prefix="/api/v1")
app.include_router(review_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
