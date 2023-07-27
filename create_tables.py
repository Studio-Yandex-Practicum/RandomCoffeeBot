import asyncio

from src.core.db.models import Base
from src.core.db.session import async_session_maker, engine


async def create_tables():
    engine_test = engine
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session_maker() as session:
        return session


if __name__ == "__main__":
    asyncio.run(create_tables())
