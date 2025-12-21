from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database import connection
from src.app.orm.orm import UserORM


@connection
async def add_one(user_data: dict, session: AsyncSession):
    new_user = await UserORM.add(session=session, **user_data)
    return new_user.id


@connection
async def add_many_users(users_data: list[dict], session: AsyncSession):
    new_users = await UserORM.add_many(session=session, instances=users_data)
    user_ilds_list = [user.id for user in new_users]
    return user_ilds_list


@connection
async def add_full_user(user_data: dict, session: AsyncSession):
    new_user = await UserORM.add_user_with_profile(session=session, user_data=user_data)
    return new_user


@connection
async def get_all_users(session):
    return await UserORM.get_all(session)
