from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from src.app.orm import users_crud, users_schemas

router = APIRouter()


@router.post("/post", response_model=users_schemas.UserSchema)
async def insert_user(user: Annotated[users_schemas.UserSchemaIn, Query()]):
    try:
        user = await users_crud.add_full_user(user.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return user


@router.post("/post_many", response_model=list[users_schemas.UserSchema])
async def insert_users(users: list[users_schemas.UserSchemaIn]):
    try:
        users = await users_crud.add_many_users([user.model_dump() for user in users])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return users


@router.get("/get_all", response_model=list[users_schemas.UserSchema])
async def get_users():
    return await users_crud.get_all_users()


@router.get("/get/{id}", response_model=users_schemas.UserSchema)
async def get_user_by_id(id: int):
    user = await users_crud.get_user_by_id(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/get_by", response_model=list[users_schemas.UserSchema])
async def search_users_endpoint(
    filters: Annotated[users_schemas.UserSearchSchema, Query()],
):
    return await users_crud.search_users(filters.model_dump(exclude_none=True))
