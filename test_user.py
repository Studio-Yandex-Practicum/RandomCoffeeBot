import asyncio

from src.core.db.models import Base, User
from src.core.db.session import async_session_maker, engine


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = async_session_maker
    async with session as session:
        async with session.begin():
            s = "IN"
            dict = {"username": "oladushkin", "first_name": "Dima", "last_name": "Shelepin", "status": s}
            session.add(User(**dict))
            session.commit()


if __name__ == "__main__":
    asyncio.run(main())
