from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.hash_password import HashPassword
from user import schemas, models


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

