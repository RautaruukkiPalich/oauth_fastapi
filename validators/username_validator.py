import re

from fastapi import HTTPException, status
from sqlalchemy import select, or_

from users import models


async def check_valid_username(username, session):
    if not await check_symbols(username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="use latin letters")
    if not await check_username_is_not_exist(username, session):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username is already exist")


async def check_symbols(username: str) -> bool:
    pattern = re.compile(r"^[A-z]+$")
    return bool(pattern.match(username))


async def check_username_is_not_exist(username: str, session) -> bool:
    stmt = select(models.User).filter(or_(
                models.User.username.startswith(username[0].lower()),
                models.User.username.startswith(username[0].upper()),
            ))

    users = await session.execute(stmt)
    return username.lower() not in [x.username.lower() for x in users.scalars().all()]
