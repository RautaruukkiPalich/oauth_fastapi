from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.oauth2 import oauth2_schema, get_current_user
from db.database import get_async_session
from user import schemas
from user.crud import change_username, change_user_password

user_router = APIRouter(tags=['user'], prefix='/me')


@user_router.get('', response_model=schemas.UserData)
async def user(
    token: str = Depends(oauth2_schema),
    session: AsyncSession = Depends(get_async_session),
):
    return await get_current_user(token, session)


@user_router.patch('')
async def patch_user(
    username: str,
    token: str = Depends(oauth2_schema),
    session: AsyncSession = Depends(get_async_session),
):
    user = await get_current_user(token, session)
    await change_username(user, username, session)

    return {}


@user_router.patch('/password')
async def change_password(
    password: str,
    token: str = Depends(oauth2_schema),
    session: AsyncSession = Depends(get_async_session),
):
    user = await get_current_user(token, session)
    await change_user_password(user, password, session)
    return {}
