from datetime import datetime
from typing import Annotated, List

from sqlalchemy import ARRAY, Integer, String, Text, func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    class_mapper,
    declared_attr,
    mapped_column,
)

from src.app.config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    def to_dict(self, include_relationships: bool = False) -> dict:
        d = {c.key: getattr(self, c.key) for c in class_mapper(self.__class__).columns}
        if include_relationships:
            for rel in class_mapper(self.__class__).relationships:
                value = getattr(self, rel.key)
                if value is None:
                    d[rel.key] = None
                elif rel.uselist:
                    d[rel.key] = [
                        item.to_dict() if hasattr(item, "to_dict") else item
                        for item in value
                    ]
                else:
                    d[rel.key] = value.to_dict() if hasattr(value, "to_dict") else value
        return d


uniq_str_an = Annotated[str, mapped_column(unique=True)]
content_an = Annotated[str | None, mapped_column(Text)]
array_or_none_an = Annotated[List[str] | None, mapped_column(ARRAY(String))]


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper


# alembic init -t async migration
# alembic revision --autogenerate -m "Initial revision"
# alembic upgrade head
