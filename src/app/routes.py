from fastapi import APIRouter, HTTPException, status
from src.app.orm import notes_crud, notes_schemas, users_crud, users_schemas

router = APIRouter()


@router.post("/users/add", response_model=users_schemas.UserSchema)
async def insert_user(user: users_schemas.UserSchemaIn):
    result = await users_crud.add_full_user(user.model_dump())
    user = users_schemas.UserSchema.model_validate(result)
    return user


@router.get("/users/get", response_model=list[users_schemas.UserSchema])
async def get_users():
    return await users_crud.get_all_users()


# ---------------------------------------------------------------------


@router.get("/", response_model=list[notes_schemas.NoteDB])
async def read_all_notes():
    return await notes_crud.select_notes()


@router.get("/{note_id}", response_model=notes_schemas.NoteDB)
async def read_note(note_id: int):
    note = await notes_crud.select_note_by_id(note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post(
    "/", response_model=notes_schemas.NoteDB, status_code=status.HTTP_201_CREATED
)
async def create_note(note: notes_schemas.NoteSchema):
    return await notes_crud.create_note(note_in=note)


@router.put("/{note_id}", response_model=notes_schemas.NoteDB)
async def update_note(note_id: int, note: notes_schemas.NoteSchema):
    updated = await notes_crud.update_note(note_id=note_id, note_in=note)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int):
    success = await notes_crud.delete_note(note_id=note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return  # 204 → no body
