from sqlalchemy.ext.asyncio import AsyncSession

from src.app.database import connection
from src.app.orm.users_orm import UserORM
from src.app.orm.users_schemas import UserSchema


@connection
async def add_one(user_data: dict, session: AsyncSession):
    new_user = await UserORM.add(session=session, **user_data)
    return UserSchema.model_validate(new_user)


@connection
async def add_many_users(users_data: list[dict], session: AsyncSession):
    new_users = await UserORM.add_many(session=session, instances=users_data)
    return [UserSchema.model_validate(user) for user in new_users]


@connection
async def add_full_user(user_data: dict, session: AsyncSession):
    new_user = await UserORM.add_user_with_profile(session=session, user_data=user_data)
    return UserSchema.model_validate(new_user)


@connection
async def get_all_users(session: AsyncSession):
    users = await UserORM.get_all(session=session)
    return [UserSchema.model_validate(user) for user in users]


@connection
async def get_user_by_id(session: AsyncSession, id: int):
    user = await UserORM.get_by_id(session=session, id=id)
    if user:
        return UserSchema.model_validate(user)
    return None


@connection
async def search_users(filters: dict, session: AsyncSession) -> list[UserSchema]:
    # users = await UserORM.find_many(session=session, **filters)
    users = await UserORM.search_by_filters(session=session, **filters)
    return [UserSchema.model_validate(user) for user in users]
