from src.core.db.models import Admin
from src.core.db.repository.admin import AdminRepository
from src.settings import Settings


class AdminService:
    def __init__(self, admin_repository: AdminRepository):
        self._admin_repository = admin_repository

    async def admin_settings(self, username: str, instance: Admin):
        if username == Settings.ADMIN:
            self.self._admin_repository.create(instance)

    async def check_if_admin(self, usename: str, user_id: int, instance: Admin):
        await self.admin_settings(usename, instance)
        if self.self_admin_repository.get_by_id(user_id) is not None:
            return True
