from pydantic import BaseModel, ConfigDict
from src.app.sql_enums import GenderEnum, ProfessionEnum
from datetime import datetime


class ProfileSchema(BaseModel):
    first_name: str
    last_name: str | None
    age: int | None
    gender: GenderEnum
    profession: ProfessionEnum
    interests: list[str] | None
    contacts: dict | None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserSchema(BaseModel):
    username: str
    email: str
    profile: ProfileSchema | None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserSchemaIn(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str | None
    age: int | None
    gender: GenderEnum
    profession: ProfessionEnum
    interests: list[str] | None
    contacts: dict | None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserSearchSchema(BaseModel):
    username: str | None = None
    email: str | None = None
    created_at_from: datetime | None = None
    created_at_to: datetime | None = None
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    gender: GenderEnum | None = None
    profession: ProfessionEnum | None = None
    interests: str | None = None
