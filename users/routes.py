from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession

from auth.hash_password import HashPassword
from auth.oauth2 import oauth2_schema, get_current_user
from auth.username_validators import check_valid_username
from db.database import get_async_session
from users import schemas, models
from users.crud import change_username, change_user_password

user_router = APIRouter(tags=['users'], prefix='/me')


@user_router.get('', response_model=schemas.UserData)
async def get_user(
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_schema),
    # current_user: models.User = Depends(get_current_user),
):
    return await get_current_user(token, session)


@user_router.patch('', status_code=status.HTTP_201_CREATED, response_model=None)
async def update_username(
    new_username: schemas.User,
    token: str = Depends(oauth2_schema),
    session: AsyncSession = Depends(get_async_session),
    # current_user: schemas.UserData = Depends(get_current_user),
):
    await check_valid_username(new_username.username, session)
    user = await get_current_user(token, session)
    await change_username(user, new_username.username, session)
    return


@user_router.patch('/password', status_code=status.HTTP_200_OK, response_model=None)
async def update_password(
    passwords: schemas.ChangePassword,
    token: str = Depends(oauth2_schema),
    session: AsyncSession = Depends(get_async_session),
    # current_user: schemas.UserData = Depends(get_current_user),
):
    user = await get_current_user(token, session)
    if not user.hashed_password == HashPassword.bcrypt(passwords.old_password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='incorrect old password',
        )
    if not passwords.password1 == passwords.password2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='passwords are not equal',
        )

    await change_user_password(user, passwords.password1, session)
    return
