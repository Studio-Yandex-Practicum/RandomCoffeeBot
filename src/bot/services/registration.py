from core.db.repository.user import UserRepository


class RegistrationService:
    """Сервис представляющий логику регистрации нового пользователя"""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def register(self, username: str, first_name: str, last_name: str, **kwargs: dict):
        await self._user_repository.create(username, first_name, last_name, **kwargs)
