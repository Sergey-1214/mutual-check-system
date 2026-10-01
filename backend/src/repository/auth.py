from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.auth import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> RefreshToken:
        token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.session.add(token)
        await self.session.flush()
        return token

    async def get_by_hash(
        self,
        token_hash: str,
        *,
        lock: bool = False,
    ) -> RefreshToken | None:
        statement = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        if lock:
            statement = statement.with_for_update()
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def revoke(
        self,
        token: RefreshToken,
        *,
        revoked_at: datetime,
        reason: str,
        replaced_by_token_id: int | None = None,
    ) -> None:
        token.revoked_at = revoked_at
        token.revoke_reason = reason
        token.replaced_by_token_id = replaced_by_token_id
        await self.session.flush()
