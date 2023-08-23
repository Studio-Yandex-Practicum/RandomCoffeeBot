import asyncio
import random
from contextlib import asynccontextmanager

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.db.models import User, UsersMatch
from src.settings import Settings

engine = create_async_engine(Settings().database_url)


async def get_session():
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


fake = Faker()


async def filling_users_in_db(session: async_sessionmaker[AsyncSession], num_users: int) -> None:
    """Заполняем базу пользователями"""
    for _ in range(num_users):
        username = fake.user_name()
        first_name = fake.first_name()
        last_name = fake.last_name()

        user = User(username=username, first_name=first_name, last_name=last_name)
        session.add(user)
    await session.commit()


async def filling_users_match_in_db(session: async_sessionmaker[AsyncSession], num_pairs: int) -> None:
    """Заполняем базу мэтчами"""
    users = await session.execute(User.__table__.select())
    users = users.all()
    pairs_created = set()  # все созданные пары сюда для отслеживания повоторений

    for user in users:
        for _ in range(num_pairs):
            matched_user = random.choice(users)
            while (user.id, matched_user.id) in pairs_created or (matched_user.id, user.id) in pairs_created:
                matched_user = random.choice(users)
            pairs_created.add((user.id, matched_user.id))
            pairs_created.add((matched_user.id, user.id))

            users_match = UsersMatch(matched_user_one=user.id, matched_user_two=matched_user.id)
            session.add(users_match)
    await session.commit()


async def delete_all_data(
    session: async_sessionmaker[AsyncSession],
) -> None:
    """Удаление всех данных User, UsersMatch из таблицы"""
    await session.execute(UsersMatch.__table__.delete())
    await session.execute(User.__table__.delete())
    await session.commit()


async def main():
    session_manager = asynccontextmanager(get_session)
    async with session_manager() as session:
        delete_old_data = input("Хотите очистить таблицу? (y/n): ").lower() == "y"
        if delete_old_data:
            await delete_all_data(session)
        await filling_users_in_db(session, num_users=10)
        await filling_users_match_in_db(session, num_pairs=3)
        print("Тестовые данные загружены в БД.")


if __name__ == "__main__":
    asyncio.run(main())
