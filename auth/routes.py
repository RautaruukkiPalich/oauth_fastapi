from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth.hash_password import HashPassword
from auth.oauth2 import create_access_token
from db.database import get_async_session
from user import schemas
from user.crud import get_user_by_username, create_user


auth_router = APIRouter(tags=['auth'], prefix='/auth')


@auth_router.post('/register')
async def register(
    request: schemas.UserAuth,
    session: AsyncSession = Depends(get_async_session),
):
    user = await create_user(request, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="already exist")

    return {}


@auth_router.post('/login')
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    user = await get_user_by_username(request.username, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bad credentials")
    if not HashPassword.verify(user.hashed_password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wrong password")

    access_token = await create_access_token(data={'username': user.username})

    return {
        'access_token': access_token,
        'token-type': 'bearer',
        'user_id': user.id,
        'username': user.username,
    }