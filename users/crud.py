from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.hash_password import HashPassword
from users import schemas, models


async def create_user(request: schemas.UserAuth, session: AsyncSession) -> models.User | None:

    user = models.User()
    user.username = request.username
    user.hashed_password = HashPassword.bcrypt(request.password)

    try:
        session.add(user)
        await session.flush()
        await session.commit()
    except IntegrityError:
        await session.rollback()
    else:
        return user
    return


async def get_user_by_username(username: str, session: AsyncSession) -> models.User | None:

    user = await session.execute(
        select(
            models.User
        ).filter(
            models.User.username == username
        )
    )
    return user.scalars().first()


async def get_user_by_id(user_id: int, session: AsyncSession) -> models.User | None:

    stmt = select(
        models.User
    ).filter(
        models.User.id == user_id
    )
    user = await session.execute(stmt)
    return user.scalars().first()


async def change_username(user: models.User, username: str, session: AsyncSession) -> models.User:
    user.username = username
    await session.flush()
    await session.commit()
    return user


async def change_user_password(user: models.User, password: str, session: AsyncSession) -> models.User:
    user.hashed_password = HashPassword.bcrypt(password)
    user.last_password_change = datetime.utcnow()
    await session.flush()
    await session.commit()
    return user


async def username_is_exist(username: str, session: AsyncSession) -> models.User | None:

    stmt = select(
        models.User
    ).filter(
        models.User.username == username
    )
    user = await session.execute(stmt)
    return user.scalars().first()
