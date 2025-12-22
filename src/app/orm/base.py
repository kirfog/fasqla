from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database import Base


class BaseORM[T: Base]:
    model: type[T]

    @classmethod
    async def add(cls, session: AsyncSession, **values) -> T:
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_many(
        cls, session: AsyncSession, instances: list[dict]
    ) -> list[T]:
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[T]:
        query = select(cls.model)
        result = await session.execute(query)
        records = result.scalars().all()
        return list(records)

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> T | None:
        query = select(cls.model).filter_by(id=id)
        # query = select(cls.model).filter(cls.model.id == id)
        result = await session.execute(query)
        user_info = result.scalar_one_or_none()
        return user_info

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        record = result.scalar_one_or_none()
        return record

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        records = result.scalars().all()
        return records
