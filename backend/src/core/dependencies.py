from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import TokenValidationError, decode_access_token
from src.db.db import get_db_session
from src.models.user import User, UserRole
from src.repository.user import UserRepository


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Требуется действующий access token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(str(payload["sub"]))
    except (TokenValidationError, KeyError, TypeError, ValueError) as error:
        raise unauthorized from error

    user = await UserRepository(session).get_by_id(user_id)
    if user is None:
        raise unauthorized
    return user


def require_roles(
    *allowed_roles: UserRole,
) -> Callable[..., Coroutine[Any, Any, User]]:
    async def check_role(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения операции",
            )
        return user

    return check_role
