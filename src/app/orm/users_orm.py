from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import selectinload
from src.app.models import Profile, User
from src.app.orm.base import BaseORM


class UserORM(BaseORM[User]):
    model = User

    @classmethod
    async def add_user_with_profile(
        cls, session: AsyncSession, user_data: dict
    ) -> User:

        user = cls.model(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )
        session.add(user)
        await session.flush()

        profile = Profile(
            user=user,
            user_id=user.id,
            first_name=user_data["first_name"],
            last_name=user_data.get("last_name"),
            age=user_data.get("age"),
            gender=user_data["gender"],
            profession=user_data.get("profession"),
            interests=user_data.get("interests"),
            contacts=user_data.get("contacts"),
        )
        session.add(profile)

        await session.commit()

        return user

    @classmethod
    async def find_many(cls, session: AsyncSession, **filters) -> list[User]:
        query = select(User).filter_by(**filters).options(selectinload(User.profile))
        result = await session.execute(query)
        return list(result.scalars().all())

    @classmethod
    async def search_by_filters(cls, session: AsyncSession, **filters) -> list[User]:
        query = select(User).options(selectinload(User.profile))

        user_columns = {c.name for c in inspect(User).columns}
        profile_columns = {c.name for c in inspect(Profile).columns}

        user_filters = {k: v for k, v in filters.items() if k in user_columns}
        profile_filters = {k: v for k, v in filters.items() if k in profile_columns}

        if user_filters:
            query = query.filter_by(**user_filters)

        if profile_filters:
            query = query.join(User.profile)
            for key, value in profile_filters.items():
                column = getattr(Profile, key)

                # if isinstance(value, str):
                #     query = query.where(column.ilike(f"%{value}%"))
                # else:
                query = query.where(column == value)

        result = await session.execute(query)
        return list(result.scalars().all())
