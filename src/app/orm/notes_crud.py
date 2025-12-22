from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database import connection
from src.app.models import Note
from src.app.orm.notes_schemas import NoteDB, NoteSchema


@connection
async def create_note(*, session: AsyncSession, note_in: NoteSchema) -> NoteDB:
    query = insert(Note).values(**note_in.model_dump()).returning(Note)
    result = await session.execute(query)
    await session.commit()
    note = result.scalar_one()
    return NoteDB.model_validate(note)


@connection
async def select_notes(session: AsyncSession) -> list[NoteDB]:
    result = await session.execute(select(Note))
    notes = result.scalars().all()
    return [NoteDB.model_validate(note) for note in notes]


@connection
async def select_note_by_id(*, session: AsyncSession, note_id: int) -> NoteDB | None:
    result = await session.execute(select(Note).where(Note.id == note_id))
    note = result.scalar_one_or_none()
    return NoteDB.model_validate(note) if note else None


@connection
async def update_note(
    *, session: AsyncSession, note_id: int, note_in: NoteSchema
) -> NoteDB | None:
    query = (
        update(Note)
        .where(Note.id == note_id)
        .values(**note_in.model_dump())
        .returning(Note)
    )
    result = await session.execute(query)
    await session.commit()
    note = result.scalar_one_or_none()
    return NoteDB.model_validate(note) if note else None


@connection
async def delete_note(*, session: AsyncSession, note_id: int) -> NoteDB:
    query = delete(Note).where(Note.id == note_id)
    result = await session.execute(query)
    await session.commit()
    note = result.scalar_one()
    return NoteDB.model_validate(note)
