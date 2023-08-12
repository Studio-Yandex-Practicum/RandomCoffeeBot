from core.db.repository.user import UserRepository
from src.core.db.models import User


class RegistrationService:
    """Сервис представляющий логику регистрации нового пользователя"""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def register(self, instance: User):
        await self.self._user_repository.update_or_create(instance)
