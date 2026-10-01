from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class GroupCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Название группы не может быть пустым")
        return value


class GroupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    teacher_id: int
    invite_code: str
    created_at: datetime


class JoinGroupRequest(BaseModel):
    invite_code: str = Field(min_length=1, max_length=12)

    @field_validator("invite_code")
    @classmethod
    def normalize_invite_code(cls, value: str) -> str:
        return value.strip().upper()


class GroupStudentRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    joined_at: datetime

