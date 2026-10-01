from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

from src.models.user import UserRole

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr = Field(max_length=256)
    password: str = Field(min_length=8, max_length=128)
    role: UserRole

    @field_validator("username")
    @classmethod
    def strip_username(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Имя пользователя не может быть пустым")
        return value

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=100)
    email: EmailStr | None = Field(default=None, max_length=256)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    role: UserRole | None = None

    @field_validator("username")
    @classmethod
    def strip_username(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("Имя пользователя не может быть пустым")
        return value

    @model_validator(mode="after")
    def reject_explicit_nulls(self) -> "UserUpdate":
        null_fields = [
            field_name
            for field_name in self.model_fields_set
            if getattr(self, field_name) is None
        ]
        if null_fields:
            raise ValueError(
                "Поля обновления не могут быть null: " + ", ".join(sorted(null_fields))
            )
        return self


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime
