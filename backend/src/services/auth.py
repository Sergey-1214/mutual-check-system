from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import (
    create_access_token,
    create_refresh_token,
    hash_token,
    verify_password,
)
from src.models.user import User
from src.repository.auth import RefreshTokenRepository
from src.repository.user import UserRepository
from src.schemas.auth import LoginRequest, RegisterRequest, TokenPair
from src.schemas.user import UserCreate
from src.services.user import UserService


class InvalidCredentialsError(Exception):
    pass


class InvalidRefreshTokenError(Exception):
    pass


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)
        self.refresh_tokens = RefreshTokenRepository(session)

    async def register(self, data: RegisterRequest) -> User:
        return await UserService(self.session).create(
            UserCreate(
                username=data.username,
                email=data.email,
                password=data.password,
                role=data.role,
            )
        )

    async def login(self, data: LoginRequest) -> TokenPair:
        user = await self.users.get_by_email(data.email)
        if user is None or not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsError("Неверный email или пароль")
        return await self._issue_pair(user)

    async def refresh(self, refresh_token: str) -> TokenPair:
        now = datetime.now(timezone.utc)
        stored = await self.refresh_tokens.get_by_hash(
            hash_token(refresh_token),
            lock=True,
        )
        if stored is None or stored.revoked_at is not None or stored.expires_at <= now:
            await self.session.rollback()
            raise InvalidRefreshTokenError("Refresh token недействителен, истёк или отозван")

        user = await self.users.get_by_id(stored.user_id)
        if user is None:
            await self.session.rollback()
            raise InvalidRefreshTokenError("Пользователь не найден")

        access_token, _ = create_access_token(user_id=user.id, role=user.role.value)
        refresh_token, expires_at = create_refresh_token()
        replacement = await self.refresh_tokens.create(
            user_id=user.id,
            token_hash=hash_token(refresh_token),
            expires_at=expires_at,
        )
        await self.refresh_tokens.revoke(
            stored,
            revoked_at=now,
            reason="rotated",
            replaced_by_token_id=replacement.id,
        )
        await self.session.commit()
        return self._pair(access_token, refresh_token)

    async def logout(self, refresh_token: str) -> None:
        stored = await self.refresh_tokens.get_by_hash(
            hash_token(refresh_token),
            lock=True,
        )
        if stored is None or stored.revoked_at is not None:
            await self.session.rollback()
            raise InvalidRefreshTokenError("Refresh token недействителен или уже отозван")

        await self.refresh_tokens.revoke(
            stored,
            revoked_at=datetime.now(timezone.utc),
            reason="logout",
        )
        await self.session.commit()

    async def _issue_pair(self, user: User) -> TokenPair:
        access_token, _ = create_access_token(user_id=user.id, role=user.role.value)
        refresh_token, expires_at = create_refresh_token()
        await self.refresh_tokens.create(
            user_id=user.id,
            token_hash=hash_token(refresh_token),
            expires_at=expires_at,
        )
        await self.session.commit()
        return self._pair(access_token, refresh_token)

    @staticmethod
    def _pair(access_token: str, refresh_token: str) -> TokenPair:
        from src.core.settings import settings

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.jwt_access_token_expire_minutes * 60,
        )
