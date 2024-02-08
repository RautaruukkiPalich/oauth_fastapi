from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.hash_password import HashPassword
from auth.oauth2 import get_current_user
from db.database import get_async_session
from users import schemas, models
from users.crud import change_username, change_user_password
from validators.username_validator import check_valid_username

user_router = APIRouter(
    tags=['user'],
    prefix='/me',
)


@user_router.get('', status_code=status.HTTP_200_OK, response_model=schemas.UserData)
async def get_user(
    current_user: models.User = Depends(get_current_user),
):
    return current_user


@user_router.patch('', status_code=status.HTTP_201_CREATED, response_model=None)
async def update_username(
    new_username: schemas.User,
    session: AsyncSession = Depends(get_async_session),
    current_user: models.User = Depends(get_current_user),
):
    await check_valid_username(new_username.username, session)
    await change_username(current_user, new_username.username, session)
    return


@user_router.patch('/password', status_code=status.HTTP_200_OK, response_model=None)
async def update_password(
    passwords: schemas.ChangePassword,
    session: AsyncSession = Depends(get_async_session),
    current_user: models.User = Depends(get_current_user),
):
    exception = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
    if not HashPassword.verify(current_user.hashed_password, passwords.old_password):
        exception.detail = 'incorrect old password',
        raise exception

    if not passwords.password1 == passwords.password2:
        exception.detail = 'passwords are not equal',
        raise exception

    await change_user_password(current_user, passwords.password1, session)
    return
