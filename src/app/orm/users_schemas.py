from pydantic import BaseModel, ConfigDict, Field
from src.app.sql_enums import GenderEnum, ProfessionEnum


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)

    model_config = ConfigDict(from_attributes=True)


class NoteDB(NoteSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


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
