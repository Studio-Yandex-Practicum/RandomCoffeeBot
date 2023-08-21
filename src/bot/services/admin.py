from src.core.db.models import Admin
from src.core.db.repository.admin import AdminRepository


class AdminService:
    def __init__(self, admin_repository: AdminRepository, admin_username: str) -> None:
        self._admin_repository = admin_repository
        self._admin_username = admin_username

    async def add_admin_if_in_settings(self, instance: Admin) -> None:
        if instance.username == self._admin_username:
            await self._admin_repository.create(instance)

    async def check_if_admin(self, user_id: int, instance: Admin) -> bool | None:
        await self.add_admin_if_in_settings(instance)
        if self._admin_repository.get_by_user_id(user_id) is not None:
            return True
        else:
            return None
