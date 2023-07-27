import asyncio

from sqlalchemy.future import select

from src.core.db.models import Base, User
from src.core.db.session import async_session_maker, engine


async def main():
    engine_test = engine
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session_maker() as ses:
        test_status = "IN_MEETING"
        obj = User(username="oladushkin", first_name="Dima", last_name="Shelepin", status=test_status)
        ses.add(obj)
        await ses.commit()
        db_objs = await ses.execute(select(User))
        result = db_objs.scalars().all()
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
