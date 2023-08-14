from src.core.db.models import Admin
from src.core.db.repository.admin import AdminRepository


class AdminRegistration:
    def __init__(self, user_repository: AdminRepository):
        self._user_repository = user_repository

    async def register(self, instance: Admin):
        await self.self._user_repository.update_or_create(instance)
