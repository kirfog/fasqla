from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models import Comment, Post, Profile, User
from src.app.orm.base import BaseORM


class UserORM(BaseORM):
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


class ProfileORM(BaseORM):
    model = Profile


class PostORM(BaseORM):
    model = Post


class CommentORM(BaseORM):
    model = Comment
