from fastapi import APIRouter, HTTPException, status

from src.app.orm import notes_crud, notes_schemas

router = APIRouter()


@router.post(
    "/", response_model=notes_schemas.NoteDB, status_code=status.HTTP_201_CREATED
)
async def post_note(note: notes_schemas.NoteSchema):
    return await notes_crud.create_note(note_in=note)


@router.get("/", response_model=list[notes_schemas.NoteDB])
async def read_all_notes():
    return await notes_crud.select_notes()


@router.get("/{note_id}", response_model=notes_schemas.NoteDB)
async def read_note(note_id: int):
    note = await notes_crud.select_note_by_id(note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


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
