import argparse
import asyncio
import random

from dependency_injector import wiring
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.models import User, UsersMatch
from src.core.db.repository.user import UserRepository
from src.core.db.repository.usersmatch import UsersMatchRepository
from src.depends import Container

fake = Faker()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Загрузка тестовых данных пользователей и их мэтчей в БД")
    parser.add_argument(
        "-u",
        "--num_users",
        type=int,
        default=10,
        help="Количество пользователей для добавления в БД (по умолчанию: 10)",
    )
    parser.add_argument(
        "-p",
        "--num_pairs",
        type=int,
        default=3,
        help="Количество пар сопоставлений для каждого пользователя (по умолчанию: 3)",
    )

    return parser.parse_args()


async def filling_users_in_db(user_repo: UserRepository, num_users: int) -> None:
    """Заполняем базу пользователями"""
    for _ in range(num_users):
        username = fake.user_name()
        first_name = fake.first_name()
        last_name = fake.last_name()
        user = User(username=username, first_name=first_name, last_name=last_name)

        await user_repo.create(user)


async def filling_users_match_in_db(session: AsyncSession, match_repo: UsersMatchRepository, num_pairs: int) -> None:
    """Заполняем базу мэтчами"""
    users = await session.execute(User.__table__.select())
    users = users.all()

    if num_pairs != 0 and len(users) <= 1:
        print("Недостаточно пользователей для создания пар. Требуется как минимум два пользователя.")
        return

    pairs_created = set()  # все созданные пары сюда для отслеживания повторений

    for user in users:
        for _ in range(num_pairs):
            other_users = [
                u
                for u in users
                if u.id != user.id and (user.id, u.id) not in pairs_created and (u.id, user.id) not in pairs_created
            ]
            if not other_users:
                break
            matched_user = random.choice(other_users)

            pairs_created.add((user.id, matched_user.id))
            pairs_created.add((matched_user.id, user.id))

            users_match = UsersMatch(matched_user_one=user.id, matched_user_two=matched_user.id)
            await match_repo.create(users_match)


async def delete_all_data(session: AsyncSession) -> None:
    """Удаление всех данных User, UsersMatch из таблицы"""
    await session.execute(UsersMatch.__table__.delete())
    await session.execute(User.__table__.delete())
    await session.commit()


@wiring.inject
async def main(
    sessionmaker: AsyncSession = wiring.Provide[Container.sessionmaker],
    user_repo: UserRepository = wiring.Provide[Container.user_repository],
    match_repo: UsersMatchRepository = wiring.Provide[Container.match_repository],
):
    args = parse_arguments()

    try:
        async with sessionmaker() as session:
            delete_old_data = input("Хотите очистить таблицу? (y/n): ").lower() == "y"
            if delete_old_data:
                await delete_all_data(session)
            await filling_users_in_db(user_repo, num_users=args.num_users)
            await filling_users_match_in_db(session, match_repo, num_pairs=args.num_pairs)
            print("Тестовые данные загружены в БД.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    asyncio.run(main())
