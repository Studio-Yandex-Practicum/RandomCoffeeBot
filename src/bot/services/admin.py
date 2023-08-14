from src.core.db.models import Admin
from src.core.db.repository.admin import AdminRepository


class AdminGettingID:
    def __init__(self, admin_repository: AdminRepository):
        self._admin_repository = admin_repository

    async def get_id(self, instance: Admin):
        await self.self._user_repository.get_admin_id(instance)
