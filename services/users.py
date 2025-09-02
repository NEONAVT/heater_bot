from dataclasses import dataclass
from datetime import datetime
from database import AsyncSessionFactory
from repository import UsersRepository
import logging

logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


@dataclass
class UsersService:
    """
    Сервис для работы с пользователями. Обеспечивает доступ к
    UsersRepository через асинхронные сессии базы данных.
    """

    async def register_user(
            self, user_id: int, chat_id: int, username: str,
            first_name: str, last_name: str):
        """
        Регистрирует пользователя в базе данных.

        Args:
            user_id (int): Идентификатор пользователя Telegram.
            chat_id (int): Идентификатор чата Telegram.
            username (str): Логин пользователя.
            first_name (str): Имя пользователя.
            last_name (str): Фамилия пользователя.

        Returns:
            Users | None: Созданный или существующий пользователь.
        """
        try:
            async with AsyncSessionFactory() as session:
                repo = UsersRepository(db_session=session)
                user = await repo.register_user(
                    user_id, chat_id, username, first_name, last_name
                )
                return user
        except Exception as e:
            logger.error(f"Ошибка регистрации пользователя: {e}")
            return None

    async def update_last_data(self, user_id: int, updated_date: datetime):
        """
        Обновляет дату последней активности пользователя.

        Args:
            user_id (int): Идентификатор пользователя.
            updated_date (datetime): Дата и время последней активности.
        """
        async with AsyncSessionFactory() as session:
            repo = UsersRepository(db_session=session)
            return await repo.update_last_data(user_id, updated_date)

    async def set_phone_number(self, user_id: int, phone_number: str):
        """
        Сохраняет номер телефона пользователя.

        Args:
            user_id (int): Идентификатор пользователя.
            phone_number (str): Телефонный номер.
        """
        async with AsyncSessionFactory() as session:
            repo = UsersRepository(db_session=session)
            return await repo.set_phone_number(user_id, phone_number)

    async def set_client_status(self, user_id: int):
        """
        Устанавливает статус пользователя "Client".

        Args:
            user_id (int): Идентификатор пользователя.
        """
        async with AsyncSessionFactory() as session:
            repo = UsersRepository(db_session=session)
            return await repo.set_client_status(user_id, status="Client")

    async def get_inactive_clients(self):
        """
        Получает всех клиентов, неактивных более 7 дней.

        Returns:
            list[Users]: Список неактивных клиентов.
        """
        async with AsyncSessionFactory() as session:
            repo = UsersRepository(db_session=session)
            return await repo.get_inactive_clients()


users_service = UsersService()
