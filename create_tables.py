import asyncio

from src.core.db.models import Base
from src.core.db.session import engine


async def create_tables() -> None:
    engine_test = engine
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())
