from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import hash_password
from src.models.user import User
from src.repository.user import UserRepository
from src.schemas.user import UserCreate, UserUpdate


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UserRepository(session)

    async def create(self, data: UserCreate) -> User:
        try:
            user = await self.repository.create(
                username=data.username,
                email=data.email,
                password_hash=hash_password(data.password),
                role=data.role,
            )
            await self.session.commit()
            return user
        except IntegrityError as error:
            await self.session.rollback()
            raise UserAlreadyExistsError(
                "Пользователь с таким username или email уже существует"
            ) from error

    async def get(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError
        return user

    async def list(self, *, offset: int, limit: int) -> Sequence[User]:
        return await self.repository.list(offset=offset, limit=limit)

    async def update(self, user_id: int, data: UserUpdate) -> User:
        user = await self.get(user_id)
        values = data.model_dump(exclude_unset=True)
        if not values:
            return user

        username = values.get("username")
        email = values.get("email")
        await self._ensure_unique(
            username=username if isinstance(username, str) else None,
            email=email if isinstance(email, str) else None,
            excluded_user_id=user_id,
        )

        password = values.pop("password", None)
        if isinstance(password, str):
            values["password_hash"] = hash_password(password)

        try:
            user = await self.repository.update(user, values)
            await self.session.commit()
            return user
        except IntegrityError as error:
            await self.session.rollback()
            raise UserAlreadyExistsError(
                "Пользователь с таким username или email уже существует"
            ) from error

    async def delete(self, user_id: int) -> None:
        user = await self.get(user_id)
        await self.repository.delete(user)
        await self.session.commit()

    async def _ensure_unique(
        self,
        *,
        username: str | None,
        email: str | None,
        excluded_user_id: int | None = None,
    ) -> None:
        if username is not None:
            existing = await self.repository.get_by_username(username)
            if existing is not None and existing.id != excluded_user_id:
                raise UserAlreadyExistsError("Этот username уже занят")
        if email is not None:
            existing = await self.repository.get_by_email(email)
            if existing is not None and existing.id != excluded_user_id:
                raise UserAlreadyExistsError("Этот email уже занят")
