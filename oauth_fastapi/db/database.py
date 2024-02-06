from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from sqlalchemy.ext.declarative import declarative_base

from config import DB_URL

Base = declarative_base()

engine: AsyncEngine = create_async_engine(
    url=DB_URL,
    # echo=True,
)


async def get_async_session() -> AsyncSession:
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session.begin() as session:
        yield session
        await session.close()
