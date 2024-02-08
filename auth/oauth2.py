from datetime import timedelta, datetime
from typing import Optional

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE
from db.database import get_async_session
from users import models
from users.crud import get_user_by_id

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE)

    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def decode_access_token(
        token: str,
        credentials_exception: HTTPException,
        session: AsyncSession,
) -> models.User:

    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as e:
        credentials_exception.detail += f": {'; '.join(e.args)}"
        raise credentials_exception

    decoded_id: int = payload.get('id')

    if not decoded_id:
        raise credentials_exception

    return await get_user_by_id(decoded_id, session)


async def get_current_user(
        token: str = Depends(oauth2_schema),
        session: AsyncSession = Depends(get_async_session),
) -> models.User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    user: models.User = await decode_access_token(token, credentials_exception, session)

    if not user:
        raise credentials_exception

    return user
