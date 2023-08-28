from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.settings import Settings

engine = create_async_engine(Settings().database_url)


async def get_session(sessionmaker=async_sessionmaker(engine, expire_on_commit=False)):
    async with sessionmaker() as session:
        yield session
