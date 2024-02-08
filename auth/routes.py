from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth.hash_password import HashPassword
from auth.oauth2 import create_access_token
from db.database import get_async_session
from users import schemas
from users.crud import get_user_by_username, create_user
from validators.password_validator import check_valid_password
from validators.username_validator import check_valid_username

auth_router = APIRouter(tags=['auth'])


@auth_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=None)
async def register(
    request: schemas.UserAuth,
    session: AsyncSession = Depends(get_async_session),
):
    username = request.username
    password = request.password

    if not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="pls enter username")
    if not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="pls enter password")

    await check_valid_username(username, session)
    await check_valid_password(password)

    user = await create_user(request, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="some error")

    return


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    exception = HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    user = await get_user_by_username(request.username, session)

    if not user:
        exception.detail = "bad credentials"
        raise exception
    if not HashPassword.verify(user.hashed_password, request.password):
        exception.detail = "wrong password"
        raise exception

    access_token = await create_access_token(data={'id': user.id})

    return {
        'access_token': access_token,
        'token-type': 'bearer',
        # 'user_id': users.id,
        # 'username': users.username,
    }
