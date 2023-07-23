from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
session_factory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session():
    async with session_factory as session:
        yield session
