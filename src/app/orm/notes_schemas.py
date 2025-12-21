from pydantic import BaseModel, ConfigDict, Field


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)

    model_config = ConfigDict(from_attributes=True)


class NoteDB(NoteSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
