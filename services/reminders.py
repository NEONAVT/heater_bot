from dataclasses import dataclass
import logging

from database import AsyncSessionFactory
from repository import ReminderRepository

logger = logging.getLogger(__name__)


@dataclass
class ReminderService:
    """
    Сервис для работы с напоминаниями. Обеспечивает доступ к
    ReminderRepository через асинхронные сессии базы данных.
    """

    async def get_last_reminder_by_chat(self, chat_id: int):
        """
        Получает последнее напоминание для заданного чата.

        Args:
            chat_id (int): Идентификатор чата Telegram.

        Returns:
            Reminder | None: Последнее напоминание или None.
        """
        async with AsyncSessionFactory() as session:
            repo = ReminderRepository(db_session=session)
            return await repo.get_last_reminder_by_chat(chat_id)

    async def save_reminder(
            self, chat_id: int, message_id: int, type_: str, username: str
    ):
        """
        Сохраняет напоминание, если оно ещё не существует.

        Args:
            chat_id (int): Идентификатор чата.
            message_id (int): Идентификатор сообщения.
            type_ (str): Тип напоминания.
            username (str): Имя пользователя, к которому относится напоминание.

        Returns:
            Reminder: Сохранённое или найденное напоминание.
        """
        async with AsyncSessionFactory() as session:
            repo = ReminderRepository(db_session=session)
            return await repo.save_reminder(
                chat_id, message_id, type_, username
            )


    async def delete_reminder(self, reminder_id: int):
        """
        Удаляет напоминание по идентификатору.

        Args:
            reminder_id (int): message_id напоминания.
        """
        async with AsyncSessionFactory() as session:
            repo = ReminderRepository(db_session=session)
            return await repo.delete_reminder(reminder_id)


reminders_service = ReminderService()
