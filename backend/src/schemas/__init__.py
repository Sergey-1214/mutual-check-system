from src.schemas.assignment import (
    AssignmentCreate,
    AssignmentListItem,
    AssignmentRead,
    CriterionCreate,
    CriterionRead,
)
from src.schemas.auth import LoginRequest, RegisterRequest, TokenPair, TokenResponse
from src.schemas.submission import SubmissionRead
from src.schemas.user import UserCreate, UserRead, UserUpdate

__all__ = [
    "AssignmentCreate",
    "AssignmentListItem",
    "AssignmentRead",
    "CriterionCreate",
    "CriterionRead",
    "LoginRequest",
    "RegisterRequest",
    "SubmissionRead",
    "TokenPair",
    "TokenResponse",
    "UserCreate",
    "UserRead",
    "UserUpdate",
]
