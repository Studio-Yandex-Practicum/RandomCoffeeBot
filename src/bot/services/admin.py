from src.core.db.models import Admin
from src.core.db.repository.admin import AdminRepository
from src.core.db.repository.user import UserRepository


class AdminService:
    def __init__(self, admin_repository: AdminRepository, admin_username: str, user_repository: UserRepository) -> None:
        self._admin_repository = admin_repository
        self._admin_username = admin_username
        self._user_repository = user_repository

    async def add_admin_if_in_settings(self, instance: Admin) -> bool | None:
        if instance.username == self._admin_username:
            await self._admin_repository.create(instance)
            return True
        else:
            return False

    async def check_if_admin(self, user_id: int, instance: Admin) -> bool | None:
        if await self._admin_repository.get_by_user_id(user_id) is not None:
            return True
        elif await self.add_admin_if_in_settings(instance):
            return True
        else:
            return False

    async def add_extra_admin(self, username: str) -> bool | None:
        if await self._admin_repository.get_by_username(username) is not None:
            return True
        instance = await self._user_repository.get_by_username(username)
        if instance is not None:
            new_admin = Admin(username=instance.username, user_id=instance.user_id)
            await self._admin_repository.create(new_admin)
            return True
        else:
            return False

    async def del_extra_admin(self, username: str) -> bool | None:
        instance = await self._admin_repository.get_by_username(username)
        if instance is not None:
            await self._admin_repository.delete(instance)
            return True
        else:
            return False

    async def get_all_admins(self) -> str | None:
        admins_username = []
        for admin in await self._admin_repository.get_all():
            admins_username.append(admin.username)
        return "\n".join(admins_username)
