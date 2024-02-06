from datetime import timedelta, datetime
from typing import Optional

import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE
from user import models
from user.crud import get_user_by_username

oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login')


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRE)

    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str, session: AsyncSession) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='couldnt validate credentionals',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        decoded_username: str = payload.get('username')

        if not decoded_username:
            raise credentials_exception
    except Exception as e:
        print(e)
        raise credentials_exception

    user = await get_user_by_username(decoded_username, session)

    if not user:
        raise credentials_exception

    return user
