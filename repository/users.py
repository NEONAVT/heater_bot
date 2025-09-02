from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from models import Users


@dataclass
class UsersRepository:
    """
    Репозиторий для работы с сущностью Users в базе данных.

    Атрибуты:
        db_session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций.
    """

    db_session: AsyncSession

    async def register_user(
        self, user_id: int, chat_id: int, username: str, first_name: str, last_name: str
    ) -> Optional[Users]:
        """
        Регистрирует нового пользователя. Если пользователь уже существует, возвращает существующую запись.

        Args:
            user_id (int): Уникальный идентификатор пользователя.
            chat_id (int): Идентификатор чата пользователя.
            username (str): Логин пользователя.
            first_name (str): Имя пользователя.
            last_name (str): Фамилия пользователя.

        Returns:
            Optional[Users]: Объект пользователя.
        """
        query = insert(Users).values(
            user_id=user_id,
            chat_id=chat_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        ).on_conflict_do_nothing().returning(Users)

        result = await self.db_session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            query_select = select(Users).where(Users.user_id == user_id)
            user = ((await self.db_session.execute(query_select))
                    .scalar_one_or_none())

        await self.db_session.commit()
        return user

    async def get_user(self, user_id: int) -> Optional[Users]:
        """
        Получает пользователя по идентификатору.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            Optional[Users]: Объект пользователя или None.
        """
        query = select(Users).where(Users.user_id == user_id)
        return (await self.db_session.execute(query)).scalar_one_or_none()

    async def update_last_data(self, user_id: int, updated_date: datetime):
        """
        Обновляет дату последнего взаимодействия пользователя.

        Args:
            user_id (int): Идентификатор пользователя.
            updated_date (datetime): Новая дата последнего взаимодействия.

        Raises:
            ValueError: Если пользователь не найден.
        """
        user = await self.get_user(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        query = update(Users).where(Users.user_id == user_id).values(
            last_updated_date=updated_date
        )
        await self.db_session.execute(query)
        await self.db_session.commit()

    async def set_phone_number(self, user_id: int, phone_number: str):
        """
        Устанавливает номер телефона пользователя.

        Args:
            user_id (int): Идентификатор пользователя.
            phone_number (str): Номер телефона.

        Raises:
            ValueError: Если пользователь не найден.
        """
        user = await self.get_user(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        query = update(Users).where(Users.user_id == user_id).values(
            phone_number=phone_number
        )
        await self.db_session.execute(query)
        await self.db_session.commit()

    async def set_client_status(self, user_id: int, status: str):
        """
        Обновляет статус пользователя.

        Args:
            user_id (int): Идентификатор пользователя.
            status (str): Новый статус.

        Raises:
            ValueError: Если пользователь не найден.
        """
        user = await self.get_user(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        query = update(Users).where(Users.user_id == user_id).values(
            status=status
        )
        await self.db_session.execute(query)
        await self.db_session.commit()

    async def get_inactive_clients(self):
        """
        Получает всех клиентов со статусом 'Client', которые не обновляли данные более 7 дней.

        Returns:
            list[Users]: Список пользователей.
        """
        period = datetime.now() - timedelta(days=7)

        query = (
            select(Users)
            .where(Users.status == "Client")
            .where(Users.last_updated_date < period)
        )

        result = await self.db_session.execute(query)
        return result.scalars().all()
