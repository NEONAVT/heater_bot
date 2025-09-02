from dataclasses import dataclass
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, and_
from models import Reminder


@dataclass
class ReminderRepository:
    """
    Репозиторий для работы с сущностью Reminder в базе данных.

    Атрибуты:
        db_session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций.
    """

    db_session: AsyncSession

    async def get_reminder(self, message_id: int) -> Optional[Reminder]:
        """
        Получает напоминание по идентификатору сообщения.

        Args:
            message_id (int): Идентификатор сообщения Telegram.

        Returns:
            Optional[Reminder]: Объект Reminder или None, если не найден.
        """
        query = select(Reminder).where(Reminder.message_id == message_id)
        return (await self.db_session.execute(query)).scalar_one_or_none()

    async def save_reminder(
            self, chat_id: int, message_id: int, type_: str, username: str
    ) -> Reminder:
        """
        Сохраняет новое напоминание в базе данных, если оно ещё не существует.

        Args:
            chat_id (int): Идентификатор чата.
            message_id (int): Идентификатор сообщения.
            type_ (str): Тип напоминания.
            username (str): Имя пользователя.

        Returns:
            Reminder: Созданное или существующее напоминание.
        """
        reminder = await self.get_reminder(message_id)
        if reminder:
            return reminder

        query = insert(Reminder).values(
            chat_id=chat_id,
            message_id=message_id,
            type=type_,
            username=username,
        ).returning(Reminder.id)

        reminder_id_result: int = (
            await self.db_session.execute(query)
        ).scalar()
        query_select = (select(Reminder)
                        .where(Reminder.id == reminder_id_result))
        user = ((await self.db_session.execute(query_select))
                .scalar_one_or_none())
        await self.db_session.commit()
        return user

    async def delete_reminder(self, message_id: int):
        """
        Удаляет напоминание по идентификатору сообщения.

        Args:
            message_id (int): Идентификатор сообщения.
        """
        reminder = await self.get_reminder(message_id)
        if reminder:
            await self.db_session.delete(reminder)
            await self.db_session.commit()

    async def get_last_reminder_by_chat(
            self, chat_id: int
    ) -> Optional[Reminder]:
        """
        Получает последнее напоминание по чату.

        Args:
            chat_id (int): Идентификатор чата.

        Returns:
            Optional[Reminder]: Последнее напоминание или None.
        """
        query = (
            select(Reminder)
            .where(Reminder.chat_id == chat_id)
            .order_by(Reminder.created_at.desc())
        )
        result = (await self.db_session.execute(query)).scalars().first()
        return result
