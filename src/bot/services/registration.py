from src.core.db.models import User
from src.core.db.repository.user import UserRepository


class RegistrationService:
    """Сервис представляющий логику регистрации нового пользователя"""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def register(self, instance: User):
        await self._user_repository.create_or_update(instance)
