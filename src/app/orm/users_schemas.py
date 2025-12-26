from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.app.sql_enums import GenderEnum, ProfessionEnum


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
    username: str = Field(..., description="User's username")
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
    first_name: str = Field(..., description="User's first name")
    last_name: str | None = Field(None, description="User's last name")
    age: int | None = Field(None, description="User's age")
    gender: GenderEnum = Field(..., description="User's gender")
    profession: ProfessionEnum | None = Field(None, description="User's profession")
    interests: list[str] | None = Field(None, description="User's interests")
    contacts: dict[str, str] | None = Field(None, description="User's contacts")

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
